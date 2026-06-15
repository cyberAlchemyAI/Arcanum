# Refine Result: Craft Ledger CSV And JSON Indexes

## Status

- Target: `arcana/craft`
- Status: `flag`
- Canonical mutation: not run
- Research mode: no-research
- Dispatch: `REFINE-DISPATCH.json`
- Runtime-backed Refine loop: executed locally through parent-native Codex stage receipts.

## Refined Synthesis

Craft should add a projection layer, not a second ledger authority. The
performance route is:

- keep `.craft/ledger.yml` as canonical YAML;
- generate `.craft/index.json` for fast agent/tool reads;
- generate `.craft/projections/*.csv` for flat human review and controlled bulk
  edits;
- allow CSV writeback only through a dry-run reconcile script that patches YAML
  after validation.

This gives agents a cheap lookup path while preserving Craft's current
source-of-truth model.

## Proposed JSON Index Shape

`index.json` should be a denormalized lookup manifest with:

- `metadata.schema_version`
- `metadata.ledger_sha256`
- `metadata.generated_at`
- `metadata.generator_version`
- `by_id`
- `by_family`
- `row_selectors`
- `open_decisions`
- `blocking_decisions`
- `active_blockers`
- `active_gaps`
- `next_moves`
- `pending_by_node`
- `artifacts_by_path`
- `reverse_links`
- `references`
- `evidence_refs`
- `stale_status`

The index points to row IDs, families, paths, selectors, source-line hints when
available, and checksums. It must not copy full row content as authority.

## Proposed CSV Tables

| CSV | Purpose |
| --- | --- |
| `contexts.csv` | Scan and edit context stage, gate, next move, and parentage. |
| `artifacts.csv` | Scan artifact ownership, status, type, and path. |
| `typed_items.csv` | Review blockers, gates, enablers, owners, and closure conditions. |
| `decisions.csv` | Review open/blocking decisions and selected options. |
| `relations.csv` | Preserve graph edges as source and target row IDs. |
| `gaps.csv` | Review active gaps where the ledger includes a gaps family. |
| `descriptions.csv` | Review description rows already present in live examples. |
| `definitions.csv` | Review definition rows already present in live examples. |
| `route_handoffs.csv` | Review route handoff rows when ledgers include them. |
| `receipts.csv` | Review receipt rows and validation evidence. |
| `recomposition.csv` | Review child-to-parent recomposition rows. |
| `pending.csv` | Give all-status reads a compact per-node fast path. |
| `links.csv` | Flatten nested row links without losing their owning row. |

CSV tables should use stable ID columns and explicit owner columns. Fields that
cannot round-trip cleanly should be read-only until an import strategy proves
safe.

`decisions.csv` should split workflow and final-state columns, using
`proposed_option`, `selected_option`, `decision_state`, `rationale`, and
`blocking` rather than forcing open decisions to look final.

## Import And Editing Rule

Direct spreadsheet editing is acceptable only as a staging format. The safe
write path is:

1. Export YAML ledger to JSON index and CSV tables.
2. User edits one or more CSV tables.
3. Import command compares CSV rows against `ledger_sha256`.
4. Import command emits a dry-run patch plan.
5. Validator checks IDs, references, nested links, enums, and required fields.
6. Only then patch `.craft/ledger.yml` and regenerate projections.

## Recommended Implementation Plan

1. Add a projection contract to the Craft schema and operating docs.
2. Add a tiny public-safe fixture with expected `index.json` and CSV outputs.
3. Add `craft-index build` to generate JSON and CSV projections.
4. Add `craft-index validate` to detect stale or broken projections.
5. Add `craft-index import-csv --dry-run` before allowing writeback.
6. Regenerate runtime mirrors only after canonical source and fixture checks pass.

## Stage Evidence

- Context Builder evidence baseline: pass, `stages/S01-CONTEXT-BUILDER.md`
- Invoke Define: pass, `stages/S02-INVOKE-DEFINE.md`
- Interrogation refine-review: pass, `stages/S03-INTERROGATION-REFINE-REVIEW.md`
- Research decision: pass, `stages/S04-RESEARCH-DECISION.md`
- Distill: pass, `stages/S05-DISTILL.md`
- Invoke Redefine / Design: pass, `stages/S06-INVOKE-DESIGN-RECEIPT.md`
- Interrogation refine-design-review: pass, `stages/S07-INTERROGATION-DESIGN-REVIEW.md`
- Distill Repair: pass, `stages/S08-DISTILL-REPAIR.md`
- Invoke Plan: pass, `stages/S09-INVOKE-PLAN-RECEIPT.md`
- Final Interrogation and Synthesis: flag, `stages/S10-FINAL-INTERROGATION-SYNTHESIS.md`

## Design And Plan Outputs

- Define: `DEFINE.md`
- Design: `INVOKE-DESIGN.md`
- Glossary consistency: `GLOSSARY-CONSISTENCY.md`
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Plan: `INVOKE-PLAN.md`
- Work-pack: `WORK-PACK.md`
- Machine receipt: `stages/execution-receipt.json`

## Open Residue

- Confirm `.craft/projections/` as the folder name, or deliberately pick a
  different generated-output namespace.
- Decide whether project-local generated projections are committed by default or
  rebuilt locally.
- Decide which CSV columns are editable in the first implementation slice.
- Decide whether JSON index should include row selectors only or shallow row
  summaries for faster status rendering.
- Close the schema gap for live row families used by examples but not yet
  formalized in the row-family contract.
- Decide whether embedded `indexes` inside `ledger.yml` remain compatibility
  data, become generator-owned, or are replaced by `.craft/index.json`.

## Next Route

Execute only the first approved SWU from `WORK-PACK.md`. The first likely SWU is
`SWU-CLP-001`, the schema/docs projection contract, not the import script.
