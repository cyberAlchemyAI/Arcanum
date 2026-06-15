# Strategy Preview: CSV And JSON Projection Layer

## Current Contract

Craft already has the correct authority model:

- YAML ledger is authoritative.
- Markdown is the human view.
- JSON index is rebuildable lookup data.
- Indexes point to row IDs and paths rather than redefining content.

## Performance Hypothesis

Most read operations do not need the full YAML tree. A generated JSON index can
serve common lookups immediately:

- find row by ID;
- list open decisions;
- list active blockers and gaps;
- find artifact by path;
- render next moves;
- render pending-by-node for all-status reads;
- find reverse links for a row.

Most human edit operations do not need nested YAML either. CSV tables can make
status, owner, next move, and decision review faster if writeback is mediated by
a validator.

## Selected Route

Use derived JSON plus derived CSV:

1. JSON serves machine performance.
2. CSV serves human review and controlled edits.
3. YAML remains authoritative.
4. Import is disabled or dry-run-only until round-trip fixtures pass.

## Rejected Routes

| Route | Reason |
| --- | --- |
| JSON-only | Improves reads but does not help bulk human editing. |
| CSV-first | Improves editing but risks flattening nested semantics too early. |
| SQLite-backed ledger | Adds runtime and migration complexity before file projections are exhausted. |

## Toy-Game Fixture

The next executable route should add a tiny fixture with:

- two contexts;
- two artifacts;
- one active blocker;
- one open decision;
- one relation;
- one nested link list.

The fixture should export to `index.json` and CSV tables, then dry-run import a
small CSV edit back into YAML without changing row IDs or link ownership.

## Validation Expectations

- JSON parses.
- CSV headers are deterministic.
- YAML parse succeeds after import.
- `by_id` resolves every exported row.
- `reverse_links` matches relation and nested link owners.
- stale generated outputs are detected through `ledger_sha256`.
- live row families without a projection schema produce an explicit flag rather
  than silent omission.
