---
module: inventory-domainspec-core
version: 0.1.0
status: draft
updatedAt: 2026-06-05
docType: research-lane-output
lane: existing-knowledge-surface-audit
dispatch: domainspec-core-tagging-indexing-20260605
---

# Existing Knowledge Surface Audit

## Purpose

Find current indexes, registries, inventories, glossaries, ontology surfaces,
work-pack surfaces, and navigation surfaces before adding new Inventory tagging
and indexing work.

Inventory should reuse these surfaces and only create new generated indexes
where lookup value is not already covered.

## Root Surfaces

| Surface | Role | Inventory Treatment |
| --- | --- | --- |
| `/home/vrondelli/projects/domainspec-core/README.md` | root operating model and quick links | cite as root orientation |
| `/home/vrondelli/projects/domainspec-core/.gitmodules` | submodule boundary map | cite as authority for nested Git zones |
| `/home/vrondelli/projects/domainspec-core/docs/registry.md` | root concept registry template | index as placeholder/navigation; do not treat as populated concept source |
| `/home/vrondelli/projects/domainspec-core/docs/glossary.md` | root glossary template | index as placeholder; definitions not populated |
| `/home/vrondelli/projects/domainspec-core/research/registry/PROJECT-INDEX.md` | canonical research project index | cite for research project list |
| `/home/vrondelli/projects/domainspec-core/ops/ASSET-OWNERSHIP-POLICY.md` | automation asset ownership policy | cite for Type A/B/C asset boundaries |
| `/home/vrondelli/projects/domainspec-core/ops/REPOSITORY-ORGANIZATION-PLAN.md` | repository organization policy | cite for self-contained research project rule |
| `/home/vrondelli/projects/domainspec-core/tools/check_github_drift.sh` | drift enforcement script | index as validation/tooling source |
| `/home/vrondelli/projects/domainspec-core/tools/check_research_structure.sh` | research structure enforcement script | index as validation/tooling source |

## Arcanum Surfaces

| Surface | Role | Inventory Treatment |
| --- | --- | --- |
| `/home/vrondelli/projects/domainspec-core/arcanum/README.md` | Arcanum framework orientation | cite for capability model |
| `/home/vrondelli/projects/domainspec-core/arcanum/registry/` | sigil/spell/packs registry | use as navigation only unless promotion evidence is cited |
| `/home/vrondelli/projects/domainspec-core/arcanum/arcana/inventory/` | Inventory source package | source of Inventory behavior |
| `/home/vrondelli/projects/domainspec-core/arcanum/arcana/inventory/development/whole-arcanum/` | existing whole-Arcanum inventory package | reuse method/tracker; avoid duplicate card work |
| `/home/vrondelli/projects/domainspec-core/arcanum/framework/` | governance and quality framework | cite for Arcanum-specific rules |
| `/home/vrondelli/projects/domainspec-core/arcanum/.arcanum/` | local runtime/observability state | exclude unless durable source promotes it |
| `/home/vrondelli/projects/domainspec-core/arcanum/benchmark/artifacts/` | generated benchmark artifacts | exclude by default |

## DomainSpec Implementation Surfaces

| Surface | Role | Inventory Treatment |
| --- | --- | --- |
| `/home/vrondelli/projects/domainspec-core/implementation/domainspec/README.md` | DomainSpec source-of-truth orientation | cite as canonical implementation source |
| `/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/registry.md` | implementation concept registry | use for DomainSpec framework lookup |
| `/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/glossary.md` | implementation glossary | use as DomainSpec definitions surface, but do not overwrite |
| `/home/vrondelli/projects/domainspec-core/implementation/domainspec/copilot/` | canonical Type A automation pack | cite for Type A assets |
| `/home/vrondelli/projects/domainspec-core/implementation/domainspec/vault/` | implementation knowledge graph/vault | index as DomainSpec-owned knowledge surface |
| `/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/research/inventory` | existing inventory-like surface | audit before creating DomainSpec implementation inventory cards |
| `/home/vrondelli/projects/domainspec-core/implementation/domainspec/.arcanum/`, `.codex/`, `.data/`, `node_modules/` | runtime/generated state | exclude by default |

## Research Project Surfaces

Root research project index:

- `/home/vrondelli/projects/domainspec-core/research/registry/PROJECT-INDEX.md`

Detected project contract surfaces:

