# Agent Line Map: Cortex PM Chief-of-Staff Agent

> Module 1 · The Agent Line
>
> ✅ **What this validates:** every risky action has a clear owner, by the end you'll have proven an above/below-the-line map with HITL checkpoints, scored on reversibility, blast radius, and measurability.

## The workflow, decision by decision

List every discrete decision or action in your agent's workflow, then score each one and place it **above** the line (a human owns it) or **below** (the agent owns it). Borderline calls get an HITL checkpoint.

| Decision / action | Reversibility (H/M/L) | Blast radius (H/M/L) | Measurability (H/M/L) | Above / Below | HITL? |
|---|---|---|---|---|---|
| Pull project state + activity | H | L | H | Below | No |
| Decide relevant context | M | M | L | HITL (agent proposes scope) | Required |
| Draft the update | H | L | M | Below | Spot-check (claims vs data) |
| Decide tone / commitment level | L | H | L | Above | — |
| Flag at-risk / escalation | M | M | M | HITL (agent surfaces; human validates) | Required |
| Choose what to escalate | M | H | M | Above | — |
| Propose a story batch (capped) | H | M | M | HITL (agent proposes queue) | Required |
| Post an update / approve a company-wide one | L | H | H | Above | Required |

## Agent anatomy (sketch)

- **Model:** Default **gpt-4o-mini** (or equivalent fast/cheap model) for routine pulls, drafts, and capped story proposals; escalate to a **frontier model** only for ambiguous cross-project tradeoffs, high-stakes wording, or when the critic loops and needs a stronger pass.
- **Tools:** Read-only **project + activity** lookup, **past-update search**, **roadmap/norms** context, **propose_stories** (capped queue — no post/create/merge).
- **Memory:** Persist **roadmap, decision log, team norms, past updates** across runs; purge one-off task noise after the HITL checkpoint.
- **Loop:** _placeholder — M2 `loop-spec.md`_
- **Bounds:** _placeholder — M5 `bounds-and-evals.md`_ (spend cap + queue cap already in `.env`)
- **Evals:** _placeholder — M5_

## The golden rule, applied

1. **Pull project state + activity** sits **below** the line because it's **high** to reverse, has **low** blast radius, and is **high** measurability to verify; deciding factor: **measurability**.

2. **Decide relevant context** sits at **HITL** because it's **medium** to reverse, has **medium** blast radius, and is **low** measurability to verify; deciding factor: **measurability**.

3. **Draft the update** sits **below** the line (with spot-check) because it's **high** to reverse, has **low** blast radius, and is **medium** measurability to verify; deciding factor: **reversibility**.

4. **Decide tone / commitment level** sits **above** the line because it's **low** to reverse, has **high** blast radius, and is **low** measurability to verify; deciding factor: **blast radius**.

5. **Flag at-risk / escalation** sits at **HITL** because it's **medium** to reverse, has **medium** blast radius, and is **medium** measurability to verify; deciding factor: **measurability** (borderline — human validates before anyone is pinged).

6. **Choose what to escalate** sits **above** the line because it's **medium** to reverse, has **high** blast radius, and is **medium** measurability to verify; deciding factor: **blast radius**.

7. **Propose a story batch (capped)** sits at **HITL** because it's **high** to reverse, has **medium** blast radius, and is **medium** measurability to verify; deciding factor: **blast radius** (queue still skews planning if wrong).

8. **Post / approve company-wide** sits **above** the line because it's **low** to reverse, has **high** blast radius, and is **high** measurability to verify; deciding factor: **reversibility**.

## Hardest call

**Choose what to escalate** — The most critical piece of a PM is decide what to escalate when there are multiple items that have similar priorities and impact. **Blast radius** settled it: wrong routing wastes the right people even when the underlying flag was reasonable. _(Share this in `#cohort-channel`.)_
