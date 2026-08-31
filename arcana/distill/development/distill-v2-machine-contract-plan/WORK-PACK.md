# Distill v2 Machine Contract Work Pack

| Field | Value |
| --- | --- |
| Work pack ID | DV2-WP-001 |
| Complexity | high |
| Output mode | split |
| Execution designation | blocked-before-execution-candidate |
| Admission timing | selected-unit-at-task-session after decision freeze |
| Entry state | blocked |
| Next owner | Distill semantic-contract owner |
| Authority effect | none |

## Objective

Implement a complete Distill v2 semantic machine family with first-class modes,
techniques, inputs, trace, result, deterministic projection, and receipt, then
prove direct and versioned adapter consumption without crossing authority boundaries.

## Entry Gate

The current `STRICT-V2` option is not sufficient because it names five schemas.
Execution requires an amended, selected, independently reviewed decision graph
covering the eight schemas and ten decisions in `SCHEMA-PLAN.md`. Until then,
every task and SWU is `blocked`.

## Ordered Frontier

`SWU-DV2-001` through `SWU-DV2-028` in numeric order. The exact list and
dependencies are authoritative in `swu-manifest.json`.

## Task Board

| Task | Contract | SWUs | Layer | State |
| --- | --- | --- | --- | --- |
| TASK-DV2-DECISIONS | [tasks/TASK-DV2-DECISIONS.md](tasks/TASK-DV2-DECISIONS.md) | none; human G0 | G0 | blocked-owner-decision |
| TASK-DV2-SCHEMAS | [tasks/TASK-DV2-SCHEMAS.md](tasks/TASK-DV2-SCHEMAS.md) | 001–007 | L0 | blocked |
| TASK-DV2-TECHNIQUES | [tasks/TASK-DV2-TECHNIQUES.md](tasks/TASK-DV2-TECHNIQUES.md) | 008–017 | L1 | blocked |
| TASK-DV2-MODES | [tasks/TASK-DV2-MODES.md](tasks/TASK-DV2-MODES.md) | 018–022 | L1 | blocked |
| TASK-DV2-PROFILE-SOURCE | [tasks/TASK-DV2-PROFILE-SOURCE.md](tasks/TASK-DV2-PROFILE-SOURCE.md) | 023 | L1 | blocked |
| TASK-DV2-FINALIZER | [tasks/TASK-DV2-FINALIZER.md](tasks/TASK-DV2-FINALIZER.md) | 024–025 | L2 | blocked |
| TASK-DV2-INTEGRATIONS | [tasks/TASK-DV2-INTEGRATIONS.md](tasks/TASK-DV2-INTEGRATIONS.md) | 026–027 | L3 | blocked; 027 cross-owner |
| TASK-DV2-VERIFY | [tasks/TASK-DV2-VERIFY.md](tasks/TASK-DV2-VERIFY.md) | 028 | L3 | blocked |

## Execution Policy

- Allowed future effect: repository-local reversible changes within one selected SWU exact write scope.
- Automatic decisions: deterministic internal routing, validation-only retries with unchanged graph identity, and atomic rollback to the prior valid family.
- Mandatory stops: semantic choice, scope/owner expansion, stale baseline, failed acceptance-critical validation, generated-sync drift, publication, deployment, destructive or external effect.
- Cross-owner Invoke mutation requires its own accepted envelope; the Distill task cannot infer it.
- No Task Session route is exposed while this work pack remains blocked.

## Validation And Closeout

Every SWU runs pre-execution, post-produce, and closeout phases from
`VALIDATION-STRATEGY.md`. Each receipt binds source anchors, exact pre/post bytes,
validator identity, command statuses, negative denominator, authority ceiling,
and deterministic successor. A later PASS cannot mask an earlier failed command.
