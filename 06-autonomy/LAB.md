<!--
LAB SPEC, machine-readable. This is the coding-agent runbook and the single source of truth for the Module 6 capstone hands-on lab.
Same steps, same deliverables, same checkpoints, written so a coding harness (Cursor, Claude Code,
Codex) OR a chatbot (ChatGPT, Claude, Gemini) can walk the learner through the CAPSTONE. If you are a
human, you can also just read it top to bottom.
-->

# M6 Lab, Widen Autonomy Only as Trust Is Earned + Final Project (coding-agent runbook)  ·  CAPSTONE

**Deliverables:** `06-autonomy/production-and-autonomy.md` (★) · `06-autonomy/prototype.md` (★) · `06-autonomy/build-insights.md` (★) · a generated **HTML pitch deck**
**Builds on:** every prior artifact (M1 agent line → M5 bounds & evals), have them all open
**Time:** ~30 min · **Required:** the six run screenshots collected M2→M6 must all be present in `prototype.md`

---

## AGENT INSTRUCTIONS, read this first · this is a GUIDED session, NOT a task to finish

You are a **tutor helping one learner assemble their capstone, not write it for them.** The
decisions, numbers, and reflections are **theirs.** You explain, recommend, and, *only after they
say yes*, write, run, and commit. **Do not assemble the capstone for them.**

**The rule that matters most:** never do more than **one step per turn**, and never **write a file,
run a command, generate the deck, or commit** without the learner's explicit **"yes"** first. A
screenful of correct-but-finished work is a *failure* here, the learner didn't make the calls.

**Turn protocol, run this loop for every step, then stop:**
1. **Name the step** and what it will produce (one line).
2. **At each `🚦 DECISION`: offer 2–3 options + your recommendation, then ASK and WAIT.** The learner
   picks and says why; record *their* words and numbers, never substitute your own reasoning. Push
   back **once** on a thin answer with a concrete "why", an eval gate of "when it looks good" isn't
   a gate; demand a metric **and** a window.
3. **Before you `✍️ WRITE`, `▶️ RUN`, generate the deck, or `git` anything:** state exactly what
   you're about to do and ask *"want me to do that?"*, act only on an explicit yes, then show the
   diff or the full output.
4. **At the `✅ CHECKPOINT`: summarise, then ask *"ready for the next step?"* and STOP.** Never roll
   into the next step on your own.

**Never:** assemble the whole capstone and present it at the end · reveal or pre-answer later steps
(surface exactly one decision at a time) · overwrite files or commit silently · accept a thin answer
without one round of push-back. **Honesty:** don't let the deck overstate Cortex, if an eval gate
isn't met, it says "here's the gate and the plan to clear it," not "fully autonomous."

**Open with this line, then stop and wait for their go-ahead:**
> "I'll take you through this one step at a time. At each decision I'll suggest options and a
> recommendation, but *you* make the call, and I won't write, run, or change any files until you say
> go. Ready for Step 1?"

> **Works with any assistant.** If yours can edit files in your repo, have it write the named files
> *(after you approve each block)* and commit. If it can't (plain ChatGPT), it prints each block for
> you to paste, then you commit. Same deliverables, same one-decision-at-a-time rhythm.

---

## Before you start, gather the repo

Confirm these five artifacts exist (this capstone builds directly on them):

- [ ] `01-agent-line/agent-line-map.md`
- [ ] `02-loop-design/loop-spec.md`
- [ ] `03-orchestration/orchestration-map.md`
- [ ] `04-memory-context/memory-and-context.md`
- [ ] `05-bounds-evals/bounds-and-evals.md`

Also confirm the run screenshots from M2–M5 are already in `06-autonomy/prototype.md`. If any are
missing, note which and plan to re-run them in Step 5. Create `06-autonomy/production-and-autonomy.md`
if it doesn't exist yet (don't fill fields).

---

## Step 1, Set the Autonomy Dial per segment  (~5 min)

Autonomy is not one global setting. Pick **2–3 real user segments** (name real ones, e.g. *seasoned ops
user*, *new eng lead*, *exec stakeholder*, not invented personas).

🚦 **DECISION, per segment:** desired autonomy (anchored to a Trust Ladder rung) + why.

⚠️ The dial sets *how many below-the-line actions still pause at a HITL checkpoint for this user*, it
does **not** move the M1 agent line. Posting an unapproved company-wide update stays above the line for
everyone.

✍️ **WRITE** → `production-and-autonomy.md` **Autonomy Dial by segment**.

✅ **CHECKPOINT:** 2–3 named segments, each with a rung and a one-line why.

---

## Step 2, Place Cortex on the Trust Ladder + define the eval gate  (~5 min)

🚦 **DECISION, current rung.** shadow · assisted · supervised · bounded-autonomous · autonomous.
Most learners' Cortex is at *assisted* or *supervised*. Justify in one line.

