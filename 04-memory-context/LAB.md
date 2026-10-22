<!--
LAB SPEC, machine-readable. This is the coding-agent runbook and the single source of truth for the Module 4 hands-on lab (the "Part B" polish-and-commit pass; Part A is the pre-lecture, build-by-instinct exercise).
Same steps, same deliverable, same checkpoints, written so a coding harness (Cursor, Claude Code,
Codex) OR a chatbot (ChatGPT, Claude, Gemini) can walk the learner through the graded build. If you are
a human, you can also just read it top to bottom.

NOTE ON PART A: Module 4's hands-on has a pre-lecture "Part A" (ground Cortex + draft the memory plan by
instinct, no rubric yet) in "Module 4 - Lab Guide (Part A).html". Do that first, by hand, and park your
draft. THIS runbook is the graded Part B: defend each call with the rubric, add the retrieval-quality
moves, finalize the memory map, re-run the grounding probe, and commit.
-->

# M4 Lab, Context Engineering & Memory / Part B (coding-agent runbook)

**Deliverable:** `04-memory-context/memory-and-context.md` (context budget · per-source retrieve-vs-long-context · retrieval-quality plan · memory map · risks & mitigations)
**Builds on:** M1 agent-line + M2 loop-spec + M3 orchestration-map + your **parked Part A draft**
**Time:** ~29 min (incl. Step 0 data-pack ingest) · **Required:** Step 4 (re-run the grounding probe, grounded answer + caught hallucination)

---

## AGENT INSTRUCTIONS, read this first · this is a GUIDED session, NOT a task to finish

You are a **tutor walking one learner through this lab one decision at a time.** The per-source
calls are **theirs.** You explain, recommend, and, *only after they say yes*, write, run, and
commit. **Do not complete the lab for them.**

