---
module: inventory-domainspec-core
version: 0.1.0
status: draft
updatedAt: 2026-06-05
docType: research-strategy
dispatch: DOMAIN-SPEC-CORE-TAGGING-INDEXING-DISPATCH.json
---

# Research Strategy: DomainSpec-Core Tagging And Indexing

## Purpose

Create a governed research route for inventorizing the whole
`/home/vrondelli/projects/domainspec-core` repository in a tagging and indexing
sense.

The goal is not to summarize every file. The goal is to build a reusable
Inventory map that lets future agents find the right source selectors, know
which zone owns which authority, and decide where focused inventory slices
should be created next.

## Target Repository

Repository root:

```text
/home/vrondelli/projects/domainspec-core
```

Known high-level zones from the current tree scan:

| Zone | Initial Role | Inventory Treatment |
| --- | --- | --- |
| `arcanum/` | Arcanum source and development system | Reuse whole-Arcanum Inventory method; do not duplicate existing cards. |
| `sigils-library/` | canonical or library-style sigil surface | Compare against `arcanum/arcana`, `arcanum/formulae`, and `arcanum/transmutations` before tagging authority. |
| `implementation/` | implementation projects | Tag by product/project, runtime surface, docs, validation, and generated state boundaries. |
| `domainspec-lean-formalization/` | Lean/formalization research corpus | Treat as research/formal-method source with its own evidence and theorem/prose split. |
| `cyberAlchemy/` | concept, ontology, presentation, and agentic-system artifacts | Treat as candidate knowledge source; respect ontology/definition promotion boundaries. |
| `docs/` | shared documentation and feature docs | Use as navigation and current product documentation evidence. |
| `research/` | research corpus and registries | Tag by project/research lane and source status. |
| `projects/` | project-local work areas | Tag by project and current artifact shape before ingestion. |
| `ops/` | operational policy and organization guidance | Treat as repository-governance evidence. |
| `tools/`, `validation/` | executable checks and validation projects | Tag as validation/runtime evidence; avoid promoting generated outputs. |
| `.arcanum/`, `.codex/`, `.agents/`, `.data/`, `.planning/` | local/runtime/planning state | Exclude by default unless a durable source artifact explicitly promotes the state. |

## Research Question

What source context does an agent need before doing repository-wide tagging and
indexing work in `domainspec-core` without flattening authority boundaries or
duplicating existing inventories?

## Strategy

Use a dispatch-backed fanout research pass followed by parent synthesis and a
human approval gate.

The research pass should produce:

- a repository zone map,
- a source inclusion/exclusion policy,
- a tag taxonomy proposal,
- an indexing shape proposal,
- duplicate inventory and authority-conflict findings,
- a prioritized slice backlog,
- an execution handoff for Inventory ingest/backfill work.

## Lanes

### Lane 1: Repository Zone And Authority Map

Scope:

- top-level folders,
- nested repository or submodule boundaries,
- source/runtime/generated/private-state classification,
- existing canonical-vs-install-snapshot relationships.

Output:

```text
arcana/inventory/development/domainspec-core/ZONE-AUTHORITY-MAP.md
```

Acceptance:

- every top-level zone has a role,
- generated/local-state zones are explicitly excluded or quarantined,
- uncertain authority is marked as residue, not resolved by assumption.

### Lane 2: Existing Knowledge And Inventory Surface Audit

Scope:

- `.arcanum/inventory`,
- Arcanum Inventory development package,
- docs indexes,
- registries,
- project READMEs,
- glossary/ontology files,
- prior work-packs and task-session results.

Output:

```text
arcana/inventory/development/domainspec-core/EXISTING-KNOWLEDGE-SURFACES.md
```

Acceptance:

- reusable surfaces are listed before new inventory work is proposed,
- duplicate inventory risk is flagged,
- surfaces are classified as canonical source, generated inventory, runtime
  state, or proposal evidence.

### Lane 3: Tag Taxonomy Proposal

Scope:

- stable tag families,
- zone tags,
- artifact-role tags,
- authority tags,
- lifecycle/status tags,
- source-quality tags,
- downstream handoff tags.

Output:

```text
arcana/inventory/development/domainspec-core/TAG-TAXONOMY.md
```

Initial required tag families:

- `zone:<name>`
- `artifact:<role>`
- `authority:<owner>`
- `status:<state>`
- `source:<class>`
- `domain:<topic>`
- `handoff:<target>`
- `risk:<risk-kind>`

Acceptance:

- tags support lookup and routing, not decoration,
- tags do not encode canonical meaning owned by Ontology Vault or Definitions
  Governance,
- tag count is bounded and deduplicated.

### Lane 4: Indexing Shape Proposal

Scope:

- repository-level index,
- zone-level indexes,
- slice indexes,
- evidence-card indexes,
- query/retrieval fixtures.

Output:

```text
arcana/inventory/development/domainspec-core/INDEXING-SHAPE.md
```

Acceptance:

- index entries point to source selectors or generated Inventory pages,
- index supports task-shaped lookup,
- broad whole-folder summaries are rejected unless the folder itself is the
  source artifact.

### Lane 5: Pilot Slice Selection

Scope:

- candidate slices from Arcanum, sigils-library, implementation/domainspec,
  cyberAlchemy, Lean formalization, and ops/tooling,
- expected retrieval questions,
- source anchors,
- validation route.

Output:

```text
arcana/inventory/development/domainspec-core/PILOT-SLICE-BACKLOG.md
```

Acceptance:

- each candidate slice has a retrieval question,
- each slice has 2-7 initial source anchors,
- each slice states why it is worth inventorizing before broad repo coverage.

## Minimum Research Artifacts

The strategy is not complete until these artifacts exist:

```text
arcana/inventory/development/domainspec-core/
  DOMAIN-SPEC-CORE-TAGGING-INDEXING-DISPATCH.json
  REPOSITORY-TAGGING-INDEXING-RESEARCH-STRATEGY.md
  ZONE-AUTHORITY-MAP.md
  EXISTING-KNOWLEDGE-SURFACES.md
  TAG-TAXONOMY.md
  INDEXING-SHAPE.md
  PILOT-SLICE-BACKLOG.md
  RESEARCH-SYNTHESIS.md
```

## Dispatch Route

Use:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py \
  arcana/inventory/development/domainspec-core/DOMAIN-SPEC-CORE-TAGGING-INDEXING-DISPATCH.json
```

The dispatch recommends subagents but does not execute them. Runtime execution
needs explicit operator approval.

## Promotion Guardrails

- Inventory may own evidence cards, source indexes, tag indexes, lookup
  fixtures, gaps, and handoff projections.
- Inventory must not promote ontology relations, canonical definitions, sigil
  lifecycle status, spell lifecycle status, or repository deletion decisions.
- Generated state remains excluded unless promoted by a durable owner artifact.
- If Arcanum and `sigils-library` both claim source authority for the same
  capability, block and route to a decision gate.
- If a tag starts to behave like canonical vocabulary, route to Definitions
  Governance before making it durable.

## First Execution Recommendation

Run the fanout research route first, not Inventory ingestion.

Recommended first approved execution:

```text
dispatch: domainspec-core-tagging-indexing-20260605
mode: research
route: repository zone map -> knowledge surface audit -> tag taxonomy -> indexing shape -> pilot slice backlog -> synthesis -> decision gate
```

After synthesis, use a decision gate to choose the first pilot slice. The likely
first slice should be either:

1. `sigils-library` vs `arcanum` authority comparison,
2. `implementation/domainspec` repo-local Arcanum install/indexing surface,
3. `cyberAlchemy` candidate knowledge-to-inventory pipeline.
