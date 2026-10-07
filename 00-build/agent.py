"""Bounded Cortex loop. Run with a task name: happy, missing-data, or jailbreak.

Human approval flags: --approve-context P-NORTH --approve-tone
These approve project-only context and concise factual tone, never publication.
"""
from __future__ import annotations

import argparse
import json
import os
import queue
import re
import threading
import time
import unicodedata
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).with_name('.env'))

import tools
from critic import review, failure_action
from prompts import CORTEX_SYSTEM

MODEL = os.environ.get('CORTEX_MODEL', 'gpt-4o')
MAX_ITERATIONS = int(os.environ.get('CORTEX_MAX_ITERATIONS', '5'))
MAX_REVISIONS = max(0, min(4, MAX_ITERATIONS - 1,
                           int(os.environ.get('CORTEX_MAX_REVISIONS', '4'))))
COST_CAP_USD = float(os.environ.get('CORTEX_COST_CAP_USD', '0.10'))
MAX_QUEUE_ITEMS = int(os.environ.get('CORTEX_MAX_QUEUE_ITEMS', '10'))
MAX_SECONDS = 600
DATA_ATTEMPTS = 3
# Conservative budgeting estimates for gpt-4o, not provider billing quotes.
PRICE_IN = float(os.environ.get('CORTEX_PRICE_IN_PER_M', '10' if MODEL == 'gpt-4o' else '0.15'))
PRICE_OUT = float(os.environ.get('CORTEX_PRICE_OUT_PER_M', '30' if MODEL == 'gpt-4o' else '0.60'))
OUTPUT_DIR = Path(__file__).parent / 'run-output'


class StopRun(Exception):
    def __init__(self, outcome, reason):
        self.outcome, self.reason = outcome, reason
        super().__init__(reason)


class Bounds:
    def __init__(self):
        self.started = time.monotonic()
        self.cost = 0.0

    def check(self):
        if time.monotonic() - self.started >= MAX_SECONDS:
            raise StopRun('stuck', '10-minute run limit reached')
        if self.cost >= COST_CAP_USD:
            raise StopRun('escalate', 'Estimated spending limit reached')

    def add(self, prompt, completion):
        self.cost += (prompt * PRICE_IN + completion * PRICE_OUT) / 1_000_000
        self.check()

    def call(self, fn, *args, **kwargs):
        """Stop waiting at the deadline, even if a request stalls.

        In-flight remote requests may finish, but no further work is started.
        Only read tools and model calls should use this wrapper.
        """
        self.check()
        result = queue.Queue()

        def worker():
            try:
                result.put((True, fn(*args, **kwargs)))
            except Exception as exc:
                result.put((False, exc))

        threading.Thread(target=worker, daemon=True).start()
        remaining = MAX_SECONDS - (time.monotonic() - self.started)
        try:
            ok, value = result.get(timeout=max(0, remaining))
        except queue.Empty:
            raise StopRun('stuck', '10-minute run limit reached') from None
        self.check()
        if not ok:
            raise value
        return value


def banner(text):
    print(f"\n{'=' * 64}\n{text}\n{'=' * 64}")


def task_override_signals(body):
    """Flag known explicit rule/permission overrides for human review.

    This conservative task preflight is not a general injection detector. Model,
    critic, scoped retrieval, and absent write tools remain separate safeguards.
    Only static signal labels are returned; untrusted text is not logged.
    """
    normalized = unicodedata.normalize('NFKC', body)
    normalized = ''.join(c for c in normalized if unicodedata.category(c) != 'Cf')
    patterns = {
        'system_override': r'\bsystem[\s_/-]+override\b',
        'admin_authority_override': r'\badmin[\s_-]+mode\s*:',
        'rule_override': (r'\b(?:ignore|disregard|override)\s+'
                          r'(?:(?:all|the|your|previous|prior|existing)\s+){0,5}'
                          r'(?:rules|instructions|norms|policies|safeguards)\b'),
        'approval_bypass': (r'\b(?:bypass|disable)\s+(?:the\s+)?'
                            r'(?:human\s+approval|hitl|approval\s+(?:gate|checkpoint))\b'),
    }
    return [label for label, pattern in patterns.items()
            if re.search(pattern, normalized, re.IGNORECASE)]


