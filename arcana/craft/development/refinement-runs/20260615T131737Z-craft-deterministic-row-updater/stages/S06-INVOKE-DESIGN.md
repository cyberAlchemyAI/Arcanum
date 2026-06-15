# S06 Invoke Design: Row Update Planner

## Invoke Result

- Mode: design.
- Spell: invoke.
- Phase status: pass.
- Outputs: this design artifact.
- Design views: context, structure, components, workflow, decision flow, dependency interface.
- Next route: refine-design-review.

## Context View

Craft stores source state in `.craft/ledger.yml`. Generated JSON indexes and
CSV projections are derived access surfaces. A row update planner must preserve
that authority model while enabling controlled writeback previews.

## High-Level Structure

```text
craft-index build
  -> emits index/projections with ledger_sha256

candidate edit source
  -> CSV row, CLI row update, form, or agent proposal
  -> normalized proposed delta

row update planner
  -> validates selector, source hash, field policy, references, enums
  -> emits patch plan

future apply step
  -> out of first slice
```

## Low-Level Components

| Component | Inputs | Outputs | First-Slice Policy |
| --- | --- | --- | --- |
| `load_ledger` | ledger path | parsed YAML, source hash | read-only |
| `build_row_index` | parsed ledger | family/id selectors | deterministic order |
| `normalize_delta` | row family, proposed fields | typed delta | reject unknown fields |
| `field_policy` | schema + family | editable/read-only map | explicit allowlist |
| `validate_delta` | selector + delta + row index | blockers/flags | block unsafe edits |
| `plan_patch` | current row + delta | ordered operations | dry-run only |
| `emit_report` | verdict + operations | JSON/Markdown report | stable sort keys |

## Workflow Process View

1. Read current ledger bytes and compute `ledger_sha256`.
2. Compare the proposed delta's expected hash with current hash.
3. Resolve exactly one row by `{family, id}`.
4. Reject row ID changes.
5. Apply field-policy allowlist.
6. Validate enum values and references.
7. Compare current and proposed field values.
8. Emit no-op when nothing changes.
9. Emit deterministic patch operations when changes are safe.
10. Never apply the patch in the first slice.

## Decision Flow View

| Decision | Default |
| --- | --- |
| Internal primitive or user-facing CLI first? | internal primitive first |
| Direct mutation allowed? | no |
| Multiple rows in one transaction? | no |
| Start with all row families? | no; start with selected simple fields |
| Unknown fields? | block |
| Read-only nested fields? | report read-only and block if changed |

## Dependency Interface View

| Dependency | Contract |
| --- | --- |
| Craft schema | supplies row families, ID fields, enums, and references. |
| Projection metadata | supplies expected ledger hash and row selector hints. |
| CSV import dry-run | future caller that batches proposed deltas. |
| Craft validator | confirms resulting plan would preserve ledger invariants. |

## Risk Register

| Risk | Guardrail |
| --- | --- |
| Planner grows into broad mutator. | first slice dry-run only. |
| CSV-specific assumptions leak into core planner. | planner consumes normalized deltas, not CSV rows. |
| Nested links/evidence get flattened incorrectly. | nested fields read-only until fixture proof. |
| Patch plan differs by row ordering. | stable sorting and canonical JSON output. |
| References break silently. | unresolved reference blocks. |

## Design Verdict

Pass. The dedicated planner is justified, but implementation should expose it as
an internal deterministic primitive first.
