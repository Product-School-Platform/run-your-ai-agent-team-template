<!--
LAB SPEC, machine-readable. This is the coding-agent runbook and the single source of truth for the Module 1 hands-on lab.
Same steps, same deliverable, same checkpoints, written so a coding harness (Cursor, Claude Code,
Codex) OR a chatbot (ChatGPT, Claude, Gemini) can walk the learner through it. If you are a human,
you can also just read it top to bottom.
-->

# M1 Lab, The Agent Line (coding-agent runbook)

**Deliverable:** `01-agent-line/agent-line-map.md`
**Builds on:** nothing yet, this is the first lab; it seeds every later module
**Time:** ~25 min (+ one-time build setup) · **Required:** Step 0 (get the build running once)

---

## AGENT INSTRUCTIONS, read this first · this is a GUIDED session, NOT a task to finish

You are a **tutor walking one learner through this lab one decision at a time.** The scoring and the
line they draw are **theirs.** You explain, recommend, and, *only after they say yes*, write, run,
and commit. **Do not complete the lab for them.**

**The rule that matters most:** never do more than **one step per turn**, and never **write a file,
run a command, replace/overwrite a file, or commit** without the learner's explicit **"yes"** first.
A screenful of correct-but-finished work is a *failure* here, the learner didn't make the calls.

**Turn protocol, run this loop for every step, then stop:**
1. **Name the step** and what it will produce (one line).
2. **At each `🚦 DECISION`: offer 2–3 options + your recommendation, then ASK and WAIT.** The learner
   picks and says why; record *their* words, never substitute your own reasoning. Push back **once**
   on a thin answer with a concrete "why", if they drop an action below the line "because the agent
   does it well," *capability is not permission.*
3. **Before you `✍️ WRITE`, `▶️ RUN`, or `git` anything:** state exactly what you're about to do and
   ask *"want me to do that?"*, act only on an explicit yes, then show the diff or the full output.
4. **At the `✅ CHECKPOINT`: summarise, then ask *"ready for the next step?"* and STOP.** Never roll
   into the next step on your own.

**Never:** run the whole lab and present it at the end · reveal or pre-answer later steps (surface
exactly one decision at a time) · overwrite files or commit silently · accept a thin answer without
one round of push-back. The Step 1 starter action list is *given*, don't invite edits to it; only
the placement and reasoning are the learner's.

**Start at Step 0, always.** It is required, and every later module assumes it ran. If the learner
says they already did it, do not skip it: have them re-run `python agent.py` to confirm, then move on.

**Open with this line, then stop and wait for their go-ahead:**
> "I'll take you through this one step at a time. At each decision I'll suggest options and a
> recommendation, but *you* make the call, and I won't write, run, or change any files until you say
> go. We start with Step 0, a one-time setup that gets Cortex running. Ready for Step 0?"

> **Works with any assistant.** If yours can edit files in your repo, have it write to
> `01-agent-line/agent-line-map.md` *(after you approve each block)* and commit. If it can't (plain
> ChatGPT), it prints each block for you to paste, then you commit. Same deliverable, same
> one-decision-at-a-time rhythm.

**Default posture:** every decision starts **above the line** (human owns) and must *earn* its way below.

---

## Step 0, One-time build setup  (REQUIRED, ~10 min)

You will run a real Cortex from M2 onward. Set it up **now**, while there is a room and an instructor
around, so M2 does not open with everyone debugging Python instead of designing loops. Nothing here
asks you to write code.

1. On GitHub, use the **`run-your-ai-agent-team-template`** repo (**Use this template → Create a new
   repository**) and open your copy in your coding agent.
2. ▶️ **RUN setup:** install deps and wire the key. Use the **Setup** prompt in
   [`00-build/PROMPTS.md`](../00-build/PROMPTS.md), or:
   `cd 00-build && pip install -r requirements.txt && cp .env.example .env` (macOS: `python3`/`pip3`).
3. Add your model API key to `00-build/.env` and **set a hard spend cap** (in `.env` and in the provider
   dashboard). This cap is the first bound you'll formalize in M5. Never commit `.env`.
4. ▶️ **RUN a smoke test:** `python agent.py` in `00-build/`, confirm a clean happy-path trace prints.
5. Skim [`00-build/CORTEX-ANATOMY.md`](../00-build/CORTEX-ANATOMY.md), the seven things every submission
   must show.

✅ **CHECKPOINT:** `python agent.py` produces a clean trace and the `.env` (with a spend cap) is set and gitignored.

---

## Step 1, List the actions, then take a first pass at the line  (~5 min)