def retrieve(bounds, name, args, valid):
    for attempt in range(1, DATA_ATTEMPTS + 1):
        print(f'\nTOOL {name}({json.dumps(args)}) attempt {attempt}/{DATA_ATTEMPTS}')
        try:
            result = bounds.call(tools.TOOLS[name], **args)
        except (ConnectionError, TimeoutError):
            raise StopRun('stuck', f'Cannot connect to required tool: {name}') from None
        except (OSError, ValueError):
            result = {'error': 'required source unavailable or unreadable'}
        if isinstance(result, dict) and not result.get('error') and valid(result):
            if name == 'get_project' and (
                result.get('status') == 'embargoed'
                or 'confidential' in result.get('flags', [])
                or 'CONFIDENTIAL' in result.get('prd_summary', '').upper()
            ):
                raise StopRun('escalate', 'Confidential project requires human review')
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return result
        print('Required data missing or invalid.')
    raise StopRun('stuck', f'{name}: required data unavailable after 3 attempts')


def validate_proposal(value):
    """A critic pass cannot substitute for either required deliverable."""
    if not isinstance(value, dict):
        return ['Output must be a JSON object.']
    if value.get('outcome') != 'done':
        return ['outcome must be done or escalate.']
    if not isinstance(value.get('update'), str) or not value['update'].strip():
        return ['A weekly update is required.']
    stories = value.get('stories')
    if not isinstance(stories, list) or not stories:
        return ['Prioritized proposed stories are required.']
    for rank, story in enumerate(stories, 1):
        if not isinstance(story, dict) or story.get('priority') != rank:
            return ['Story priorities must be sequential: 1, 2, ...']
        if any(not isinstance(story.get(k), str) or not story[k].strip()
               for k in ('title', 'reason', 'source')):
            return ['Each story needs a title, priority reason, and source.']
    return []


def render_proposal(value):
    lines = [value['update'].strip(), '\nPrioritized proposed stories:']
    for s in value['stories']:
        lines.append(f"{s['priority']}. {s['title']} — {s['reason']} (source: {s['source']})")
    lines.append('\nFor human approval. Nothing posted or created in a tracker.')
    return '\n'.join(lines)


def story_evidence(sources):
    """Link literal PRD feature names to open issues, preserving both source roles.

    This is a retrieval aid, not approval or a replacement for independent review.
    Unmatched issues remain in the full activity source for the model to inspect.
    """
    project = sources['get_project']
    match = re.search(r'In scope:\s*(.*?)(?:\.\s*Out of scope:|$)',
                      project.get('prd_summary', ''), re.IGNORECASE)
    if not match:
        return []
    features = [part.strip().rstrip('.') for part in match.group(1).split(',')]
    return [{'scope_source': f'get_project / {project["prd"]}',
             'scope_item': feature,
             'work_source': f'get_activity / {item["id"]}',
             'work_evidence': item['title']}
            for item in sources['get_activity']['activity']
            if item.get('type') == 'issue_open' and item.get('id') and item.get('title')
            for feature in features if feature and feature.casefold() in item['title'].casefold()]


def finish(which, outcome, reason, draft, bounds):
    banner(f'{outcome.upper()}: {reason}')
    print(f'Estimated recorded cost: ${bounds.cost:.4f}')
    print('Nothing posted, no tickets created, no commitments made.')
    if draft:
        print('\nDRAFT HELD FOR HUMAN REVIEW:\n' + draft)
    OUTPUT_DIR.mkdir(exist_ok=True)
    # Clear stale successful output even when the new run produces no draft.
    out = OUTPUT_DIR / f'status-update-{which}.md'
    out.write_text(f'# {outcome.upper()}\n\n{reason}\n\nEstimated recorded cost: '
                   f'${bounds.cost:.4f}\n\n{draft or "No draft produced."}\n', encoding='utf-8')
    (OUTPUT_DIR / f'result-{which}.json').write_text(json.dumps({
        'outcome': outcome, 'reason': reason, 'cost_usd': bounds.cost,
        'elapsed_seconds': round(time.monotonic() - bounds.started, 2),
        'draft': draft,
    }, indent=2), encoding='utf-8')
    print(f'Saved result: {out}')
    return outcome


