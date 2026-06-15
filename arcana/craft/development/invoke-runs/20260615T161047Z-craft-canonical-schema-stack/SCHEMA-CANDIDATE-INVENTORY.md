# Schema Candidate Inventory

## Purpose

Identify the Craft concepts and artifacts that need canonical schema coverage
before index, projection, interface, or row-update tooling becomes safe.

## Current Canonical Coverage

| Surface | Status | Notes |
| --- | --- | --- |
| `templates/ledger.schema.yml` | canonical-first | Owns source ledger policy, links, indexes key list, enums, five row families, validation rules, blocker lifecycle, conflict policy, and deferrals. |
| `examples/body-war-ledger.yml` | canonical example | Exercises descriptions, definitions, gaps, route handoffs, receipts, relations, and recomposition beyond the current schema. |
| `examples/goldenquill-ledger.yml` | canonical example | Exercises descriptions, definitions, gaps, relations, and recomposition beyond the current schema. |
| `examples/*-CRAFT.md` | canonical examples | Exercise anchors, quick links, sections, gaps, definitions, route evidence, recomposition, and artifact links. |
| `ARCHITECTURE.md` | canonical baseline | Explicitly marks no planner, no projections, no shipped index builder, and schema/example tension. |

## Candidate Schemas

### P0 Source Ledger Schemas

`ledger-core.schema.yml`

- Preserve existing row families: `contexts`, `artifacts`, `relations`,
  `typed_items`, `decisions`.
- Promote example-backed row families: `descriptions`, `definitions`, `gaps`,
  `recomposition`.
- Add ID patterns and reference rules for:
  - `DESC-*`
  - `DEF-*`
  - `GAP-*`
  - recomposition child/parent context refs.
- Keep definitions local-candidate unless an owner route promotes them.

`index.schema.yml`

- Formalize embedded `indexes`.
- Formalize generated `.craft/index.json`.
- Required generated metadata:
  - `schema_version`
  - `ledger_sha256`
  - `generated_at`
  - `generator_version`
  - `source_ledger`
  - `stale_status`
- Required lookup groups:
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

### P1 Interface And Exchange Schemas

`interface.schema.yml`

- `CRAFT.md` required sections by current examples.
- Anchor conventions for context, artifact, blocker, enabler, decision, gap,
  route evidence, and recomposition.
- Quick links and pending-by-node requirements.
- `state all` payload shape.
- `Craft Result` output envelope from `SKILL.md`.

`route-exchange.schema.yml`

- `route_handoffs`
- `receipts`
- `route_events`
- capability refs and native verdict ownership.
- application policies:
  - `record-only`
  - `apply-to-context`
  - `open-residue`
  - `recompose-child`

### P2 Derived Surface Schemas

`projection.schema.yml`

- `.craft/projections/manifest.yml`
- CSV table identity, headers, read-only/editable policy, source hash,
  generated timestamp, and source family.
- Initial tables:
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

`row-update.schema.yml`

- normalized edit proposal:
  - `family`
  - `row_id`
  - `expected_ledger_sha256`
  - `source_surface`
  - `field_deltas`
- field policy:
  - editable
  - read-only
  - blocked
  - review-needed
- report shapes:
  - pass patch plan
  - pass no-op
  - flag review-needed
  - block safety violation.

`validation.schema.yml`

- structured validation report:
  - verdict
  - rule IDs
  - severity
  - evidence
  - residue
  - next route
  - checked schemas
  - checked files.

`artifact-manifest.schema.yml`

- `.craft/artifacts/manifest.yml`
- artifact file identity, owner context, artifact row reference, checksum,
  public-boundary flag, source route, and freshness.

## Concepts That Should Not Become Schemas Yet

| Concept | Reason |
| --- | --- |
| Global definition authority | Craft owns local candidates only; definitions-governance owns canonical definitions. |
| Generic runtime adapter API | Broader runtime handoff belongs outside Craft's first schema stack. |
| Direct YAML apply mode | Needs row-update dry-run proof first. |
| Exact Markdown prose rendering | Interface schema should validate anchors/sections/content obligations, not prose wording. |
| Private project-specific artifact types | Public Craft schema should keep artifact type open unless observed broadly. |

## First Slice Recommendation

Implement only the P0 schema slice first:

1. Create `templates/schemas/ledger-core.schema.yml`.
2. Create `templates/schemas/index.schema.yml`.
3. Keep `templates/ledger.schema.yml` as compatibility entrypoint.
4. Add example validation notes for current Body War and GoldenQuill ledgers.
5. Defer interface, route-exchange, projection, row-update, validation-report,
   and artifact-manifest schemas until the core/index split validates.

This gives the row updater a stable family/index base without prematurely
blessing CSV writeback.
