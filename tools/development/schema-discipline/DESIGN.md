# Design: Schema Discipline For Arcanum And CyberAlchemy

## Design Thesis

Arcanum and CyberAlchemy should adopt schema discipline as a cross-cutting governance and validation pattern. The practice should begin with explicit templates, field tiers, inline enums, provenance, and small validators, then only add stronger schema tooling where repeated failure proves it is needed.

## Shared Schema Discipline Contract

All artifact-family contracts should use this structure:

| Section | Purpose |
| --- | --- |
| Identity | Artifact family, `schema_version`, stable id, path, owner. |
| Authority | `status`, candidate/canonical boundary, allowed use. |
| Field tiers | Required, recommended, optional fields or sections. |
| Enums | Legal values documented inline with field meaning. |
| Provenance | Source inputs, generator route, task/session id, timestamps when relevant. |
| Validation | Mechanical checks, review checks, fixtures, or quality bar. |
| Failure modes | Named `blocked`, `flagged`, `failed`, `deferred`, `rejected`, or contradiction cases. |
| Non-goals | What this schema must not claim or govern. |

## Markdown Templates Vs JSON Schemas Vs Validators

| Surface | Use For | Avoid |
| --- | --- | --- |
| Markdown templates | Human-facing contracts, sigils, spells, work-packs, handoffs, ontology candidates, design packages. | Treating prose templates as machine validation by themselves. |
| JSON templates | Runtime state, indexes, evidence manifests, context-pack indexes, adapter results, records consumed by tools. | Encoding everything as JSON when human review is primary. |
| Shell and `jq` validators | Required-file checks, JSON parse checks, enum checks, stable path checks, validation-grade checks. | Building a brittle parser for rich Markdown. |
| JSON Schema or richer libraries | Later repeated structured surfaces with many consumers and persistent drift. | Default adoption before small validators fail. |

## Enum Documentation Rule

Controlled values must be documented where the field is defined.

Each enum should include:

- field name;
- allowed values;
- meaning of each value;
- whether unset or `null` is allowed;
- whether invalid values block or flag validation.

Initial enum families:

| Family | Values |
| --- | --- |
| Runtime status | `queued`, `running`, `passed`, `flagged`, `blocked`, `failed` |
| Adapter status | `not-started`, `running`, `passed`, `flagged`, `blocked`, `failed` |
| Validation grade | `contract`, `adapter-safety`, `execution`, `null` |
| Target kind | `command`, `skill`, `task`, `swu`, `stage`, `manual` |
| Loop role | `root`, `stage`, `candidate`, `nested`, `repair`, `continuation` |
| Ontology lifecycle status | `raw`, `catalogedEvidence`, `reviewableSignal`, `lifecycleEvidenceEnvelope`, `promotionRecordDraft`, `candidate`, `premise`, `reviewed`, `promoted`, `policy`, `constitution`, `axiom`, `contradicted`, `retired`, `rejected`, `deferred` |
| Promotion gate result | `pass`, `flag`, `block`, `defer`, `reject`, `promote`, `contradict`, `retire` |

## Artifact Family Map

| Family | Contract Form | First Schema Discipline Move |
| --- | --- | --- |
| Runtime artifacts | JSON templates plus Markdown handoff template. | Keep `RUN.json`, `STATUS.json`, adapter result, `events.jsonl`, and adapter profile evidence aligned with runtime schema docs. |
| Runtime handoffs | Markdown template with required sections. | Require objective, target, inputs, allowed write scope, expected outputs, validation, blocked conditions, adapter preference, and nesting policy. |
| Sigils | Markdown skill/sigil template. | Add source schema discipline for frontmatter, objective, logic type, process, quality bar, anti-patterns, and output contract. |
| Spells / invoke modules | Markdown formulae and concept models. | Add field tiers, enum tables, lifecycle references, and related actions to module design outputs. |
| Context packs | Markdown plus JSON/index. | Require obligation coverage, selected sources, source selectors, gaps, authority precedence, and provenance. |
| Task-session handoffs | Markdown plus JSON/index session evidence. | Block delegation unless strict coverage and validation/write-scope fields exist. |
| Development work-packs | Markdown work-pack with tables. | Normalize SWU id, dependencies, write scope, done criteria, verification, owner, status, and evidence. |
| Ontology promotion | Markdown candidate design plus structured `PromotionRecord` template. | Keep one primary claim per record, source input pointers, confidence split, review owner, use scope, contradiction path, rollback/retirement, and bridge validation. |
| Observability | JSONL envelopes and summaries. | Validate route identity, terminal state, recurrence/severity, dedupe key, and review status without promoting meaning automatically. |

