---
name: inventory
description: "Use when: installing or maintaining a repository-local compiled knowledge inventory that lets agents ingest once, index, tag, query, lint, and reuse context across sigils."
argument-hint: "<install|ingest|lookup|query|lint|validate|backfill|sync> [--path <repo-root>] [--root <inventory-root>] [--source <path>] [--type <entry-type>] [--query <text>] [--dry-run]"
tier: arcana
domain: knowledge-inventory
version: 0.1.0
origin: generalized from recurring inventory and compiled-wiki maintenance practice
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions, Task
---

# Sigil: Inventory

<objective>
Install and maintain a repository-local compiled knowledge layer that keeps raw sources immutable, generated inventory pages current, and reusable context available to other sigils.
</objective>

<logic-type>
Arcana: long-lived knowledge maintenance, local schema governance, ingestion, linting, and cross-sigil integration.
</logic-type>

<core-promise>
Inventorize once, reuse many times.
</core-promise>

<modes>
- `install`: create or adapt the local inventory package.
- `ingest`: process raw sources into generated inventory pages and optional source-backed evidence-cards.
- `lookup`: return matching entries, evidence-cards, candidate EvidenceSets, source refs, selectors, exclusions, and gaps for another sigil.
- `query`: answer from inventory pages and optionally file the answer as a synthesis page.
- `lint`: health-check contradictions, staleness, orphans, missing links, tags, source coverage, human and machine index freshness, evidence-card fields, EvidenceSet references, owner/status pairs, trace, residue, and non-authority handoff language.
- `validate`: check package structure, `index.md` and `index.json` coverage, machine index parseability, log parseability, tag consistency, evidence links, evidence-card schema fields, EvidenceSet references, and downstream packet boundaries.
- `backfill`: build inventory entries from existing repository artifacts.
- `sync`: update inventory files after schema or convention changes.
</modes>

<default-package>
Use `.arcanum/inventory/` unless the user chooses an existing docs, wiki, or knowledge-base location.

Default layout:

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
</default-package>

<install-process>
1. Detect existing repository knowledge systems before asking questions:
   - docs folders,
   - wiki or notes folders,
   - architecture packages,
   - existing indexes,
   - generated context packs,
   - decision records,
   - observability packages.
2. Ask only unanswered setup questions:
   - inventory root path,
   - raw source location,
   - generated wiki or entry location,
   - whether existing docs should be adopted or left separate,
   - tagging style,
   - frontmatter preference,
   - wiki-link preference,
   - machine index policy, defaulting to `index.json` as the primary machine view,
   - optional CSV projection policy for flat exports,
   - source immutability policy,
   - observability integration preference.
3. Create or adapt the inventory package from templates.
4. Record the local schema and selected conventions.
5. Append an install entry to the log.
6. Return the package path, selected conventions, and next recommended ingest.
</install-process>

<ingest-process>
1. Resolve source path or source set.
2. Confirm raw sources are read-only inputs.
3. Read each source and extract reusable knowledge:
   - source summary,
   - entities,
   - concepts,
   - decisions,
   - workflows,
   - architecture layers,
   - implementation patterns,
   - interfaces,
   - dependency rules,
   - test patterns,
   - observability signals,
   - contradictions,
   - open questions.
4. When the source detail needs selector-level reuse, draft an `evidence-card` with `source_refs`, authority level, captured metadata, `promotion_owner`, and optional `trace` or `residue`.
5. Create or update generated inventory pages.
6. Link related entries and update backlinks when the local schema uses them.
7. Flag contradictions and stale claims instead of silently overwriting them.
8. Update `index.md`, `index.json`, `tags.md`, and `log.md`.
9. Update optional `indexes/*.json` and CSV projections when the local schema enables them.
10. Emit observability signals when the observability package exists.
</ingest-process>

<lookup-process>
1. Read `index.json` first when present for machine lookup; fall back to `index.md` only when no machine view exists, and report that fallback as a validation gap.
2. Read `index.md` for human orientation, summaries, and nearby gaps.
3. Search entries by type, tag, source, title, summary, selector, status, and query text.
4. Include matching evidence-cards when they provide better selector-level evidence than a broad page.
5. Include candidate EvidenceSets when a stable group of card IDs answers the task faster than independent card matches.
6. Return selector-level matches suitable for downstream sigils.
7. Include why each match is relevant and which task or obligation it can satisfy.
8. Include excluded matches when they clarify why nearby evidence was not selected.
9. Report gaps when inventory does not cover the requested topic.
</lookup-process>

