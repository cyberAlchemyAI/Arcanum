---
module: inventory-interface-link-index
version: current
status: draft
updatedAt: 2026-06-05
docType: research
owner: inventory
---

# Index Technique Research

## Purpose

Identify indexing techniques Inventory should support while staying JSON +
Markdown based.

The archived repository-wide research package contains a tag taxonomy and
proposed repository/zone/surface/slice indexes. This active document extracts
the reusable techniques and extends them for the Inventory interface.

## Existing Technique Baseline

Already present in current Inventory design:

| Technique | Current Form | Gap |
| --- | --- | --- |
| faceted tags | `TAG-TAXONOMY.md` tag families | needs counts, owners, and validation |
| layered indexes | repository -> zone -> slice -> card | needs link and selector indexes |
| source-backed cards | evidence-card contract | needs interface path from prompt to card |
| EvidenceSets | candidate grouped card refs | needs repeated-use promotion criteria |
| retrieval fixtures | `retrieval.json` per slice | needs standard query/result shape |
| coverage reports | `COVERAGE.md` | needs gap queue integration |

## Techniques To Add

### 1. Selector Index

Purpose:

Map source selectors to cards and records.

Use when:

- future agents need to jump to exact source context,
- broad source pages are too expensive to reread,
- validation needs to ensure every claim has source support.

File:

```text
indexes/selector-index.json
```

Shape:

```json
{
  "selector_id": "sel-arcanum-readme-capability-model",
  "path": "arcanum/README.md",
  "selector": "# Capability Model",
  "line_start": null,
  "line_end": null,
  "card_refs": [
    "card-arcanum-capability-model"
  ],
  "tags": [
    "zone:arcanum",
    "artifact:readme"
  ]
}
```

Validation:

- path exists,
- selector is either heading, line span, or named anchor,
- card refs exist.

### 2. Link Index

Purpose:

Store typed relationships among sources, cards, generated records, and handoff
targets without making them ontology relations.

File:

```text
indexes/link-index.json
```

Shape:

```json
{
  "links": [
    {
      "from": "card-arcanum-capability-model",
      "edge": "cites",
      "to": "arcanum/README.md#capability-model",
      "evidence": "source_ref",
      "authority": "inventory-read-model",
      "non_authority_notice": "Inventory link only; not an Ontology Vault relation."
    }
  ]
}
```

Initial edge vocabulary:

| Edge | Meaning |
| --- | --- |
| `cites` | card or record cites source selector |
| `summarizes` | generated record summarizes source/card |
| `indexes` | index entry points to source/card/record |
| `duplicates-risk` | two surfaces may duplicate scope |
| `conflicts-with` | two sources conflict or claim overlapping authority |
| `hands-off-to` | Inventory output routes to another owner |
| `derived-from` | generated artifact came from source/card |
| `excludes` | record intentionally excludes nearby source |

Validation:

- both endpoints resolve or are marked external,
- edge is in controlled vocabulary,
- relation-like edges include non-authority notice.

### 3. Backlink Index

Purpose:

Answer "what uses this source/card/tag?" without editing every Markdown file.

File:

```text
indexes/backlink-index.json
```

Shape:

```json
{
  "target": "arcanum/README.md#capability-model",
  "used_by": [
    {
      "ref": "card-arcanum-capability-model",
      "edge": "cites",
      "slice_id": "sigils-library-arcanum-authority"
    }
  ]
}
```

Validation:

- every backlink is generated from `link-index.json`,
- do not hand-edit backlinks.

### 4. Traceability Matrix

Purpose:

Borrow DomainSpec's discipline: every generated artifact should trace to source
and every important obligation should trace to validation or coverage.

File:

```text
indexes/traceability-matrix.json
```

Shape:

