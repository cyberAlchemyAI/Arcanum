# Schema Discipline Integration

## Purpose

Refresh the durable runtime package with the schema lessons from the `knowledge-taxonomy` context pack and the Arcanum/CyberAlchemy schema-discipline handoff.

This artifact does not make the durable runtime responsible for all Arcanum and CyberAlchemy schema governance. It defines what this runtime package should adopt now and what should remain in the follow-up schema-discipline design thread.

## Source Inputs

- `tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md`
- `tools/development/handoffs/20260525-schema-discipline-arcanum-cyberalchemy-handoff.md`
- `RUNTIME-SCHEMAS.md`
- `ADAPTER-CONTRACT-DECISIONS.md`
- `WORK-PACK.md`
- `tools/development/task-sessions/20260525T1920Z-runtime-runner-until-blocker.md`

## Adopt Now

The runtime package should adopt schema discipline as a lightweight contract pattern:

- required, recommended, and optional field tiers in schema documentation,
- inline enum lists where implementers edit or validate runtime fields,
- stable ids and paths instead of free-text references,
- provenance for generated adapter evidence,
- validation grades that distinguish contract proof, adapter-safety proof, and execution proof,
- small shell and `jq` validation before introducing schema libraries.

These choices are already aligned with the current runtime design. This refresh makes them explicit.

## Runtime-Specific Contract

For runtime v1, schema discipline applies to these artifact families:

| Artifact | Required Discipline |
| --- | --- |
| `RUN.json` | `schema_version`, stable ids, adapter profile path, target kind, loop role, artifact path fields. |
| `STATUS.json` | status enum, adapter status enum, validation grade enum, blocked/failure fields. |
| `RUNTIME-HANDOFF.md` | fixed section set, immutable request semantics, explicit write scope and blocked conditions. |
| `events.jsonl` | normalized event names, runner-owned ordering, adapter event contributions only. |
| `artifacts/adapter-profile.json` | selected adapter properties, limitations, failure model, and validation surface. |

## Non-Goals

Do not add these to the runtime slice:

- a dependency on `knowledge-taxonomy`,
- a graph database,
- YAML or frontmatter parsing infrastructure,
- Zod or JSON Schema across every artifact by default,
- a universal ontology for runtime state,
- cross-project schema migration before the runtime family proves the pattern.

## Work-Pack Impact

No new runtime implementation layer is required.

Instead:

- `SWU-RUNTIME-001` must keep runtime docs/templates aligned with field tiers and inline enums.
- `SWU-RUNTIME-002` must prove the contract with JSON and path checks.
- `SWU-RUNTIME-003` must preserve adapter profile provenance and validation grade evidence.
- The schema-discipline follow-up thread owns cross-Arcanum and CyberAlchemy generalization.

## Follow-Up Boundary

The separate schema-discipline thread should produce:

- `tools/development/schema-discipline/DEFINE.md`
- `tools/development/schema-discipline/DESIGN.md`
- `tools/development/schema-discipline/IMPLEMENTATION-LAYERING.md`
- `tools/development/schema-discipline/WORK-PACK.md`
- `tools/development/schema-discipline/VALIDATION.md`

That thread may later promote runtime patterns into shared Arcanum/CyberAlchemy practice, but runtime implementation should continue from `SWU-RUNTIME-003` without waiting for the broader design pass.
