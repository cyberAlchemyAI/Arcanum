---
module: inventory-interface-link-index
version: current
status: draft
updatedAt: 2026-06-05
docType: refine-synthesis
owner: inventory
---

# Refine Synthesis: Inventory Interface And Indexing

## Result

The Inventory work should pivot from "research the whole repository" to
"design the interface and index/link architecture that makes any future
inventorization safe."

The core architecture is:

```text
chat-first interface
  -> target inference
  -> confirmation
  -> bounded slice
  -> JSON indexes
  -> Markdown coverage and explanation
  -> lookup/status/explain views
```

## What Already Exists

Useful current assets:

- `arcana/inventory/SKILL.md` has technical modes, evidence-card contract,
  EvidenceSet contract, lookup/query/lint/validate rules.
- `archive/domainspec-core-research-20260605/TAG-TAXONOMY.md` defined initial
  tag families during the archived repository research pass.
- `archive/domainspec-core-research-20260605/INDEXING-SHAPE.md` defined
  repository/zone/slice/card index layers during the archived research pass.
- DomainSpec provides strong linking patterns: authority maps, stable IDs,
  typed relationships, traceability matrices, source-of-truth registries, and
  required backlinks where they matter.

## Main Gaps

1. No default `$inventory` interface.
2. No target inference record.
3. No confirmation proposal schema.
4. No selector index.
5. No link index.
6. No generated backlink index.
7. No traceability matrix for Inventory slices.
8. No gap/risk queue.
9. No clear rule for Markdown as human projection and JSON as machine source.

## Design Decision

Use JSON + Markdown as the source-of-truth interface substrate.

Do not introduce a database, vector store, or full web UI yet.

## Required Artifacts Added

- `INTERFACE-ARCHITECTURE.md`
- `INDEX-TECHNIQUE-RESEARCH.md`
- `LINKING-DISCIPLINE.md`

## Recommended Next Implementation Work

### SWU 1: Add Inventory Auto Interface Contract

Change:

- update `arcana/inventory/SKILL.md`
- add default/no-mode behavior,
- add `auto`, `inventorize`, `status`, `continue`, and `explain` interface
  modes,
- require target inference and confirmation before mutation.

Acceptance:

- `$inventory` without explicit mode has defined behavior,
- vague prompt produces a target proposal,
- mutation waits for confirmation.

### SWU 2: Add Index Schema Pack

Create templates/schemas for:

- `selector-index.json`
- `link-index.json`
- `backlink-index.json`
- `traceability-matrix.json`
- `gap-risk-index.json`
- `query-pattern-index.json`

Acceptance:

- JSON examples validate structurally,
- edge/tag vocabularies are controlled,
- relation-like links carry non-authority notices.

### SWU 3: Add First Slice Using The Interface

Target:

```text
sigils-library-arcanum-authority
```

Output:

```text
slices/sigils-library-arcanum-authority/
  cards.json
  index.json
  retrieval.json
  COVERAGE.md
```

Acceptance:

- target confirmation captured,
- cards cite selectors,
- link index and gap/risk row record authority conflict,
- lookup result can show selected/excluded/gaps.

## Open Decisions

| Decision | Options | Recommendation |
| --- | --- | --- |
| Interface storage | transient chat only, Markdown only, JSON + Markdown | JSON + Markdown |
| First index set | tag only, tag + selector, full set | tag + selector + link + gap/risk |
| Backlinks | manual Markdown, generated JSON, none | generated JSON |
| Semantic edges | Inventory-owned, Ontology-owned, mixed | Inventory uses read-model edges only |
| First UI | chat views, static HTML, full web app | chat views first |

## Confirmation Gate

The next executable step is not more research. It is implementation design:

```text
Update Inventory skill/interface contract and add JSON index schema templates.
```

This should run through a bounded task-session or direct patch after approval.
