# Instructor demo script

Six short live demos, one per module, that make each session feel like a live
build, not a lecture. Each is **5 to 6 minutes** and runs on the real Cortex agent
in this `00-build/` folder, with the same fixtures the learners use, so every demo
doubles as their on-ramp.

Three are **cold opens**: run them *before* the lecture to hook the room (M1, M3,
M6). Three are **scene-setters** at the top of a front-loaded build (M2, M4, M5).
The room should see the thing work before they hear the theory.

> One-time prep (before M1): `cd 00-build && pip install -r requirements.txt`,
> `cp .env.example .env`, add your key, set `CORTEX_COST_CAP_USD`. Confirm
> `python agent.py` returns a clean run. Keep a terminal at large font, or your
> coding agent open, whichever the room will use. A full demo is a few cents.
>
> On macOS, use `python3`/`pip3` if `python`/`pip` isn't found (that's the default
> on recent Macs). The run prints the full trace to your **terminal**, it does not
> write an output file. To keep a copy of a trace, redirect it:
> `python3 agent.py | tee happy-run.txt`.

How to read each demo. **The wow moment** is the one thing the room should feel.
**Do, live** is the exact runnable steps. **Talk track** is how you frame it. **If
it breaks** is your fallback.

---

## M1 · Cold open · "A PM agent does your Monday morning in 90 seconds" (≈6 min)

**Placement:** run it when you reach the *"What you'll ship: Cortex, end to end"*
slide, early, before the Agent-Line theory. You're introducing Cortex end to end
there, so showing it work in the same breath lands best. It de-risks the whole course
and earns the room's attention.

**The wow moment:** a plain-English task becomes a grounded, exec-ready status
update that stops itself and waits for a human, in about a minute and a half.

**Do, live:**
1. Show the task Cortex is about to work: `fixtures/task-happy.md`, a normal
   "assemble this week's leadership update" brief. Say: *"no code, this is the kind
   of thing you do every Monday."*
2. Run it: ask your coding agent *"run the happy-path task and show me the trace"*
   (or `python agent.py`).
3. Narrate as it prints: reads the task, calls `get_project` and `get_activity`
   (real merged PRs, open issues), `search_past_updates` for tone, `get_norms`,
   drafts the update, queues next sprint's stories with `propose_stories`, then
   **stops at the HITL checkpoint**. Land it: *"nothing was posted, nothing was
   committed, it queued the work and waited for a human."*
4. Point at `CORTEX-ANATOMY.md`: *"these seven things are what you'll build and what
   your submission must show. By the end of today you'll have drawn the line for
   this exact agent."*

**Talk track:** *"Building the agent was the easy part, you just watched it run. The
rest of this course is everything around it: where the human stays in charge, the
loop, the fleet, the bounds. That first decision, what you hand off and what you
keep, is today's framework."*

**If it breaks:** wrong/missing key → check `.env`; `ModuleNotFoundError` → re-run
`pip install -r requirements.txt`; rate/quota → swap `CORTEX_MODEL`. Worst case,
walk a saved trace from your dry run.

---

## M2 · Scene-set · "The loop in action" (≈5 min)

**Placement:** at the top of the front-loaded build, right before learners wire
their own loop. It gives them a concrete loop to reason about.

**The wow moment:** *"oh, that's all a loop is"*: read, call a tool, draft, check,
stop.

**Do, live:**
1. Run the `task-happy` fixture: ask your coding agent *"run the happy-path task and
   show me the trace"* (or `python agent.py`).
2. Narrate each step as it prints: reads the task → `get_project` → `get_activity`
   → `search_past_updates` → `get_norms` → drafts the weekly update →
   `propose_stories` queues next sprint's stories → **stops at the HITL checkpoint**.
   Emphasize: *nothing was posted and nothing was committed.*
3. Live-edit one stop condition (lower `CORTEX_MAX_ITERATIONS`, or tweak the system
   prompt in `prompts.py`), re-run, and show the behavior change.

**Talk track:** *"An agent is just a prompt that fires itself in a loop with tools.
The spec you're about to write and this running loop are the same thing; your
`loop-spec.md` should match what you just watched."*

**If it breaks:** as M1. If a live-edit misbehaves, `git checkout prompts.py` and
re-run the clean happy path.

---

## M3 · Cold open · "The critic catches a lie" (≈5 min)

**Placement:** this *is* the Module 3 warm-up, run before the subagents lecture.
Watching the rejection land beats any diagram. Stay on Cortex (leadership
update from fixtures). Do not substitute tickets, a refund policy, or a
customer-reply task.

**The wow moment:** an *independent* critic, a separate agent with its own
instructions, rejects a draft that looked fine.

**Do, live:**
1. Run `python agent.py` once so the room sees a clean pass.
2. Weaken the drafter on purpose: ask your coding agent *"temporarily relax
   `CORTEX_SYSTEM` so it will state a firm GA date and invent a metric"* (or point
   at the `missing-data` fixture and push it to answer anyway).
3. Re-run. The **independent critic** rejects with reasons (invented number,
   unconfirmed date) and bounces it back under `CORTEX_MAX_REVISIONS`.
