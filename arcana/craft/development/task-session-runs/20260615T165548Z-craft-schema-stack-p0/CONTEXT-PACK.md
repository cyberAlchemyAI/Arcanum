# Context Pack: SWU-CSS-001 Craft Schema Stack P0

## Task

- Task session: `20260615T165548Z-craft-schema-stack-p0`
- Selected unit: `SWU-CSS-001`
- Source design: `../invoke-runs/20260615T161047Z-craft-canonical-schema-stack/`
- Runtime: local
- Runtime handoff: none

## Objective

Create the first canonical Craft schema-stack slice: source-ledger and index
schema coverage only. Keep `ledger.schema.yml` as the compatibility entrypoint,
add schema-stack files under `templates/schemas/`, and update Craft root docs to
name the stack.

## Obligations

| ID | Obligation | Evidence |
| --- | --- | --- |
| O1 | Keep `.craft/ledger.yml` authoritative. | `SKILL.md` storage contract; `ARCHITECTURE.md` source authority. |
| O2 | Preserve `ledger.schema.yml` as the compatibility entrypoint. | `INVOKE-DESIGN-SCHEMA-STACK.md` high-level structure view. |
| O3 | Promote example-backed rows: `descriptions`, `definitions`, `gaps`, `recomposition`. | Body War and GoldenQuill ledgers; schema-stack inventory. |
| O4 | Add generated/embedded index schema coverage without making indexes authoritative. | `SKILL.md` linking/indexing contract; index proposal result. |
| O5 | Do not implement projection, CSV import, row-update apply mode, scripts, or generated mirror refresh. | `IMPLEMENTATION-LAYERING-SEED.md` first executable slice. |
| O6 | Update root documentation/source authority to name the stack. | SWU write scope. |
| O7 | Validate YAML readability, example family coverage, public-boundary scan, and diff checks. | Task-session validation surface. |

## Selected Sources

| Source | Selectors | Why Included |
| --- | --- | --- |
| `arcana/craft/SKILL.md` | source authority, storage contract, linking/indexing, core methods, quality bar | Controls runtime behavior and non-goals. |
| `arcana/craft/ARCHITECTURE.md` | source authority, low-level components, current contract tensions, comparison checklist | Current architecture baseline. |
| `arcana/craft/templates/ledger.schema.yml` | full file | Current compatibility schema entrypoint. |
| `arcana/craft/examples/body-war-ledger.yml` | top-level families, route handoffs, receipts, recomposition | Example-backed source rows and deferred route exchange rows. |
| `arcana/craft/examples/goldenquill-ledger.yml` | top-level families, definitions, gaps, recomposition | Example-backed source rows. |
| `arcana/craft/development/invoke-runs/20260615T161047Z-craft-canonical-schema-stack/INVOKE-DESIGN-SCHEMA-STACK.md` | high-level structure, component table, handoff | Defines schema stack and first slice. |
| `arcana/craft/development/invoke-runs/20260615T161047Z-craft-canonical-schema-stack/SCHEMA-CANDIDATE-INVENTORY.md` | P0/P1/P2 inventory | Controls priority and deferrals. |
| `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml` | descriptions, definitions, gaps draft | Historical draft used as evidence, not copied blindly. |
| `development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml` | route handoffs/receipts/events draft | Deferred to P1 route-exchange schema. |

## Decisions And Assumptions

| Item | Resolution |
| --- | --- |
| Schema entrypoint | Keep `templates/ledger.schema.yml` as a readable aggregate/compatibility entrypoint. |
| Versioning | Bump canonical schema version to `0.3.0` and mark compatibility with `0.2.0` examples. |
| New canonical files | Add `templates/schemas/ledger-core.schema.yml` and `templates/schemas/index.schema.yml`. |
| Deferred files | Do not add interface, route-exchange, projection, row-update, validation, or artifact-manifest schema files in this slice. |
| Route rows in examples | Leave `route_handoffs` and `receipts` as future P1 route-exchange coverage, not P0 ledger-core. |
| Generated mirrors | Do not refresh generated skill copies in this task session. |

## Write Scope

- `arcana/craft/templates/ledger.schema.yml`
- `arcana/craft/templates/schemas/ledger-core.schema.yml`
- `arcana/craft/templates/schemas/index.schema.yml`
- `arcana/craft/ARCHITECTURE.md`
- `arcana/craft/README.md`
- `arcana/craft/SKILL.md`
- `arcana/craft/development/task-session-runs/20260615T165548Z-craft-schema-stack-p0/`

## Validation Surface

1. Parse all Craft schema YAML files with `python3`.
2. Check current examples expose row families covered by the P0 schemas or
   explicitly deferred.
3. Check docs mention the schema stack and P0 deferrals.
4. Run public-boundary scan for local-only leakage.
5. Run trailing whitespace and `git -C arcanum diff --check` for touched files.

## Strict Coverage

Pass. Every mutation obligation is covered by source evidence or explicitly
deferred. Runtime handoff is not applicable.