def run(which='happy', *, approved_context=None, approved_tone=False, demo_bad_metric=False):
    bounds = Bounds()
    draft = ''
    try:
        task = tools.get_task(which)
        if 'error' in task:
            raise StopRun('stuck', task['error'])
        banner(f'CORTEX RUN: {which}; limit 10 minutes; queue cap {MAX_QUEUE_ITEMS}')
        signals = task_override_signals(task['body'])
        if signals:
            print('SECURITY EVENT: ' + json.dumps({
                'event': 'prompt_injection_detected', 'source': 'task_brief',
                'signals': signals, 'action': 'refuse_and_escalate',
            }))
            raise StopRun('escalate', 'Prompt injection detected in task brief; '
                          'embedded rule/permission overrides refused; human review required')
        print(task['body'])
        match = re.search(r'^Project:\s*(P-[A-Z0-9-]+)', task['body'], re.MULTILINE)
        if not match:
            raise StopRun('escalate', 'A human must identify the project and scope')
        project_id = match.group(1)
        project = retrieve(bounds, 'get_project', {'project_id': project_id},
                           lambda r: r.get('project_id') == project_id
                           and all(r.get(k) for k in ('name', 'status', 'prd_summary')))
        if project.get('status') == 'at_risk' or project.get('flags'):
            raise StopRun('escalate', 'Project risk flags require human validation and routing')
        if approved_context != project_id or not approved_tone:
            raise StopRun('awaiting_approval',
                          f'Approve {project_id} context: project/PRD, activity, project-only '
                          'past updates and roadmap, and team norms. Approve concise factual '
                          'tone with no commitments before drafting. Use --approve-context '
                          f'{project_id} --approve-tone only after human approval.')
        print(f'Human-approved context: {project_id}; tone: concise, factual, no commitments.')
        sources = {'get_project': project}
        sources['get_activity'] = retrieve(bounds, 'get_activity', {'project_id': project_id},
                                           lambda r: r.get('project_id') == project_id
                                           and bool(r.get('activity')))
        if any(a.get('type') == 'issue_open' and a.get('severity', '').lower() == 'sev-1'
               for a in sources['get_activity']['activity']):
            raise StopRun('escalate', 'Open Sev-1 requires human risk validation and routing')
        project_name = project['name'].split(' (')[0]
        for name, field, query in [('search_past_updates', 'matches', project_name),
                                    ('get_roadmap', 'roadmap', project_name),
                                    ('get_norms', 'norms', 'team norms')]:
            sources[name] = retrieve(bounds, name, {'query': query}, lambda r, f=field: bool(r.get(f)))
        if 'CONFIDENTIAL' in sources['get_roadmap']['roadmap'].upper():
            raise StopRun('escalate', 'Confidential roadmap requires human review')
        sources['story_evidence'] = story_evidence(sources)
        print('\nSTORY EVIDENCE (separate scope and unfinished-work sources):\n'
              + json.dumps(sources['story_evidence'], ensure_ascii=False, indent=2))
        source_text = json.dumps(sources, ensure_ascii=False)
        client = OpenAI(max_retries=0, timeout=60)
        messages = [
            {'role': 'system', 'content': CORTEX_SYSTEM},
            {'role': 'user', 'content': f'TASK:\n{task["body"]}\nSOURCES:\n{source_text}'},
        ]
        for iteration in range(1, MAX_ITERATIONS + 1):
            banner(f'DRAFT ITERATION {iteration}')
            resp = bounds.call(client.chat.completions.create, model=MODEL,
                               messages=messages, temperature=0,
                               response_format={'type': 'json_object'})
            bounds.add(resp.usage.prompt_tokens, resp.usage.completion_tokens)
            raw = resp.choices[0].message.content or ''
            try:
                proposed = json.loads(raw)
            except json.JSONDecodeError:
                proposed = None
            if demo_bad_metric and iteration == 1 and isinstance(proposed, dict) and proposed.get('outcome') == 'done':
                metric = next((a for a in sources['get_activity']['activity']
                               if a.get('type') == 'metric' and a.get('name') == 'activation_rate'), None)
                if metric is None:
                    raise StopRun('stuck', 'Bad-metric demo requires an activation_rate source')
                print('LAB TEST INJECTION: replace update with an invented 80% activation metric; '
                      f'source remains {metric["value"]}, prior {metric["prior"]}.')
                proposed['update'] = (f'{project_name} ({project_id}) weekly VP update: '
                                      f'activation_rate is 80%, up from {metric["prior"]} '
                                      f'{metric["window"]} (source: get_activity). '
                                      'Draft for human approval.')
                raw = json.dumps(proposed)
            if isinstance(proposed, dict) and proposed.get('outcome') == 'escalate':
                raise StopRun('escalate', str(proposed.get('reason') or 'Model requests human review'))
            errors = validate_proposal(proposed)
            if not errors:
                if len(proposed['stories']) > MAX_QUEUE_ITEMS:
                    raise StopRun('escalate', 'Story limit reached; do not split the batch')
                draft = render_proposal(proposed)
                print(draft)
                banner('CRITIC: independent validation')
                verdict = bounds.call(review, client, MODEL, draft,
                                      f'Runtime queue cap: {MAX_QUEUE_ITEMS}\n' + task['body'] + '\n' + source_text)
                bounds.add(verdict['_usage']['prompt'], verdict['_usage']['completion'])
                print(json.dumps({k: v for k, v in verdict.items() if k != '_usage'}, indent=2))
                action = failure_action(verdict, iteration - 1, MAX_REVISIONS)
                if action == 'escalate':
                    raise StopRun('escalate', 'Critic blocked output: ' + '; '.join(verdict['reasons']))
                if action == 'revise':
                    print(f'FAIL-ACTION: return to Cortex for revision {iteration}/{MAX_REVISIONS}; '
                          f'failed checks: {verdict.get("failed_checks", [])}')
                errors = verdict['reasons'] if verdict['verdict'] != 'pass' else []
                if verdict['verdict'] != 'pass' and not errors:
                    errors = ['Critic did not approve.']
            if not errors:
                stories = [f"{s['priority']}. {s['title']} — {s['reason']} (source: {s['source']})"
                           for s in proposed['stories']]
                bounds.check()
                queued = tools.propose_stories(project_id, stories,
                                              'Prioritized proposals; human approval required')
                bounds.check()
                print('\nTOOL propose_stories -> ' + json.dumps(queued, ensure_ascii=False, indent=2))
                if queued.get('status') != 'queued_for_approval':
                    raise StopRun('escalate', 'Story queue rejected; human review required')
                return finish(which, 'success', 'HITL CHECKPOINT: weekly update and prioritized '
                              'stories passed the critic; awaiting your claims spot-check and '
                              'approval of both outputs. Publishing remains human-owned.', draft, bounds)
            print('REJECTED: ' + json.dumps(errors))
            if iteration - 1 >= MAX_REVISIONS:
                raise StopRun('escalate', f'Draft still rejected after {MAX_REVISIONS} revisions')
            messages.extend([{'role': 'assistant', 'content': raw},
                             {'role': 'user', 'content': 'Fix these issues or escalate: ' + json.dumps(errors)}])
        raise StopRun('stuck', 'Iteration limit reached without completing')
    except StopRun as stop:
        return finish(which, stop.outcome, stop.reason, draft, bounds)
    except Exception as exc:
        # SDK exceptions may include request details: log only their type.
        return finish(which, 'stuck', f'Required model/tool failed ({type(exc).__name__}); '
                      'human action required', draft, bounds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task', nargs='?', default='happy', choices=['happy', 'missing-data', 'jailbreak'])
    parser.add_argument('--approve-context', help='Project ID whose context a human approved')
    parser.add_argument('--approve-tone', action='store_true', help='Human approved concise factual tone, no commitments')
    parser.add_argument('--demo-bad-metric', action='store_true', help='Lab-only: inject an incorrect 80%% metric into the first draft')
    args = parser.parse_args()
    if args.demo_bad_metric and args.task != 'happy':
        parser.error('--demo-bad-metric requires the happy fixture')
    if args.demo_bad_metric:
        OUTPUT_DIR = OUTPUT_DIR / 'critic-demo'
    run(args.task, approved_context=args.approve_context, approved_tone=args.approve_tone,
        demo_bad_metric=args.demo_bad_metric)
