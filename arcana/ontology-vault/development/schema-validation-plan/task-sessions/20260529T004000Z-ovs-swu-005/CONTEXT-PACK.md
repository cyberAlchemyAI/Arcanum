# Context Pack: OVS-SWU-005

Status: pass
Task Session: `20260529T004000Z-ovs-swu-005`
Selected unit: `OVS-SWU-005`

## Task Scope

Add a CyberAlchemy PromotionRecord pressure fixture.

Dependencies:

- `OVS-SWU-004`: pass

Write scope:

- `arcana/ontology-vault/development/schema-validation-plan/fixtures/valid/`
- task-session validation note under this session folder

Boundary decision:

- Do not write to `arcana/ontology-vault/development/cyberalchemy-ontology-lifecycle/fixtures/` in this task because that package README lists mutation of the package as out of scope.
- Use the CAOL package as source evidence only.

## Controlling Sources

| Source | Selector | Obligation |
| --- | --- | --- |
| `../cyberalchemy-ontology-lifecycle/ONTOLOGY-VAULT-BRIEF.md` | `First Validation Scenario` | Model the first working slice as a schema pressure fixture. |
| `../cyberalchemy-ontology-lifecycle/ONTOLOGY-VAULT-BRIEF.md` | `PromotionRecord Boundary For Ontology Vault` | Preserve one primary claim, confidence split, owner, gate, use scope, contradiction path, rollback/retirement, and bridge validation. |
| `../cyberalchemy-ontology-lifecycle/README.md` | `Boundary` | Use CAOL as evidence without mutating the CAOL package. |

## Gate Checks

| Gate | Result |
| --- | --- |
| Exactly one SWU selected | pass |
| CAOL scenario available | pass |
| Package mutation avoided | pass |
| Validator exists | pass |
