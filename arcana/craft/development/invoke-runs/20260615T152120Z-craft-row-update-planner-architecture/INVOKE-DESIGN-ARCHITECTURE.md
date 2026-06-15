# Architecture Bundle: Craft Row Update Planner

## Design Identity

- Spell: `invoke`
- Mode: `design`
- Target artifact: Craft deterministic row update planner proposal.
- Target owner: `arcana/craft`
- Phase status: `pass`
- Source refine run: `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/`
- Architecture profile: Module Formulae six-view architecture bundle.

## Design Intent

Craft needs a deterministic row update planner so CSV writeback and later edit
surfaces can reuse one safe reconciliation primitive. The architecture keeps
`.craft/ledger.yml` authoritative, makes every generated or edited surface a
staging input, and emits dry-run patch plans before any future YAML mutation is
allowed.

This bundle is proposal architecture only. It does not implement scripts,
change Craft canonical source, refresh generated mirrors, or move publication
state.

## Inputs

- `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/RESULT.md`
- `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/stages/S06-INVOKE-DESIGN.md`
- `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/stages/S08-DISTILL-REPAIR.md`
- `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/WORK-PACK.md`
- `arcana/craft/SKILL.md`
- `arcana/craft/templates/ledger.schema.yml`
- `arcana/craft/development/refinement-runs/20260615T121512Z-craft-ledger-csv-json-indexes/RESULT.md`

## 1. Context View

```text
Craft user or agent
  proposes row-level edit through CSV, CLI, form, or local runtime action
      |
      v
row update planner
  reads .craft/ledger.yml + schema + proposal metadata
      |
      +--> pass: deterministic patch plan
      +--> pass: no-op report
      +--> block: safety violation report
      +--> flag: supported but review-needed report

future owner-approved apply step
  remains outside this proposal architecture
```

Craft's canonical ledger is YAML. `CRAFT.md`, `.craft/index.json`, and
`.craft/projections/*.csv` are derived or staged views. The row update planner
sits between edit proposals and future YAML mutation, not beside the ledger as a
second state store.

## 2. High-Level Structure View

```text
source ledger boundary
  .craft/ledger.yml
  arcana/craft/templates/ledger.schema.yml
      |
      v
read/index boundary
  load_ledger
  build_row_index
  derive selectors and references
      |
      v
proposal boundary
  normalized proposed delta
  expected ledger_sha256
  source surface metadata
      |
      v
planner boundary
  field_policy
  validate_delta
  plan_patch
  emit_report
      |
      v
evidence boundary
  patch-plan JSON/Markdown
  no-op report
  block report
```

The key architectural move is separating proposal normalization from patch
planning. CSV import becomes one producer of normalized deltas; it should not
own ledger reconciliation rules.

## 3. Low-Level Components View

| Component | Inputs | Output | Rule |
| --- | --- | --- | --- |
| `load_ledger` | ledger path or bytes | parsed YAML, `ledger_sha256` | read-only; byte hash is freshness authority. |
| `load_schema_contract` | `ledger.schema.yml` | family, ID, enum, reference, field metadata | schema is the source for field validity. |
| `build_row_index` | parsed ledger | `{family, id}` selectors and reference graph | stable ordering; duplicate IDs block. |
| `normalize_delta` | edit source payload | typed field delta | input format specific; no validation authority. |
| `field_policy` | family + schema + planner allowlist | editable/read-only decision | explicit allowlist for first slice. |
| `validate_delta` | row, delta, row index, schema | pass/flag/block reasons | blocks stale source, ID churn, invalid enum, bad reference. |
| `plan_patch` | current row + validated delta | ordered patch operations | dry-run only; no file write. |
| `emit_report` | verdict + operations + reasons | stable JSON/Markdown report | deterministic output ordering. |

## 4. Workflow Process View