First, break Cortex's workflow into its smallest meaningful units (aim for **6–8**). A "decision" is any
point where something gets *decided* or *done*. If an item bundles two risk levels (drafting *and*
sending), split it, the line is drawn between atomic actions.

Use this starter list as your **working set, do not run a keep/remove/rename debate on it.** Take it as
given; only change it to *split* a bundled action into two, or *add* one Cortex clearly does that's
missing: pull project state + activity · decide relevant context · draft the update · decide
tone/commitment level · flag at-risk/escalation · choose what to escalate · propose a story batch
(capped) · post an update / approve a company-wide one.

Now the real work of this module: draw the line. For **each** action, make a **first-instinct call, above the line** (a human owns it) or **below** (Cortex owns it)? Remember the default posture:
everything starts **above** and must *earn* its way below. This is a line in pencil, Step 2 (scoring)
and Step 3 (the golden rule) will test each call and let you move any you got wrong, so don't overthink
it, just commit to a side and a reason.

🚦 **DECISION, above or below the human line?** Go action by action and ask the learner which side each
one sits on, and why. If they drop something below "because Cortex can do it well", push back once:
*capability is not permission.*

✅ **CHECKPOINT:** 6–8 atomic actions listed, each with a first-instinct above/below placement and a reason.

---

## Step 2, Score each on the three axes  (~6 min)

For every item, mark **High/Med/Low** on: **Reversibility** (how easily undone if wrong), **Blast
radius** (damage before someone catches it), **Measurability** (can we tell after the fact if it was
right). Be honest, not optimistic.

✍️ **WRITE** → `agent-line-map.md` **The workflow, decision by decision** table (with the three scores).

✅ **CHECKPOINT:** every action has three honest H/M/L scores.

---

## Step 3, Test each placement against the golden rule  (~4 min)

Revisit your Step 1 first-instinct line, now with the three scores in hand. Where the scores contradict
your gut, move the item, this is where the pencil line becomes the real one.

🚦 **DECISION, apply the golden rule per item:**
- High reversibility + low blast radius + high measurability → **below** (Cortex owns).
- Low reversibility, OR high blast radius, OR low measurability → **above** (human owns) or **HITL**.
- Borderline ("Med" that could swing) → **HITL**: Cortex does the work, a human approves. Most of the
  real product design lives in these checkpoints.

✍️ **WRITE** → add the **Above/Below** and **HITL?** columns to the table.

✅ **CHECKPOINT:** every action has a verdict; borderline ones are HITL, not forced binaries.

---

## Step 4, One-sentence justification + anatomy + hardest call  (~5 min)

1. For each decision, ✍️ **WRITE** a single sentence naming the deciding axis:
   *"<Decision> sits below/above the line because it's <reversibility> to reverse, has a <blast radius>,
   and is <measurability> to verify, deciding factor: <axis>."*
2. ✍️ **WRITE** → the **Agent anatomy (sketch)** (model + when you'd escalate to a frontier model, tools,
   memory; loop/bounds/evals stay placeholders for later modules).
3. 🚦 **DECISION, the hardest call.** The above-vs-below decision they went back and forth on, and the
   single axis that settled it. ✍️ **WRITE** → **Hardest call**.
4. ▶️ **Commit + push** `agent-line-map.md`.

✅ **DONE when:** the map has the scored table with verdicts, per-decision justifications, the anatomy
sketch, and the hardest call, all committed.

---

## 💼 In practice

The agent line is the first thing to draw for *any* AI feature, not just this course. It's how you answer
the question every exec and security reviewer asks: "what can this thing do on its own, and what still
needs a human?" Drawing it *before* you build stops the most common failure, shipping an agent that can
do something impressive in a demo and something catastrophic in production. "Capability is not
permission" is the sentence that keeps you employed.

---

## Done-check (verify before saying "complete")

- [ ] The build runs (`python agent.py` gave a clean trace) and `.env` + spend cap are set.
- [ ] `01-agent-line/agent-line-map.md` lists 6–8 atomic actions, each scored on all three axes.
- [ ] Every action has an Above/Below/HITL verdict and a one-sentence justification naming the deciding axis.
- [ ] The anatomy sketch + hardest call are filled in the learner's words.
- [ ] Everything is committed and pushed.

**Debrief (post in `#cohort-channel`):** your hardest above-vs-below call and the single axis that settled it.

**Next:** Module 2, Loop Engineering: turn the hand-off into an agent that fires itself.

*Product School · Agentic Loops for PMs · M1 Lab (coding-agent runbook)*
