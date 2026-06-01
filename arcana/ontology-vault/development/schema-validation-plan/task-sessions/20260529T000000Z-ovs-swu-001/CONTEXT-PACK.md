# Context Pack: OVS-SWU-001

Status: pass
Task Session: `20260529T000000Z-ovs-swu-001`
Selected unit: `OVS-SWU-001`

## Task Scope

Create positive fixtures for branch and axis coverage.

Parent task:

- `OVS-TEST-001 Fixture Set`

Write scope:

- `arcana/ontology-vault/development/schema-validation-plan/fixtures/valid/`

Out of scope:

- invalid fixtures,
- validator implementation,
- JSON Schema generation,
- canonical Ontology Vault templates,
- Inventory,
- structured-action-schema.

## Controlling Sources

| Source | Selector | Obligation |
| --- | --- | --- |
| `../WORK-PACK.md` | `OVS-SWU-001` | Create valid fixtures covering branch values and selected axes. |
| `../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` | `Entry Schema` | Preserve required fields and enum candidates. |
| `../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` | `Validation Plan` | Cover branch, role-axis, governance-outcome, and contradiction examples. |
| `../IMPLEMENTATION-LAYERING.md` | `L0 Boundary` | Create fixtures before validator code. |

## Decisions

| Decision | Selected option | Rationale |
| --- | --- | --- |
| Fixture format | JSON | JSON is inspectable, parseable by `python3` standard library, and compatible with the simple YAML-shaped maps/lists used by the schema candidate. |

## Gate Checks

| Gate | Result |
| --- | --- |
| Exactly one SWU selected | pass |
| Dependencies available | pass |
| Write scope present | pass |
| Validation surface available | pass |
| No runtime delegation requested | pass |
| No canonical mutation required | pass |

## Acceptance Evidence Needed

- fixture list,
- manual review summary,
- `jq empty` over fixture JSON files,
- artifact constitution validation.
