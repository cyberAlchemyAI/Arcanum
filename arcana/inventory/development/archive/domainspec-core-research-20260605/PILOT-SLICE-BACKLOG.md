---
module: inventory-domainspec-core
version: 0.1.0
status: draft
updatedAt: 2026-06-05
docType: research-lane-output
lane: pilot-slice-backlog
dispatch: domainspec-core-tagging-indexing-20260605
---

# Pilot Slice Backlog

## Purpose

Choose focused first slices for repository-wide tagging and indexing work.

Each slice must answer a retrieval question. Broad whole-folder summary is
blocked.

## Ranking Criteria

| Criterion | Meaning |
| --- | --- |
| retrieval value | likely to help future agents quickly select source context |
| authority risk | likely to prevent wrong source/promotion assumptions |
| duplicate risk | likely to prevent duplicated inventory/index work |
| boundedness | can be handled with 2-7 source anchors |
| validation value | exercises tags, indexing, source refs, exclusions, and handoff rules |

## Candidate Slices

### Slice 1: Arcanum vs Sigils Library Authority

Retrieval question:

```text
Which source should an agent use when deciding whether a reusable capability belongs to Arcanum, sigils-library, or both?
```

Source anchors:

- `/home/vrondelli/projects/domainspec-core/arcanum/README.md`
- `/home/vrondelli/projects/domainspec-core/arcanum/registry/SIGILS.md`
- `/home/vrondelli/projects/domainspec-core/arcanum/registry/SPELLS.md`
- `/home/vrondelli/projects/domainspec-core/sigils-library/README.md`
- `/home/vrondelli/projects/domainspec-core/sigils-library/arcana/README.md`
- `/home/vrondelli/projects/domainspec-core/sigils-library/formulae/README.md`
- `/home/vrondelli/projects/domainspec-core/sigils-library/transmutations/README.md`

Expected tags:

- `zone:arcanum`
- `zone:sigils-library`
- `artifact:registry`
- `authority:arcanum`
- `authority:sigils-library`
- `risk:authority-conflict`
- `handoff:decision-gate`

Why first:

- It addresses the highest source-authority risk for reusable capabilities.
- It directly affects Inventory's ability to tag Arcanum-related work.

Stop condition:

- Block if the slice starts deciding which source is canonical instead of
  documenting evidence and routing the conflict.

### Slice 2: Root Asset Ownership And Automation Surface

Retrieval question:

```text
Which source owns Type A, Type B, and Type C automation assets, and how should indexing avoid consumer-copy drift?
```

Source anchors:

- `/home/vrondelli/projects/domainspec-core/README.md`
- `/home/vrondelli/projects/domainspec-core/ops/ASSET-OWNERSHIP-POLICY.md`
- `/home/vrondelli/projects/domainspec-core/ops/AGENT-SKILL-TRIAGE-MATRIX.md`
- `/home/vrondelli/projects/domainspec-core/tools/check_github_drift.sh`
- `/home/vrondelli/projects/domainspec-core/.github/gsd-file-manifest.json`
- `/home/vrondelli/projects/domainspec-core/implementation/domainspec/copilot/README.md`

Expected tags:

- `zone:ops`
- `zone:implementation-domainspec`
- `zone:validation-poker-team`
- `artifact:policy`
- `domain:automation-assets`
- `authority:root-governance`
- `risk:path-drift`

Why first:

- It is bounded and policy-backed.
- It clarifies root vs implementation vs validation ownership.

Stop condition:

- Block if drift findings imply edits to submodules or consumer copies without a
  separate task-session.

### Slice 3: Research Project Contract Index

Retrieval question:

```text
How should an agent find each research project's contracts, inventories, dependencies, and traceability surfaces without reading internal project files directly?
```

Source anchors:

- `/home/vrondelli/projects/domainspec-core/research/registry/PROJECT-INDEX.md`
- `/home/vrondelli/projects/domainspec-core/ops/REPOSITORY-ORGANIZATION-PLAN.md`
- `/home/vrondelli/projects/domainspec-core/research/projects/domainspec/PROJECT.yaml`
- `/home/vrondelli/projects/domainspec-core/research/projects/mars/PROJECT.yaml`
- `/home/vrondelli/projects/domainspec-core/research/projects/meta-meta/PROJECT.yaml`
- `/home/vrondelli/projects/domainspec-core/research/projects/mogt-agentic-conversation/PROJECT.yaml`

Expected tags:

- `zone:research`
- `artifact:registry`
- `artifact:inventory`
- `source:research`
- `authority:research-project`
- `domain:repository-governance`

Why first:

- The repo organization plan explicitly requires self-contained project
  contracts.
