---
module: inventory-whole-arcanum
task: TASK-WAI-004
swu: SWU-WAI-009
status: built
layer: L2
createdAt: 2026-06-01
docType: task-session-context
---

# Context Pack: SWU-WAI-009 Composition Family Cards

## Selected Scope

`SWU-WAI-009` expands the composition source families into inventory cards:

- `spells/`
- `transmutations/`
- `formulae/`

The write scope is limited to:

- `arcana/inventory/development/whole-arcanum/cards/composition/`

## Controlling Sources

- `arcana/inventory/development/whole-arcanum/WORK-PACK.md`
- `arcana/inventory/development/whole-arcanum/work-pack/tasks/TASK-WAI-004-expanded-capability-waves.md`
- `arcana/inventory/development/whole-arcanum/source-manifest.json`
- `arcana/inventory/development/whole-arcanum/SOURCE-POLICY.md`
- Representative `spells/*/README.md`, `transmutations/*/SKILL.md`, and `formulae/*/SKILL.md`

## Constraints

- Preserve the difference between spells, transmutations, and formulae.
- Do not copy full composition instructions into inventory cards.
- Use small selector spans.
- Capture overlap as duplicate or ownership risk, not as merged authority.
- Validate the slice with the slice-aware evidence-card validator.

## Decision Pack

No blocker-level decision is visible. The non-blocking card granularity choice is:

| Option | Consequence | Decision |
| --- | --- | --- |
| Card per composition artifact | More complete but slower to query and harder to maintain. | Rejected for this L2 slice. |
| Cluster by composition role | Faster agent retrieval while preserving tier boundaries. | Selected. |

## Gate Verdict

Proceed. `SWU-WAI-008` completed, `SWU-WAI-009` has a bounded write scope, and
the source manifest plus policy provide enough context.

