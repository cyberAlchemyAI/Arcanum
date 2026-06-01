# Context Pack: OVS-SWU-003

Status: pass
Task Session: `20260529T002000Z-ovs-swu-003`
Selected unit: `OVS-SWU-003`

## Task Scope

Implement required-field and enum validation for the branch-aware ontology schema fixtures.

Dependencies:

- `OVS-SWU-001`: pass
- `OVS-SWU-002`: pass

Write scope:

- `arcana/ontology-vault/development/schema-validation-plan/tests/`
- minimal task-session evidence under this folder

Out of scope:

- canonical runtime validator,
- JSON Schema generation,
- template mutation,
- Inventory or structured-action-schema mutation.

## Implementation Choice

Use a `python3` standard-library script over JSON fixtures.

Rationale:

- fixtures are JSON,
- no YAML dependency is needed,
- the plan explicitly prefers `python3` when validating schema work.

## Gate Checks

| Gate | Result |
| --- | --- |
| Exactly one SWU selected | pass |
| Positive fixtures exist | pass |
| Negative fixtures exist | pass |
| Parser dependency decision safe | pass |
| No canonical mutation required | pass |
