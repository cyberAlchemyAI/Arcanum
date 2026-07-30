---
module: goal-decision-frontier-experiment
version: plan-v1
status: plan-authored
updatedAt: 2026-07-30
docType: work-pack
lifecycle_owner: spellcraft
selected_swu: none
---

# WORK-PACK: Goal Decision Frontier Experiment

## Purpose

Provide the source-of-truth implementation plan for testing a decision
frontier without conflating Plan completeness, lifecycle acceptance, SWU
selection, fixture behavior, canonical adoption, or production readiness.

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass |
| executionAdmissionStatus | block-until-spellcraft-acceptance-and-selection |
| complexity | medium |
| outputMode | split |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| distillValidationStatus | pass |
| implementationDetailStatus | pass; five task-linked specs |
| distillChildRunId | distill-20260730T171429Z-goal-decision-frontier-plan |
| distillTelemetryStatus | recorded with partial runtime evidence at central line 442 |
| invokeTelemetryStatus | recorded at central line 441 |
| swuAtomicityStatus | pass |
| firstUnitNarrownessStatus | pass |
| closeoutSyncStatus | pass; current owner route `invoke:refresh:apply-approved` |
| activeLayerWindow | L0 |
| firstCandidateSwu | SWU-DFE-001 |
| selectedSwu | none |
| readinessProfile | experiment |

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependency |
| --- | --- | --- | --- | --- |
| S-001 | closed schemas and graph validation | L0 | [W1](work-pack/waves/W1.md) | W0 |
| S-002 | pure reason-complete frontier | L0 | [W2](work-pack/waves/W2.md) | 001 |
| S-003 | digest-bound claim control | L1 | [W3](work-pack/waves/W3.md) | 002 |
| S-004 | immutable reconciliation proposals | L1 | [W4](work-pack/waves/W4.md) | 003 |
| S-005 | explicit HITL stop | L2 | [W5](work-pack/waves/W5.md) | 004 |
| S-006 | strict Way Clear predicate | L2 | [W6](work-pack/waves/W6.md) | 005 |
| S-007 | decision/execution non-collapse | L2 | [W7](work-pack/waves/W7.md) | 006 |
| S-008 | independent closure and authority hash | L3 | [W8](work-pack/waves/W8.md) | all mutation units |
| S-009 | lifecycle decision | L3 | [W9](work-pack/waves/W9.md) | closure |

## Task Board

| Task | Unit | Layer | Status |
| --- | --- | --- | --- |
| [Contract](work-pack/tasks/TASK-DFE-CONTRACT.md) | SWU-DFE-001 | L0 | candidate, not selected |
| [Reducer](work-pack/tasks/TASK-DFE-REDUCER.md) | SWU-DFE-002 | L0 | dependency-bound |
| [Claim](work-pack/tasks/TASK-DFE-CLAIM.md) | SWU-DFE-003 | L1 | dependency-bound |
| [Reconcile](work-pack/tasks/TASK-DFE-RECONCILE.md) | SWU-DFE-004 | L1 | dependency-bound |
| [Boundary](work-pack/tasks/TASK-DFE-BOUNDARY.md) | SWU-DFE-005, SWU-DFE-006, SWU-DFE-007 | L2 | serial dependency-bound |
| [Verify](work-pack/tasks/TASK-DFE-VERIFY.md) | VERIFY-DFE-001 | L3 | closure-only |
| [Readiness](work-pack/tasks/TASK-DFE-READINESS.md) | READINESS-DFE-001 | L3 | closure-only |

## Atomicity

| Unit | One primary behavior | Split result |
| --- | --- | --- |
| SWU-DFE-001 | reject invalid contract/graph input | schema and negative fixtures remain one fail-closed boundary |
| SWU-DFE-002 | derive frontier and reasons | canonicalization stays with reducer because bytes are its acceptance output |
| SWU-DFE-003 | enforce claim compare-and-set | stale and competing claims are one concurrency boundary |
| SWU-DFE-004 | stage causal reconciliation | resolution validation and proposal output are one transition boundary |
| SWU-DFE-005 | enforce the HITL stop | route emission and auto-resolution rejection are one human-control boundary |
| SWU-DFE-006 | evaluate strict Way Clear | open-decision and fog mutants test one terminal predicate |
| SWU-DFE-007 | prove execution non-collapse | byte identity is one independently acceptable state boundary |

## Execution Handoff

