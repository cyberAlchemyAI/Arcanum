---
module: inventory-domainspec-core
version: 0.1.0
status: draft
updatedAt: 2026-06-05
docType: research-lane-output
lane: tag-taxonomy
dispatch: domainspec-core-tagging-indexing-20260605
---

# Tag Taxonomy

## Purpose

Define a bounded tag vocabulary for repository-wide Inventory lookup in
`domainspec-core`.

Tags are retrieval aids. They are not canonical definitions, ontology relations,
or lifecycle promotion markers.

## Tag Rules

1. Every inventory entry should have at least one `zone:*` tag.
2. Every source-backed entry should have one `source:*` tag.
3. Authority-sensitive entries should have one `authority:*` tag.
4. Tags must answer lookup/routing questions. Avoid decorative synonyms.
5. Do not create a new tag when an existing tag family can represent the need.
6. If a tag starts defining canonical meaning, route to Definitions Governance.

## Required Tag Families

### Zone Tags

Pattern:

```text
zone:<zone-id>
```

Initial values:

| Tag | Use |
| --- | --- |
| `zone:root` | root docs, root policy, root repo state |
| `zone:ops` | repository governance and asset ownership |
| `zone:research` | root research project system |
| `zone:implementation-domainspec` | DomainSpec implementation submodule |
| `zone:validation-poker-team` | validation harness submodule |
| `zone:arcanum` | Arcanum submodule |
| `zone:sigils-library` | sigils-library capability source/candidate |
| `zone:lean-formalization` | DomainSpec theorem/formalization repo |
| `zone:cyberalchemy` | CyberAlchemy product/ontology workspace |
| `zone:projects` | project-local workspaces |
| `zone:tools` | root scripts and validation tooling |
| `zone:runtime-state` | local/generated runtime state |

### Artifact Role Tags

Pattern:

```text
artifact:<role>
```

Initial values:

| Tag | Use |
| --- | --- |
| `artifact:readme` | orientation documents |
| `artifact:registry` | registry/index documents |
| `artifact:glossary` | glossary or term surfaces |
| `artifact:ontology` | ontology/candidate ontology surfaces |
| `artifact:policy` | governance/policy docs |
| `artifact:plan` | plans, roadmaps, work-packs |
| `artifact:source-code` | executable code source |
| `artifact:script` | command/tool scripts |
| `artifact:validation` | validators, checks, fixtures |
| `artifact:inventory` | existing inventory-like surfaces |
| `artifact:evidence` | evidence/result surfaces |
| `artifact:runtime-state` | generated runtime state |
| `artifact:navigation` | workspace or operator navigation |

### Authority Tags

Pattern:

```text
authority:<owner>
```

Initial values:

| Tag | Use |
| --- | --- |
| `authority:root-governance` | root repo policy and organization |
| `authority:domainspec-implementation` | DomainSpec implementation framework source |
| `authority:research-project` | project-local research contracts |
| `authority:validation-harness` | poker-team validation evidence |
| `authority:arcanum` | Arcanum framework/capability source |
| `authority:sigils-library` | sigils-library claimed capability source |
| `authority:cyberalchemy-candidate` | CyberAlchemy candidate system/ontology material |
| `authority:inventory` | Inventory-owned generated evidence/index/read models |
| `authority:ontology-vault` | ontology promotion owner |
| `authority:definitions-governance` | canonical definition owner |
| `authority:unknown` | unresolved or conflicting owner |

### Status Tags

Pattern:

```text
status:<state>
```

Initial values:

| Tag | Use |
| --- | --- |
| `status:active` | currently active source or project |
| `status:planning` | planning-stage artifact |
| `status:candidate` | candidate knowledge or proposal |
| `status:draft` | draft strategy or design |
| `status:generated` | generated output/state |
| `status:deprecated` | legacy/deprecated surface |
| `status:unknown` | status unclear from source |
| `status:blocked` | blocked pending decision |

### Source Class Tags

Pattern:

```text
source:<class>
```