| Project | Contract Surfaces |
| --- | --- |
| `research/projects/domainspec` | `PROJECT.yaml`, `README.md`, `claims/CLAIMS.md`, `deps/DEPENDENCIES.yaml`, `registry/ARTIFACT-INDEX.md`, `registry/TRACEABILITY-MATRIX.md`, `inventory/` |
| `research/projects/mars` | `PROJECT.yaml`, `README.md`, `claims/CLAIMS.md`, `deps/DEPENDENCIES.yaml`, `registry/ARTIFACT-INDEX.md`, `registry/TRACEABILITY-MATRIX.md`, `inventory/` |
| `research/projects/meta-meta` | `PROJECT.yaml`, `README.md`, `claims/CLAIMS.md`, `deps/DEPENDENCIES.yaml`, `registry/ARTIFACT-INDEX.md`, `registry/TRACEABILITY-MATRIX.md`, `inventory/` |
| `research/projects/mogt-agentic-conversation` | `PROJECT.yaml`, `README.md`, `claims/CLAIMS.md`, `deps/DEPENDENCIES.yaml`, `registry/ARTIFACT-INDEX.md`, `registry/TRACEABILITY-MATRIX.md`, `inventory/` |

Treatment:

- Parent Inventory should create cross-project lookup entries.
- Project-local `inventory/` folders remain project-owned.
- Cross-project reuse should cite `deps/DEPENDENCIES.yaml` and `exports/`, not
  internal result files.

## Formalization Surfaces

| Surface | Role | Inventory Treatment |
| --- | --- | --- |
| `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/README.md` | formalization root catalog | cite for theorem repo orientation |
| `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/GLOSSARY.md` | formalization terms and milestone codes | route definition promotion separately |
| `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-formalization/` | Lean proof corpus | index by proof topic and status |
| `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/research*/` | research spines and bridges | index by research lane |
| `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/vault/` | formalization ontology/vault | do not merge with parent Inventory without owner review |

## CyberAlchemy Surfaces

| Surface | Role | Inventory Treatment |
| --- | --- | --- |
| `/home/vrondelli/projects/domainspec-core/cyberAlchemy/README.md` | candidate product/system orientation | index as candidate knowledge source |
| `/home/vrondelli/projects/domainspec-core/cyberAlchemy/agentic-system-navigation.md` | artifact navigation | index as navigation |
| `/home/vrondelli/projects/domainspec-core/cyberAlchemy/agentic-system-inventory-ontology-pipeline.md` | inventory-to-ontology pipeline | strong pilot candidate |
| `/home/vrondelli/projects/domainspec-core/cyberAlchemy/ontology/` | candidate ontology pack | route promotion to ontology owner |
| `/home/vrondelli/projects/domainspec-core/cyberAlchemy/ontology/source-digests/` | compiled source digests | useful source-backed candidate evidence |

## Project-Local Surfaces

| Zone | Existing Surfaces | Treatment |
| --- | --- | --- |
| `projects/goldenquill` | `README.md`, `docs/AGENT_CONTEXT_INDEX.md`, `docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md` | do not duplicate; parent index can point to existing project indexes |
| `projects/pos-multilevel` | `README.md`, `docs/glossary.md`, `docs/registry.md` | project-local DomainSpec-style docs |
| `projects/sonar-loop` | `README.md` | project-local source |
| `projects/whisky-doses` | `docs/PLAN.md`, `domainspec/README.md` | project-local plan and DomainSpec workspace |

## Validation Surfaces

| Surface | Role | Treatment |
| --- | --- | --- |
| `/home/vrondelli/projects/domainspec-core/validation/poker-team/README.md` | validation harness source | index as submodule source |
| `/home/vrondelli/projects/domainspec-core/validation/poker-team/docs/registry.md` | validation concept registry | Type C/project-local |
| `/home/vrondelli/projects/domainspec-core/validation/poker-team/docs/glossary.md` | validation glossary | Type C/project-local |
| `/home/vrondelli/projects/domainspec-core/validation/sigil-spell-sandbox/.sigils/inventory` | sandbox inventory | project-local sandbox; do not promote |

## Duplicate Inventory Risks

1. `research/projects/*/inventory` already exists. Parent Inventory should
   aggregate handles, not rewrite project inventories.
2. `arcanum/arcana/inventory/development/whole-arcanum` already owns
   whole-Arcanum Inventory shape.
3. `implementation/domainspec/docs/research/inventory` may overlap with
   DomainSpec implementation inventory work.
4. `cyberAlchemy/agentic-system-inventory-ontology-pipeline.md` may look like an
   Inventory spec but is candidate system design, not parent Inventory source.
5. `projects/goldenquill/docs/*INDEX.md` already provides project-specific
   memory/context indexes.

## Recommended Reuse Rule

Parent `domainspec-core` Inventory should own:

- repository zone index,
- cross-zone tag taxonomy,
- cross-zone lookup handles,
- source inclusion/exclusion policy,
- pilot slice backlog,
- handoff records to downstream owner inventories.

It should not own:

- project-local research inventories,
- DomainSpec implementation definitions,
- validation harness overlays,
- Arcanum sigil/spell promotion,
- CyberAlchemy ontology promotion.