**The rule that matters most:** never do more than **one step per turn**, and never **write a file,
run a command, replace/overwrite a file, swap fixtures, or commit** without the learner's explicit
**"yes"** first. A screenful of correct-but-finished work is a *failure* here, the learner didn't
make the calls. (This includes Step 0: don't swap the data-pack fixtures for them without a yes.)

**Turn protocol, run this loop for every step, then stop:**
1. **Name the step** and what it will produce (one line).
2. **At each `🚦 DECISION`: offer 2–3 options + your recommendation, then ASK and WAIT.** The learner
   picks and says why; record *their* words, never substitute your own reasoning. Push back **once**
   on a thin answer with a concrete "why", a retrieved source with *no* agentic move is naive RAG,
   the thing that made Cortex hallucinate.
3. **Before you `✍️ WRITE`, `▶️ RUN`, replace/ingest a file, or `git` anything:** state exactly what
   you're about to do and ask *"want me to do that?"*, act only on an explicit yes, then show the
   diff or the full output.
4. **At the `✅ CHECKPOINT`: summarise, then ask *"ready for the next step?"* and STOP.** Never roll
   into the next step on your own.

**Never:** run the whole lab and present it at the end · reveal or pre-answer later steps (surface
exactly one decision at a time) · overwrite files, swap fixtures, or commit silently · accept a thin
answer without one round of push-back.

**Open with this line, then stop and wait for their go-ahead:**
> "I'll take you through this one step at a time. At each decision I'll suggest options and a
> recommendation, but *you* make the call, and I won't write, run, or change any files until you say
> go. Ready for Step 0?"

> **Works with any assistant.** If yours can edit files in your repo, have it write to
> `04-memory-context/memory-and-context.md` *(after you approve each block)*, run the probe, and
> commit. If it can't (plain ChatGPT), it prints each block for you to paste, then you commit. Same
> deliverable, same one-decision-at-a-time rhythm.

The build runs on `00-build/fixtures/`; the sources are the real tools in `00-build/tools.py`
(`get_task`, `get_project`, `get_activity`, `search_past_updates`, `get_roadmap`, `get_norms`).

---

## Before you start

Confirm (ask, don't assume):

- [ ] Their repo is open; M1/M2/M3 artifacts exist; the build ran in M2.
- [ ] They have their **parked Part A draft** (per-source gut calls + remember/forget + "how it rots").
      If skipped, have them skim Part A first.

---

## Step 0, Ingest this week's data pack (download → add → run → push)  (~4 min)

Module 4 is about *what data flows into the agent*, so start by **ingesting new data
into the repo yourself**, instead of running on data that was silently pre-loaded. The
learner downloads the **Cortex Data Pack** (a refreshed pull), drops it into their
`fixtures/`, runs the agent on it, and pushes the change to GitHub. This is the exact
loop a PM runs whenever a source updates.

1. ▶️ **Download** `cortex-data-pack.zip` from the Module 4 resources (the deck's
   *Resources & templates* slide, or the Lab Guide). Unzip it.
2. ▶️ **Add it to the repo.** Copy the **five data files** (`projects.json`,
   `past-updates.json`, `decision-log.json`, `roadmap.md`, `team-norms.md`) into
   `00-build/fixtures/`, overwriting the older pull. **Leave the `task-*.md` files
   alone.** Then `git status` / `git diff --stat` so the learner *sees* the ingest.
3. ▶️ **RUN** `python agent.py` on the new data. The draft should now cite the
   **new** numbers (activation `43%`, prior `41%`; PRs #820/#823), grounded on files
   the learner just added. `Pulsar` (new) and `Orbit` stay out of any company-wide update.
4. ▶️ **Commit + push** the fixtures: `git add 00-build/fixtures/` →
   `git commit -m "Ingest 2026-07-06 data pack"` → `git push`. (Full steps and the
   copy-paste commands are in the pack's `INGEST.md`.)

> **Bring your own instead (optional).** A learner who'd rather ground Cortex in their
> *real* team's norms/roadmap/updates can skip the pack and follow
> `00-build/fixtures/BRING-YOUR-OWN-DATA.md`, same download→add→run→push loop, their
> numbers. Hold them to that guide's three flags (one **confidential** item, one
> **held/unconfirmed** launch, one **citable metric with a prior**) so Step 4's
> grounding probe still catches a hallucination.

✅ **CHECKPOINT:** `git diff --stat` shows the five fixtures changed; a run cites the
new figures; the commit is pushed. Now Cortex is grounded on data the learner ingested.

---

## Step 1, Defend each retrieve-vs-long-context call with the rubric  (~7 min)

Run **each source** through the rubric: **size · volatility · citation/audit · cost · latency**. Keep or
flip the Part A call, and get a one-line *why* naming the **deciding factor**.

🚦 **DECISION, per source (from the build):** `get_activity` (large/grows), `search_past_updates`
(unbounded), `get_roadmap` (medium; confidential flags), `get_norms` (medium; must stay current),
`get_task` (one static doc). Retrieve or long-context? Offer the worked-example default, but make them
defend *their* call.

✍️ **WRITE** → `memory-and-context.md` **§1 Context budget** + **§2 Retrieve vs. long-context (per source)**.

✅ **CHECKPOINT:** every source has a decision + deciding factor; the context budget states priority order.

---

## Step 2, Retrieval quality plan (the agentic moves)  (~5 min)

For every **retrieve** source, 🚦 **DECISION, ** which of the five agentic moves its failure mode
demands (not all five everywhere): **routing · document grading · reranking · self-verification ·
caching**.

⚠️ If a retrieved source has **no** move checked, that's naive RAG, at minimum, grade what comes back.

✍️ **WRITE** → `memory-and-context.md` **§3 Retrieval quality plan** (a source × move grid).

✅ **CHECKPOINT:** each retrieved source has at least one agentic move justified by its failure mode.

---

## Step 3, Memory map + risks & mitigations  (~5 min)

🚦 **DECISION, memory map:** what Cortex stores in **working** (this run), **episodic** (past
runs/threads), **semantic** (durable facts/prefs), and **shared** (across agents), with a lifetime/TTL
for each.

🚦 **DECISION, risks & mitigations:** cover all four, **drift**, **poisoning**, **staleness**,
**PII/retention**, each with where it bites Cortex and the mitigation. (This is where the A3 "how it
rots" sketch gets real.) Tie read/write scope back to the M1 agent line and TTLs forward to M5 bounds.

✍️ **WRITE** → `memory-and-context.md` **§4 Memory map** + **§5 Memory risks & mitigations**.

✅ **CHECKPOINT:** four memory types scoped with TTLs; all four risks have mitigations.

---

## Step 4, Re-run grounding to match the plan  (REQUIRED, ~5 min)

Make the retrieve-vs-long-context distinction real in the build.

1. ▶️ **RUN the happy path** (`python agent.py`) and point out the **exact pulled data** each claim came
   from (a retrieve source like `get_activity`/`get_norms` that Cortex must *cite*; the task itself as a
   long-context source).
2. ▶️ **RUN the probe:** withhold a source Cortex needs (remove `get_activity`, or run
   `python agent.py missing-data`). A well-grounded Cortex says "I can't verify that" or escalates
   instead of inventing, and the critic catches an invented metric.

📸 **CAPTURE (required):** two states, (a) a grounded answer citing pulled data, and (b) the
withheld-source case where Cortex refuses/gets caught, into `06-autonomy/prototype.md` with captions.

3. ▶️ **Commit + push** `memory-and-context.md`.

✅ **DONE when:** all five sections are filled, the grounding capture is saved, and everything is committed.

---

## 💼 In practice

This is the module that decides whether your agent is confidently wrong or reliably right. "Retrieve vs.
long-context per source" is the call that keeps costs sane and answers grounded, and it's exactly the
conversation you'll have with engineers building any RAG or agent feature. The memory risks (drift,
poisoning, staleness, PII) are the ones that surface six months after launch when a stored fact goes
stale or a bad input gets trusted forever. A PM who can point at *why* each source is retrieved and *what*
the agent forgets and when is the one who prevents those incidents.

---

## Done-check (verify before saying "complete")

- [ ] `04-memory-context/memory-and-context.md` has all five sections **in the learner's words**.
- [ ] Every source has a retrieve/long-context decision with a named deciding factor.
- [ ] Every retrieved source has at least one agentic-retrieval move (no naive-RAG rows).
- [ ] Memory map covers working/episodic/semantic/shared with TTLs; all four risks have mitigations.
- [ ] The required grounding capture (grounded + withheld-source) is in `06-autonomy/prototype.md`.
- [ ] Everything is committed and pushed.

**Debrief (post in `#cohort-channel`):** your trickiest retrieve-vs-long-context call and the single
rubric factor (size, volatility, citation, cost, or latency) that settled it.

**Next:** Module 5, Bounds, Trust & Evals: make it fail safe and prove it.

*Product School · Agentic Workflows & Loops · M4 Lab / Part B (coding-agent runbook)*
