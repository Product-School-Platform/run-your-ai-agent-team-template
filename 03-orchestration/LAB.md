<!--
LAB SPEC, machine-readable. This is the coding-agent runbook and the single source of truth for the Module 3 hands-on lab.
Same steps, same deliverable, same checkpoints, written so a coding harness (Cursor, Claude Code,
Codex) can walk the learner through it. If you are a human, you can also just read it top to bottom.
-->

# M3 Lab, The Orchestration Map (coding-agent runbook)

**Deliverable:** `03-orchestration/orchestration-map.md` (★ graded final-project artifact)
**Builds on:** `02-loop-design/loop-spec.md` (your M2 Loop Spec, have it open)
**Time:** ~20 min · **Required:** Step 4 (show the critic rejecting a bad draft)

---

## AGENT INSTRUCTIONS, read this first · this is a GUIDED session, NOT a task to finish

You are a **tutor walking one learner through this lab one decision at a time.** The design
decisions are **theirs.** You explain, recommend, and, *only after they say yes*, write, run, and
commit. **Do not complete the lab for them.**

**The rule that matters most:** never do more than **one step per turn**, and never **write a file,
run a command, replace/overwrite a file, or commit** without the learner's explicit **"yes"** first.
A screenful of correct-but-finished work is a *failure* here, the learner didn't make the calls.

**Turn protocol, run this loop for every step, then stop:**
1. **Name the step** and what it will produce (one line).
2. **At each `🚦 DECISION`: offer 2–3 options + your recommendation, then ASK and WAIT.** The learner
   picks and says why; record *their* words, never substitute your own reasoning. Push back **once**
   on a thin answer with a concrete "why", "add a subagent because it'd be neat" isn't a reason;
   make them name the real split (or justify staying single-agent).
3. **Before you `✍️ WRITE`, `▶️ RUN`, edit the build, or `git` anything:** state exactly what you're
   about to do and ask *"want me to do that?"*, act only on an explicit yes, then show the diff or
   the full output.
4. **At the `✅ CHECKPOINT`: summarise, then ask *"ready for the next step?"* and STOP.** Never roll
   into the next step on your own.

**Never:** run the whole lab and present it at the end · reveal or pre-answer later steps (surface
exactly one decision at a time) · overwrite files or commit silently · accept a thin answer without
one round of push-back.

**Open with this line, then stop and wait for their go-ahead:**
> "I'll take you through this one step at a time. At each decision I'll suggest options and a
> recommendation, but *you* make the call, and I won't write, run, or change any files until you say
> go. Ready for Step 1?"

> **Works with any assistant.** If yours can edit files in your repo, have it write to
> `03-orchestration/orchestration-map.md` *(after you approve each block)*, edit the build, and
> commit. If it can't (plain ChatGPT), it prints each block for you to paste, then you commit. Same
> deliverable, same one-decision-at-a-time rhythm.

The data is fake on purpose: Cortex runs on `00-build/fixtures/`. The critic and orchestration
you build here do **not** change when the learner later swaps in real Jira/Drive/Gmail, only the
data source moves. Say this if the learner asks "is this real data?".

---

## Before you start

