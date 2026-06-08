---
name: MOGT Live Approval Repair Pack
description: Repair work-pack for converting MOGT live approval from repair-needed toward approve-ready.
created: 2026-06-08
status: in_progress
source_refresh: development/refresh-runs/20260608T140408Z-live-approval-repair-needed/REFRESH-REPORT.md
---

# MOGT-LIVE-APPROVAL-REPAIR-PACK

## Objective

Repair the local approval blockers that prevent MOGT E1/E2/E4 from moving into
claim-bearing live evidence collection. Keep E3 second-wave by default.

## Boundary

Do not run live experiments. Do not update `results/MOGT-EVIDENCE-STATUS.md`,
paper result sections, or publication claims. This pack prepares the approval
surface only.

## SWU Manifest

| SWU ID | Parent Task | Status | Objective | Acceptance Evidence |
| --- | --- | --- | --- | --- |
| SWU-MOGT-REPAIR-001 | TASK-MOGT-REPAIR-001 | flag | Create and record 3-5 reviewer calibration examples. | `MOGT-REVIEWER-CALIBRATION-SET.md` exists with four examples and all first-wave dimensions; independent reviewer scoring remains required before pass. |
| SWU-MOGT-REPAIR-002 | TASK-MOGT-REPAIR-002 | ready | Close E1 protocol hard gates G1-G3. | E1 protocol gate table updated with evidence links; source bundle and inventory readiness notes. |
| SWU-MOGT-REPAIR-003 | TASK-MOGT-REPAIR-003 | ready | Close E2 protocol hard gates G1-G3 and source-normalization notes. | E2 protocol gate table updated with evidence links; Pareto/weighted-sum source-normalization note. |
| SWU-MOGT-REPAIR-004 | TASK-MOGT-REPAIR-004 | ready | Close E4 protocol hard gates G1-G3 and overhead thresholds. | E4 protocol gate table updated with evidence links; latency/cost/reviewer-burden stop thresholds. |
| SWU-MOGT-REPAIR-005 | TASK-MOGT-REPAIR-005 | ready | Define concrete live-run parameters and evidence mutation owners. | Model/version, temperature, scenario counts, policy regimes, cost bounds, output paths, mutation owner, adjudication gate, and paper rewrite owner. |
| SWU-MOGT-REPAIR-006 | TASK-MOGT-REPAIR-006 | pending | Rerun `MOGT-LIVE-EVIDENCE-APPROVAL` after repairs. | Approval result becomes either approve-ready, repair-needed, research-gap, or block from local evidence. |

## TASK-MOGT-REPAIR-001

### Objective

Create and record the 3-5 example reviewer calibration set required by the
finalized reviewer rubric.

### Write Scope

- `research/mogt-agentic-conversation/development/MOGT-REVIEWER-CALIBRATION-SET.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-REPAIR-001-RESULT.md`
- `research/mogt-agentic-conversation/development/MOGT-LIVE-APPROVAL-REPAIR-PACK.md`

### Done Criteria

- Calibration set has 3-5 examples.
- Examples span easy, ambiguous, and failure cases.
- First-wave score dimensions are all represented.
- At least two independent reviewers score all examples before production scoring.
- Score disagreements greater than `0.25` are adjudicated and recorded.

### Completion Evidence

- Calibration set: `research/mogt-agentic-conversation/development/MOGT-REVIEWER-CALIBRATION-SET.md`
- Result: `research/mogt-agentic-conversation/development/TASK-MOGT-REPAIR-001-RESULT.md`

### Current Gate

The calibration set artifact exists. Independent reviewer scoring and
adjudication remain required before this SWU can be marked `completed`.

## Promotion Rule

`SWU-MOGT-REPAIR-006` cannot start until `SWU-MOGT-REPAIR-001` through
`SWU-MOGT-REPAIR-005` have recorded acceptance evidence.
