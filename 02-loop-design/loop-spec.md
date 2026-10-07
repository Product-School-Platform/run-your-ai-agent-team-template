# Loop Spec: Cortex PM Chief-of-Staff Agent

> Module 2 · Loop Engineering, ★ Deliverable 2
>
> ✅ **What this validates:** the agent knows when to run and when to stop, by the end you'll have proven a one-page Loop Spec with a trigger, a definition of "done," and explicit stop conditions.
>
> Your one-page blueprint for how the work you handed to the agent (M1) actually *runs*.
> An agent is just a prompt that fires itself, this spec says when it fires, what "done" means, and what it needs to do the job. Living document; refine as the course progresses.

## 1. Trigger & loop type

**Chosen type:** cron

**Schedule:** Every Tuesday at 9:30 AM in `America/New_York` (Eastern local time, adjusting automatically for daylight saving time).

**Why:** Cortex runs one hour before my Tuesday 10:30 AM VP meeting so I have time to review. Cron fits the fixed schedule; heartbeat, hook, and goal loops aren't needed.

**Duplicate prevention:** Track each project and reporting week to prevent duplicate runs.

## 2. Goal / definition of done

The weekly update for my VP and properly prioritized proposed stories pass the critic and are queued for my approval. Both elements need my approval. Cortex publishes nothing and creates no tickets automatically.

## 3. Stop conditions

| Condition | What it looks like | What happens |
|---|---|---|
| **Success** | The weekly VP update and prioritized proposed stories both pass the critic and are queued for my approval. | Stop at the human review checkpoint; nothing is published and no tickets are created. |
| **Stuck / give up** | Required data or information is still missing after 3 retrieval attempts; Cortex cannot connect to a required tool; or the run reaches 10 minutes without completing. | Stop, log the reason, and hand off to me. |
| **Escalate to human** | Data conflicts; confidential information is encountered; a request involves publishing or making commitments; the critic still rejects the output after 2 revisions; a spending or story limit is reached; or a human checkpoint in the agent-line map is reached. | Stop, record the reason, and hold the affected action for my approval. |

**Human checkpoints:** Follow [the agent-line map](../01-agent-line/agent-line-map.md): I approve relevant context, spot-check draft claims against data, decide tone and commitment level, validate risk flags, choose what to escalate, approve proposed stories, and own publishing or company-wide approval. Cortex waits for the required human decision before proceeding with the affected action.

## 4. State

Keep the last 12 months of history for each project: weekly updates, decisions, escalations, proposed user stories, approvals, and communications. This makes it easy for me to look up past outputs and decisions. Keep each project's information separate.

Track run status and reporting week for each project to prevent duplicate runs.

## 5. The five things a loop can lean on

State tracking is required. External connectors are planned; the current build uses its existing tools and critic.

| Component | For Cortex |
|---|---|
| **Work tree** (isolated workspace per run, a git worktree) | No separate workspace needed yet; Cortex only reads data and produces drafts. |
| **Skills** (reusable capabilities) | No additional reusable skills needed yet; the current prompts and tools cover this workflow. |
| **Plugins / connectors** (tools & access, optional if you don't have one yet) | Planned: Slack, Teams, email, and a ticket platform. These are not connected to Cortex yet. |
| **Subagents** (independent check when the loop can't grade itself) | Keep the existing critic to check drafts; no extra specialists needed yet. |
| **State tracking** | Keep 12 months of project-specific outputs, decisions, escalations, stories, approvals, and communications. Track run status and reporting week to prevent duplicates. |

> Context plan (M4) and the hand-off to bounds & evals (M5) come in later modules, you'll add them to their own deliverables then, not here.

## Link to live loop

[Cortex agent](../00-build/agent.py). Run `python agent.py happy --approve-context P-NORTH --approve-tone` only after approving Northstar-only context and a concise factual tone with no commitments. Without approval flags, the run stops at context/tone approval. Run `python agent.py missing-data` to demonstrate three failed retrieval attempts and a human handoff.

The current build enforces the stop conditions and saves local results. The Tuesday schedule, 12-month history, and cross-run duplicate prevention remain planned; external connectors are not connected. Spending is estimated after requests, so a request can exceed the configured threshold.

### Step 4 verification

- Eleven offline tests passed for output requirements, approval gates, retrieval and connection failures, time/spending/story limits, revision limits, escalation outcomes, and project-scoped retrieval.
- Happy path: a `gpt-4o` verification run produced the VP update and three ranked stories, passed the critic, and stopped at human approval. The run used temporary `CORTEX_MODEL=gpt-4o`, `CORTEX_PRICE_IN_PER_M=10`, and `CORTEX_PRICE_OUT_PER_M=30` overrides (conservative cost estimates, not quoted pricing). The recorded estimate was $0.0450. The saved default model was not changed; its verification attempts escalated on incorrect critic judgments about PRD scope.
- Missing data: `P-HALO` retrieval failed exactly three times, then stopped and handed off without calling the model or inventing a launch date.
- Local full traces: `00-build/run-output/trace-happy.txt` and `00-build/run-output/trace-missing-data.txt` (gitignored). These runs used fixture data, not live connectors.
