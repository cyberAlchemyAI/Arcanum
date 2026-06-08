---
module: inventory-interface-link-index
version: current
status: draft
updatedAt: 2026-06-05
docType: design
owner: inventory
---

# Linking Discipline

## Purpose

Adapt DomainSpec's linking and traceability discipline to Inventory.

The goal is practical: every generated Inventory object should make it obvious
where it came from, what it links to, what it excludes, and which owner must
decide unresolved authority.

## DomainSpec Lessons To Reuse

### 1. Source Of Truth Links

DomainSpec uses authority maps and source-of-truth notes to decide which
artifact wins when sources disagree.

Inventory adaptation:

- every generated record needs `source_refs`,
- every source surface needs `authority_owner`,
- every conflict gets `risk:authority-conflict`,
- Inventory records must not decide another owner's authority.

### 2. Stable IDs

DomainSpec traceability depends on stable concept/test/rule IDs or heading
anchors.

Inventory adaptation:

- every card has stable `card_id`,
- every slice has stable `slice_id`,
- every selector has stable `selector_id`,
- every generated Markdown record has a frontmatter `id`,
- IDs must not be renumbered after publication.

### 3. Typed Relationships

DomainSpec uses typed relationship vocabularies to make graphs navigable.

Inventory adaptation:

- use typed Inventory links, not prose-only references,
- keep edge vocabulary small,
- mark relation-like links as non-authority read models,
- route ontology relation promotion to Ontology Vault.

### 4. Traceability Matrix

DomainSpec research/project work uses traceability matrices to connect claims,
experiments, artifacts, and evidence.

Inventory adaptation:

- each slice should have traceability from source anchors to cards,
- each card should trace to selectors,
- each retrieval fixture should trace to cards,
- each gap should trace to source refs and next owner.

### 5. Required Backlinks Only When Useful

DomainSpec research notes warned against high-boilerplate templates where every
small artifact must carry heavy backlink sections.

Inventory adaptation:

- store backlinks as generated JSON, not hand-maintained Markdown boilerplate,
- require manual backlinks only in `COVERAGE.md` for important omissions,
- keep card JSON compact.

## Inventory Link Model

Inventory should support two link layers.

### Human Markdown Links

Use Markdown links for:

- coverage reports,
- architecture docs,
- source explanations,
- next-route handoffs.

Rule:

```text
Human-facing Markdown should link to local canonical files whenever possible.
```

### Machine JSON Links

Use JSON links for:

- card-to-source refs,
- card-to-card relations,
- card-to-handoff target,
- source-to-selector backlinks,
- tag-to-card lookup,
- validation traceability.

Rule:

```text
Machine links are the canonical Inventory index. Markdown links are readable projections.
```

## Required Link Fields

### Evidence Card

Required:

```json
{
  "card_id": "card-id",
  "source_refs": [
    {
      "path": "path/to/source.md",
      "selector": "# Heading",
      "line_start": null,
      "line_end": null
    }
  ],
  "tags": [],
  "links": []
}
```

### Link Row

Required:

```json
{
  "from": "card-id-or-record-id",
  "edge": "cites",
  "to": "path-or-card-id",
  "evidence": "source_ref | inference | synthesis | open_question",
  "authority": "inventory-read-model",
  "non_authority_notice": "Required when edge could be mistaken for ontology, definition, lifecycle, or runtime authority."
}
```

### Markdown Record Frontmatter

Required:

```yaml
---
id: inventory-record-id
recordType: source-summary | coverage | synthesis | handoff | gap
sourceClass: canonical | submodule | research | project-local | generated | runtime | candidate
authorityOwner: inventory | root-governance | arcanum | domainspec-implementation | unknown
tags: []
sourceRefs: []
updatedAt: 2026-06-05
---
```

## Edge Vocabulary

Use this initial controlled set:

| Edge | From | To | Use |
| --- | --- | --- | --- |
| `cites` | card/record | source selector | source evidence |
| `summarizes` | record | card/source | generated human summary |
| `indexes` | index row | card/source/record | lookup membership |
| `derived-from` | generated artifact | source/card | generated provenance |
| `excludes` | retrieval/coverage | source/card | intentional omission |
| `duplicates-risk` | source/card | source/card | duplicate inventory risk |
| `conflicts-with` | source/card | source/card | authority or claim conflict |
| `hands-off-to` | card/gap | owner/capability | downstream route |
| `validates` | validation row | card/index | validation coverage |

Do not add semantic edges such as `part-of`, `causes`, `is-a`, or
`depends-on` until Ontology Vault or Definitions Governance owns the vocabulary.

## Link Validation Rules

1. Every `source_ref.path` must exist unless explicitly marked external.
2. Every internal card link must point to an existing `card_id`.
3. Every edge must be in the controlled vocabulary.
4. Every `conflicts-with`, `duplicates-risk`, or `hands-off-to` link must have
   a gap/risk row or downstream route.
5. Every relation-like link must include non-authority language.
6. Markdown links must use local canonical paths where available.
7. Generated backlink files must be derived from `link-index.json`, not edited
   manually.

## Interface Display Rule

When showing a lookup result, display:

1. selected cards,
2. why selected,
3. source selectors,
4. excluded nearby cards,
5. unresolved gaps,
6. next owner if the answer requires promotion or decision.

This keeps the interface useful without pretending Inventory is a canonical
ontology or definition system.
