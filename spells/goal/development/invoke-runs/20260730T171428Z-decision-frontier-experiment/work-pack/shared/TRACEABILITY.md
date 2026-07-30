# Traceability

## Requirements To Units

| Requirement | Primary unit | Witness |
| --- | --- | --- |
| FR-01, FR-02 | SWU-DFE-001 | DFE-FIX-003 |
| FR-03, FR-04 | SWU-DFE-002 | DFE-FIX-001 |
| FR-05 | SWU-DFE-002 plus SWU-DFE-004 | DFE-FIX-005, DFE-FIX-006 |
| FR-06 | SWU-DFE-003 | DFE-FIX-002, DFE-FIX-004 |
| FR-08 | SWU-DFE-004 | DFE-FIX-005, DFE-FIX-007 |
| FR-07 | SWU-DFE-005 | DFE-FIX-011 |
| FR-09 | SWU-DFE-006 | DFE-FIX-012 |
| FR-10 | SWU-DFE-007 | DFE-FIX-008 |
| FR-11 | SWU-DFE-002 | DFE-FIX-009 |
| FR-12 | VERIFY-DFE-001 | DFE-FIX-010 |

## Architecture Extensions

| Extension | Units |
| --- | --- |
| persistence/concurrency | SWU-DFE-001, 003 |
| integration/versioning | READINESS-DFE-001 decides a separate adapter Design route |
| state/event | SWU-DFE-003, 004, 005, 006, 007 |
| data lifecycle | SWU-DFE-001 and VERIFY-DFE-001 |
| validation contracts | all mutation units plus VERIFY-DFE-001 |

## Witness Ownership

| Witness | Owning unit |
| --- | --- |
| DFE-FIX-001 | SWU-DFE-002 |
| DFE-FIX-002 | SWU-DFE-003 |
| DFE-FIX-003 | SWU-DFE-001 |
| DFE-FIX-004 | SWU-DFE-003 |
| DFE-FIX-005 | SWU-DFE-004 |
| DFE-FIX-006 | SWU-DFE-002 |
| DFE-FIX-007 | SWU-DFE-004 |
| DFE-FIX-008 | SWU-DFE-007 |
| DFE-FIX-009 | SWU-DFE-002 |
| DFE-FIX-010 | VERIFY-DFE-001 |
| DFE-FIX-011 | SWU-DFE-005 |
| DFE-FIX-012 | SWU-DFE-006 |

## Invariant Coverage

| Invariant group | Enforced by |
| --- | --- |
| Craft authority and proposal-only outputs | 001 schemas, 004 output, VERIFY authority hash |
| precise frontier and retained exclusions | 002 |
| digest-bound claim and HITL | 003, 005 |
| decision/execution separation | 007 and independent closure |
| deterministic replay | 002 |
| no promotion/readiness overclaim | shared closeout and READINESS-DFE-001 |

Every planned witness has one owning mutation or closure unit and is reconciled by
VERIFY-DFE-001.
