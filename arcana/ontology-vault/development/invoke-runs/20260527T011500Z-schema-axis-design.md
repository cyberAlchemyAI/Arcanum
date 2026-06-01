# Invoke Design: Schema Axis Values

Status: pass
Mode: design
Date: 2026-05-27
Target: `arcana/ontology-vault/development/BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md`

## Request

Proceed with the values selected by the role/lifecycle redundancy refinement:

- `lifecycle_status`
- `claim_role`
- `governance_outcome`
- `bridge_outcome`

## Canonical Sources Used

- `spells/invoke/README.md`
- `spells/invoke/design.md`
- `arcana/ontology-vault/development/BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md`
- `arcana/ontology-vault/development/general-ontology-lifecycle/refinement-runs/20260527T010000Z-role-lifecycle-redundancy/RESULT.md`

## Design Decision

The branch-aware ontology schema candidate now separates lifecycle maturity from claim function and validation outcome.

Selected axes:

| Axis | Purpose |
| --- | --- |
| `lifecycle_status` | Governance maturity and permitted reliance. |
| `claim_role` | What kind of claim, record, or governance function the entry is playing. |
| `governance_outcome` | Accepted special consequence when applicable, such as `policy`, `constitution`, or `axiom`. |
| `bridge_outcome` | Cross-branch validation result. |

## Changes Made

- Replaced top-level candidate `status` with the four selected axes.
- Updated edge schema to use `lifecycle_status` and `bridge_outcome`.
- Added required field rules for the four axes.
- Added validation rule `V11: Role And Lifecycle Axis Split`.
- Updated example entries to use the selected axes.
- Added validation examples for role-axis, governance-outcome, and contradiction cases.

## Boundaries

This run did not mutate:

- Inventory,
- structured-action-schema,
- canonical Ontology Vault templates,
- canonical branch conventions.

## Gaps

- The schema is still exploratory and non-canonical.
- A JSON Schema should wait until examples validate.
- The selected axis values still need example validation across Arcanum, CyberAlchemy, DomainSpec, and future-system examples.

## Next Route

`ontology-vault validate`
