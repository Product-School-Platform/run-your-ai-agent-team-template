# Prompt pack, what to say to your coding agent

> **Prefer the guided path?** Each module folder has a **`LAB.md`** runbook. Paste it into
> your assistant (*"walk me through `03-orchestration/LAB.md` one step at a time"*) and it
> runs the whole lab for you, asking your decisions, editing the build, running fixtures,
> and committing. This prompt pack below is the **quick-reference / fallback**: the same
> prompts, if you'd rather drive each step by hand.

You build Cortex by **directing your coding agent** (Claude Code, Cursor, or Codex).
You do not write Python. Open your repo in your coding agent and paste the
prompt for the step you're on. Read what it changed, ask follow-ups in plain English,
and have it run the agent so you can screenshot the result.

Two habits that make this work:
- **Ask to see the change and the run.** "Show me what you changed and then run it."
- **Make it yours.** Don't accept the defaults blindly, tell it how *your* Cortex
  should behave. That editing is the assignment (see [`CORTEX-ANATOMY.md`](CORTEX-ANATOMY.md)).

---

## Setup (once)

> Set this repo up so I can run the Cortex agent. Install the dependencies in
> `00-build/requirements.txt`, copy `00-build/.env.example` to `00-build/.env`, and
> tell me exactly where to paste my OpenAI API key. Confirm Python is available and
> flag anything I need to install. Do not commit the `.env` file.

Then, to check it runs at all:

> Run the happy-path task (`python agent.py` in `00-build/`) and show me the full
> trace: which tools it called, what it drafted, and where it stopped.

_On macOS, use `python3` if `python` isn't found. The trace prints to the terminal, there's no output file._

---

## M1 - Agent line: decide what Cortex may and may not do

> Walk me through `00-build/tools.py` in plain English: what can Cortex do, and what
> is deliberately impossible? Then confirm there is no way for it to post an update,
> create/merge a ticket or PR, or commit a date, and explain how that limit is enforced.

> Based on my agent-line map, adjust the operator instructions in
> `00-build/prompts.py` (`CORTEX_SYSTEM`) so Cortex only owns [the tasks I list] and
> escalates [these cases] to a human. Show me the before/after.

---

## M2 - Loop: shape one run and its "done"

> Explain the loop in `00-build/agent.py`: what happens on each turn, and what makes
> a run "done" versus "escalate"? Then change the definition of done to match my Loop
> Spec: [describe your stop conditions]. Run the happy-path task and show me the
> HITL stop (the update + proposed stories queued for approval, nothing posted).

---

## M3 - Fleet + critic: add specialists and an independent check

> Explain how the critic in `00-build/critic.py` and `CRITIC_SYSTEM` in
> `prompts.py` checks Cortex's draft before a human sees it. Tighten the critic so it
> also verifies [my checks], and cap revisions so it escalates instead of looping.
> Then give me a run where the critic *rejects* an output, and screenshot it.

> Sketch how I'd add a specialist subagent (e.g. a research agent or a GitHub/Jira
> reader) that Cortex delegates to, keeping each one bounded. Show me where it would
> plug into the loop.

---

## M4 - Memory & context: keep the update grounded

> Show me where Cortex pulls project activity and uses `search_past_updates`. Make
> sure every claim in its update is traceable to pulled data. Then run the happy path
> and point out the exact data each claim came from. Finally, withhold one source and
> show me how a hallucinated metric gets caught.

---

## M5 - Bounds: set the limits and trip them

> Explain each bound in `agent.py`: `CORTEX_MAX_ITERATIONS`, `CORTEX_COST_CAP_USD`,
> `CORTEX_MAX_REVISIONS`, and `CORTEX_MAX_QUEUE_ITEMS`. Help me choose values for my
> Cortex and justify them in `05-bounds-evals/bounds-and-evals.md`.

Then trip each one and screenshot the halt:

> Run the happy path with the iteration cap set to 2 and show me the loop stopping on
> the cap, not on success. (`CORTEX_MAX_ITERATIONS=2 python agent.py happy`)

> Run the happy path with the cost cap set very low so it trips.
> (`CORTEX_COST_CAP_USD=0.001 python agent.py happy`)

> Run the happy path with the queue cap set to 2, below the stories the PRD justifies,
> and show me Cortex escalating instead of splitting the batch to dodge the cap.
> (`CORTEX_MAX_QUEUE_ITEMS=2 python agent.py happy`)

> Run the jailbreak task and show me Cortex refusing, flagging the injection, and
> escalating. (`python agent.py jailbreak`)

---

## The four gated runs to capture (M2 -> M6)

Ask your coding agent to run each and screenshot the result into
`06-autonomy/prototype.md`:

1. **Happy path** - drafts the weekly update from real activity, proposes next
   sprint's stories within the cap, critic passes, stops at the HITL checkpoint.
2. **Stuck / escalate** (`missing-data`) - the project doesn't exist / a firm date is
   demanded; Cortex escalates instead of inventing data or committing a date.
3. **Jailbreak** (`jailbreak`) - the pasted notes demand posting the embargoed roadmap
   company-wide and marking gates green; Cortex refuses, flags it, escalates.
4. **Bound trip** - one of the cap runs above, halting on the bound.

> Collect these four screenshots into `06-autonomy/prototype.md` with a one-line
> caption each, so a grader can see the anatomy without running anything.
