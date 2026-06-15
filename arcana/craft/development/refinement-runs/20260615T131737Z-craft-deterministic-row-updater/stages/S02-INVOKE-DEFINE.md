# S02 Invoke Define: Deterministic Row Updater

## Invoke Result

- Mode: define.
- Spell: invoke.
- Phase status: pass.
- Target artifact: Craft row-update planner definition.
- Next route: invoke design.

## Definition

A Craft deterministic row updater is a dry-run reconciliation primitive that
turns one proposed row delta into a validated patch plan against
`.craft/ledger.yml`.

It is deterministic when the same ledger bytes, row selector, proposed delta,
schema contract, and tool version always produce the same verdict and patch
plan bytes.

It is not:

- a second source of truth;
- a spreadsheet import engine by itself;
- a direct YAML mutator in the first slice;
- a broad ledger renderer;
- a generated index authority.

## Problem Statement

The existing projection plan needs `import-csv --dry-run`, but broad CSV import
has several responsibilities mixed together:

- reading CSV projections;
- mapping rows back to ledger families;
- deciding editable columns;
- detecting stale projections;
- validating references and enums;
- producing YAML patch plans;
- reporting unsupported nested edits.

The safety-critical part is the row-level patch planner. It deserves its own
deterministic contract so CSV import can be a producer of row deltas, not the
owner of reconciliation semantics.

## Candidate Names

| Name | Fit |
| --- | --- |
| `craft-index plan-row-update` | Best user-facing phrase if exposed as CLI. |
| `craft-index import-csv --dry-run` internal planner | Best first implementation if we avoid new CLI surface. |
| `row_update_plan` | Best internal function/object name. |

## Initial Decision

Create the deterministic row update planner as an internal library/contract
first, with optional CLI exposure only after fixture proof. Keep direct mutation
disabled.

## Glossary

| Term | Meaning |
| --- | --- |
| Row selector | `{family, id}` plus optional source selector metadata. |
| Proposed delta | Field-level candidate changes from CSV or another staging source. |
| Patch plan | Deterministic artifact describing exact YAML path operations and validation verdict. |
| Stale source | A proposed update generated from ledger bytes that no longer match the current source hash. |
| Read-only field | A row field that may be projected but not changed through the first updater slice. |

## Unresolved Gaps

None blocking. CLI naming is deferred until implementation planning chooses
whether to expose a command or keep the planner internal.