<query-process>
1. Resolve the question and search the inventory machine index first when available.
2. Read relevant generated pages and their source references.
3. Synthesize an answer with citations to inventory pages and raw source references when available.
4. Ask whether the answer should be filed as a synthesis page when it has durable value.
5. If filed, update `index.md`, `index.json`, tags, and log.
</query-process>

<lint-process>
Check for:

- contradictions between pages,
- stale claims superseded by newer sources,
- orphan pages with no incoming or outgoing links,
- important concepts mentioned but lacking pages,
- missing cross-references,
- untagged pages,
- invalid frontmatter when frontmatter is enabled,
- raw sources not yet inventoried,
- generated pages without source coverage,
- log entries that do not match the configured heading pattern,
- missing, stale, or unparsable `index.json`,
- machine index rows that lack source path, projection source, freshness, validation boundary, or residue fields when required by the local schema,
- CSV projections that do not declare their `index.json` source or are treated as authoritative,
- evidence-cards missing `source_refs`,
- evidence-cards with unknown controlled vocabulary values,
- EvidenceSets with unknown controlled vocabulary values,
- EvidenceSets that reference missing evidence-card IDs,
- EvidenceSets that duplicate evidence-card source excerpts or summaries,
- full evidence-cards missing `trace`,
- terminal promotion status with `promotion_owner: none`,
- relation candidates missing a non-authority notice,
- unresolved `residue` that should be surfaced in lookup or validation output.
</lint-process>

<machine-index-contract>
`index.md` is the human-readable catalog. `index.json` is the primary machine-readable catalog.

The machine index must be JSON, parse with `jq`, and preserve enough structure for downstream sigils to filter without reparsing Markdown. Repositories may add CSV projections for spreadsheets or shell pipelines, but CSV projections are secondary read models whose source must be `index.json`.

Minimum `index.json` shape:

```json
{
  "schema_version": "inventory.index.v0.1",
  "inventory_root": ".arcanum/inventory",
  "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "human_index": "index.md",
  "entries": [
    {
      "id": "stable-entry-id",
      "path": "entries/example.md",
      "kind": "page | entry | query | lint | raw-manifest | evidence-card-bundle | evidence-set-bundle",
      "type": "concept",
      "title": "Entry title",
      "summary": "Short reusable summary.",
      "tags": ["inventory"],
      "sources": ["source/path.md#selector"],
      "updated": "YYYY-MM-DD",
      "status": "candidate",
      "confidence": "high | medium | low",
      "selectors": [],
      "evidence_card_ids": [],
      "evidence_set_ids": [],
      "residue": []
    }
  ],
  "indexes": {
    "by_id": {},
    "by_type": {},
    "by_tag": {},
    "by_source": {},
    "by_status": {},
    "by_evidence_card": {},
    "by_evidence_set": {}
  },
  "projections": [
    {
      "path": "projections/index.csv",
      "format": "csv",
      "source": "index.json",
      "purpose": "flat table export",
      "freshness": "generated-from-current-index"
    }
  ],
  "validation": {
    "parseable": true,
    "source_coverage": "complete | partial | unknown",
    "validation_boundary": "inventory-read-model-only"
  }
}
```

Optional indexes under `indexes/*.json` may specialize selector, link, backlink, tag, traceability, query-pattern, gap/risk, or projection lookup. They must declare their source index and remain Inventory read models, not Ontology Vault relations or Definitions Governance authority.
</machine-index-contract>

<evidence-card-contract>
Evidence-cards are source-backed Inventory records. They may capture candidate claims, concepts, methods, questions, relation candidates, contradictions, and operational lessons.

Required authoring behavior:

