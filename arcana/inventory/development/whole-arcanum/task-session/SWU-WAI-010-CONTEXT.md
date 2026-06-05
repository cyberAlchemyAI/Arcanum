---
module: inventory-whole-arcanum
task: TASK-WAI-004
swu: SWU-WAI-010
status: built
layer: L2
createdAt: 2026-06-01
docType: task-session-context
---

# Context Pack: SWU-WAI-010 Runtime And Governance Support Cards

## Selected Scope

`SWU-WAI-010` expands runtime and governance support surfaces into inventory
cards:

- `framework/`
- `registry/`
- `tools/`
- native/generated skill runtime packages

The write scope is limited to:

- `arcana/inventory/development/whole-arcanum/cards/runtime/`

## Controlling Sources

- `arcana/inventory/development/whole-arcanum/WORK-PACK.md`
- `arcana/inventory/development/whole-arcanum/work-pack/tasks/TASK-WAI-004-expanded-capability-waves.md`
- `arcana/inventory/development/whole-arcanum/source-manifest.json`
- `arcana/inventory/development/whole-arcanum/SOURCE-POLICY.md`
- `framework/ARTIFACT-CONSTITUTION.md`
- `framework/runtime/README.md`
- `framework/observability/README.md`
- `registry/SIGILS.md`
- `tools/arcanum`
- generated native skill package metadata supplied by the runtime

## Constraints

- Keep generated telemetry and local runtime state out of source inventory.
- Preserve the difference between canonical source, generated runtime package,
  legacy command adapter, registry index, and validation tool.
- Use selector spans instead of whole-file ingestion.
- Capture duplicate or authority risks in coverage notes.
- Validate the slice with the slice-aware evidence-card validator.

## Decision Pack

No blocker-level decision is visible. The non-blocking card granularity choice is:

| Option | Consequence | Decision |
| --- | --- | --- |
| Catalog every legacy command adapter | High coverage, low signal, large maintenance load. | Rejected. |
| Cluster runtime support by role | Faster query surface while preserving authority boundaries. | Selected. |

## Gate Verdict

Proceed. `SWU-WAI-008` and `SWU-WAI-009` completed, and this final L2 slice has
bounded source families plus a runnable validation surface.
