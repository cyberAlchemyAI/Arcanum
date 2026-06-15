# Invoke Design: Craft Canonical Schema Stack

## Design Identity

- Spell: `invoke`
- Mode: `design`
- Target artifact: Craft canonical schema stack proposal.
- Target owner: `arcana/craft`
- Phase status: `pass-with-gated-implementation`
- Architecture profile: Module Formulae six-view design bundle.

## Design Intent

Craft currently has one canonical ledger schema and several prose/interface
contracts. Recent index, projection, and row-update proposals need a schema
stack instead of one overloaded file. The stack should keep `.craft/ledger.yml`
authoritative, make every derived or exchanged surface explicit, and let future
tools validate each layer before any mutation path exists.

This is authoring output only. It does not create canonical schema files, edit
`ledger.schema.yml`, implement scripts, refresh runtime mirrors, or publish
submodule state.

## Inputs

- `arcana/craft/ARCHITECTURE.md`
- `arcana/craft/SKILL.md`
- `arcana/craft/README.md`
- `arcana/craft/templates/ledger.schema.yml`
- `arcana/craft/examples/body-war-ledger.yml`
- `arcana/craft/examples/goldenquill-ledger.yml`
- `arcana/craft/development/refinement-runs/20260615T121512Z-craft-ledger-csv-json-indexes/RESULT.md`
- `arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/INVOKE-DESIGN-ARCHITECTURE.md`
- `arcana/craft/development/invoke-runs/20260615T152120Z-craft-row-update-planner-architecture/INVOKE-DESIGN-ARCHITECTURE.md`
- `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml`
- `development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml`

## 1. Context View

```text
Craft canonical package
  owns operating method, architecture baseline, examples, and schemas
      |
      v
schema stack
  defines one validation contract per Craft layer
      |
      +--> source ledger rows
      +--> embedded/generated indexes
      +--> human interface and export surfaces
      +--> route handoff/receipt/event exchange
      +--> projections and CSV staging
      +--> row-update planner deltas and reports
      +--> validation reports and artifact manifests
      |
      v
future tools
  validate, render, index, project, plan, or apply only through the relevant schema
```

The stack is needed because Craft's current behavior spans more than ledger row
families. `SKILL.md` names interface operations, all-status output, receipt
application, route memory, and recomposition. The examples already contain
`descriptions`, `definitions`, `gaps`, `route_handoffs`, `receipts`, and
`recomposition`, while the current canonical schema formalizes only
`contexts`, `artifacts`, `relations`, `typed_items`, and `decisions`.

## 2. High-Level Structure View

Recommended canonical target:

```text
arcana/craft/templates/
  ledger.schema.yml              # compatibility entrypoint and composition manifest
  schemas/
    ledger-core.schema.yml       # source ledger metadata and row families
    index.schema.yml             # embedded indexes and .craft/index.json
    interface.schema.yml         # CRAFT.md, state all, Craft Result output
    route-exchange.schema.yml    # route_handoffs, receipts, route_events
    projection.schema.yml        # .craft/projections manifest and CSV tables
    row-update.schema.yml        # normalized deltas, field policy, patch plans
    validation.schema.yml        # validate reports, residue, pass/flag/block reasons
    artifact-manifest.schema.yml # .craft/artifacts inventory and evidence refs
```

`ledger.schema.yml` should remain the public compatibility entrypoint. It can
either continue as the aggregate schema or become a manifest that composes the
sub-schemas after compatibility validation exists.

## 3. Low-Level Components View

