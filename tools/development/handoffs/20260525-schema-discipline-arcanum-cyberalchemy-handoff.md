# Handoff: Schema Discipline For Arcanum And CyberAlchemy

## Purpose

Start a focused design/refinement thread for making schema discipline a reusable Arcanum and CyberAlchemy practice.

The goal is not to add heavy schema infrastructure. The goal is to promote lightweight, repeatable schema discipline across capabilities, runtime artifacts, sigils, spells, ontology work, context packs, and development handoffs.

## New Thread Prompt

```text
You are working in:

/home/vrondelli/projects/domainspec-core/arcanum

Run a focused Arcanum design/refinement pass for making schema discipline part of Arcanum and CyberAlchemy as a whole.

Do not implement code yet. Produce a decision-complete architecture and work-pack.

Primary question:
How should Arcanum and CyberAlchemy adopt lightweight schema discipline across runtime artifacts, sigils, spells, context packs, task-session handoffs, ontology/promotion records, and development packages without adding unnecessary dependencies or overhead?

Core direction:
Use schema discipline as a governance and validation pattern, not as a heavy framework.

Use these source artifacts first:

- tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md
- tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/RUNTIME-SCHEMAS.md
- tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/ADAPTER-CONTRACT-DECISIONS.md
- tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md
- tools/development/task-sessions/20260525T1920Z-runtime-runner-until-blocker.md
- framework/QUALITY-BAR.md
- framework/templates/sigil-template.md
- spells/invoke/templates/module-formulae/concept-model.md
- arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md
- development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md if present
- development/cyberalchemy-ontology-lifecycle/INTERROGATION-VERDICT.md if present
- development/cyberalchemy-ontology-lifecycle/PROMOTION-LIFECYCLE.md if present

Use the `knowledge-taxonomy` repo only as a precedent, not as a dependency:

- inline enum lists where implementers look,
- required/recommended/optional field tiers,
- stable ids and paths instead of free-text references,
- provenance on generated artifacts,
- validation grades or profiles,
- small mechanical validators with jq/shell before introducing schema libraries,
- honest scope boundaries and named failure modes.

Explicitly avoid:

- adding a graph database,
- adding YAML/frontmatter parser dependencies,
- adding Zod/JSON Schema everywhere by default,
- creating a universal ontology for runtime state,
- treating candidate schema docs as canonical without validation.

Questions to answer:

1. What does "schema discipline" mean in Arcanum/CyberAlchemy?
2. What is the minimum shared schema contract every artifact family should follow?
3. Which artifact families need schema discipline first?
4. What belongs in Markdown templates vs JSON schemas vs shell/jq validators?
5. How should enum values be documented and validated?
6. How should provenance, schema_version, status, and validation_grade appear across artifacts?
7. How should this integrate with refine, invoke, context-builder, task-session, experiment-harness, observability, and ontology promotion?
8. What are the first implementation slices?
9. What should explicitly remain out of scope?

Required output files:

- tools/development/schema-discipline/DEFINE.md
- tools/development/schema-discipline/DESIGN.md
- tools/development/schema-discipline/IMPLEMENTATION-LAYERING.md
- tools/development/schema-discipline/WORK-PACK.md
- tools/development/schema-discipline/VALIDATION.md

Final synthesis format:

- Summary
- Design principles
- Shared schema discipline contract
- Artifact family map
- Validation approach
- Integration with Arcanum skills
- Integration with CyberAlchemy ontology/promotion work
- First implementation slice
- Explicit non-goals
- Open decisions, only if genuinely unresolved
```

## Why This Deserves Its Own Thread

The durable runtime work surfaced one local version of the problem:

- `RUN.json` and `STATUS.json` need stable fields and enums.
- `adapter_profile_path` needs profile evidence.
- `validation_grade` prevents weak proof from masquerading as execution proof.
- Codex state policy needed a precise distinction between shared mutable state and run-local mutable state.

The same pattern appears elsewhere:

- sigil templates need source-schema discipline,
- context-builder handoffs need strict coverage contracts,
- task-session needs SWU and handoff schemas,
- invoke work-packs need execution-ready field discipline,
- ontology promotion needs candidate vs canonical schema boundaries,
- observability needs signal schema compatibility.

This should be designed as a cross-cutting Arcanum/CyberAlchemy practice, not patched into one runtime file at a time.

## Suggested First Slice

Start with a small "Schema Discipline Contract" document, not code:

```text
tools/development/schema-discipline/SCHEMA-DISCIPLINE-CONTRACT.md
```

It should define:

- schema_version,
- status,
- owner,
- required/recommended/optional tiers,
- inline enum rule,
- provenance rule,
- validation surface,
- blocked-vs-flagged rule,
- candidate-vs-canonical promotion rule.

Then apply it to one artifact family first:

```text
framework/runtime/
```

Do not broaden to all sigils/spells until the runtime family proves the pattern.

## Current Evidence

Context pack created from `cyberAlchemyAI/knowledge-taxonomy`:

```text
tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md
```

Key conclusion:

```text
Use knowledge-taxonomy as a schema-design precedent, not a runtime dependency.
```

Runtime design already uses some of this:

- `schema_version`
- `adapter_profile_path`
- `validation_grade`
- inline enum docs
- small `jq`/shell validation

## Manual Launch

Open a new Codex thread and paste the "New Thread Prompt" above.

This current session cannot directly create a new Codex UI thread. If a future local tool exposes a thread/session API, this handoff can be used as the payload.
