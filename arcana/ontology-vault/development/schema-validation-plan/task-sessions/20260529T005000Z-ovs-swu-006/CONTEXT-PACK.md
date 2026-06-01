# Context Pack: OVS-SWU-006

Status: pass
Task Session: `20260529T005000Z-ovs-swu-006`
Selected unit: `OVS-SWU-006`

## Task Scope

Add DomainSpec and future-system fixtures.

Dependencies:

- `OVS-SWU-005`: flag, non-blocking schema gap carried forward.

Write scope:

- `arcana/ontology-vault/development/schema-validation-plan/fixtures/valid/`
- task-session validation note under this session folder

Boundary:

- Do not mutate DomainSpec.
- Do not mutate structured-action-schema.
- Treat DomainSpec and future-system examples as pressure fixtures only.

## Controlling Sources

| Source | Selector | Obligation |
| --- | --- | --- |
| `../handoffs/DOMAIN-SPEC-ONTOLOGY-LIFECYCLE-HANDOFF.md` | `Target Boundary` | Keep DomainSpec particulars out of general Ontology Vault while pressure-testing bridge classification. |
| `../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` | `Validation Plan` | Add DomainSpec and future-system examples. |

## Gate Checks

| Gate | Result |
| --- | --- |
| Exactly one SWU selected | pass |
| DomainSpec source handoff exists | pass |
| DomainSpec mutation avoided | pass |
| Future-system fixture can be bounded as placeholder | pass |
