# Inventory

Inventory is an Arcana sigil for installing and maintaining a repository-local compiled knowledge layer.

It is inspired by the wiki pattern: raw sources remain immutable, while an LLM-maintained inventory accumulates summaries, entity pages, concept pages, architecture notes, pattern entries, contradictions, tags, indexes, and logs. The human view stays Markdown; the machine view is JSON so agents can filter without reparsing prose. The repository stops treating knowledge as something to rediscover from raw documents every time and starts treating it as a maintained asset.

## Problem It Solves

Retrieval from raw files is useful, but it does not compound. Every question asks the agent to rediscover and resynthesize knowledge from scattered sources.

Inventory solves this by creating a maintained intermediate layer between raw sources and task execution. New sources are ingested once, integrated into existing pages, cross-linked, tagged, and logged. Later sigils can query the inventory before searching the whole repository.

## Evidence-Card Layer

Inventory can also maintain source-backed `evidence-card` records for reusable, selector-level knowledge.

An evidence-card is a compact unit with `source_refs`, authority state, captured provenance, optional `trace`, optional `residue`, and promotion metadata such as `promotion_owner`. Cards are designed for task-shaped lookup, linting, and downstream handoff packets without making Inventory the owner of ontology relations or canonical definitions.

Use evidence-cards when a source detail needs to be:

- inspected quickly through stable selectors,
- reused in more than one task,
- grouped into retrieval output,
- linted for authority or schema gaps,
- handed to Ontology Vault or Definitions Governance as candidate evidence.

Evidence-card handoffs must include a non-authority notice: downstream owners decide promotion, not Inventory.

## EvidenceSet Candidate Layer

Inventory may maintain candidate `EvidenceSet` records when the same evidence-card group needs to be reused across retrieval or handoff assembly.

An EvidenceSet is a flat grouped-evidence artifact: it stores included evidence-card IDs, excluded card IDs, reasons, index terms, handoff intent, a short synthesis note, residue, status, and promotion owner. It references evidence-cards rather than copying source excerpts, summaries, trace arrays, or captured metadata.

EvidenceSets are candidate-level until an explicit later promotion decision. They do not replace Context Builder packs, own ontology or definition authority, implement a ledger, or add a human UI surface.

## Use When

- a repository accumulates knowledge across many files, docs, conversations, or source captures,
- agents repeatedly rediscover the same architecture, terminology, decisions, or patterns,
- `context-builder` needs better selector-level evidence,
- `architecture-pattern-inventory` needs a broader knowledge substrate,
- a team wants a local markdown wiki that an LLM maintains,
- raw sources should stay immutable while generated summaries evolve.

## Do Not Use When

- the repository is too small to need a maintained knowledge layer,
- raw sources are not available or cannot be cited,
- the user wants one temporary answer rather than reusable inventory,
- the repository already has a maintained inventory and only needs a narrow lookup,
- the workflow cannot tolerate generated markdown updates.

## Architecture

Inventory uses four layers:

1. Raw sources: user-curated source material that the sigil reads but does not modify.
2. Inventory wiki: generated markdown pages the sigil creates and updates.
3. Machine index: `index.json` plus optional specialized `indexes/*.json` files for fast lookup, traceability, and validation.
4. Schema: local conventions that tell future agents how to ingest, tag, query, lint, and maintain the inventory.

## Default Package

The recommended install root is:

```text
.arcanum/inventory/
```

The default package contains:

```text
.arcanum/inventory/
  README.md
  schema.md
  index.md
  index.json
  log.md
  tags.md
  indexes/
  raw/
  wiki/
  entries/
  queries/
  lint/
```

Install mode may adapt to an existing docs, wiki, notes, or architecture package instead of creating a competing structure.

## Operations

- `install`: detect existing knowledge systems, ask setup questions, and create or adapt the inventory package.
- `ingest`: read raw sources, create source summaries, update related entries, refresh `index.md` and `index.json`, flag contradictions, and append the log.
- `lookup`: return relevant inventory pages, machine index entry IDs, evidence-cards, EvidenceSets, source refs, selectors, excluded matches, and gaps for another sigil.
- `query`: answer against the inventory and optionally file the answer as a synthesis page.
- `lint`: find contradictions, stale claims, orphan pages, missing backlinks, untagged pages, source coverage gaps, stale or unparsable machine indexes, invalid evidence-card enums, unsafe owner/status pairs, missing `source_refs`, missing `trace`, and unresolved `residue`.
- `validate`: check package structure, `index.md` and `index.json` coverage, log parseability, tag consistency, evidence links, evidence-card schema fields, EvidenceSet references, and downstream non-authority packet language.
- `backfill`: build entries from existing docs, architecture packages, context packs, decisions, or generated artifacts.
- `sync`: update package conventions after schema changes.

## Integration

[context-builder](../../transmutations/context-builder/) should consume inventory lookups before broad source search when building a task context pack.

[architecture-pattern-inventory](../architecture-pattern-inventory/) can read the inventory before mapping architecture and can contribute entries such as architecture layers, implementation patterns, dependency rules, test patterns, and observability signals.

Use the [repository observability package](../../framework/observability/REPOSITORY-PACKAGE.md) when available to record install decisions, ingests, contradictions, lint gaps, and validation results.

Ontology Vault and Definitions Governance may consume evidence-card handoff packets or candidate EvidenceSets, but those packets and sets are read models. `promotion_owner`, `governed_ref`, and non-authority notices must make clear when evidence is only captured or candidate-level.

## Machine Index

`index.md` is the human catalog. `index.json` is the primary machine catalog. It should parse with `jq`, include stable entry IDs, paths, types, tags, sources, status, freshness, residue, and derived lookup maps such as `by_id`, `by_type`, `by_tag`, and `by_source`.

CSV files may be emitted under `projections/` for spreadsheet or shell-table use, but they are projections from `index.json`, not authority. A CSV projection must declare its JSON source, purpose, and freshness.

## Why This Is Arcana

Inventory coordinates installation, local schema design, source ingestion, cross-page maintenance, lookup contracts, linting, and integration with other sigils. It is a long-lived repository knowledge system, not a one-time synthesis artifact.