```text
1. Read ledger bytes.
2. Compute current ledger_sha256.
3. Load schema contract and planner field policy.
4. Normalize proposed edit into:
     family, row_id, expected_ledger_sha256, field_deltas.
5. Compare expected and current ledger hashes.
6. Resolve exactly one row by family and row_id.
7. Reject any row ID mutation.
8. Classify each proposed field as editable or read-only.
9. Validate enum values, required fields, references, and no-op status.
10. Emit deterministic report:
      pass with patch plan,
      pass with no-op,
      flag with review-needed residue,
      or block with exact reason.
11. Stop before YAML mutation.
```

## 5. Decision Flow View

| Decision | Selected Behavior | Reason |
| --- | --- | --- |
| Source of truth | `.craft/ledger.yml` | Preserves Craft storage contract. |
| First exposure | internal planner primitive | Avoids creating public CLI semantics before fixture proof. |
| First mutation mode | dry-run only | Prevents accidental YAML writes. |
| First update granularity | one row at a time | Keeps patch plan inspectable and deterministic. |
| First field policy | selected scalar/simple fields | Avoids unsafe nested evidence/link flattening. |
| Stale source | block | Prevents projection writeback over newer ledger state. |
| ID churn | block | Preserves row identity and index stability. |
| Unknown fields | block | Prevents silent schema drift. |
| Nested evidence edits | read-only/block | Deferred until specific fixture proof. |
| No semantic diff | pass no-op | Lets callers distinguish harmless edits from failures. |

## 6. Dependency Interface View

| Dependency | Interface | Contract |
| --- | --- | --- |
| Craft schema | `ledger.schema.yml` | Supplies row families, ID fields, enum values, and reference rules. |
| Craft ledger | `.craft/ledger.yml` | Supplies current authoritative state and source hash. |
| Projection metadata | `.craft/index.json` / `.craft/projections/*.csv` | Supplies `ledger_sha256`, row selectors, and staged field values. |
| CSV import dry-run | future caller | Produces normalized deltas and aggregates planner reports. |
| Craft validator | future validation caller | Confirms planned operations would preserve ledger invariants. |
| Task Session | next lifecycle owner | Executes `SWU-CRU-001` or later SWUs; Invoke does not execute. |

## Architecture Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Split row planner from CSV import. | selected | Keeps reconciliation reusable and testable below CSV import. |
| Keep direct apply mode out of first architecture. | selected | Dry-run proof is required before mutation. |
| Treat generated projection files as staging inputs. | selected | Generated files cannot become authority. |
| Use toy fixture before implementation. | selected | Proves pass/no-op/block behavior cheaply. |
| Defer public CLI name. | deferred | The first architecture needs stable semantics, not a command surface. |

## Open Risks

| Risk ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| R-CRU-1 | Planner grows into broad ledger editor. | high | First slice is dry-run and one-row only. |
| R-CRU-2 | CSV-specific assumptions leak into core planner. | medium | Planner consumes normalized deltas, not CSV rows. |
| R-CRU-3 | Nested fields are flattened unsafely. | high | Nested evidence/link edits are read-only until fixture proof. |
| R-CRU-4 | Patch output differs across runs. | medium | Stable sorting and canonical report output are required. |
| R-CRU-5 | Generated metadata is trusted when stale. | high | Expected hash mismatch blocks. |

## Planning Notes

- Direct implementation constraints: first implementation must be patch-plan
  only, not apply mode.
- Boundary rules: no canonical Craft source mutation from this architecture
  bundle; no generated mirror refresh until later validation passes.
- Testability implications: toy fixture must include pass, no-op, stale hash,
  ID churn, invalid enum, unresolved reference, and read-only nested-field cases.

## Handoff Targets

- `IMPLEMENTATION-LAYERING-SEED.md`
- `DESIGN-TRANSPORT.md`
- Existing next execution source: `../refinement-runs/20260615T131737Z-craft-deterministic-row-updater/WORK-PACK.md`

## Architecture Verdict

Pass. The proposal is architecture-ready for a bounded `task-session` on
`SWU-CRU-001`, with implementation still blocked until that route is explicitly
started.
