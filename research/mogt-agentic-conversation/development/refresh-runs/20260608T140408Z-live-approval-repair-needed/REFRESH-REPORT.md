---
name: MOGT Live Approval Repair Needed Refresh Report
description: Invoke refresh report for the MOGT live-evidence approval repair-needed verdict.
created: 2026-06-08
mode: refresh
mutation_mode: proposal-only
phase_status: pass
---

# Refresh Report: MOGT Live Approval Repair Needed

## Identity

- Source session reference: current MOGT live-evidence approval gate
- Evidence date: 2026-06-08
- Refresh scope: convert the `repair-needed` approval verdict into a proposal-only planning delta for the MOGT workflow artifacts.
- Mutation mode: proposal-only
- Target lifecycle owner: `research/mogt-agentic-conversation`

## Source Signals

| Signal ID | Type | Source | Claim | Confidence | Mutation Safety |
| --- | --- | --- | --- | --- | --- |
| SIG-MOGT-REFRESH-001 | status_changed | `development/MOGT-LIVE-EVIDENCE-APPROVAL-RESULT.md#verdict` | Live evidence approval is decided as `repair-needed`; live experiments are not approved. | high | safe |
| SIG-MOGT-REFRESH-002 | blocker_opened | `development/MOGT-LIVE-EVIDENCE-APPROVAL-RESULT.md#calibration-status` | A 3-5 example reviewer calibration set is required before production scoring. | high | safe |
| SIG-MOGT-REFRESH-003 | blocker_opened | `experiments/E1-tradeoff-traceability-baseline/protocol.md`, `experiments/E2-pareto-arbitration-quality/protocol.md`, `experiments/E4-overhead-feasibility-envelope/protocol.md` | E1, E2, and E4 hard gates G1-G3 remain `pending`. | high | safe |
| SIG-MOGT-REFRESH-004 | route_changed | `development/MOGT-LIVE-EVIDENCE-APPROVAL-RESULT.md#next-recommended-route` | Next route should be `MOGT-LIVE-APPROVAL-REPAIR-PACK`, then return to live approval. | high | safe |
| SIG-MOGT-REFRESH-005 | blocker_opened | `development/MOGT-LIVE-EVIDENCE-APPROVAL-RESULT.md#live-run-parameter-status` | Concrete live model/run parameters are not approved. | high | safe |
| SIG-MOGT-REFRESH-006 | blocker_opened | `development/MOGT-LIVE-EVIDENCE-APPROVAL-RESULT.md#evidence-mutation-policy` | Evidence-status mutation and paper result rewrites remain blocked until claim adjudication exists. | high | blocked |
| SIG-MOGT-REFRESH-007 | no_op | `development/MOGT-LIVE-EVIDENCE-APPROVAL-RESULT.md#e3-decision` | E3 is already represented as second-wave by default. | high | safe |

## Target Artifact Inventory

| Artifact | Owner | Current Claim | Refresh Relevance |
| --- | --- | --- | --- |
| `development/MOGT-LIVE-EVIDENCE-APPROVAL-RESULT.md` | MOGT approval gate | Approval verdict is `repair-needed`. | Primary source signal. |
| `development/MOGT-LIVE-EXPERIMENT-APPROVAL-CHECKLIST.md` | MOGT approval gate | Live experiments are not approved; next actions list repairs. | Already represents the verdict; no direct patch needed. |
| `development/MOGT-REVIEWER-RUBRIC-DRAFT.md` | MOGT reviewer rubric | Rubric is finalized as a scoring gate and requires 3-5 calibration examples. | Confirms calibration requirement. |
| `development/WORK-PACK.md` | MOGT harness development pack | Harness SWUs are complete; no live-approval repair SWUs exist. | Candidate target for a future approved plan update. |
| `results/MOGT-EVIDENCE-STATUS.md` | MOGT evidence audit | All claims remain insufficient. | Must not be upgraded from repair evidence. |
| `experiments/E1-tradeoff-traceability-baseline/protocol.md` | MOGT experiment protocol | G1-G3 are pending. | Repair scope. |
| `experiments/E2-pareto-arbitration-quality/protocol.md` | MOGT experiment protocol | G1-G3 are pending. | Repair scope. |
| `experiments/E4-overhead-feasibility-envelope/protocol.md` | MOGT experiment protocol | G1-G3 are pending. | Repair scope. |

## Delta Summary