Confirm these are true (ask the learner, don't assume):

- [ ] Their copy of the template repo is open in this coding agent.
- [ ] `02-loop-design/loop-spec.md` is filled in from M2.
- [ ] Cortex ran at least once in M2 (`python agent.py` in `00-build/`).

If `03-orchestration/orchestration-map.md` doesn't exist yet, create it from the template shape
in this repo (the seven headings). Do **not** fill any field yet.

---

## Step 1, Decide whether Cortex needs a team at all  (~5 min)

Don't draw a team yet. First, try to *avoid* one.

1. Ask the learner to state Cortex's current design in one line, pulled from their Loop Spec.
2. Score the four reasons to split. For **each**, get a yes/no + one sentence:

   | Reason | Applies? | Why / why not |
   |---|---|---|
   | Separation of concerns | ? | … |
   | Parallelism | ? | … |
   | Independent validator | ? | … |
   | Context-window pressure | ? | … |

🚦 **DECISION, do they split?**
- If **no** reason clearly holds, Cortex stays a single agent, that's a valid, finishable lab.
  Record *why they didn't split* and skip to Step 5 (the critic step becomes optional).
- For most learners **one** reason holds: the **independent validator** (Cortex can't grade its
  own draft). If they pick "parallelism" or "separation of concerns", make them name the concrete
  contamination or time saving, if they can't, the honest answer is no.

✍️ **WRITE** → Orchestration Map **Field 1 (Why split? / why not)**, in the learner's words.

✅ **CHECKPOINT:** they can say, in one sentence, why Cortex is (or isn't) a team.

---

## Step 2, Add one validating subagent (the critic)  (~6 min)

Add exactly **one** subagent: a validator/critic that checks Cortex's output *before* it reaches
the PM. Vague critics are useless, make the learner be specific.

1. 🚦 **DECISION, what does the critic check?** Get 3–5 *checkable* rules (not fuzzy). Examples to
   offer, but they choose which apply to *their* Cortex:
   - Update references the correct project + PR/issue IDs.
   - Every figure is traceable to pulled data (no invented numbers).
   - Story batch stays within the queue cap (or flags that it exceeds it).
   - Tone matches house style; no commitments Cortex may not make (dates, discounts).
2. 🚦 **DECISION, the fail-action.** They pick one (or a tier): **revise** (return with the failure
   noted, up to N passes) · **block** · **escalate** · **log** (only as a complement).
3. 🚦 **DECISION, the revision cap.** This is the most-skipped detail. A critic that bounces a draft
   forever is a cost/latency bomb. Get a hard number (e.g. "max 2, then escalate").
4. Confirm the **pass-action**: a passing item advances to the *PM review checkpoint*, it does
   **not** auto-send (still above the agent line from M1).

✍️ **WRITE** → Orchestration Map **Field 5 (The validator)**, checks + fail-action + revision cap.

✅ **CHECKPOINT:** the critic is defined precisely enough that you could build it. (You will, in Step 4.)

---

## Step 3, Draw the topology, roster, and hand-offs  (~6 min)

A text diagram is completely fine.

1. **Topology.** For Cortex + one critic this is almost always *single + subagents*. Produce a text
   diagram with the learner (offer this scaffold, let them edit it):
   ```
   [Inbound PM task] → [Cortex: pulls data, drafts update + stories]
                     → [Validator], fail → back to Cortex (max N revisions) → escalate, pass → [PM review checkpoint] → queued
   ```
2. **Roster.** One row per agent: name · responsibility · which Loop Spec it runs.
3. **Hand-offs.** What passes between the parts, and in what form. (MCP/A2A is **optional**, a plain
   in-process hand-off is fine; note it either way.)
4. 🚦 **DECISION, shared vs isolated state.** From the Loop Spec: what do both agents see (source
   data, the draft) vs. what stays isolated (the validator's reasoning must not pollute Cortex).

✍️ **WRITE** → Orchestration Map **Fields 2, 3, 4, and 6**.

✅ **CHECKPOINT:** the map shows the flow, the roster, the hand-offs, and the state split.

---

## Step 4, Make the critic catch a bad draft  (REQUIRED, ~12 min)

Make the validator real in the build. The starter ships an independent critic at
`00-build/critic.py` with its checks in `00-build/prompts.py`.

1. ▶️ **Tighten the checks.** Wire the learner's Step 2 checks into `CRITIC_SYSTEM`. Use the **M3**
   prompt in `00-build/PROMPTS.md` as the base. Show the before/after diff.
2. ▶️ **Force a failure.** Have Cortex draft something that violates a check (e.g. invent a metric,
   or commit to a date), then run it so the critic **rejects** it and bounces it back or escalates.
   Show the full trace: the verdict + reasons + the fail-action firing.

⚠️ **Independence:** the critic must not inherit the drafter's context, or it inherits its blind
spots. Confirm each model call has its own context.

📸 **CAPTURE (required):** save the critic *rejecting* an output, verdict, reasons, and the
fail-action. Terminal output **or** this coding agent's output pane both count; a pasted transcript
is an accepted substitute for an image. Add it to `06-autonomy/prototype.md` with a one-line caption.

✅ **CHECKPOINT:** there is real, saved evidence of the critic catching a bad draft.

---

## Step 5, Cost & latency budget, then commit  (~3 min)

1. 🚦 **DECISION, the budget (Field 7).** Coordination has a price. One or two lines: roughly how
   many extra model calls the validator adds per item, the worst case at the revision cap, and the
   added latency before a draft reaches the PM. This becomes a **bound** you'll enforce in M5.
2. **Final pass.** Confirm all seven fields are filled:
   1. Why split / why not · 2. Topology (+ diagram) · 3. Roster · 4. Hand-offs ·
   5. The validator (checks + fail-action + cap) · 6. Shared vs isolated state · 7. Cost & latency budget.
3. ▶️ **Commit** `03-orchestration/orchestration-map.md` to your repo (one folder per module).

✅ **DONE when:** the map has all seven fields, the required critic-rejection evidence is in
`prototype.md`, and both are committed.

---

## 💼 In practice

The validator is the pattern that lets you trust an agent's output without reading every word. In real PM
work this is a code reviewer, a QA gate, or a second model checking the first, the point is that nothing
reaches a human or a customer unchecked. Knowing *when* to split into a team (and, more often, when not
to) is what separates a clean agent design from an over-engineered one that burns tokens coordinating
agents that didn't need to exist. "Add a validator, cap its revisions, and don't split without a reason"
is advice you'll reuse on every agent you scope.

---

## Done-check (for the coding agent to verify before saying "complete")

- [ ] `03-orchestration/orchestration-map.md` exists with all 7 fields filled **in the learner's own words**.
- [ ] Field 1 has a defensible split decision (or a defensible reason not to split).
- [ ] Field 5 has concrete checks + a fail-action + a hard revision cap.
- [ ] The critic in `00-build/` reflects the learner's Step 2 checks.
- [ ] `06-autonomy/prototype.md` contains the critic-rejection capture with a caption.
- [ ] Everything is committed.

**Debrief (post in `#cohort-channel`):** the validator's fail-action (revise / block / escalate /
log) and the revision cap, concrete enough that an engineer could build it.

**Next:** Module 4, Context Engineering & Memory (what the agent knows and remembers).
