# Build Insights: Cortex PM Chief-of-Staff Agent

> Module 6 · ★ Deliverable 4, what you learned building it
>
> ✅ **What this validates:** you can reflect on what building it taught you, by the end you'll have proven the friction, the learning, and the aha that changes how you'd design your next agent.

## Friction

The biggest friction was getting the draft and critic to agree on what the evidence supported. Cortex sometimes added unsupported wording, while the critic sometimes rejected valid claims. Fixing this required clearer source attribution—using the PRD to establish scope and issue #825 to support the analytics-review work—and checking that the critic still rejected the fake 80% metric.

## Learning

I learned that claims need evidence supporting their exact meaning: the PRD can establish scope, while an issue supports specific planned work. I also learned that a critic can make mistakes, so I need to test both valid claims and deliberately faulty inputs. Finally, shipping an agent requires clear stopping rules, saved traces, and human approval alongside useful outputs.

## Aha moment

My aha moment was realizing that autonomy should be earned through evidence. A successful demo is a starting point; Cortex needs consistent quality and safety results over the six-week supervised window before I widen its autonomy. This changed how I would design my next agent: define the human boundaries and advancement gate from the beginning.

## What you'd do differently

If I rebuilt Cortex, I would add source-attribution checks and safety evals from the beginning, testing valid claims, unsupported metrics, missing data, and jailbreak attempts before expanding the workflow. I would also add a pre-request cost estimate and an output-token limit to reduce spending overshoot while preserving enough budget for useful corrections.
