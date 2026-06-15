# Refine Seed Proposal: Craft Ledger CSV And JSON Indexes

## Raw Intent

Refine the use of CSVs and JSON indexes so Craft ledgers are faster and easier
to read and edit.

## Refined Seed

Craft should keep `.craft/ledger.yml` as the only source of truth, then add a
scriptable projection layer:

- `.craft/index.json` is the fast lookup surface for agents and tools.
- `.craft/projections/*.csv` are optional flat editing and review projections.
- CSV edits are only accepted through an import/reconcile script that patches
  the YAML ledger after validation.
- Generated artifacts carry source hash, schema version, generator version, and
  generated time so stale projections are detectable.

## Target Outcome

A future Craft update should let agents do common reads without scanning the
whole YAML document and let humans bulk-review or spreadsheet-edit row families
without making CSV authoritative.

## Candidate Data Surfaces

| Surface | Role | Authority |
| --- | --- | --- |
| `.craft/ledger.yml` | Canonical nested ledger state. | Source of truth. |
| `.craft/index.json` | Derived read index and integrity manifest. | Generated lookup only. |
| `.craft/projections/contexts.csv` | Flat context rows for review and edits. | Generated projection. |
| `.craft/projections/artifacts.csv` | Artifact path/status ownership table. | Generated projection. |
| `.craft/projections/typed_items.csv` | Blockers, gates, and enablers. | Generated projection. |
| `.craft/projections/decisions.csv` | Decision rows, proposed options, selected options, and blocking status. | Generated projection. |
| `.craft/projections/relations.csv` | Edge table for row-to-row relationships. | Generated projection. |
| `.craft/projections/gaps.csv` | Gap rows when present in a ledger. | Generated projection. |
| `.craft/projections/descriptions.csv` | Description rows when present in a ledger. | Generated projection. |
| `.craft/projections/definitions.csv` | Definition rows when present in a ledger. | Generated projection. |
| `.craft/projections/route_handoffs.csv` | Route handoff rows when present in a ledger. | Generated projection. |
| `.craft/projections/receipts.csv` | Receipt rows when present in a ledger. | Generated projection. |
| `.craft/projections/recomposition.csv` | Recomposition rows when present in a ledger. | Generated projection. |
| `.craft/projections/pending.csv` | Compact pending-by-node status for all-status reads. | Generated projection. |
| `.craft/projections/links.csv` | Normalized row links extracted from nested lists. | Generated projection. |

## Strategy

1. Define the projection contract before adding scripts.
2. Keep JSON as the optimized machine-read path.
3. Keep CSV as a constrained human-edit path.
4. Require a generator/import validator before any CSV writeback becomes
   supported.
5. Add public-safe fixtures before generated runtime mirrors are refreshed.

## Initial Gate Decisions

| Decision | Proposed Default |
| --- | --- |
| Is CSV source of truth? | No. CSV is generated and optionally importable. |
| Is `.craft/index.json` source of truth? | No. It is rebuildable lookup data. |
| Can users edit CSVs directly? | Yes, but only as input to a reconcile command. |
| Should indexes be committed? | Project-local policy, but stale-index checks must exist. |
| Should Craft use SQLite? | Not in this update. Keep portable file surfaces first. |

## Stop Conditions

- Block if any proposal makes generated CSV or JSON more authoritative than
  `.craft/ledger.yml`.
- Block if private workspace evidence is copied into public Craft fixtures.
- Block if CSV import semantics cannot preserve stable row IDs and nested links.
- Block if projection generation silently skips live row families that examples
  already use.