| Unit | Exact scope | Validation | Owner | Successor |
| --- | --- | --- | --- | --- |
| SWU-DFE-001 | [inventory](work-pack/tasks/TASK-DFE-CONTRACT.md#exact-write-scope) | contract and graph mutants | Task Session -> Invoke Refresh under Spellcraft lifecycle | SWU-DFE-002 eligible |
| SWU-DFE-002 | [inventory](work-pack/tasks/TASK-DFE-REDUCER.md#exact-write-scope) | frontier fixtures and replay | same | SWU-DFE-003 eligible |
| SWU-DFE-003 | [inventory](work-pack/tasks/TASK-DFE-CLAIM.md#exact-write-scope) | claim fixtures | same | SWU-DFE-004 eligible |
| SWU-DFE-004 | [inventory](work-pack/tasks/TASK-DFE-RECONCILE.md#exact-write-scope) | resolution/reconciliation fixtures | same | SWU-DFE-005 eligible |
| SWU-DFE-005 | [inventory](work-pack/tasks/TASK-DFE-BOUNDARY.md#exact-write-scope-swu-dfe-005) | HITL route and auto-resolution mutant | same | SWU-DFE-006 eligible |
| SWU-DFE-006 | [inventory](work-pack/tasks/TASK-DFE-BOUNDARY.md#exact-write-scope-swu-dfe-006) | terminal, open, and fog fixtures | same | SWU-DFE-007 eligible |
| SWU-DFE-007 | [inventory](work-pack/tasks/TASK-DFE-BOUNDARY.md#exact-write-scope-swu-dfe-007) | exact execution-state bytes and collapse mutant | same | VERIFY-DFE-001 eligible |

Every row uses [the shared closeout contract](work-pack/shared/CLOSEOUT-CONTRACT.md).
No successor is selected by a passing receipt.

## Blockers

| ID | Description | Owner |
| --- | --- | --- |
| A-001 | Spellcraft has not accepted the experiment route. | Spellcraft |
| A-002 | No SWU is selected. | user and Spellcraft |
| A-003 | All implementation witnesses are unexecuted. | future Task Sessions |
| A-004 | Adapters, workflow benefit, and canonical adoption are unproved and out of scope. | later Spellcraft, Experiment Harness, and Invoke Design |

These block mutation and adoption claims, not Plan structure.

## Required Links

- [shared context](work-pack/shared/CONTEXT.md)
- [shared decisions](work-pack/shared/DECISIONS.md)
- [shared gaps](work-pack/shared/GAPS.md)
- [traceability](work-pack/shared/TRACEABILITY.md)
- [closeout contract](work-pack/shared/CLOSEOUT-CONTRACT.md)
- [command matrix](work-pack/shared/COMMAND-MATRIX.json)
- [terminal receipt schema](TASK-SESSION-RECEIPT.schema.json)
- [closeout receipt schema](CLOSEOUT-RECEIPT.schema.json)
- [continuation state](CONTINUATION.json)
- [contract detail](work-pack/details/CONTRACT.md)
- [reducer detail](work-pack/details/REDUCER.md)
- [claim detail](work-pack/details/CLAIM.md)
- [reconciliation detail](work-pack/details/RECONCILE.md)
- [control-boundary detail](work-pack/details/BOUNDARY.md)
- [W0 baseline](work-pack/waves/W0.md)
- [W1 contract](work-pack/waves/W1.md)
- [W2 frontier](work-pack/waves/W2.md)
- [W3 claims](work-pack/waves/W3.md)
- [W4 reconciliation](work-pack/waves/W4.md)
- [W5 HITL](work-pack/waves/W5.md)
- [W6 Way Clear](work-pack/waves/W6.md)
- [W7 non-collapse](work-pack/waves/W7.md)
- [W8 closure](work-pack/waves/W8.md)
- [W9 readiness](work-pack/waves/W9.md)
- [validation strategy](VALIDATION-STRATEGY.md)
- [Distill request](DISTILL-RUN-REQUEST.json)
- [Plan Distill](DISTILL-VALIDATION.md)
- [Dispatch](INVOKE-DISPATCH.json)

## Gate Rules

1. Plan validation can mark `workPackGateStatus: pass`.
2. `selectedSwu: none` keeps execution blocked regardless of that result.
3. Every mutation is serial and limited to its exact inventory.
4. Failed negatives, undeclared deltas, private content, or authority
   overclaims block the unit.
5. L3 may only choose the next governed route.