| Schema | Canonical Surface | Owns | First Required Content |
| --- | --- | --- | --- |
| `ledger-core.schema.yml` | `.craft/ledger.yml` | Ledger metadata, source-of-truth policy, row ID/link/reference rules, and row families. | Existing five row families plus formal `descriptions`, `definitions`, `gaps`, and `recomposition`. |
| `index.schema.yml` | `indexes` in ledger and `.craft/index.json` | Required lookup keys, freshness metadata, row selectors, pending summaries, reverse links, and stale status. | Compatibility for embedded `indexes`; generated-index metadata and no-authority rules. |
| `interface.schema.yml` | `CRAFT.md`, `state all`, `Craft Result` | Human anchors, quick links, per-node pending output, status table fields, and command/result envelopes. | Anchors from examples plus `Pending by node` and output contract from `SKILL.md`. |
| `route-exchange.schema.yml` | Ledger route rows and `.craft/artifacts/*` receipts | Handoffs, receipts, route events, capability refs, receipt status, and application policy. | Candidate interface/interaction drafts, updated for current capability refs. |
| `projection.schema.yml` | `.craft/projections/*.csv` | Projection manifest, CSV table headers, source hash, editable/read-only columns, and supported families. | Tables from CSV/index refine result, with read-only defaults for nested fields. |
| `row-update.schema.yml` | Dry-run planner input/output | Normalized deltas, expected hash, field policy, verdicts, patch operations, no-op and block reports. | One-row dry-run planner contract for schema-defined families first. |
| `validation.schema.yml` | `validate` reports and tool receipts | Pass/flag/block reports, validation rule references, evidence, residue, and follow-up route. | Existing `VAL-*` rules plus structured report shape. |
| `artifact-manifest.schema.yml` | `.craft/artifacts/` | Artifact inventory, source path, owner context, artifact kind, status, checksum, and privacy/public-boundary flags. | Receipt/handoff/report file inventory that points back to `artifacts` rows. |

## 4. Workflow Process View

```text
1. Read current architecture baseline.
2. Identify which Craft layer a new behavior touches.
3. Load the layer schema and the compatibility entrypoint.
4. Validate source ledger rows before derived or exchanged surfaces.
5. Validate generated index/projection freshness against ledger hash.
6. Validate interface output as derived view only.
7. Validate handoffs/receipts/events as exchange records owned by called capabilities.
8. Validate planner deltas and patch plans before any future apply step.
9. Emit validation and artifact-manifest evidence.
10. Keep `.craft/ledger.yml` as source of truth throughout.
```

Schema validation should proceed from authority outward: source ledger first,
derived indexes second, human and projection views third, exchange and planner
reports only after the source row contract passes.

## 5. Decision Flow View

| Decision | Selected Behavior | Reason |
| --- | --- | --- |
| Keep one public entrypoint | `ledger.schema.yml` remains the compatibility entrypoint. | Existing examples and downstream references already point there. |
| Split layer schemas | Add `templates/schemas/*.schema.yml`. | Prevents index/interface/projection/planner rules from bloating one file. |
| Promote example-only rows | Formalize `descriptions`, `definitions`, `gaps`, and `recomposition`. | They are already live in examples and named by `SKILL.md`. |
| Separate route exchange from artifacts | Yes. | Handoff/receipt/event rows have lifecycle semantics beyond generic artifacts. |
| Separate generated indexes from embedded indexes | Yes, but keep compatibility. | Existing ledgers include embedded `indexes`; `.craft/index.json` needs freshness metadata. |
| Treat projections as staging | Yes. | CSV tables are review/import staging, never source authority. |
| Make planner reports schema-governed before apply | Yes. | The row updater must produce deterministic dry-run evidence before mutation. |
| Avoid broad schema implementation in one step | Yes. | First implementation should create the stack scaffold and migrate only proven families. |

## 6. Dependency Interface View

| Dependency | Interface | Contract Needed |
| --- | --- | --- |
| Current Craft package | `SKILL.md`, `README.md`, `ARCHITECTURE.md` | Source authority and current architecture baseline. |
| Current ledger schema | `templates/ledger.schema.yml` | Compatibility entrypoint and existing rules. |
| Example ledgers | `examples/*.yml` | Evidence for row families and link/index usage. |
| Example human views | `examples/*-CRAFT.md` | Evidence for interface anchors, quick links, section names, and current rendering style. |
| Interface draft | `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml` | Candidate descriptions/definitions/gaps and interface method rules. |
| Interaction draft | `development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml` | Candidate route handoffs, receipts, events, and exchange validation rules. |
| Index/projection proposal | latest refine and invoke index runs | Proposed `.craft/index.json`, projections, and CSV table contracts. |
| Row-update proposal | latest row planner invoke run | Proposed normalized delta, patch plan, and dry-run report contracts. |