```json
{
  "rows": [
    {
      "obligation": "card claims must cite source selectors",
      "source": "arcana/inventory/SKILL.md#evidence-card-contract",
      "artifact": "slices/sigils-library-arcanum-authority/cards.json",
      "validation": "validate-evidence-card-fixtures",
      "status": "planned"
    }
  ]
}
```

Validation:

- every slice has at least one traceability row,
- validation refs are either concrete scripts or explicit manual checks.

### 5. Surface Index

Purpose:

Record existing registries, glossaries, inventories, ontology packs, and source
digests before creating new records.

Already proposed in `INDEXING-SHAPE.md`; should become mandatory before
backfill.

Additional fields:

- `adopt | link-only | exclude | needs-decision`,
- `duplicate_risk`,
- `authority_owner`,
- `safe_lookup_use`,
- `unsafe_use`.

### 6. Query Pattern Index

Purpose:

Capture repeated lookup questions so Inventory improves from use.

File:

```text
indexes/query-pattern-index.json
```

Shape:

```json
{
  "query_pattern_id": "qp-source-authority",
  "example_queries": [
    "which source owns this?",
    "what should I read before changing inventory?"
  ],
  "preferred_indexes": [
    "surface-index.json",
    "link-index.json",
    "selector-index.json"
  ],
  "expected_result_shape": "selected records, excluded records, gaps, next route"
}
```

Validation:

- query patterns point to existing retrieval fixtures,
- repeated patterns may justify an EvidenceSet candidate.

### 7. Gap/Risk Queue

Purpose:

Make unresolved residue operational.

File:

```text
indexes/gap-risk-index.json
```

Shape:

```json
{
  "gap_id": "gap-arcanum-sigils-library-authority",
  "kind": "authority-conflict",
  "summary": "Arcanum and sigils-library both claim sigil/capability authority.",
  "source_refs": [
    "arcanum/README.md",
    "sigils-library/README.md"
  ],
  "owner": "decision-gate",
  "status": "open",
  "next_route": "decision-gate"
}
```

Validation:

- every `risk:*` tag on a card either has a closed reason or a gap/risk row.

### 8. Projection Index

Purpose:

Let Inventory project JSON indexes into Markdown, HTML, SQLite, or vector search
without changing source-of-truth files.

File:

```text
indexes/projection-index.json
```

Shape:

```json
{
  "projection_id": "html-inventory-browser",
  "source_indexes": [
    "repository-index.json",
    "tag-index.json",
    "link-index.json"
  ],
  "projection_type": "html",
  "status": "planned",
  "authority": "read-model-only"
}
```

Validation:

- projections are read models,
- projection artifacts never become canonical source.

## Technique Stack Recommendation

Minimum viable stack:

```text
tag-index
surface-index
selector-index
link-index
traceability-matrix
gap-risk-index
```

Defer:

- vector index,
- SQLite projection,
- full browser UI,
- embedding search,
- automatic graph inference.

Reason:

The immediate failure mode is not search power. It is losing source authority,
link discipline, and confirmation UX. JSON indexes plus Markdown records solve
that first.

## External Technique Adaptation Notes

Use these common indexing patterns, adapted locally:

| General Technique | Inventory Adaptation |
| --- | --- |
| inverted index | tag/query term index pointing to card IDs |
| faceted navigation | tag families with counts and owner/risk facets |
| citation graph | source/card/record link index |
| adjacency list | typed link index JSON |
| materialized view | generated Markdown/HTML projection |
| backlink graph | generated backlink index from link index |
| traceability matrix | source -> card -> validation rows |
| authority file | zone/surface owner map |
| retrieval fixture | example query with selected/excluded records |
| gap ledger | operational residue queue |

## Research Conclusion

Inventory should become a small linked-data system stored in JSON and Markdown.

The first implementation should not chase semantic search. It should make the
deterministic indexes correct:

- stable IDs,
- source selectors,
- typed links,
- controlled tags,
- generated backlinks,
- traceability rows,
- gap/risk queue,
- confirmation before mutation.
