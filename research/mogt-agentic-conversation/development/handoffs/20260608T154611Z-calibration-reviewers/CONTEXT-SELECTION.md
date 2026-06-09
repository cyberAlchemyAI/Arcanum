---
name: MOGT Calibration Reviewer Handoff Context Selection
description: Invoke handoff context selection for human, Model X, and Model Y calibration reviewers.
created: 2026-06-08
mode: invoke-handoff
coverage: pass
---

# MOGT Calibration Reviewer Handoff Context Selection

## Source Session Reference

Current MOGT repair session for `MOGT-LIVE-APPROVAL-REPAIR-PACK`, especially
`SWU-MOGT-REPAIR-001`.

## Handoff Type

`execution-continuation`

The next sessions do not run experiments. They only score the already-created
calibration examples and return bounded reviewer outputs.

## Selected Context

| Obligation | Selected Evidence |
| --- | --- |
| Score the calibration examples only | `development/MOGT-REVIEWER-CALIBRATION-SET.md` |
| Use the finalized scoring anchors | `development/MOGT-REVIEWER-RUBRIC-DRAFT.md` |
| Preserve repair-pack boundary | `development/MOGT-LIVE-APPROVAL-REPAIR-PACK.md` |
| Keep live approval blocked until scoring/adjudication | `development/TASK-MOGT-REPAIR-001-RESULT.md` |
| Keep E3 out of first-wave calibration | `MOGT-REVIEWER-CALIBRATION-SET.md` and rubric scope decision |

## Excluded Context

| Excluded Context | Reason |
| --- | --- |
| Full prior conversation transcript | Not needed; reviewer task is bounded by the calibration sheet and rubric. |
| Live experiment protocols beyond score dimensions | Reviewers must not repair protocols or run experiments. |
| Evidence-status and paper result files | Reviewers must not mutate claims or paper results. |

## Shared Reviewer Rules

- Do not run live experiments.
- Do not update `results/MOGT-EVIDENCE-STATUS.md`.
- Do not update paper result sections or publication claims.
- Do not inspect other reviewers' scores before returning your own.
- Score with numeric values in `0..1`.
- Score only dimensions requested in the calibration sheet.
- Return short rationales, not long essay reviews.
- Flag uncertainty instead of inventing missing evidence.

## Coverage Result

Coverage: pass.

The selected source artifacts cover the reviewer scoring task, isolation rules,
non-goals, and return format. Actual reviewer independence must be enforced by
separate execution sessions or human process controls.
