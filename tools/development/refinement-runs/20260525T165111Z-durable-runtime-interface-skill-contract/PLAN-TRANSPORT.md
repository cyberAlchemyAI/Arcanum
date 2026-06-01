# Plan Transport: Durable Arcanum Runtime Interface

## Source Inputs

- `INVOKE-DEFINE.md`
- `RUNTIME-GLOSSARY.md`
- `DEFINE-TRANSPORT.md`
- `INVOKE-DESIGN.md`
- `ARCHITECTURE-BUNDLE.md`
- `GLOSSARY-CONSISTENCY.md`
- `DESIGN-TRANSPORT.md`
- `INTERROGATION-REVIEW.md`
- `DISTILL-REVIEW.md`
- `RUNTIME-SCHEMAS.md`
- `EXECUTION-PACK.md`
- `RUNTIME-ADAPTER-PATTERN.md`
- `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`
- `RUNTIME-ADAPTER-DESIGN-TRANSPORT.md`
- `RUNTIME-ADAPTER-INTERROGATION-REVIEW.md`
- `RUNTIME-ADAPTER-DISTILL-REVIEW.md`
- `ADAPTER-CONTRACT-DECISIONS.md`
- `SCHEMA-DISCIPLINE-INTEGRATION.md`
- `tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md`
- `tools/development/handoffs/20260525-schema-discipline-arcanum-cyberalchemy-handoff.md`
- `RESULT.md`
- `evidence-index.json`

## Produced Plan Outputs

- `INVOKE-PLAN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `EXECUTION-PACK.md`
- `RUNTIME-SCHEMAS.md`
- `RUNTIME-ADAPTER-PATTERN.md`
- `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `RUNTIME-ADAPTER-DESIGN-TRANSPORT.md`
- `ADAPTER-CONTRACT-DECISIONS.md`
- `SCHEMA-DISCIPLINE-INTEGRATION.md`
- `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`
- `PLAN-TRANSPORT.md`

## Approved Delivery Boundary

Implement runtime foundation and active orchestrator migration only:

- `framework/runtime/`
- `tools/arcanum-runtime-run`
- `tools/arcanum`
- active refine runtime docs/templates/fixtures
- task-session runtime adapter boundary

Deferred:

- background scheduler,
- remote queue,
- dashboard,
- complete historical `/goal` cleanup.
- broad Arcanum/CyberAlchemy schema-discipline rollout.

## Execution-Ready Unit

Start with:

```text
SWU-RUNTIME-001
```

from `WORK-PACK.md`.

L0 runtime viability requires:

```text
SWU-RUNTIME-001 + SWU-RUNTIME-002
```

`SWU-RUNTIME-001` is the first execution target; `SWU-RUNTIME-002` is required before promoting L0.

`SWU-RUNTIME-003` must not start until adapter contract decisions are implemented in runtime schema and runner behavior.

The schema-discipline refresh does not add a new execution unit. It tightens acceptance for the existing units by requiring documented schema versions, enum values, stable ids/paths, provenance, and validation grades.

`SWU-RUNTIME-004` proved command transport only. `SWU-RUNTIME-004.5` is now required before L3 to prove runtime-backed `tools/arcanum --exec` reproduces command-owned invoke artifacts in a declared target development directory.

## Next Route

`task-session` or local bounded implementation on `SWU-RUNTIME-004.5`.
