# Invoke Design: Craft Projection Layer

## Design Summary

Craft should separate canonical state from generated access surfaces. The
ledger remains readable and editable as YAML. Generated projections make common
reads cheap and make bulk review possible without weakening authority.

## Components

| Component | Role | Authority |
| --- | --- | --- |
| `ledger.yml` | Canonical nested Craft state. | Source of truth. |
| `index.json` | Lookup manifest, freshness state, reverse links, pending summaries. | Generated. |
| `projections/*.csv` | Flat family-specific review/import staging. | Generated. |
| `craft-index build` | Rebuild JSON and CSV from YAML. | Deterministic tool. |
| `craft-index validate` | Check freshness and projection consistency. | Validator. |
| `craft-index import-csv --dry-run` | Produce a YAML patch plan from edited CSVs. | Dry-run only at first. |

## JSON Index Contract

`index.json` should include:

- metadata: schema version, ledger hash, generated timestamp, generator version;
- `by_id`: row ID to row family and selector;
- `by_family`: row IDs grouped by family;
- status indexes: open decisions, blocking decisions, active blockers, active
  gaps, next moves, pending by node;
- path indexes: artifacts by path and source-line hints where available;
- graph indexes: reverse links, normalized references, evidence refs;
- stale status: current, stale, invalid, or unsupported-family.

## CSV Projection Contract

Use `.craft/projections/` to make generated status obvious. Initial projections:

- `contexts.csv`
- `artifacts.csv`
- `typed_items.csv`
- `decisions.csv`
- `relations.csv`
- `gaps.csv`
- `descriptions.csv`
- `definitions.csv`
- `route_handoffs.csv`
- `receipts.csv`
- `recomposition.csv`
- `pending.csv`
- `links.csv`

CSV files should include stable ID columns, owner/scope columns, status columns,
and a `source_hash` or projection manifest reference when needed. Complex nested
fields are read-only until import semantics are proven.

## Key Decisions

- Select `.craft/projections/` instead of `.craft/tables/` because the files are
  derived views, not authority tables.
- Treat embedded `indexes` in `ledger.yml` as compatibility data until a
  generator-owned policy replaces or refreshes them.
- Split `decisions.csv` into workflow and final-state columns:
  `decision_state`, `proposed_option`, `selected_option`, `rationale`,
  `blocking`.
- Normalize evidence and links into `references`, `links_out`, `links_in`, and
  `evidence_refs` in JSON.

## Failure Modes

- CSV flattening loses nested links or evidence references.
- Generated files become stale and are trusted accidentally.
- Existing example row families are silently skipped.
- Public fixtures accidentally include private workspace data.

## Design Verdict

`flag`: the design is coherent and additive, but implementation must first close
the live row-family schema gap and create a toy-game fixture before import is
enabled.
