# Implementation Layering Seed: Craft Schema Stack

## Layering Intent

Create a safe promotion path for canonical Craft schemas without turning the
schema work into projection/import tooling.

## Layers

| Layer | Question | Includes | Excludes | Promotion Evidence |
| --- | --- | --- | --- | --- |
| L0 | Can Craft validate the source-ledger families it already uses? | `ledger-core.schema.yml`, formal descriptions/definitions/gaps/recomposition, compatibility entrypoint. | Generated index builder, CSV, row updater. | Current examples map to schema families without unmodeled top-level rows. |
| L1 | Can Craft validate lookup/index surfaces without authority drift? | `index.schema.yml`, embedded index object shape, generated index metadata, stale policy. | Status renderer and projections. | Index schema proves source hash, stale status, required lookup groups, and row-ID-only authority. |
| L2 | Can Craft validate interface and exchange surfaces? | `interface.schema.yml`, `route-exchange.schema.yml`, validation report shape. | CSV writeback and YAML apply. | Human view examples and route/receipt examples validate as derived/exchange surfaces. |
| L3 | Can Craft validate generated projections and planner reports? | `projection.schema.yml`, `row-update.schema.yml`, artifact manifest schema. | Direct apply mode unless separately approved. | Toy fixtures prove pass/no-op/flag/block planner reports and read-only projection defaults. |

## First Executable Slice

`SWU-CSS-001`: Canonical source/index schema scaffold.

- Write scope:
  - `arcana/craft/templates/ledger.schema.yml`
  - `arcana/craft/templates/schemas/ledger-core.schema.yml`
  - `arcana/craft/templates/schemas/index.schema.yml`
  - `arcana/craft/ARCHITECTURE.md`
  - `arcana/craft/README.md`
  - `arcana/craft/SKILL.md`
- Goal:
  - Create the schema-stack entrypoint and promote only source-ledger and index
    coverage that is already backed by examples and current contracts.
- Acceptance:
  - The compatibility entrypoint remains readable as the canonical schema path.
  - Example-backed top-level rows have schema coverage.
  - Generated-index authority rules are explicit.
  - No projection import, planner apply, or runtime mirror refresh occurs.
- Validation:
  - YAML parse for schema files.
  - Markdown link/grep checks for canonical docs.
  - Public-boundary scan.
  - `git diff --check` on touched canonical files.

## Deferred Slices

| Slice | Layer | Reason For Deferral |
| --- | --- | --- |
| `SWU-CSS-002` interface schema | L2 | Needs renderer/status obligations separated from exact prose. |
| `SWU-CSS-003` route-exchange schema | L2 | Needs capability-ref enum review and receipt ownership wording. |
| `SWU-CSS-004` projection schema | L3 | Depends on index schema and CSV read-only policy. |
| `SWU-CSS-005` row-update schema | L3 | Depends on source/index/projection contracts. |
| `SWU-CSS-006` validation and artifact manifest schemas | L2/L3 | Useful but not blocking for source/index schema stabilization. |
