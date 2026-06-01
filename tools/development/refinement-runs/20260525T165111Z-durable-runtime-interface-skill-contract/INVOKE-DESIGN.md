## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/design.md`
- Outputs: `INVOKE-DESIGN.md`, `ARCHITECTURE-BUNDLE.md`, `GLOSSARY-CONSISTENCY.md`, `ADAPTER-CONTRACT-DECISIONS.md`, `SCHEMA-DISCIPLINE-INTEGRATION.md`, `DESIGN-TRANSPORT.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: architecture profile with runtime infrastructure companion design.
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Work-pack: n/a
- Decisions: two-folder authority model; immutable handoff; runtime-owned status/events; adapter-owned concrete execution/classification; adapter profile evidence in every run; validation grades; lightweight schema discipline through field tiers, inline enums, stable ids/paths, and small `jq`/shell validation; feature-flag migration for `tools/arcanum --exec`.
- Unresolved gaps: none blocking.
- Next route: plan

## Design Summary

The runtime design separates orchestration semantics from execution mechanics.

Refine and task-session remain domain orchestrators. The runtime runner handles durable execution state and adapter invocation.

The runtime family is also the first proving ground for a broader Arcanum/CyberAlchemy schema-discipline practice. The design adopts zero-dependency schema discipline now and leaves cross-project generalization to the dedicated handoff.

## Six-View Coverage

| View | Status | Artifact |
| --- | --- | --- |
| Context | pass | `ARCHITECTURE-BUNDLE.md#context-view` |
| High-level structure | pass | `ARCHITECTURE-BUNDLE.md#high-level-structure-view` |
| Low-level components | pass | `ARCHITECTURE-BUNDLE.md#low-level-components-view` |
| Workflow process | pass | `ARCHITECTURE-BUNDLE.md#workflow-process-view` |
| Decision flow | pass | `ARCHITECTURE-BUNDLE.md#decision-flow-view` |
| Dependency interface | pass | `ARCHITECTURE-BUNDLE.md#dependency-interface-view` |

## Design Decisions

| Decision | Selected | Rejected | Rationale |
| --- | --- | --- | --- |
| Runtime state owner | `.arcanum/runtime/runs/<id>/` | refine run folder | Prevents target-local manifests from becoming execution databases. |
| Orchestrator evidence owner | target-local run folder | runtime folder only | Keeps refine/task-session evidence navigable to humans. |
| Handoff mutability | immutable | status written into handoff | Keeps request and execution state separate. |
| Adapter evidence | profile path plus optional JSON snapshot | adapter id only | Makes runtime properties, limitations, and validation surface auditable. |
| Event ownership | runner-owned log, adapter event contributions | direct adapter writes | Keeps runtime event ordering deterministic. |
| Validation proof | `contract`, `adapter-safety`, `execution` grades | one generic pass label | Prevents safe blocked Codex runs from being mistaken for execution proof. |
| Schema discipline | field tiers, inline enums, stable ids/paths, provenance, shell/`jq` checks | heavy schema framework by default | Keeps runtime artifacts mechanically checkable without adding broad dependencies. |
| Migration path | feature flag first | hard cutover | Reduces risk to existing command users. |
| First adapter | `dry-run` | `codex-exec` first | Proves contract before depending on Codex backend. |

## Design Transport

- Approved define artifact: `INVOKE-DEFINE.md`
- Glossary: `RUNTIME-GLOSSARY.md`
- Architecture bundle: `ARCHITECTURE-BUNDLE.md`
- Adapter contract decisions: `ADAPTER-CONTRACT-DECISIONS.md`
- Schema discipline integration: `SCHEMA-DISCIPLINE-INTEGRATION.md`
- Recommended next route: `invoke plan`

## Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: trigger if `SWU-RUNTIME-003` starts without adapter contract evidence or if runtime templates drift from the schema-discipline rules.
- RECOMMENDATION: continue-to-invoke-plan with adapter contract repair included.
- DEDUPE_KEY: invoke-design-durable-runtime-20260525T165111Z
