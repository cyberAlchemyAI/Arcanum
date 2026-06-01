---
module: inventory-whole-arcanum
task: TASK-WAI-003
status: completed
layer: L1
---

# TASK-WAI-003: Governance And Lifecycle Pilot Slices

## Objective

Create a high-value cross-capability pilot that helps agents answer whether a
planned implementation can proceed without violating governance or lifecycle
ownership.

## Implementation Detail

Build two pilot groups:

- governance cards for artifact/schema constitutions and validators,
- lifecycle cards for invoke/refine/task-session execution boundaries.

Then compose a candidate EvidenceSet for a realistic question:

> Can this planned Inventory SWU be executed directly, or does it need another
> decision gate first?

## Smallest Working Units

| SWU | Goal | Write Scope | Done Criteria | Validation |
| --- | --- | --- | --- | --- |
| SWU-WAI-005 | Create constitution/schema governance cards. | `cards/governance/` | cards identify source authority and validators | card validation |
| SWU-WAI-006 | Create invoke/refine/task-session lifecycle cards. | `cards/lifecycle/` | cards distinguish authoring, refinement, and execution | card validation |
| SWU-WAI-007 | Create cross-pilot EvidenceSet. | `evidence-sets/` | set records selected and excluded evidence | retrieval review |

## Completion Evidence

| SWU | Result | Evidence |
| --- | --- | --- |
| SWU-WAI-005 | pass | Governance slice contains Artifact Constitution and Schema Constitution cards; slice validator passes. |
| SWU-WAI-006 | pass | Lifecycle slice contains Invoke, Refine, and Task Session cards; slice validator passes. |
| SWU-WAI-007 | pass | Cross-pilot candidate EvidenceSet references only known W1 card IDs and records selected/excluded evidence. |

## Execution Assumptions

- `SWU-WAI-005` should create at least two governance cards:
  - Artifact Constitution source authority and generated/local runtime boundary,
  - Schema Constitution `.schema.yml` rule and validation boundary.
- `SWU-WAI-006` should create at least three lifecycle cards:
  - Invoke authoring/refresh/plan boundary,
  - Refine discovery/design loop boundary,
  - Task Session execution/synchronization boundary.
- `SWU-WAI-007` should reference only known W1 card IDs and keep status
  candidate-level.

## Result

See `arcana/inventory/development/whole-arcanum/task-session/TASK-WAI-003-RESULT.md`.

## Source Anchors

- `framework/ARTIFACT-CONSTITUTION.md`
- `framework/SCHEMA-CONSTITUTION.md`
- `spells/invoke/README.md`
- `spells/invoke/plan.md`
- `arcana/task-session/SKILL.md`
- `arcana/refine/SKILL.md`