- every material claim points to `source_refs` or is explicitly marked as inference, synthesis, or open question,
- `trace` records field-level extraction or assignment decisions for full cards,
- `residue` preserves schema or instance ambiguity instead of hiding it,
- `promotion_owner` records who owns terminal promotion decisions,
- downstream packets include non-authority language and do not imply ontology or definition promotion,
- `governed_ref` appears only after the downstream owner creates a real governed artifact.
</evidence-card-contract>

<evidence-set-contract>
EvidenceSets are candidate Inventory records that group evidence-card IDs for repeated retrieval and handoff assembly.

Required authoring behavior:

- reference evidence-card IDs instead of copying card content,
- include `card_refs` with inclusion reasons,
- include `excluded_card_refs` with boundary reasons,
- include `index_terms` for shell plus `jq` lookup,
- include `handoff_target`, `synthesis_note`, and `residue`,
- keep `status` candidate-level unless a later explicit promotion decision exists,
- do not imply ontology, definition, ledger, or Context Builder authority.
</evidence-set-contract>

<entry-types>
Default entry types:

- `source`,
- `entity`,
- `concept`,
- `architecture-layer`,
- `implementation-pattern`,
- `decision`,
- `capability`,
- `workflow`,
- `interface`,
- `dependency-rule`,
- `test-pattern`,
- `observability-signal`,
- `question`,
- `contradiction`,
- `synthesis`.

Repositories may add custom entry types in `schema.md` when they define required fields, evidence rules, tag rules, and update behavior.
</entry-types>

<integration-contract>
For `context-builder`, lookup output should include:

- machine index entry ID when available,
- inventory page path,
- evidence-card ID when available,
- selector or heading,
- summary,
- tags,
- confidence,
- source references,
- task obligation fit,
- excluded matches when useful,
- unresolved gaps.

For `architecture-pattern-inventory`, inventory output should support entries for:

- architecture layers,
- implementation patterns,
- dependency rules,
- test patterns,
- observability signals,
- relationship notes.
</integration-contract>

<authority-rule>
Raw sources are read-only inputs. Generated inventory pages may evolve, but every material claim should point back to source evidence or be marked as inference, synthesis, or open question.

Inventory owns evidence-cards, indexes, lint findings, and handoff projections. Ontology Vault owns governed meaning, relations, confidence, and promotion. Definitions Governance owns canonical definitions. Evidence-card handoff packets are non-authority read models until a downstream owner accepts them.
</authority-rule>

<observability>
When `.arcanum/observability/` exists, emit post-run signals for:

- mode,
- install decisions,
- source count,
- entries created,
- entries updated,
- contradictions found,
- lint gaps,
- validation result,
- downstream sigil lookups,
- filed query syntheses.
</observability>

<quality-bar>
A successful execution must:

- preserve raw source immutability,
- create or respect a local schema,
- maintain `index.md`, `index.json`, and `log.md`,
- tag generated pages consistently,
- link generated knowledge to source evidence,
- expose a parseable machine index before claiming lookup readiness,
- flag contradictions instead of hiding them,
- expose lookup results that other sigils can consume,
- avoid creating a competing system when a repository already has a usable wiki or inventory.
</quality-bar>

<anti-patterns>
Avoid:

- editing raw sources during ingest,
- making generated pages the sole authority for source facts,
- leaving `index.md` as the only machine lookup surface after install or sync,
- treating CSV projections as authoritative when `index.json` is missing or stale,
- dumping source summaries without updating related pages,
- creating tags ad hoc without recording them,
- answering queries from raw files while ignoring the inventory,
- overwriting contradictions instead of recording them,
- installing a new package when existing repository conventions can be adapted,
- letting inventory maintenance replace human source curation.
</anti-patterns>

<output-contract>
Return:

```markdown
## Inventory Result

- Mode: install | ingest | lookup | query | lint | validate | backfill | sync
- Repository: <path>
- Inventory root: <path>
- Files changed: <paths or none>
- Sources processed: <count>
- Entries created: <count>
- Entries updated: <count>
- Index updated: yes | no
- Machine index updated: yes | no | not applicable
- Log updated: yes | no
- Contradictions flagged: <count>
- Lint gaps: <count>
- Validation: pass | fail | not run
- Downstream lookup output: <summary or none>
- Next action: <action>
```
</output-contract>