## Schema Coverage Inventory

| Concept Or Artifact | Current State | Schema Need | Priority |
| --- | --- | --- | --- |
| `contexts` | canonical schema | keep in ledger-core | P0 |
| `artifacts` | canonical schema | keep in ledger-core; add artifact manifest linkage | P0 |
| `relations` | canonical schema | keep in ledger-core; include new route row refs when promoted | P0 |
| `typed_items` | canonical schema | keep in ledger-core | P0 |
| `decisions` | canonical schema | keep in ledger-core | P0 |
| `descriptions` | examples and interface draft | promote to ledger-core | P0 |
| `definitions` | examples and interface draft | promote to ledger-core with local-candidate rule | P0 |
| `gaps` | examples and interface draft | promote to ledger-core and index schema | P0 |
| `recomposition` | examples and method contract | promote to ledger-core or dedicated recomposition section | P0 |
| embedded `indexes` | canonical schema only as key list | formal index object shape and compatibility policy | P0 |
| `.craft/index.json` | named, not specified | generated index schema with hash/freshness/readiness | P0 |
| `CRAFT.md` | prose/examples | interface schema for anchors, sections, quick links, derived status | P1 |
| `state all` / pending-by-node | `SKILL.md` contract | interface schema for per-node status payload | P1 |
| `Craft Result` output | `SKILL.md` contract | interface schema for result envelope | P1 |
| `route_handoffs` | Body War example and interaction draft | route-exchange schema | P1 |
| `receipts` | Body War example and interaction draft | route-exchange schema | P1 |
| `route_events` | interaction draft only | route-exchange schema, candidate until example exists | P2 |
| `.craft/artifacts/` | storage contract only | artifact manifest schema | P2 |
| `.craft/projections/*.csv` | proposal only | projection schema with table headers and edit policy | P2 |
| CSV import staging metadata | proposal only | projection schema plus row-update schema | P2 |
| row update normalized delta | proposal only | row-update schema | P2 |
| patch plan / no-op / block report | proposal only | row-update schema and validation schema | P2 |
| validation report | method contract only | validation schema | P2 |

## Architecture Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Schema split creates incompatible duplicate authority. | high | Keep `ledger.schema.yml` as entrypoint until composed validation exists. |
| Example-only rows stay informal. | high | Promote `descriptions`, `definitions`, `gaps`, and `recomposition` first. |
| Index schema implies generated files are authority. | high | Require `ledger_sha256`, stale status, and source-of-truth policy. |
| Interface schema overfits current Markdown. | medium | Validate anchors/sections and required content, not exact prose. |
| Projection schema unlocks unsafe writeback too early. | high | Default nested fields to read-only and require row-update dry-run. |
| Route exchange schema claims owner verdicts. | high | Store receipts as evidence; called capability remains verdict owner. |
| Artifact manifest leaks local-only paths in public fixtures. | medium | Use synthetic fixtures and public-boundary scan before promotion. |

## Handoff To Planning

Recommended next route is `invoke plan` or `task-session` for one bounded
schema-stack slice:

1. Create `templates/schemas/` with a minimal schema-stack manifest.
2. Promote current example-backed row families into the canonical schema stack.
3. Add `index.schema.yml` for embedded indexes and generated `.craft/index.json`.
4. Update `ARCHITECTURE.md`, `README.md`, and `SKILL.md` to name the schema stack.
5. Validate against current examples and run public-boundary/diff checks.

Projection, row-update, artifact-manifest, and full interface schemas should be
planned as follow-up slices after the P0 source/index schemas are stable.

## Architecture Verdict

Pass with gated implementation. The missing layer schemas are real, but direct
canonical mutation should start with source-ledger and index schemas before
planner/projection behavior.
