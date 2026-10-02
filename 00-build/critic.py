"""Independent validator (M3). A separate model call that never saw the drafting
context, so it can't inherit the draft's blind spots. Returns a pass/fail verdict.
The revision cap that stops a critic<->drafter loop lives in `agent.py`.
"""

from __future__ import annotations

import json

from prompts import CRITIC_SYSTEM


def review(client, model: str, proposed_output: str, source_data: str) -> dict:
    """Return {"verdict": "pass"|"fail", "reasons": [...]} for a proposed output."""
    resp = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": CRITIC_SYSTEM},
            {"role": "user", "content":
                f"SOURCE DATA Cortex used:\n{source_data}\n\n"
                f"CORTEX PROPOSED OUTPUT:\n{proposed_output}"},
        ],
        response_format={"type": "json_object"},
    )
    usage = resp.usage
    try:
        verdict = json.loads(resp.choices[0].message.content)
    except (json.JSONDecodeError, TypeError):
        verdict = {"verdict": "fail", "reasons": ["critic returned unparseable output"]}
    if (not isinstance(verdict, dict)
            or verdict.get('verdict') not in ('pass', 'fail')
            or not isinstance(verdict.get('reasons'), list)
            or any(not isinstance(r, str) for r in verdict.get('reasons', []))):
        verdict = {"verdict": "fail", "reasons": ["critic returned invalid verdict schema"]}
    verdict["_usage"] = {"prompt": usage.prompt_tokens, "completion": usage.completion_tokens}
    return verdict
