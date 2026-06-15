# S08 Distill Repair: Toy Fixture Constraints

## Repair Verdict

- Mode: repair.
- Status: pass.
- Selected repair: constrain first implementation to a dry-run row update planner with a tiny toy fixture.

## Toy Fixture

Fixture name: `craft-row-update-planner-toy`

Minimum rows:

- one `contexts` row with editable `stage`, `gate`, `next_move`;
- one `artifacts` row with editable `status` and `notes`;
- one `decisions` row with editable `selected`, `rationale`, `status`, and `blocking`;
- one relation or link target to prove references are checked.

Required cases:

| Case | Expected Result |
| --- | --- |
| Current source hash matches and scalar field changes. | pass with patch plan. |
| Current source hash differs. | block stale source. |
| Proposed row ID differs. | block ID churn. |
| Proposed enum value invalid. | block enum violation. |
| Proposed reference target missing. | block unresolved reference. |
| Proposed read-only nested evidence edit. | block read-only nested edit. |
| Proposed value equals current value. | pass no-op. |

## Repaired First Slice

The first slice should not be `import-csv --dry-run` itself. It should be:

```text
row-update planner dry-run for selected scalar fields
```

CSV import then becomes a later caller that maps projection rows into planner
inputs.

## Acceptance Guardrails

- No direct YAML write.
- No arbitrary nested updates.
- No generated projection authority.
- No parent-only fixture data.
- No generated runtime mirror refresh until canonical checks pass.

## Recomposition

This repair composes into the existing `SWU-CII-005` by making its dry-run patch
plan behavior depend on a smaller tested planner.
