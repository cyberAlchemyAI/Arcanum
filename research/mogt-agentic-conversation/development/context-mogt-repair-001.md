---
name: MOGT Repair 001 Context Pack
description: Lean task-session context pack for SWU-MOGT-REPAIR-001.
created: 2026-06-08
selected_unit: SWU-MOGT-REPAIR-001
strict_coverage: pass
---

# MOGT Repair 001 Context Pack

## Selected Unit

`SWU-MOGT-REPAIR-001` from proposed `MOGT-LIVE-APPROVAL-REPAIR-PACK`.

Objective: create and record 3-5 reviewer calibration examples before
production scoring.

## Controlling Sources

- `research/mogt-agentic-conversation/development/refresh-runs/20260608T140408Z-live-approval-repair-needed/REFRESH-REPORT.md`
- `research/mogt-agentic-conversation/development/refresh-runs/20260608T140408Z-live-approval-repair-needed/REFRESH-PATCH-PROPOSAL.md`
- `research/mogt-agentic-conversation/development/MOGT-LIVE-EVIDENCE-APPROVAL-RESULT.md`
- `research/mogt-agentic-conversation/development/MOGT-LIVE-EXPERIMENT-APPROVAL-CHECKLIST.md`
- `research/mogt-agentic-conversation/development/MOGT-REVIEWER-RUBRIC-DRAFT.md`
- `research/mogt-agentic-conversation/development/fixtures/mogt-runtime-decision-receipts.jsonl`
- E1, E2, and E4 protocol files

## Hard Constraints

- Do not run live experiments.
- Do not update `results/MOGT-EVIDENCE-STATUS.md`.
- Do not update paper result sections or publication claims.
- Keep E3 second-wave by default.
- Calibration examples must span easy, ambiguous, and failure cases.
- Production scoring remains blocked until at least two independent reviewers
  score all calibration examples and disagreements greater than `0.25` are
  adjudicated.

## Write Scope

- `research/mogt-agentic-conversation/development/MOGT-LIVE-APPROVAL-REPAIR-PACK.md`
- `research/mogt-agentic-conversation/development/MOGT-REVIEWER-CALIBRATION-SET.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-REPAIR-001-RESULT.md`
- `research/mogt-agentic-conversation/development/context-mogt-repair-001.md`
- `research/mogt-agentic-conversation/development/context-mogt-repair-001.index.json`

## Done Criteria

- A calibration set artifact exists with 3-5 examples.
- First-wave production dimensions are covered:
  - `traceability_coverage`
  - `acceptance_score`
  - `decision_quality_score`
  - `frontier_traceability`
  - `overhead_acceptability`
  - `quality_retention`
- Reviewer scoring and adjudication requirements are represented without
  pretending a single-agent run completed independent review.

## Gate Assessment

Local creation of the calibration examples can proceed.

Completion as fully passed is blocked by missing independent reviewer scoring.
The task result should therefore be `FLAG` unless independent reviewer scores
are provided in the same task-session.