- Existing project inventories should be reused, not duplicated.

Stop condition:

- Block if the slice consumes internal project results as cross-project source
  without dependency/export evidence.

### Slice 4: DomainSpec Implementation Source Surface

Retrieval question:

```text
Which DomainSpec implementation surfaces should Inventory use for framework behavior, automation packs, docs registry, glossary, and generated/runtime exclusions?
```

Source anchors:

- `/home/vrondelli/projects/domainspec-core/implementation/domainspec/README.md`
- `/home/vrondelli/projects/domainspec-core/implementation/domainspec/AUTHORITY-MAP.md`
- `/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/registry.md`
- `/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/glossary.md`
- `/home/vrondelli/projects/domainspec-core/implementation/domainspec/copilot/README.md`
- `/home/vrondelli/projects/domainspec-core/implementation/domainspec/vault/ontology-conventions.md`

Expected tags:

- `zone:implementation-domainspec`
- `source:submodule`
- `authority:domainspec-implementation`
- `artifact:registry`
- `artifact:glossary`
- `artifact:ontology`
- `risk:submodule-boundary`

Why first:

- It is the canonical DomainSpec implementation source of truth.
- It has nested runtime/generated state that must be excluded.

Stop condition:

- Block if parent Inventory would mutate the implementation submodule.

### Slice 5: CyberAlchemy Inventory-To-Ontology Pipeline

Retrieval question:

```text
What evidence already exists for CyberAlchemy's source -> inventory -> ontology -> context -> execution loop, and what promotion boundaries apply?
```

Source anchors:

- `/home/vrondelli/projects/domainspec-core/cyberAlchemy/README.md`
- `/home/vrondelli/projects/domainspec-core/cyberAlchemy/agentic-system-inventory-ontology-pipeline.md`
- `/home/vrondelli/projects/domainspec-core/cyberAlchemy/agentic-system-ontology-entry-model.md`
- `/home/vrondelli/projects/domainspec-core/cyberAlchemy/agentic-system-first-working-slice.md`
- `/home/vrondelli/projects/domainspec-core/cyberAlchemy/ontology/README.md`
- `/home/vrondelli/projects/domainspec-core/cyberAlchemy/ontology/source-ledger.md`
- `/home/vrondelli/projects/domainspec-core/cyberAlchemy/ontology/source-digests/README.md`

Expected tags:

- `zone:cyberalchemy`
- `domain:cyberalchemy`
- `artifact:ontology`
- `artifact:inventory`
- `source:candidate`
- `authority:cyberalchemy-candidate`
- `risk:ontology-promotion`
- `handoff:ontology-vault`

Why first:

- It directly tests Inventory-to-ontology boundary behavior.
- It is likely to help clarify what Inventory should and should not own.

Stop condition:

- Block if candidate ontology entries are promoted as governed ontology without
  owner approval.

### Slice 6: Lean Formalization Orientation

Retrieval question:

```text
How should agents find formalization evidence, proof status, glossary terms, and research axes without mixing prose, Lean proof, and candidate research claims?
```

Source anchors:

- `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/README.md`
- `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/GLOSSARY.md`
- `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/THERMODYNAMICS.md`
- `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/lean-formalization/NAMING.md`
- `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/research/README.md`
- `/home/vrondelli/projects/domainspec-core/domainspec-lean-formalization/vault/ontology-conventions.md`

Expected tags:

- `zone:lean-formalization`
- `domain:formalization`
- `artifact:glossary`
- `artifact:source-code`
- `source:research`
- `risk:definition-promotion`

Why first:

- It has high retrieval value for formal claims.
- It needs strong separation between proof source, glossary, and research notes.

Stop condition:

- Block if Inventory tries to decide mathematical truth instead of indexing
  source status and selectors.

## Recommended First Slice

Recommended:

```text
Slice 1: Arcanum vs Sigils Library Authority
```

Reason:

- It is the sharpest authority risk in the current tagging/indexing plan.
- It affects the user's current Inventory/Arcanum work directly.
- It is bounded enough for a first Inventory card/index/retrieval proof.

Fallback:

```text
Slice 2: Root Asset Ownership And Automation Surface
```

Use this if the operator wants a lower-conflict first slice focused on root repo
governance and automation drift.

## Deferred Slices

| Slice | Reason Deferred |
| --- | --- |
| project-local GoldenQuill indexes | already has project-specific indexes; parent should only add a lookup handle later |
| validation poker-team concept registry | submodule and Type C local overlay boundary should be handled after Type A/B policy slice |
| full projects folder | too broad; must split by project and retrieval question |
| generated runtime state | excluded by default |
