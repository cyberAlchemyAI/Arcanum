# Goal Runtime Fixture Report

| Fixture | Result | Stop Reason | Frontier Schema | Result Schema |
| --- | --- | --- | --- | --- |
| `read_only_frontier` | PASS | none | pass | pass |
| `protected_frontier` | STOP | t3-node | pass | pass |
| `missing_source` | BLOCK | source-authority | pass | pass |

## Delegation And Staging

| Fixture | Receipt | Audit | Delta | Receipt Schema |
| --- | --- | --- | --- | --- |
| `delegation_staging` | closed | pass | staged | pass |
| `audit_veto` | closed | block | n/a | pass |

## Approval Boundary

| Fixture | State | Stop Reason | Token Schema |
| --- | --- | --- | --- |
| `approval_exact` | ready-for-craft-apply | none | pass |
| `ambient_approval` | blocked | ambient-approval | n/a |

## Gap Discovery

| Fixture | Result | Stop Reason | Proposals | Duplicates |
| --- | --- | --- | --- | --- |
| `gap_discovery` | PASS | dedupe-complete | 1 | 1 |
| `budget_stop` | STOP | budget-ceiling | 0 | 0 |

## Telemetry

| Fixture | Telemetry Schema |
| --- | --- |
| `delegation_staging` | pass |

Overall: pass
