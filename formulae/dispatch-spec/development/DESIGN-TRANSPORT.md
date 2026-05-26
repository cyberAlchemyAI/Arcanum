# Dispatch Spec Design Transport

## Invoke Transport Report

- Mode: `design`
- Target artifact: `dispatch-spec`
- Transport status: `local-artifact-only`
- Necronomicon update: none
- Registry update: none
- Promotion status: candidate only

## Six-View Coverage

| View | Status |
| --- | --- |
| Context view | pass |
| High-level structure view | pass |
| Low-level components view | pass |
| Workflow process view | pass |
| Decision flow view | pass |
| Dependency interface view | pass |

## Design Decisions

- Keep `dispatch-spec` as Formulae validation, not orchestration.
- Keep route interpretation with Necronomicon, Invoke, Spellcraft, or other owner capabilities.
- Use `dispatch_id` as the observability grouping key.
- Preserve Frame/Handle style handoffs without importing Weaver implementation structure.
- Defer validator script, fixtures, registry entry, and telemetry integration to later tasks.

## Unresolved Gaps

| Gap | Severity | Next Route |
| --- | --- | --- |
| Validator script not implemented. | medium | `task-session` |
| Fixtures not created. | medium | `experiment-harness` or `task-session` |
| Observability fields not wired into hooks. | medium | observed invocation loop / signal observer task |
| Registry entry absent. | low while draft | `sigil-development` after validation |

## Next Recommended Route

Run `invoke plan` or direct `task-session` for the validator implementation slice.

