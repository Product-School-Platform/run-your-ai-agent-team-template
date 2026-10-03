# Orchestration Map: Cortex PM Chief-of-Staff Agent

> Module 3 · Orchestration & Subagents, ★ Deliverable 3
>
> ✅ **What this validates:** nothing advances unchecked, by the end you'll have proven a justified topology, a roster, and a validator with a defined fail action.
>
> Builds on your M2 Loop Spec. Only split one agent into a team when there's a real reason, coordination has a cost.

## 1. Why split? (or why not)

**Decision:** Keep Cortex responsible for both the weekly VP update and prioritized stories, with one independent critic for an additional review before the outputs reach me.

- **Separation of concerns: No.** Both tasks relate to the same project, so I do not need to separate them.
- **Parallelism: No.** There is not a lot of data or work to do in parallel.
- **Independent validator: Yes.** I want an additional review before the outputs come to me for review.
- **Context-window pressure: No.** The current data fits one agent; there is no need to split for this reason yet.

## 2. Topology

**Pattern:** Single agent + one validating subagent, running sequentially.

```
[Scheduled PM task]
  -> [Cortex: read approved data, draft VP update + prioritized stories]
  -> [Independent critic]
       Pass -> [PM approval checkpoint: both outputs queued, nothing sent]
       Correctable failure -> [Cortex revises, maximum 2 revisions] -> [Critic]
       Still failing after 2 revisions -> [Stop and escalate to PM]
       Confidentiality / unauthorized commitment -> [Stop and escalate immediately]
```

## 3. Roster

| Agent / subagent | Responsibility | Runs which Loop Spec |
|---|---|---|
| Cortex | Reads approved project data and prepares the weekly VP update and prioritized stories; revises when requested. | [M2 Loop Spec](../02-loop-design/loop-spec.md) |
| Critic / Validator | Independently checks both outputs against source data and the five checks in Field 5; returns specific feedback. | Validation step within the M2 loop, with the failure actions and revision cap in Field 5. |

## 4. Communication & hand-offs

Use direct, in-process handoffs within the Python program; no extra service, MCP, or A2A protocol is needed.

- **Cortex to critic:** Approved source data, the drafted weekly VP update, and prioritized proposed stories.
- **Critic to Cortex:** A structured verdict (pass/fail), failed checks, and specific reasons. Correctable failures return for revision; sensitive failures stop for human review.
- **To me:** Both passing outputs are queued for my approval. Unresolved or sensitive failures are handed to me with the reason; nothing is sent automatically.

## 5. The validator

**What the critic checks:**

1. The update references the correct project and PR/issue IDs.
2. Do not invent facts, metrics, dates, progress, or context. Every factual claim must be justified by real source data, information, and context. Proposed priorities must explain their reasoning using that evidence.
3. Proposed stories fit the PRD, explain their priority, and do not duplicate completed work.
4. The story batch stays within the configured queue limit.
5. Both outputs await my approval, with no confidential disclosures or unauthorized commitments.

**Fail action:** Send correctable failures back to Cortex with the failed checks and reasons. Confidentiality or unauthorized-commitment issues stop immediately and escalate to me.

**Revision cap:** Allow at most 2 revisions after the initial draft. If the revised output still fails, stop and escalate to me.

**Pass action:** Send the weekly VP update and prioritized stories to my approval checkpoint. A critic pass is not my approval; nothing is sent automatically.

## 6. State: shared vs isolated

- **Shared:** Approved source data, the weekly update, and proposed stories.
- **Isolated:** Each agent's conversation and reasoning. The critic receives its own instructions and checks the evidence independently, without inheriting Cortex's drafting conversation.
- **Feedback returned:** Only the verdict, failed checks, and specific reasons return to Cortex, not the critic's private reasoning or conversation.
- **Across runs:** Follow the M2 plan for 12 months of project-specific history; give the critic only the approved data needed for the current review.

## 7. Cost & latency budget

**Estimated spending limit:** $0.10 for the whole run, including drafting and critic calls. Stop and hand off when the recorded estimate reaches the limit. This is checked after requests, so one request can exceed the threshold; it is not a provider billing cap.

**Call budget:** Normally 1 draft call + 1 critic call (2 total). With 2 revisions, at most 3 draft calls + 3 critic calls (6 total). The critic adds 1 call normally and up to 3 at the revision cap; cost or time limits can stop the run earlier.

**Latency budget:** Keep the existing 10-minute limit for the whole run. Validation adds one sequential model-call wait per draft, up to three waits. Actual latency varies. The saved four-call rejection demo took about 8.4 seconds overall and recorded a conservative $0.0916 estimate; this is one observation, not a guaranteed runtime or price.

Carry the $0.10 threshold, 10-minute limit, and 2-revision cap into M5 bounds and evals.
