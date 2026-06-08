---
constitution_id: framework.markdown-linking
title: Markdown Linking Constitution
status: candidate
owner: Constitution Governance
authority_level: candidate
updated_at: 2026-06-07
artifact_id: framework.markdown-linking.constitution
artifact_type: constitution
intent: Govern Markdown navigability, local link hygiene, and relation-like edge declarations.
constitution_selectors:
  - framework.artifact
  - framework.artifact-metadata
  - framework.markdown-linking
validation_profile:
  - markdown-linking
  - artifact-constitution
---

# Markdown Linking Constitution

## Purpose

Markdown artifacts should be traversable without rediscovering their context.
This constitution governs local links, source references, relationship
descriptions, and edge-like claims in Markdown source and durable evidence.

It adapts the useful DomainSpec pattern of frontmatter edges plus body
relationship tables, while keeping Arcanum authority boundaries separate from
DomainSpec implementation authority.

## Scope

Applies to:

- new or materially changed governed Markdown source artifacts,
- task packs, work-packs, handoffs, constitution packs, validation reports,
  architecture notes, design notes, and capability docs,
- Markdown records that cite source evidence, summarize other artifacts, name
  dependencies, route handoffs, or describe relationships between artifacts,
- generated Markdown only when promoted to durable evidence.

Does not apply to:

- vendored third-party Markdown,
- transient generated output that is not promoted,
- tiny local scratch notes that are not source, durable evidence, or validation
  input,
- legacy Markdown until touched by a scoped migration task.

## Selection Predicates

Use this constitution when:

- a Markdown artifact is created or materially revised,
- a task asks whether docs are navigable, linked, traceable, or graph-ready,
- a Markdown artifact names source evidence, dependencies, handoffs, ownership,
  supersession, validation, exclusions, conflicts, or related artifacts,
- a validator or context pack needs to distinguish human links from typed
  relation claims.

Do not load this constitution when:

- the task only edits non-Markdown source code,
- the Markdown artifact is known generated runtime state,
- Context Builder only needs one cited excerpt and no relationship discipline is
  being evaluated.

## Core Terms

| Term | Meaning |
| --- | --- |
| Human link | A normal Markdown link that helps a reader navigate to a file, heading, source, or next action. |
| Source reference | A link that supports a claim, summary, fixture, or generated record with evidence. |
| Relation-like claim | A statement that one artifact governs, derives from, supersedes, validates, blocks, depends on, hands off to, conflicts with, or excludes another artifact. |
| Typed edge | A relation-like claim expressed with a controlled edge label and enough context to audit direction and authority. |
| Non-authority notice | A short statement that a relation is a candidate/read-model/projection when it could be mistaken for canonical ontology, definition, lifecycle, or runtime authority. |

## Rules

| Rule ID | Rule | Validation Mode | Validator | Status |
| --- | --- | --- | --- | --- |
| `markdown.linking.local-links-resolve` | Local Markdown links in governed Markdown must resolve to existing files, and same-file anchors must point to headings when anchor checking is enabled. | deterministic | `tools/check_markdown_links.sh <file>` | candidate |
| `markdown.linking.entrypoint-required` | Governed Markdown longer than a tiny note should include an entrypoint path: a source, parent, related doc, next route, or validation command that lets a reader continue. | hybrid | future Markdown linking profile plus review | candidate |
| `markdown.linking.source-claims-cite` | Claims that summarize, derive from, or validate another artifact should include a source reference or explicit evidence gap. | hybrid | future Markdown linking profile plus review | candidate |
| `markdown.linking.relation-claims-typed` | Relation-like claims should use a controlled edge label instead of prose-only relationship language when the relation affects execution, validation, authority, or retrieval. | review | Constitution Governance review until an edge adapter exists | candidate |
| `markdown.linking.edge-direction-visible` | Typed edges must make direction visible: source artifact, edge label, target artifact, and a short reason or evidence note. | review | future edge-table adapter | candidate |
| `markdown.linking.non-authority-boundary` | Relation-like projections that are not canonical authority must say so, especially Inventory, research, context, and generated read models. | hybrid | future edge adapter plus review | candidate |
| `markdown.linking.no-broken-handoff` | Handoff, next-route, validation, and task dependency links must resolve or be marked blocked/deferred with a concrete reason. | hybrid | link checker plus review | candidate |

## Recommended Edge Vocabulary

Use narrow local vocabularies when a capability already owns one. When no
narrower vocabulary exists, use this candidate fallback:

