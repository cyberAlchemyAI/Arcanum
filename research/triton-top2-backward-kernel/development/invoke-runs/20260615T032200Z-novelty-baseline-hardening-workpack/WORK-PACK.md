# Work Pack - Novelty And Baseline Hardening

Status: `ready-for-task-session`
Owner: `research/triton-top2-backward-kernel`

## Objective

Close the most visible baseline and novelty gaps before any stronger CAP2 claim.

## Source Evidence

- `stages/subagents/novelty-prior-art-reviewer.md`
- `stages/subagents/baseline-coverage-reviewer.md`
- `RELAXATION-CANDIDATES.md`
- `CAP2-PRIOR-ART-COMPARISON.md`
- `FINAL-PRIOR-ART-NOVELTY-REPORT.md`

## Task Board

| Task ID | Layer | Task | Status |
| --- | --- | --- | --- |
| TASK-NOV-001 | L0 | Add entmax baseline or explicit deferral artifact. | ready |
| TASK-NOV-002 | L1 | Create CAP2 novelty/prior-art comparison matrix. | ready-after-001 |
| TASK-NOV-003 | L1 | Add CAP2 soft-rank equivalence/overlap check. | ready-after-002 |
| TASK-NOV-004 | L2 | Add CAP2 kill/promote checklist. | ready-after-003 |
| TASK-NOV-005 | L3 | Sync final novelty report and paper claim guards. | ready-after-004 |

## SWU Manifest

| SWU ID | Parent | Goal | Write Scope | Validation |
| --- | --- | --- | --- | --- |
| SWU-NOV-001 | TASK-NOV-001 | Implement entmax reference baseline or write formal deferral with source. | `reference/router_reference.py`, `reference/router_torch.py`, tests, or `ENTMAX-BASELINE-DEFERRED.md` | pytest or deferral review |
| SWU-NOV-002 | TASK-NOV-002 | Add matrix covering NeuralSort/SoftSort, SOFT top-k, convex sparse top-k, sparsemax/entmax, ReMOE. | `CAP2-NOVELTY-COMPARISON-MATRIX.md` | every row has source/evidence |
| SWU-NOV-003 | TASK-NOV-003 | Compare CAP2 formula to soft-rank style formulas. | `CAP2-SOFT-RANK-EQUIVALENCE-CHECK.md` | algebra review |
| SWU-NOV-004 | TASK-NOV-004 | Define kill/promote criteria and acceptance thresholds. | `CAP2-KILL-PROMOTE-CHECKLIST.md` | criteria map to tests/evidence |
| SWU-NOV-005 | TASK-NOV-005 | Update reports without overclaiming. | `FINAL-PRIOR-ART-NOVELTY-REPORT.md`, paper claim guards | non-claims preserved |

## Gates

- Do not claim novelty unless matrix and equivalence check support it.
- Entmax may be deferred, but deferral must be explicit and visible.
- CAP2 remains candidate-only until the gate changes.

## Next Route

`task-session` beginning with `SWU-NOV-001`.
