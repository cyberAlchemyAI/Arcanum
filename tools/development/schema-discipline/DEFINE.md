# Define: Schema Discipline For Arcanum And CyberAlchemy

## Summary

Schema discipline is a lightweight governance practice for making Arcanum and CyberAlchemy artifacts reviewable, machine-checkable where cheap, and honest about authority. It is not a new schema framework and it is not a dependency mandate.

The shared goal is to make each artifact family answer the same minimum questions:

- What schema or template version is this artifact following?
- What status or authority level does this artifact have?
- Who or what owns review and mutation?
- Which fields are required, recommended, or optional?
- Which enum values are allowed?
- What provenance proves where this artifact came from?
- What validation surface makes the artifact trustworthy enough for its intended use?

## Design Principles

- Copy patterns, not infrastructure.
- Keep enum values inline where implementers edit or validate the artifact.
- Prefer stable ids and paths over free-text references.
- Use Markdown templates for human-facing contracts and JSON only when structured runtime consumption is needed.
- Use `jq`, shell checks, and targeted fixture validation before introducing schema libraries.
- Preserve candidate-vs-canonical boundaries explicitly.
- Treat observability, telemetry, and generated artifacts as evidence inputs, not authority by themselves.
- Record validation strength with a grade instead of implying every pass proves full execution.

## Definition

Schema discipline means applying a small repeatable contract to repo artifacts so humans and agents can tell:

1. what shape the artifact claims to follow;
2. which parts are mandatory;
3. which values are controlled;
4. what authority the artifact has;
5. how it was produced;
6. how it can be validated;
7. what it must not be used to claim.

It is discipline because it changes authoring and review habits before it changes tooling.

## Minimum Shared Contract

Every schema-disciplined artifact family should define:

| Field / Rule | Meaning |
| --- | --- |
| `schema_version` | Stable artifact-family version or template version. |
| `status` | Controlled authority or lifecycle state. |
| `owner` | Human, lifecycle route, or capability responsible for review. |
| Required fields | Fields without which the artifact cannot be consumed. |
| Recommended fields | Fields expected for normal review, but not always blocking. |
| Optional fields | Fields allowed for richer evidence without changing the contract. |
| Inline enums | Legal values documented beside the field or template section. |
| Provenance | Source, agent, command, task, route, or activity that produced the artifact. |
| Validation surface | Exact review, command, fixture, or `jq` check that can validate it. |
| Failure modes | Named ways the artifact can be blocked, flagged, rejected, or deferred. |

## Artifact Families To Prioritize

| Priority | Artifact Family | Reason |
| --- | --- | --- |
| 1 | `framework/runtime/` | Already has `RUN.json`, `STATUS.json`, adapter profiles, statuses, validation grades, and event ownership. |
| 2 | Context packs and task-session handoffs | Runtime delegation requires strict coverage, Markdown plus JSON/index evidence, source selectors, gaps, and provenance. |
| 3 | Sigil and spell templates | Capability contracts need predictable objectives, logic type, quality bar, anti-patterns, and output contracts. |
| 4 | Invoke work-packs and development packages | SWUs, source anchors, write scopes, validation, and execution evidence need consistent field discipline. |
| 5 | CyberAlchemy ontology promotion | `PromotionRecord`, `ReviewableSignal`, confidence fields, candidate status, and bridge validation need explicit schema boundaries. |
| 6 | Observability records | Signals should remain compatible, dedupable, and reviewable without becoming ontology truth. |

## Explicit Non-Goals

- Do not add a graph database.
- Do not add a YAML/frontmatter parser dependency just to read Markdown metadata.
- Do not require Zod, JSON Schema, or another schema library everywhere by default.
- Do not create a universal ontology for runtime state.
- Do not treat candidate schema documents as canonical before validation.
- Do not migrate every existing artifact in one pass.

## Source Basis

- `tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/RUNTIME-SCHEMAS.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/ADAPTER-CONTRACT-DECISIONS.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- `tools/development/task-sessions/20260525T1920Z-runtime-runner-until-blocker.md`
- `framework/QUALITY-BAR.md`
- `framework/templates/sigil-template.md`
- `spells/invoke/templates/module-formulae/concept-model.md`
- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- `development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md`
- `development/cyberalchemy-ontology-lifecycle/PROMOTION-LIFECYCLE.md`
- `development/cyberalchemy-ontology-lifecycle/INTERROGATION-VERDICT.md`