| Edge | Use |
| --- | --- |
| `cites` | source evidence or supporting reference |
| `summarizes` | generated or human summary of another artifact |
| `derived-from` | generated provenance or adaptation from a source artifact |
| `governs` | constitution or policy authority over an artifact or rule |
| `validates` | validation report, fixture, or script covers an artifact |
| `supersedes` | artifact replaces an earlier artifact |
| `depends-on` | execution or interpretation requires another artifact |
| `blocks` | unresolved condition prevents progress |
| `hands-off-to` | next owner, capability, or task-session route |
| `conflicts-with` | authority, claim, or design conflict |
| `excludes` | intentional omission from a scope, retrieval set, or coverage map |

Do not use semantic ontology edges such as `is-a`, `part-of`, or `causes`
unless Ontology Vault or Definitions Governance owns the vocabulary for the
target scope.

## Accepted Relationship Shapes

### Related Docs

Use when a Markdown artifact only needs human navigation:

```markdown
## Related Docs

- [Artifact Constitution](ARTIFACT-CONSTITUTION.md)
```

### Connections

Use when a Markdown artifact carries edge-like relations:

```markdown
## Connections

| Target | Edge | Reason |
| --- | --- | --- |
| [Artifact Constitution](ARTIFACT-CONSTITUTION.md) | governs | Defines artifact classes and validation obligations. |
```

### Source References

Use when a claim depends on source evidence:

```markdown
## Source References

- [Inventory Linking Discipline](../arcana/inventory/development/LINKING-DISCIPLINE.md) - adapted as candidate evidence, not framework authority.
```

## Examples

Preferred:

- a work-pack task links to its parent work-pack, selected context pack,
  validation command, and downstream route,
- a constitution includes `Related Constitutions` or `Connections` rows for
  broader and narrower rule packs,
- an Inventory-generated read model uses `derived-from` or `summarizes` plus a
  non-authority notice,
- a validation report links to the artifact it validates and the validator that
  produced the result.

Allowed during migration:

- a legacy Markdown file can remain unlinked until it is materially revised,
- a brief changelog or stub can link only to its parent artifact,
- relation-like claims may stay prose-only when no controlled vocabulary exists,
  but the document should flag the vocabulary gap.

## Non-Examples

- A handoff names a target task but provides no path or next route.
- A Markdown summary says it is "based on prior research" without citing the
  research artifact or declaring an evidence gap.
- A generated read model declares an ontology relation without a
  non-authority notice or Ontology Vault promotion path.
- A task dependency points to a deleted file without a blocked/deferred reason.

## Composition

Precedence:

1. task-specific constitution pack,
2. capability-specific linking or index discipline,
3. artifact-type constitution,
4. this framework Markdown Linking Constitution,
5. repository-wide defaults.

Conflicts:

- narrower capability vocabularies override the fallback edge vocabulary for
  their own artifacts,
- if a document's link text implies authority but its metadata says candidate or
  generated, report `flag` and require review,
- if a deterministic link check passes but relation authority is unclear, report
  `flag`, not `pass`.

## Validation

For a targeted Markdown file:

```bash
bash tools/check_markdown_links.sh path/to/file.md
```

For the constitution itself:

```bash
bash tools/check_markdown_links.sh framework/MARKDOWN-LINKING-CONSTITUTION.md
tools/validate-artifact-constitution.sh
```

Current deterministic coverage checks local Markdown link targets. Edge
vocabulary, source-reference adequacy, and non-authority notices are candidate
review or future adapter checks until a Markdown linking profile is implemented.

## Promotion Boundary

Required before canonical status:

- validator coverage for local links has passing and failing fixtures,
- at least one task pack or capability adopts `Related Docs`, `Connections`, or
  `Source References` consistently,
- edge vocabulary adapter is designed or explicitly scoped out,
- legacy migration policy decides whether existing Markdown is warn-only,
  backfilled, or out of scope,
- Constitution Governance verifies that this constitution composes cleanly with
  Inventory, Ontology Vault, Definitions Governance, and artifact metadata.

## Maintenance

Split trigger:

- split link resolution, source references, and typed edge vocabulary into
  separate constitutions if the validator surface becomes too large.

Retirement trigger:

- retire only if a repository-wide typed document registry provides equivalent
  link resolution, relation typing, source reference, and authority-boundary
  guarantees.

## Related Constitutions

- [Artifact Constitution](ARTIFACT-CONSTITUTION.md) governs artifact classes and
  validation obligations.
- [Artifact Metadata Constitution](ARTIFACT-METADATA-CONSTITUTION.md) governs
  selectors and validation profiles for governed artifacts.
- [Schema Constitution](SCHEMA-CONSTITUTION.md) governs canonical
  machine-readable schema artifacts.

## Source References

- [Inventory Linking Discipline](../arcana/inventory/development/LINKING-DISCIPLINE.md) provides candidate Inventory-specific link, source reference, and edge vocabulary evidence.
- [Inventory Validator Task](../arcana/inventory/development/work-pack/tasks/TASK-INT-004-validator.md) records a narrower future validator path for Inventory links and indexes.