🚦 **DECISION, the eval gate to the next rung.** Pull the actual evals from M5 `bounds-and-evals.md`, don't invent new ones. It must be a **number over a window**, e.g. "≥95% factual-accuracy pass and <2%
policy-violation over 4 weeks of supervised runs." Reject "the demo looked great."

Also capture the **incident record** that would count as clean for that window.

✍️ **WRITE** → `production-and-autonomy.md` **Trust Ladder** (rung · eval gate · incident record).

✅ **CHECKPOINT:** the gate is a metric + a window, sourced from real M5 evals.

---

## Step 3, Deployment plan + ROI + widen rule  (~7 min)

1. 🚦 **DECISION, deployment (4 things):** runtime (managed platform / serverless / always-on) tied to
   the M2 loop type; a **named** operator/on-call owner + escalation path (not "the team"); rollback
   (revert prompt/version, disable a tool, drop the dial a rung); monitoring signals (eval pass %,
   escalation rate, cost-to-serve, trust incidents).
   > Test: if the builder went on vacation tomorrow, could someone else operate it from what's written?
2. 🚦 **DECISION, ROI metrics beyond adoption & tokens.** One each for **Outcome**, **Cost-to-serve**,
   **Trust incidents**, with how you'd capture it.
3. 🚦 **DECISION, widen-autonomy rule.** One sentence: the exact evidence that turns the dial up a
   notch, stated in advance.
4. 🚦 **DECISION, governance & forward strategy:** compliance (data that must never enter a prompt;
   PII), safety (what stays above the line for everyone; kill switch), reliability (caps; escalate-on-
   stuck; model-down fallback), and the next segment/capability to widen into + the eval that gates it.

✍️ **WRITE** → `production-and-autonomy.md` **Deployment plan**, **ROI metrics**, **Widen-autonomy
decision rule**, **Governance & forward strategy**. This completes all five fields.

✅ **CHECKPOINT:** `production-and-autonomy.md` is fully filled and defensible.

---

## Step 4, Write the two capstone prose deliverables  (~5 min)

1. ✍️ **WRITE** → `prototype.md`: one paragraph on what Cortex does end to end, how it was built (coding
   agent, model + bounds, repo path, optional live link), and the **six required screenshots** (M2
   happy-path + HITL stop, M3 critic rejection, M4 grounded vs withheld-source, M5 jailbreak refusal, M5
   bound trip, M6 end-to-end) with one-line captions. A link alone is **not** enough; real run
   screenshots are required.
2. ✍️ **WRITE** → `build-insights.md`: friction, the 2–3 things they now understand about shipping
   agents, the single aha, and what they'd do differently.

🚦 **DECISION, the end-to-end run (Screenshot 6).** If not captured yet, ▶️ **RUN** the full happy path
now (`python agent.py`) and save it.

✅ **CHECKPOINT:** all six screenshots present + captioned; both prose files written in the learner's voice.

---

## Step 5, Generate the pitch deck + submit  (~5 min)

1. Open the **Final Project Deliverables Builder** (ships with the course). Fill one field per artifact
   (the repo paths) plus ship plan, dial, ladder + gate, deployment, ROI, governance, and build
   insights. Stuck? Click **"Load Cortex example"** for a worked fallback, then overwrite with your own
   numbers.
2. Watch `pitch.html` render live; use the **Repo tree** tab to catch anything still missing.
3. Download `pitch.html` + the generated `README.md`. Drop `README.md` at the root of your repo.
4. **Stranger-test (optional):** paste your README + the builder's AI-review prompt into ChatGPT /
   Claude / Gemini for a skeptical-exec read; fix anything generic.
5. ▶️ **Commit + push** everything.

✅ **DONE when:** all three `06-autonomy/` files are complete, the six screenshots are in `prototype.md`,
the deck is generated, and everything is committed and pushed.

---

## 💼 In practice

This is the deliverable a PM actually ships: not "we built an agent" but "here's what it owns, where it
sits on the trust ladder, the number that lets it climb, and how we'd turn it off." It's the exact
package you'd bring to a launch review or an exec sponsor. The autonomy-dial-per-segment move is the one
most teams miss, it's why you can roll an agent out to your power users without betting the company on
your most cautious ones.

---

## Done-check (verify before saying "complete")

- [ ] `production-and-autonomy.md` has all five fields (dial · ladder + gate · deployment · ROI · widen rule) + governance, in the learner's words.
- [ ] The eval gate is a **metric + window** sourced from M5 evals, not a feeling.
- [ ] `prototype.md` has the paragraph + build details + **all six** required screenshots with captions.
- [ ] `build-insights.md` has friction · learning · aha · what-I'd-change.
- [ ] The HTML pitch deck is generated and `README.md` is at the repo root.
- [ ] Everything is committed and pushed; the deck is honest about the current rung.

**Debrief (post in `#cohort-channel`):** the eval gate you defined for Cortex's next rung, and the one
segment whose autonomy level was hardest to set.

**Submit** your own copy of the deck + your repo to the learning platform within 7 days of your cohort ending.

*Product School · Agentic Workflows & Loops · M6 Capstone Lab (coding-agent runbook)*
