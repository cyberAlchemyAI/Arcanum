---
module: inventory-whole-arcanum
task: TASK-WAI-005
swu: SWU-WAI-011
status: built
layer: L3
createdAt: 2026-06-01
docType: task-session-context
---

# Context Pack: SWU-WAI-011 Refresh And Lint Contract

## Selected Scope

`SWU-WAI-011` adds a repeatable refresh and lint command contract for the
whole-Arcanum inventory.

The write scope is limited to whole-arcanum validator and documentation paths:

- `arcana/inventory/development/whole-arcanum/scripts/`
- `arcana/inventory/development/whole-arcanum/OPERATIONAL-COMMANDS.md`
- `arcana/inventory/development/whole-arcanum/task-session/`
- work-pack status artifacts

## Controlling Sources

- `arcana/inventory/development/whole-arcanum/WORK-PACK.md`
- `arcana/inventory/development/whole-arcanum/work-pack/tasks/TASK-WAI-005-operational-readiness.md`
- `arcana/inventory/development/whole-arcanum/work-pack/waves/W3-operational-readiness.md`
- `arcana/inventory/scripts/validate-evidence-card-slice.sh`
- `arcana/inventory/scripts/validate-evidence-card-fixtures.sh`
- L2 coverage reports under `cards/*/COVERAGE.md`
- `framework/ARTIFACT-CONSTITUTION.md`

## Constraints

- Keep the operational surface shell plus `jq` oriented.
- Do not introduce a human UI.
- Validate all current slices, candidate EvidenceSet references, source
  selector spans, fixture examples, and artifact constitution checks.
- Report warnings honestly without treating known pre-existing constitution
  warnings as current task blockers.

## Decision Pack

No blocker-level decision is visible. The non-blocking contract shape choice is:

| Option | Consequence | Decision |
| --- | --- | --- |
| Documentation only | Easy to write but not runnable. | Rejected. |
| Runnable shell contract plus docs | Agent-fast, repeatable, and suitable for readiness evidence. | Selected. |

## Gate Verdict

Proceed. W2 is complete, L3 is open, and the validation surface can be built
from existing slice validators and shell plus `jq`.

