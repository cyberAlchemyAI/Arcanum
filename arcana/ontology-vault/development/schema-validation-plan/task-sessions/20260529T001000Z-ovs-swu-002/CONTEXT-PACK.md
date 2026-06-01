# Context Pack: OVS-SWU-002

Status: pass
Task Session: `20260529T001000Z-ovs-swu-002`
Selected unit: `OVS-SWU-002`

## Task Scope

Create negative fixtures for invalid schema states.

Parent task:

- `OVS-TEST-001 Fixture Set`

Dependencies:

- `OVS-SWU-001`: pass

Write scope:

- `arcana/ontology-vault/development/schema-validation-plan/fixtures/invalid/`

Out of scope:

- validator implementation,
- JSON Schema generation,
- canonical template mutation,
- Inventory or structured-action-schema mutation.

## Controlling Rules

| Rule | Invalid fixture target |
| --- | --- |
| Axis split | overloaded `status`; `claim_role: candidate` |
| Operational context | missing `branch_context.operating_context` |
| Bridge evidence | missing bridge scope, edge, or evidence coverage |
| Inventory non-authority | `inventory_refs[]` without `non_authority_notice: true` |
| Confidence split | collapsed confidence without separate evidence and commitment |

## Gate Checks

| Gate | Result |
| --- | --- |
| Exactly one SWU selected | pass |
| Dependency `OVS-SWU-001` complete enough | pass |
| Write scope present | pass |
| No validator implementation required | pass |
| No canonical mutation required | pass |
