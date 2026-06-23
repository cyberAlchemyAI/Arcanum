# Inventory Schema

Schema Artifact Role: package-conventions

This file documents package conventions. It is not the canonical machine-readable schema artifact for evidence-cards or EvidenceSets.

This file defines the local conventions for the inventory package.

## Storage

- Inventory root: `.arcanum/inventory/`
- Raw sources: `raw/`
- Generated wiki pages: `wiki/`
- Typed entries: `entries/`
- Query syntheses: `queries/`
- Lint reports: `lint/`
- Machine index: `index.json`
- Optional specialized indexes: `indexes/*.json`
- Optional CSV projections: `projections/*.csv`

## Source Policy

- Raw sources are immutable.
- Generated pages must cite source files, source headings, or source selectors when possible.
- Claims without direct source support must be marked as inference, synthesis, or open question.

## Page Frontmatter

Use frontmatter when the repository accepts it:

```yaml
type: concept
status: active
tags: []
sources: []
updated: YYYY-MM-DD
confidence: high | moderate | low
related: []
```

If frontmatter is not used, keep equivalent metadata in a `Metadata` table near the top of each generated page.

## Entry Types

Default entry types:

- source
- entity
- concept
- architecture-layer
- implementation-pattern
- decision
- capability
- workflow
- interface
- dependency-rule
- test-pattern
- observability-signal
- question
- contradiction
- synthesis

Custom entry types must define purpose, required fields, evidence rules, tag rules, and update behavior.

## Link Policy

- Prefer ordinary markdown links for repository portability.
- Wiki links may be used only when the repository explicitly chooses that convention.
- Every generated page should link to related pages when meaningful.

## Machine Index Policy

- `index.md` is the human-readable catalog.
- `index.json` is the primary machine-readable catalog and must parse with
  `jq`.
- Every generated page, typed entry, query file, lint report, evidence-card
  bundle, and EvidenceSet bundle should have a stable row in `index.json`.
- Machine index rows should include stable ID, path, kind, type, title, summary,
  tags, sources, updated date, status, confidence when known, selectors,
  evidence-card IDs, EvidenceSet IDs, and unresolved residue.
- `index.json` should include derived lookup maps such as `by_id`, `by_type`,
  `by_tag`, `by_source`, and `by_status` when useful.
- Optional `indexes/*.json` files may specialize selector, link, backlink, tag,
  traceability, query-pattern, gap/risk, or projection lookup.
- Optional CSV files under `projections/` are flat read-model projections from
  `index.json`; they must declare their source, purpose, and freshness and must
  not replace `index.json`.

## Log Heading Pattern

Use this heading pattern for parseable log entries:

```markdown
## [YYYY-MM-DD] <mode> | <short title>
```
