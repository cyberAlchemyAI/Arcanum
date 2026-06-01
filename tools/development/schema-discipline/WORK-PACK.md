# Work Pack: Schema Discipline For Arcanum And CyberAlchemy

## Objective

Adopt lightweight schema discipline as a repeatable governance and validation practice across Arcanum and CyberAlchemy without adding unnecessary dependencies or a heavy schema framework.

## Source Design References

- `tools/development/schema-discipline/DEFINE.md`
- `tools/development/schema-discipline/DESIGN.md`
- `tools/development/schema-discipline/IMPLEMENTATION-LAYERING.md`
- `tools/development/schema-discipline/SCHEMA-DISCIPLINE-CONTRACT.md`
- `tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/RUNTIME-SCHEMAS.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/ADAPTER-CONTRACT-DECISIONS.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`
- `development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md`
- `development/cyberalchemy-ontology-lifecycle/PROMOTION-LIFECYCLE.md`

## Current State

- Runtime already has the strongest concrete schema surface: `RUN.json`, `STATUS.json`, adapter result, adapter profile evidence, event ownership, validation grades, and `jq` validation.
- Task-session and context-builder already require stricter handoff evidence for delegation, especially Markdown plus JSON/index artifacts and strict coverage.
- Sigil and spell templates have structured sections, but they do not yet share a named schema discipline contract.
- CyberAlchemy ontology lifecycle design has a candidate `PromotionRecord` boundary, confidence split, reviewable signal model, and candidate-vs-promoted separation.
- The knowledge-taxonomy precedent supports required/recommended/optional tiers, inline enums, stable ids, provenance, validation profiles, small validators, and explicit failure modes.

## Delivery Slices

| Slice | Layer | Goal | Status |
| --- | --- | --- | --- |
| SCHEMA-L0 | L0 | Establish the shared contract and apply it to `framework/runtime/`. | ready |
| SCHEMA-L1 | L1 | Apply the contract to context packs, task-session handoffs, and development work-packs. | blocked by L0 |
| SCHEMA-L2 | L2 | Apply the contract to sigil/spell authoring templates and capability quality bars. | blocked by L1 |
| SCHEMA-L3 | L3 | Define CyberAlchemy `PromotionRecord` template and candidate validation checklist. | blocked by L2 or explicit owner decision |
| SCHEMA-L4 | L4 | Decide whether any family needs stronger schema tooling. | blocked by drift evidence |

## SWU Manifest

| SWU | Parent Slice | Dependencies | Write Scope | Done Criteria | Verification | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-SCHEMA-001 | SCHEMA-L0 | none | `tools/development/schema-discipline/` | Contract, define, design, layering, work-pack, and validation docs exist. | `test -f` for all required files and `git diff --check -- tools/development/schema-discipline`. | local-fallback |
| SWU-SCHEMA-002 | SCHEMA-L0 | SWU-SCHEMA-001 | `framework/runtime/`, `tools/development/schema-discipline/VALIDATION.md` | Runtime contract review maps `RUN.json`, `STATUS.json`, adapter profile, validation grade, events, and blocked/flagged rules to schema discipline. | Runtime dry-run checks plus targeted `jq` checks listed in `VALIDATION.md`. | local-fallback |
| SWU-SCHEMA-003 | SCHEMA-L1 | SWU-SCHEMA-002 | context-builder/task-session docs and templates only | Handoff schema names required/recommended/optional fields, strict coverage, source selectors, gaps, provenance, validation, and write scope. | One reviewed handoff fixture or template check; JSON/index parses if present. | local-fallback |
| SWU-SCHEMA-004 | SCHEMA-L1 | SWU-SCHEMA-003 | development work-pack templates/docs | Work-pack/SWU fields normalize id, dependency, write scope, done criteria, verification, owner, status, and execution evidence. | Review current work-pack examples and run diff whitespace checks. | local-fallback |
| SWU-SCHEMA-005 | SCHEMA-L2 | SWU-SCHEMA-004 | `framework/templates/`, spell/sigil template docs | Sigil/spell templates cite schema discipline for frontmatter, objective, logic type, process, quality bar, anti-patterns, and output contract. | Template review and stale-language search. | local-fallback |
| SWU-SCHEMA-006 | SCHEMA-L3 | SWU-SCHEMA-005 or owner decision | CyberAlchemy development package only | Candidate `PromotionRecord` template/checklist exists without canonical ontology mutation. | Review checklist confirms candidate status, confidence split, owner, use scope, contradiction, rollback/retirement, and bridge validation. | ontology-owner |
| SWU-SCHEMA-007 | SCHEMA-L4 | SWU-SCHEMA-006 plus drift evidence | selected artifact family only | Stronger schema tooling decision is recorded for one family or explicitly rejected. | Drift evidence plus dependency decision review. | local-fallback |

## First Implementation Slice

### SWU-SCHEMA-001: Create Schema Discipline Package

Outcome: the design/refinement package exists and can be reviewed before implementation.

Write scope:

- `tools/development/schema-discipline/DEFINE.md`
- `tools/development/schema-discipline/DESIGN.md`
- `tools/development/schema-discipline/IMPLEMENTATION-LAYERING.md`
- `tools/development/schema-discipline/SCHEMA-DISCIPLINE-CONTRACT.md`
- `tools/development/schema-discipline/WORK-PACK.md`
- `tools/development/schema-discipline/VALIDATION.md`

Acceptance:

- Required output files exist.
- Design answers all handoff questions.
- Layering starts with runtime and defers broad migration.
- Validation document lists review checks and concrete commands.

### SWU-SCHEMA-002: Runtime Family Review

Outcome: runtime becomes the first proven artifact family.

Write scope:

- `framework/runtime/`
- `tools/development/schema-discipline/VALIDATION.md`

Scope:

- Review runtime templates against `SCHEMA-DISCIPLINE-CONTRACT.md`.
- Confirm `schema_version`, status, owner/provenance equivalent, field tiers, inline enums, validation grade, adapter profile evidence, event ownership, and blocked/flagged rules.
- Add only minimal doc/template adjustments if gaps are found.

Acceptance:

- Runtime dry-run still passes.
- `RUN.json` and `STATUS.json` parse with `jq`.
- `adapter_profile_path` and `validation_grade` checks pass.
- No schema library or new dependency is added.

## Explicit Non-Goals

- No canonical ontology mutation in this work-pack.
- No universal schema framework.
- No broad sigil/spell migration in L0.
- No graph database.
- No YAML/frontmatter dependency.
- No JSON Schema or Zod adoption by default.
- No direct promotion of observability signals.

## Blocked Conditions

- Any slice that would mutate canonical CyberAlchemy ontology without owner decision must block.
- Any slice that requires a new dependency before small validators fail must block and require a decision.
- Any handoff or runtime artifact missing required provenance or validation surface must block runtime delegation rather than silently flagging.
