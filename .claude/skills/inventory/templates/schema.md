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

## Log Heading Pattern

Use this heading pattern for parseable log entries:

```markdown
## [YYYY-MM-DD] <mode> | <short title>
```