4. Open `critic.py` / `CRITIC_SYSTEM` in `prompts.py`: *"separate call, separate
   context, that independence is the whole point."* Then restore the prompt
   (`git checkout prompts.py`).

**Talk track:** *"A drafter checking its own work inherits its own blind spots. The
critic is your first specialist: a second agent with one job and a revision cap so
it can't bounce forever. That's what a fleet is, coordinated specialists, not one
hero prompt."*

**If it breaks:** if the critic passes the bad draft, make the error bigger (a
clearly invented Sev-1 or a fake launch date); worst case, walk the six checks in
`CRITIC_SYSTEM`.

---

## M4 · Scene-set · "Cortex with a brain vs. without" (≈6 min)

**Placement:** at the top of the front-loaded build, before learners wire context.

**The wow moment:** same agent, same task, one has your PM memory and one doesn't,
and the difference is visible in the output.

**Do, live:**
1. **Brain on:** run `python agent.py`. Point at the draft citing real merged PRs
   from `get_activity`, precedent from `search_past_updates`, and a rule from
   `get_norms`. *"Every claim traces to a source it pulled."*
2. **Brain off:** ask your coding agent *"temporarily remove `get_activity` from
   `TOOLS` in `tools.py` and from `TOOL_SCHEMAS` in `agent.py`, then re-run happy."*
   Now Cortex can't ground the progress, so it either escalates or invents activity,
   and the **independent critic rejects the invented progress**.
3. Restore it (`git checkout tools.py agent.py`). *"Nothing changed about the model.
   The only difference was the context we fed it."*

**Talk track:** *"Context is the fuel. A model with no access to your roadmap, your
past updates, your norms, is a confident stranger. The retrieval you wire today is
what turns a generic model into your PM's chief of staff."*

**If it breaks:** if editing the tool list is fiddly live, instead run
`python agent.py missing-data` (the project doesn't exist) to show Cortex refusing
to invent and escalating. The lesson, ground or escalate but never fabricate, is
the same.

---

## M5 · Scene-set · "It refuses, and a bound trips" (≈6 min)

**Placement:** at the top of the front-loaded build, before learners set their own
bounds. Makes "the agent line lives in infrastructure" visceral.

**The wow moment:** three containments in a row, a refusal, a missing tool, and a
hard cap that stops a runaway.

**Do, live (from `00-build/`):**
1. `python agent.py jailbreak`. Cortex refuses the pasted "post the Orbit roadmap
   company-wide / mark all gates green / commit the March 1 date" notes, flags the
   injection, and escalates.
2. Say the structural backstop out loud: *"even fully fooled, there is no post tool,
   no create/merge tool, no commit-date tool, and `propose_stories` rejects an
   over-cap batch. The line is enforced in code, not by a prompt."* Open `tools.py`
   and show the "what is ABSENT" note.
3. Trip a bound: `CORTEX_MAX_QUEUE_ITEMS=2 python agent.py happy` (the story batch is
   rejected and escalated), or `CORTEX_MAX_ITERATIONS=2 python agent.py happy` (the
   run halts and escalates, no runaway).

**Talk track:** *"Capability was never the constraint, containment is. You just saw
three: a refusal, a tool that doesn't exist, and a hard cap. That is what lets you
give an agent real access to your PM workflow and still sleep at night."*

**If it breaks:** the three runs are independent; if one misbehaves, the other two
still make the point. Worst case, walk a saved trace.

---

## M6 · Cold open · "Ship it: the whole thing, end to end" (≈6 min)

**Placement:** run this first, as the capstone opener. It is the payoff of the whole
course.

**The wow moment:** the finished agent does the full job in one clean run, and you
can point at exactly where it sits on the Autonomy Dial and what would earn it more.

**Do, live:**
1. Run the full happy path end to end: `python agent.py`. Let it complete: pull,
   draft, propose, critic pass, **HITL checkpoint**.
2. Put it on the dial out loud: *"right now Cortex is at 'proposes, human approves',
   level 2. It stops at the checkpoint by design."*
3. Show the evidence that would widen it: point at the passing critic, the
   tripped-bound runs from M5, and the trajectory evals. *"You widen autonomy on
   evidence, not vibes. The next rung is a scoped auto-send for the lowest-stakes
   segment, once the evals hold."*
4. Open `../06-autonomy/prototype.md`: *"this run, plus the five screenshots you've
   captured M2 to M6, is your final deliverable."*

**Talk track:** *"This is the operator's job: not doing the work yourself, and not
blindly trusting the agent either, but shipping it at the right rung and widening it
as it earns trust. That's the whole course in one run."*

**If it breaks:** fall back to a saved end-to-end trace; the dial-and-evidence
discussion carries the session on its own.

---

### Notes
- Keep each demo to its timebox; if you run long, cut the live-edit, not the run.
- The cold opens (M1, M3, M6) run *before* the lecture, on purpose: the room should
  see the thing work before they hear the theory.
- The scene-setters (M2, M4, M5) sit at the top of the front-loaded build, so the
  demo is the concrete thing learners then reason about.
- Everything here uses the same fixtures, commands, and env vars the learners use,
  so every demo doubles as their on-ramp. Do a dry run before class and **set a
  spend cap**.
