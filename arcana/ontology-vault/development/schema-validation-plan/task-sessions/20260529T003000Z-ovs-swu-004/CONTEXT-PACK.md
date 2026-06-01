# Context Pack: OVS-SWU-004

Status: pass
Task Session: `20260529T003000Z-ovs-swu-004`
Selected unit: `OVS-SWU-004`

## Task Scope

Implement cross-field rules.

Dependencies:

- `OVS-SWU-003`: pass

Write scope:

- `arcana/ontology-vault/development/schema-validation-plan/tests/`
- fixture adjustments if needed

## Cross-Field Rules

| Rule | Implemented check |
| --- | --- |
| V3 | Operational entries require `operating_context`. |
| V4 | Bridge entries require `bridge_scope` and edges unless marked `evidence-gap`. |
| V5 | Inventory references require `non_authority_notice: true`. |
| V8 | Confidence requires separate `evidence` and `commitment`. |
| V9 | Promoted entries require promoted governance state, no blockers, owner, and evidence. |
| V11 | No overloaded `status`; no `claim_role: candidate`; contradicted bridge outcome requires counterevidence. |

## Gate Checks

| Gate | Result |
| --- | --- |
| Exactly one SWU selected | pass |
| Required-field validator exists | pass |
| Negative fixtures exist | pass |
| No canonical mutation required | pass |
