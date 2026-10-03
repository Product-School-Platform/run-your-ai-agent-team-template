import contextlib
import io
import json
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

import agent
import tools
import critic

PROPOSAL = {'outcome': 'done', 'update': 'Northstar draft for review.', 'stories': [
    {'priority': 1, 'title': 'Review empty-state copy', 'reason': 'Open issue', 'source': '#818'}]}


def response(value):
    return NS(usage=NS(prompt_tokens=1, completion_tokens=1),
              choices=[NS(message=NS(content=json.dumps(value)))])


class LoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = patch.object(agent, 'OUTPUT_DIR', Path(self.tmp.name))
        self.out.start()
        self.addCleanup(self.out.stop)
        self.stdout = contextlib.redirect_stdout(io.StringIO())
        self.stdout.__enter__()
        self.addCleanup(self.stdout.__exit__, None, None, None)

    def run_mock(self, value=PROPOSAL, verdict='pass'):
        client = Mock()
        client.chat.completions.create.return_value = response(value)
        critic = {'verdict': verdict, 'reasons': [] if verdict == 'pass' else ['Unsupported claim'],
                  '_usage': {'prompt': 1, 'completion': 1}}
        with patch.object(agent, 'OpenAI', return_value=client), patch.object(agent, 'review', return_value=critic):
            outcome = agent.run(approved_context='P-NORTH', approved_tone=True)
        return outcome, client.chat.completions.create.call_count

    def test_success_requires_both_outputs(self):
        self.assertEqual(self.run_mock()[0], 'success')
        result = json.loads((Path(self.tmp.name) / 'result-happy.json').read_text())
        self.assertIn('HITL CHECKPOINT', result['reason'])
        self.assertIn('Review empty-state copy', result['draft'])

    def test_missing_stories_never_pass(self):
        outcome, calls = self.run_mock({'outcome': 'done', 'update': 'Draft', 'stories': []})
        self.assertEqual((outcome, calls), ('escalate', 3))

    def test_critic_rejection_stops_after_two_revisions(self):
        self.assertEqual(self.run_mock(verdict='fail'), ('escalate', 3))

    def test_escalation_is_not_success(self):
        self.assertEqual(self.run_mock({'outcome': 'escalate', 'reason': 'Conflicting data'})[0], 'escalate')

    def test_sensitive_critic_failure_stops_without_revision_or_queue(self):
        client = Mock()
        client.chat.completions.create.return_value = response(PROPOSAL)
        verdict = {'verdict': 'fail', 'reasons': ['Unapproved date commitment'],
                   'failed_checks': ['unauthorized_commitment'],
                   '_usage': {'prompt': 1, 'completion': 1}}
        with patch.object(agent, 'OpenAI', return_value=client), patch.object(agent, 'review', return_value=verdict), patch.object(tools, 'propose_stories') as queue:
            self.assertEqual(agent.run(approved_context='P-NORTH', approved_tone=True), 'escalate')
        self.assertEqual(client.chat.completions.create.call_count, 1)
        queue.assert_not_called()

    def test_critic_context_and_verdict_schema(self):
        client = Mock()
        client.chat.completions.create.return_value = response({'verdict': 'pass', 'reasons': []})
        verdict = critic.review(client, 'test-model', 'DRAFT', 'SOURCE')
        self.assertEqual(verdict['verdict'], 'fail')
        messages = client.chat.completions.create.call_args.kwargs['messages']
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['content'], critic.CRITIC_SYSTEM)
        self.assertIn('SOURCE', messages[1]['content'])
        self.assertIn('DRAFT', messages[1]['content'])

    def test_failure_routing(self):
        for check in ['confidentiality', 'unauthorized_commitment']:
            self.assertEqual(critic.failure_action({'verdict': 'fail', 'failed_checks': [check]}, 0), 'escalate')
        ordinary = {'verdict': 'fail', 'failed_checks': ['grounding']}
        self.assertEqual(critic.failure_action(ordinary, 0), 'revise')
        self.assertEqual(critic.failure_action(ordinary, 1), 'revise')
        self.assertEqual(critic.failure_action(ordinary, 2), 'escalate')

    def test_missing_data_three_attempts_without_model(self):
        getter = Mock(return_value={'error': 'project_not_found'})
        with patch.dict(tools.TOOLS, get_project=getter), patch.object(agent, 'OpenAI') as client:
            self.assertEqual(agent.run('missing-data'), 'stuck')
        self.assertEqual(getter.call_count, 3)
        client.assert_not_called()

    def test_connection_failure_stops_immediately(self):
        getter = Mock(side_effect=ConnectionError)
        with patch.dict(tools.TOOLS, get_project=getter):
            self.assertEqual(agent.run(), 'stuck')
        self.assertEqual(getter.call_count, 1)

    def test_context_gate_precedes_model(self):
        with patch.object(agent, 'OpenAI') as client:
            self.assertEqual(agent.run(), 'awaiting_approval')
        client.assert_not_called()

    def test_deadline_interrupts_stalled_call(self):
        release = threading.Event()
        try:
            with patch.object(agent, 'MAX_SECONDS', 0.05):
                with self.assertRaises(agent.StopRun) as stop:
                    agent.Bounds().call(release.wait)
            self.assertEqual(stop.exception.outcome, 'stuck')
        finally:
            release.set()

    def test_cost_cap_checked_before_any_call(self):
        action = Mock()
        with patch.object(agent, 'COST_CAP_USD', 0):
            with self.assertRaises(agent.StopRun):
                agent.Bounds().call(action)
        action.assert_not_called()

    def test_story_cap(self):
        with patch.object(agent, 'MAX_QUEUE_ITEMS', 0):
            self.assertEqual(self.run_mock()[0], 'escalate')

    def test_retrieval_does_not_leak_other_projects(self):
        roadmap = tools.get_roadmap('Northstar')['roadmap']
        self.assertNotIn('Orbit', roadmap)
        self.assertNotIn('Vega', roadmap)
        self.assertTrue(all(r['project'] == 'Northstar' for r in tools.search_past_updates('Northstar')['matches']))
        self.assertEqual(tools.search_past_updates('unknown')['matches'], [])


if __name__ == '__main__':
    unittest.main()
