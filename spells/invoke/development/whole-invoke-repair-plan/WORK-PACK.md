# Whole Invoke Repair Work Pack

| Field | Value |
| --- | --- |
| Work pack ID | WIR-WP-001 |
| Complexity | high |
| Output mode | split |
| Execution designation | blocked-before-execution-candidate |
| Admission timing | selected-unit-at-task-session |
| Entry state | blocked |
| Next owner | invoke-plan-producer repair owner |
| Authority effect | none |

## Objective

Implement a trustworthy, producer-complete, consumer-closed Invoke workflow while preserving exact authority and compatibility boundaries.

## Ordered Frontier

`SWU-WIR-001` → `SWU-WIR-002` → `SWU-WIR-003` → `SWU-WIR-004` → `SWU-WIR-005` → `SWU-WIR-006` → `SWU-WIR-007` → `SWU-WIR-008` → `SWU-WIR-009` → `SWU-WIR-011` → `SWU-WIR-012` → `SWU-WIR-010` → `SWU-WIR-013`.

## Task Board

| Task | Contract | SWUs | Layer | State |
| --- | --- | --- | --- | --- |
| TASK-WIR-ADMISSION | [tasks/TASK-WIR-ADMISSION.md](tasks/TASK-WIR-ADMISSION.md) | 001–002 | L0 | blocked |
| TASK-WIR-PLAN-CHAIN | [tasks/TASK-WIR-PLAN-CHAIN.md](tasks/TASK-WIR-PLAN-CHAIN.md) | 003–005 | L1 | blocked |
| TASK-WIR-MODES | [tasks/TASK-WIR-MODES.md](tasks/TASK-WIR-MODES.md) | 006–009 | L2 | blocked |
| TASK-WIR-BOUNDARIES | [tasks/TASK-WIR-BOUNDARIES.md](tasks/TASK-WIR-BOUNDARIES.md) | 011–012 | L2 | blocked |
| TASK-WIR-FULL-REMOVAL | [tasks/TASK-WIR-FULL-REMOVAL.md](tasks/TASK-WIR-FULL-REMOVAL.md) | 010 | L3 | blocked |
| TASK-WIR-LAB | [tasks/TASK-WIR-LAB.md](tasks/TASK-WIR-LAB.md) | 013 | L3 | blocked |

## Execution Policy

- Allowed future effect: `repository-local-reversible` within the selected SWU write scope.
- Automatic decisions: deterministic internal routing, declared reversible fallback, one typed unchanged-route retry, fresh Task Session resumption.
- Mandatory stops: semantic choice, scope or authority expansion, stale baseline, failed acceptance-critical validation, publication, deployment, destructive or external effect.
- No Task Session route is exposed while this work pack remains blocked.

## Validation and Closeout

Every SWU uses pre-execution, post-produce, and closeout phases defined in `VALIDATION-STRATEGY.md`. Each task contract declares exact target families, baseline requirements, admitted delta classes, owner validation, expected receipt, and deterministic successor. Current readiness proof: absent by design.
