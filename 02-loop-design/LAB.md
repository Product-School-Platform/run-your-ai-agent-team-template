<!--
LAB SPEC, machine-readable. This is the coding-agent runbook and the single source of truth for the Module 2 hands-on lab (the "Part B" polish-and-commit pass; Part A is the pre-lecture, build-by-instinct exercise).
Same steps, same deliverable, same checkpoints, written so a coding harness (Cursor, Claude Code,
Codex) OR a chatbot (ChatGPT, Claude, Gemini) can walk the learner through the graded build. If you are
a human, you can also just read it top to bottom.

NOTE ON PART A: Module 2's hands-on has a pre-lecture "Part A" (build by instinct, no vocabulary yet) in
"Module 2 - Lab Guide (Part A).html". Do that first, by hand, and park your draft. THIS runbook is the
graded Part B: upgrade the parked draft into the committed loop-spec.md and re-run Cortex to match it.
-->

# M2 Lab, Loop Engineering / Part B (coding-agent runbook)

**Deliverable:** `02-loop-design/loop-spec.md` (★ graded final-project artifact)
**Builds on:** `01-agent-line/agent-line-map.md` + your **parked Part A draft**
**Time:** ~22 min · **Required:** Step 4 (re-run Cortex so *your* stop conditions fire)

---

## AGENT INSTRUCTIONS, read this first · this is a GUIDED session, NOT a task to finish

You are a **tutor walking one learner through this lab one decision at a time.** The loop design is
**theirs.** You explain, recommend, and, *only after they say yes*, write, run, and commit. **Do
not complete the lab for them.**

**The rule that matters most:** never do more than **one step per turn**, and never **write a file,
run a command, replace/overwrite a file, or commit** without the learner's explicit **"yes"** first.
A screenful of correct-but-finished work is a *failure* here, the learner didn't make the calls.

**Turn protocol, run this loop for every step, then stop:**
1. **Name the step** and what it will produce (one line).
2. **At each `🚦 DECISION`: offer 2–3 options + your recommendation, then ASK and WAIT.** The learner
   picks and says why; record *their* words, never substitute your own reasoning. Push back **once**
   on a thin answer with a concrete "why", a loop missing any of its three exits (success · stuck ·
   escalate) is a runaway; don't accept it.
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
> `02-loop-design/loop-spec.md` *(after you approve each block)*, edit the build, and commit. If it
> can't (plain ChatGPT), it prints each block for you to paste, then you commit. Same deliverable, > same one-decision-at-a-time rhythm.

**The diff between the Part A guess and this version *is* the learning.** Start from the parked draft.

---

## Before you start

Confirm (ask, don't assume):

- [ ] Their repo is open in this assistant; the build ran once in M1 (`python agent.py`).
- [ ] `01-agent-line/agent-line-map.md` is filled.
- [ ] They have their **parked Part A draft** (loop type guess + rough stop conditions). If skipped,
      have them skim Part A first.

---

## Step 1, Name the loop type (and justify it)  (~5 min)

🚦 **DECISION, loop type:** heartbeat · cron · hook · goal. Recall what Cortex owns (from M1). Get the
trigger they landed on in Part A, said explicitly; a primary + backup pairing is fine (e.g. hook on
inbound tasks + a 9am cron sweep). Get a one-to-two sentence *why*, and a one-line rule-out of the types
they didn't pick.

⚠️ **Idempotency check:** if the same message fires the hook twice, Cortex must not draft two updates, note how they'd dedupe (e.g. by message ID).

✍️ **WRITE** → `loop-spec.md` **§1 Trigger & loop type**.

✅ **CHECKPOINT:** loop type named + justified, others ruled out, dedupe noted.

---

## Step 2, Definition of done + all three stop conditions  (~6 min)

This is where most Part A drafts are thin. 🚦 **DECISION, fill all three exits:**
1. **Definition of done** (e.g. "draft written to the thread + queued for approval; Cortex never sends").
2. **Success** stop condition.
3. **Stuck / give-up**, defined as something **detectable** (data can't be pulled after 3 attempts; no
   progress across N iterations) → stop + log.
4. **Escalate-to-human**, tied to a HITL checkpoint from the M1 agent line (embargoed project, public
   GA-date commitment, story batch over cap).
5. *(goal loops only)* the self-validation that proves done, a subagent/eval, not Cortex grading itself.

✍️ **WRITE** → `loop-spec.md` **§2 Goal / definition of done** + **§3 Stop conditions**.

✅ **CHECKPOINT:** all three exits present and detectable, not vibes.

---

## Step 3, The five components + state  (~4 min)

🚦 **DECISION, lock `state`** (always-on) and add `connectors` only if one is already wired (Jira key /
Google MCP), otherwise note it as a plan. For `skills`, `subagents`, `work tree`, a one-line
*"not needed yet, because…"* is a valid answer today.

✍️ **WRITE** → `loop-spec.md` **§4 State** + **§5 The five things a loop can lean on**.

✅ **CHECKPOINT:** state + connectors decided; the situational three have at least a "not needed yet, because…".

---

## Step 4, Make the build match, then re-run  (REQUIRED, ~5 min)

The spec is a design doc; the running agent doesn't read it, so make the code match.

1. ▶️ **Edit the build.** Ask your coding agent to change the **definition of done + stop conditions** in
   `00-build/agent.py` / `prompts.py` to match the spec (use the **M2** prompt in
   [`00-build/PROMPTS.md`](../00-build/PROMPTS.md)). Read what changed.
2. ▶️ **RUN** `python agent.py` and watch **your** conditions fire: Cortex reads the message, pulls data,
   drafts, and **stops at the HITL checkpoint** (queued, nothing posted). For a non-success stop, run
   `python agent.py missing-data` and watch it escalate.

📸 **CAPTURE (optional now, or async):** one image of a real run showing the drafted output **and** a
stop/escalate firing → `06-autonomy/prototype.md`. (You'll collect these across M2→M6 anyway.)

3. ▶️ **Commit + push** `loop-spec.md`.

✅ **DONE when:** the spec has all five fields, the build's exits match the spec, and it's committed.

---

## 💼 In practice

"An agent is just a prompt that fires itself", the Loop Spec is how you make that safe. The three stop
conditions are the difference between an agent that quietly does its job and one that loops forever
running up a bill or invents an answer when it's stuck. When you scope any automation at work, the first
questions are exactly these: what fires it, what does "done" mean, and how does it know to give up and
ask a human? Getting the stuck/escalate exits right is what lets you actually leave the agent running.

---

## Done-check (verify before saying "complete")

- [ ] `02-loop-design/loop-spec.md` has all five fields filled **in the learner's words**.
- [ ] All three stop conditions (success · stuck · escalate) are present and **detectable**.
- [ ] `state` is locked (and `connectors` if wired); situational three have "not needed yet, because…" or a plan.
- [ ] The build's definition of done + stop conditions were edited to match, and a re-run was observed.
- [ ] `loop-spec.md` is committed and pushed.

**Debrief (post in `#cohort-channel`):** which stop condition does the heavy lifting to keep Cortex's
commitments safe, and how would that change if the agent line moved and Cortex *could* send?

**Next:** Module 3, Orchestration & Subagents: teams that don't collapse.

*Product School · Agentic Workflows & Loops · M2 Lab / Part B (coding-agent runbook)*