Initial values:

| Tag | Use |
| --- | --- |
| `source:canonical` | direct source-of-truth document or code |
| `source:submodule` | nested Git/submodule source |
| `source:research` | research project source |
| `source:project-local` | local project source |
| `source:generated` | generated artifact |
| `source:runtime` | local runtime/session state |
| `source:navigation` | navigation/helper surface |
| `source:candidate` | proposal/candidate knowledge |

### Domain Tags

Pattern:

```text
domain:<topic>
```

Initial values:

| Tag | Use |
| --- | --- |
| `domain:domainspec` | DomainSpec framework/product work |
| `domain:meta-meta` | meta-meta framework research |
| `domain:mars` | MARS research orchestration |
| `domain:arcanum` | Arcanum capability method |
| `domain:cyberalchemy` | CyberAlchemy product/system knowledge |
| `domain:formalization` | Lean/math formalization |
| `domain:validation` | validation harness/case study |
| `domain:agentic-systems` | agent coordination/governance |
| `domain:repository-governance` | repo structure/policy |
| `domain:automation-assets` | agents/skills/copilot assets |

### Handoff Tags

Pattern:

```text
handoff:<target>
```

Initial values:

| Tag | Use |
| --- | --- |
| `handoff:inventory` | Inventory follow-up |
| `handoff:context-builder` | selector/context pack needed |
| `handoff:task-session` | bounded execution work |
| `handoff:decision-gate` | authority or route decision |
| `handoff:ontology-vault` | relation/meaning promotion |
| `handoff:definitions-governance` | canonical definition work |
| `handoff:sigil-development` | sigil lifecycle work |
| `handoff:spellcraft` | spell lifecycle work |
| `handoff:repository-governance` | repo moves/deletions/ownership |

### Risk Tags

Pattern:

```text
risk:<risk-kind>
```

Initial values:

| Tag | Use |
| --- | --- |
| `risk:authority-conflict` | multiple surfaces claim same authority |
| `risk:duplicate-inventory` | existing inventory/index could be duplicated |
| `risk:generated-state` | generated/runtime state might be mistaken for source |
| `risk:path-drift` | canonical path and current path differ |
| `risk:tag-sprawl` | too many or overlapping tags |
| `risk:definition-promotion` | tag/term needs Definitions Governance |
| `risk:ontology-promotion` | relation/meaning needs Ontology Vault |
| `risk:submodule-boundary` | nested Git ownership applies |

## Entry Tag Profiles

### Repository Zone Entry

Required:

- `zone:<zone-id>`
- `artifact:navigation` or `artifact:policy`
- `source:canonical` or `source:submodule`
- `authority:<owner>`

Optional:

- `risk:<risk-kind>`
- `handoff:<target>`

### Existing Knowledge Surface Entry

Required:

- `zone:<zone-id>`
- `artifact:registry`, `artifact:glossary`, `artifact:inventory`, or
  `artifact:ontology`
- `source:<class>`
- `authority:<owner>`

Optional:

- `status:<state>`
- `risk:duplicate-inventory`

### Pilot Slice Entry

Required:

- `zone:<zone-id>`
- `domain:<topic>`
- `source:<class>`
- `handoff:task-session`

Optional:

- `risk:<risk-kind>`
- `authority:<owner>`

## Rejected Tag Shapes

Do not use:

- author/person tags unless ownership lookup explicitly requires them,
- one-off file-name tags,
- broad tags such as `important`, `todo`, or `misc`,
- ontology relation tags such as `depends-on` or `part-of` unless owned by a
  downstream relation model,
- status tags that imply lifecycle promotion without owner evidence.

## Residue

- `authority:sigils-library` and `authority:arcanum` should remain separate
  until source authority is decided.
- Root `docs/glossary.md` and implementation `docs/glossary.md` are different
  surfaces; do not merge their terms with one tag-only rule.
- Some existing project indexes may already have their own vocabulary. Parent
  tags should wrap them for lookup without rewriting local semantics.