## Integration With Arcanum Skills

| Capability | Integration |
| --- | --- |
| `refine` | Generated run manifests, evidence indexes, and refinement packages should carry `schema_version`, status, provenance, validation surface, and blocked-vs-flagged rules. |
| `invoke` | Define/design/plan outputs should include source anchors, status, field tier expectations, validation, and explicit non-goals. |
| `context-builder` | Handoff mode should persist Markdown and JSON/index evidence with strict coverage, selected sources, gaps, and provenance. |
| `task-session` | Before delegation, require a schema-disciplined work-pack/SWU and context handoff; after execution, record validation evidence and unresolved gaps. |
| `experiment-harness` | Experiment specs and result records should distinguish fixture validation, live evidence, and blocked evidence. |
| `observability` / `signal-observer` | Signal envelopes should support compatibility checks and review routing, not direct canonical promotion. |
| `sigil-development` | New or revised sigils should use the shared contract in templates and quality bars. |

## Integration With CyberAlchemy Ontology / Promotion Work

CyberAlchemy should adopt schema discipline through `PromotionRecord`, not through direct mutation of canonical ontology files.

Minimum `PromotionRecord` discipline:

| Field | Tier | Rule |
| --- | --- | --- |
| `id` | required | Stable reference for one claim or decision. |
| `claim` | required | One primary claim only. |
| `claimType` | required | Inline enum; do not bundle unrelated claims. |
| `sourceInputs` | required | Pointers to source selectors, evidence, signals, lifecycle envelopes, or user decisions. |
| `provenance` | required | Activity/agent/entity-style production record. |
| `branchTarget` | required | Business, System, Bridge, or candidate Operational extension. |
| `status` | required | Candidate/promoted state remains visible. |
| `evidenceConfidence` | required | Evidence strength and rationale. |
| `commitmentConfidence` | required | Reliance strength and rationale. |
| `reviewOwner` | required | Owner or lifecycle route for the gate. |
| `gateResult` | required | Inline gate-result enum. |
| `useScope` | conditional | Required before promoted use. |
| `contradictionPath` | required | How later evidence challenges or reopens the record. |
| `rollbackOrRetirement` | conditional | Required before promoted use. |
| `bridgeValidation` | conditional | Required before cross-branch operational use. |

## Validation Approach

Begin with a profile-based validation ladder:

| Grade / Profile | Meaning | Example |
| --- | --- | --- |
| `contract` | Required files, fields, templates, and parse checks pass. | Runtime dry-run produces parseable `RUN.json` and `STATUS.json`. |
| `adapter-safety` | Isolation, preflight, blocked reporting, and closeout are correct. | `codex-exec` blocks safely while preserving adapter profile evidence. |
| `execution` | Requested work actually completes and writes clean output. | Runtime-backed execution returns `passed` and result evidence. |
| `reviewed-candidate` | Human/agent review confirms candidate schema is coherent but not canonical. | CyberAlchemy promotion design is usable as scaffold only. |
| `promoted` | Owner-approved schema governs active artifact family use. | Runtime family contract accepted under `framework/runtime/`. |

## First Implementation Slice

Start with `tools/development/schema-discipline/SCHEMA-DISCIPLINE-CONTRACT.md`, then apply it to `framework/runtime/`.

The first runtime slice should not broaden to sigils, spells, or ontology promotion. It should prove:

- contract document exists;
- runtime artifacts cite or conform to field tiers and inline enums;
- `RUN.json` and `STATUS.json` validation commands remain simple;
- adapter profile evidence and validation grade stay mandatory;
- blocked-vs-flagged behavior is explicit;
- no new dependencies are introduced.

## Open Decisions

No blocker decision is needed for the design package. The main future decision is when a repeated artifact-family validator has enough consumer pressure to justify JSON Schema or a stronger library.