| Delta | Target Artifact | Proposed State | Evidence |
| --- | --- | --- | --- |
| status_changed | `development/WORK-PACK.md` | Add a new proposed section for `MOGT-LIVE-APPROVAL-REPAIR-PACK` with ready SWUs, while keeping harness SWUs completed. | SIG-MOGT-REFRESH-001, SIG-MOGT-REFRESH-004 |
| blocker_opened | `development/WORK-PACK.md` | Represent calibration, protocol gates, live-run parameters, and evidence mutation policy as repair tasks. | SIG-MOGT-REFRESH-002, SIG-MOGT-REFRESH-003, SIG-MOGT-REFRESH-005, SIG-MOGT-REFRESH-006 |
| no_op | `results/MOGT-EVIDENCE-STATUS.md` | Leave all claim evidence statuses unchanged. | SIG-MOGT-REFRESH-006 |
| no_op | `development/MOGT-LIVE-EXPERIMENT-APPROVAL-CHECKLIST.md` | No patch needed; latest repair-needed state is already represented. | SIG-MOGT-REFRESH-001 |
| no_op | E3 first-wave planning | Keep E3 second-wave by default. | SIG-MOGT-REFRESH-007 |

## Proposed Changes

- Create an approved follow-up work-pack or append an approved proposal section to `development/WORK-PACK.md` for `MOGT-LIVE-APPROVAL-REPAIR-PACK`.
- Split the repair pack into SWUs:
  - `SWU-MOGT-REPAIR-001`: create and record the 3-5 example reviewer calibration set.
  - `SWU-MOGT-REPAIR-002`: close E1 protocol hard gates G1-G3.
  - `SWU-MOGT-REPAIR-003`: close E2 protocol hard gates G1-G3 and source-normalization notes.
  - `SWU-MOGT-REPAIR-004`: close E4 protocol hard gates G1-G3 and overhead stop thresholds.
  - `SWU-MOGT-REPAIR-005`: define concrete live-run parameters and evidence mutation owners.
  - `SWU-MOGT-REPAIR-006`: rerun `MOGT-LIVE-EVIDENCE-APPROVAL` after repairs.
- Preserve the current evidence boundary: no live experiments, no paper result rewrites, and no claim evidence promotion.

## Applied Changes

- n/a; mutation mode is proposal-only.

## Skipped Changes

| Candidate Change | Reason Skipped |
| --- | --- |
| Update `development/WORK-PACK.md` directly | Requires explicit apply approval or task-session execution over the repair pack. |
| Update `results/MOGT-EVIDENCE-STATUS.md` | Repair-needed approval evidence does not support claim upgrades. |
| Update paper result sections | No claim-bearing live evidence exists. |
| Include E3 in first-wave live approval | E3 is second-wave by default unless explicitly approved later. |

## Blockers And Gaps

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| Reviewer calibration examples missing | MOGT repair pack | open | Create 3-5 calibration examples and score them with at least two reviewers. |
| E1 G1-G3 pending | MOGT repair pack | open | Complete protocol measurability, source validation, and inventory readiness gates. |
| E2 G1-G3 pending | MOGT repair pack | open | Complete protocol gates and normalize/source-check Pareto and weighted-sum authorities. |
| E4 G1-G3 pending | MOGT repair pack | open | Complete protocol gates and specify overhead feasibility thresholds. |
| Live model/run parameters missing | MOGT repair pack | open | Define concrete models, temperature, scenario counts, policy regimes, cost limits, and output paths. |
| Evidence mutation policy missing | MOGT repair pack | open | Name mutation owner, adjudication gate, and paper rewrite owner before any evidence-status update. |
| E3 first-wave inclusion | MOGT research workflow | deferred | Keep second-wave by default. |

## Validation

- `sed -n '1,220p' research/mogt-agentic-conversation/development/MOGT-LIVE-EVIDENCE-APPROVAL-RESULT.md`
- `sed -n '1,180p' research/mogt-agentic-conversation/development/MOGT-LIVE-EXPERIMENT-APPROVAL-CHECKLIST.md`
- `sed -n '1,220p' research/mogt-agentic-conversation/development/WORK-PACK.md`
- `sed -n '1,140p' research/mogt-agentic-conversation/results/MOGT-EVIDENCE-STATUS.md`
- `rg -n "G1|G2|G3|pending" research/mogt-agentic-conversation/experiments/E1-tradeoff-traceability-baseline/protocol.md research/mogt-agentic-conversation/experiments/E2-pareto-arbitration-quality/protocol.md research/mogt-agentic-conversation/experiments/E4-overhead-feasibility-envelope/protocol.md`

## Next Route

- Recommended route: task-session
- Rationale: the refresh has enough evidence to propose bounded repair SWUs, but it must not execute repairs or mutate evidence artifacts in refresh mode.

## Gate Result

- Status: pass
- Reason: source evidence, target artifact inventory, refresh scope, and mutation mode are present; every proposed delta maps to a refresh signal; no unauthorized mutation was applied.
