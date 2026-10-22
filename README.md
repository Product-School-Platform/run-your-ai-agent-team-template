# Cortex: PM Chief-of-Staff Agent

> My final project for Product School's **Agentic Workflows & Loops** certification. A chief-of-staff agent that turns raw inputs (project state, GitHub/Jira activity, roadmap, past updates) into finished PM work, a leadership status update and a proposed backlog for a human to clear, built loop-first, bounded, grown into a fleet, and shipped up the Trust Ladder.

This is a **template repo**. Click **Use this template → Create a new repository**, name it `pm-os-agent` (or your own agent's name), and fill in one folder per module as you go.

---

## The story this repo tells

Strategy first, structure second. This repo is the **build journey of one agent, Cortex**, laid out as the exact sequence of decisions a PM makes when shipping an AI agent team. **Each folder is one framework from the course**, in the order you actually use it, and each ends in a **validation point** — a deliverable, a validator, or an eval — that proves the step is sound before you build on the next one.

Read it top to bottom as a narrative:

| # | The move (story beat) | Framework | Folder | What this step validates |
|---|---|---|---|---|
| 1 | **Draw the line** — decide what the agent owns vs. what stays human, *before* anything runs | The Agent Line | `01-agent-line/` | Every risky action has a clear owner |
| 2 | **Make it loop** — turn that hand-off into an agent that fires itself and knows when it's "done" | Loop Engineering | `02-loop-design/` | The agent knows when to run and when to stop ★ |
| 3 | **Grow the team** — split into a fleet only when there's a real reason, and add a validator | Orchestration | `03-orchestration/` | Nothing advances unchecked ★ |
| 4 | **Feed it context** — give each run the right memory without leaking or drifting | Context Engineering & Memory | `04-memory-context/` | The agent reasons on the right, safe inputs |
| 5 | **Bound it & prove it** — design for when it goes sideways, and spec it by writing its evals | Bounds, Trust & Evals | `05-bounds-evals/` | It fails safe and is measured |
| 6 | **Ship & widen trust** — demo it, reflect, and set how far up the Trust Ladder it may climb | Autonomy & the Trust Ladder | `06-autonomy/` | It runs end-to-end and earns autonomy with evidence ★ |

> **Why the numbers?** The folders keep a leading number so they sort in build order on GitHub; the name after it (`-agent-line`, `-loop-design`, …) is the framework. Number = *when*, name = *what*.

---

## How each lab runs: paste the module's `LAB.md` into your AI assistant

Every module folder ships a **`LAB.md`** — a runbook written *for your AI assistant*. Instead of reading a
guide and filling in a form, you **paste the module's `LAB.md` into your coding agent (Claude Code, Cursor,
Codex) or a chatbot (ChatGPT, Claude, Gemini)** and it walks you through the lab: it asks for your
decisions one step at a time, writes the deliverable file, runs Cortex where needed, and commits.

| Module | Paste this into your assistant |
|---|---|
| M1 | `01-agent-line/LAB.md` |
| M2 | `02-loop-design/LAB.md` |
| M3 | `03-orchestration/LAB.md` |
| M4 | `04-memory-context/LAB.md` |
| M5 | `05-bounds-evals/LAB.md` |
| M6 | `06-autonomy/LAB.md` |

A good opener: *"Open `05-bounds-evals/LAB.md` in this repo and walk me through it one step at a time.
Stop and ask me at every decision."* If your assistant can't read files (plain ChatGPT), paste the
`LAB.md` contents directly and it will print each block for you to paste into the deliverable file.

> The **prompt pack** in [`00-build/PROMPTS.md`](00-build/PROMPTS.md) is the quick-reference / fallback:
> the individual prompts the `LAB.md` files use, if you'd rather drive step by step yourself.

---

## Deliverables at a glance

| # | Deliverable | Module | Status | File |
|---|---|---|---|---|
| 1 | **Working agent demo** (real run screenshots; link optional) | Built across labs | ☐ | `06-autonomy/prototype.md` |
| 2 | **Loop Spec** | M2 | ☐ | `02-loop-design/loop-spec.md` |
| 3 | **Orchestration Map** | M3 | ☐ | `03-orchestration/orchestration-map.md` |
| 4 | **Insights: build process** | M6 | ☐ | `06-autonomy/build-insights.md` |
| 5 | **Bounds, trust & autonomy strategy** | M6 | ☐ | `06-autonomy/production-and-autonomy.md` |

## The agent in one sentence

_What does your agent do, for whom, and where is the agent line, what does it decide vs. what stays human?_

## Build & demo

- **How you built it:** _which coding agent (Claude Code / Cursor / Codex) you directed, start in `00-build/`_
- **Demo link:** _[optional shareable URL]_
- **Run screenshots:** _required, collected M2 to M6 in `06-autonomy/prototype.md`_

## Where it sits on the Trust Ladder

_shadow · assisted · supervised · bounded-autonomous · autonomous, which rung today, and what eval evidence would let it climb the next one?_

---

## How to submit

- Turn the five deliverable files into your final presentation with the **Final Project Deliverables Builder** that ships with the course. It generates `pitch.html` + a clean `README.md` for you.
- Submit both on the learning platform within 7 days of your cohort ending: your presentation and your repo link.

## Repo structure

```
pm-os-agent/
├── README.md                          ← this dashboard
├── 00-build/                          ← runnable starter: the transparent Cortex agent,
│   │                                    fixtures, RUNBOOK, PROMPTS, CORTEX-ANATOMY
│   ├── RUNBOOK.md                     ← open in your coding agent, add a key, run a fixture, screenshot
│   ├── PROMPTS.md                     ← the prompt pack: what to say to your coding agent
│   ├── CORTEX-ANATOMY.md              ← the 7 things every submission must show
│   ├── agent.py · critic.py · tools.py · prompts.py
│   └── fixtures/                      ← mock PM tasks + project/roadmap/updates/norms data
├── 01-agent-line/
│   └── agent-line-map.md              ← M1: what to hand to the agent (above vs below the line)
├── 02-loop-design/
│   └── loop-spec.md                   ← M2: the Loop Spec                 ★ Deliverable 2
├── 03-orchestration/
│   └── orchestration-map.md           ← M3: your fleet + the validator     ★ Deliverable 3
├── 04-memory-context/
│   └── memory-and-context.md          ← M4: retrieve-vs-long-context + your PM brain
├── 05-bounds-evals/
│   └── bounds-and-evals.md            ← M5: hard bounds + trajectory evals
└── 06-autonomy/
    ├── prototype.md                   ← demo + screenshots                ★ Deliverable 1
    ├── build-insights.md              ← friction · learning · aha         ★ Deliverable 4
    └── production-and-autonomy.md     ← dial · Trust Ladder · governance  ★ Deliverable 5
```
