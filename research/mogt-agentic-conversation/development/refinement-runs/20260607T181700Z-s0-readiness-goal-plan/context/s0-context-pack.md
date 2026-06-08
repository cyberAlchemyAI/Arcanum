---
name: MOGT S0 Goal Context Pack
description: Strict handoff context for the split Codex goal profile.
created: 2026-06-07
strict_coverage: pass
---

# MOGT S0 Goal Context Pack

## Objective

Execute the next bounded MOGT publication-readiness task: complete S0 follow-through and S3 harness feasibility without running live experiments.

## Required Inputs

- `research/mogt-agentic-conversation/development/scaffold-readiness.md`
- `research/mogt-agentic-conversation/development/mogt-publication-research.dispatch.json`
- `research/mogt-agentic-conversation/runbooks/PUBLICATION-RESEARCH-STRATEGY.md`
- `research/mogt-agentic-conversation/experiments/EXPERIMENTS.md`
- `research/mogt-agentic-conversation/papers/PAPER-REVIEW.md`
- `research/mogt-agentic-conversation/results/MOGT-EVIDENCE-STATUS.md`
- `arcana/experiment-harness/SKILL.md`

## Constraints

- Local evidence only.
- No live experiments.
- No paper result-section rewrite.
- No canonical tool mutation.
- If Experiment Harness cannot support MOGT execution evidence, produce a blocked feasibility result and route to the development pack.

## Required Outputs

- `research/mogt-agentic-conversation/development/HARNESS-FEASIBILITY.md`
- Optional if blocked: `research/mogt-agentic-conversation/development/WORK-PACK.md`
- Updated task result or goal report.

## Validation

Run Dispatch Spec validation for the publication route and record whether goal-part files remain under 4000 characters.
