## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/plan.md`
- Outputs: `INVOKE-PLAN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, `EXECUTION-PACK.md`, `RUNTIME-SCHEMAS.md`, `ADAPTER-CONTRACT-DECISIONS.md`, `SCHEMA-DISCIPLINE-INTEGRATION.md`, `RUNTIME-ADAPTER-SURFACE-REFRESH.md`, `INSTALL-RUNTIME-SELECTION-REFRESH.md`, `PLAN-TRANSPORT.md`
- Design views: n/a
- Glossary consistency: pass
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Work-pack: `WORK-PACK.md`
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: task specs complete
- Smallest working units: complete
- Target artifact: Durable Arcanum Runtime Interface, tools/framework runtime implementation cycle
- Template or recipe selection: invoke plan medium-complexity split handoff using approved define/design artifacts in this refinement run.
- Decisions: collapse active execution into `tools/arcanum`; preserve runtime adapter selection through `--adapter <adapter-id>` plus adapter profile discovery; select the default runtime adapter during Arcanum installation through `--default-adapter <adapter-id>`; expose post-install runtime interchange through default-adapter get/set and explicit overrides; keep `tools/arcanum-runtime-run` only as a temporary shim or remove it; add adapter contract repair before codex-exec; run Codex through the normal CLI environment by default; write command output directly to requested `--output`; add `SWU-RUNTIME-004.5` to prove artifact-producing command reproduction; migrate active refine/task-session/context-builder runtime contracts after command-owned artifact reproduction exists; preserve runtime envelope as evidence only; adopt lightweight schema discipline for runtime artifacts without adding a schema dependency.
- Unresolved gaps: no blocker gaps after this refresh; historical Codex Goal cleanup is deferred outside active runtime paths.
- Next route: task-session at `SWU-RUNTIME-008`

## Planning Context

### Source Artifacts

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
- `RUNTIME-ADAPTER-DESIGN-TRANSPORT.md`
- `RUNTIME-ADAPTER-INTERROGATION-REVIEW.md`
- `RUNTIME-ADAPTER-DISTILL-REVIEW.md`
- `ADAPTER-CONTRACT-DECISIONS.md`
- `SCHEMA-DISCIPLINE-INTEGRATION.md`
- `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`
- `SINGLE-COMMAND-SURFACE-REFRESH.md`
- `RUNTIME-ADAPTER-SURFACE-REFRESH.md`
- `INSTALL-RUNTIME-SELECTION-REFRESH.md`
- `REFINE-SEED-PROPOSAL.md`
- `RUNTIME-HANDOFF.md`
- `RUN-MANIFEST.md`
- `RESULT.md`
- `evidence-index.json`
- `stages/01-context-builder.md`
- `stages/02-invoke-define.md`
- `stages/03-interrogation-refine-review.md`
- `stages/04-research-decision.md`
- `stages/05-distill.md`
- `stages/06-invoke-design.md`
- `stages/07-interrogation-design-review.md`
- `stages/08-distill-repair.md`
- `stages/09-invoke-plan.md`
- `stages/10-final-interrogation.md`

### Delivery Boundary

Implement the generic durable runtime foundation and migrate active refine/task-session runtime surfaces. Do not implement a background scheduler, dashboard, remote queue, or complete historical `/goal` cleanup in this slice.

## Implementation Objective

Create one active Arcanum command surface where `tools/arcanum --exec` executes commands through a selected runtime adapter, optionally records a runtime envelope, and updates active refine/task-session/context-builder contracts away from Codex Goal.

## Activation Gate

- Approved define artifact: `INVOKE-DEFINE.md`
- Approved glossary: `RUNTIME-GLOSSARY.md`
- Approved design artifact: `INVOKE-DESIGN.md`
- Architecture bundle: `ARCHITECTURE-BUNDLE.md`
- Glossary consistency: `GLOSSARY-CONSISTENCY.md`, pass
- Delivery boundary: active runtime foundation and active refine/task-session migration only
- Lifecycle owner: tools/framework runtime implementation cycle
- Schema discipline boundary: runtime family only; cross-Arcanum/CyberAlchemy generalization is deferred to the schema-discipline handoff.

## Plan Summary

The plan is split into four layers:

- L0: prove durable runtime envelope folders and dry-run evidence.
- L1: add Codex CLI execution with adapter profile evidence, classified outcomes, and validation grade evidence.
- L2: prove `tools/arcanum --exec` preserves requested output and command-owned artifact reproduction.
- L3: migrate active refine, task-session, and context-builder contracts to runtime handoff language after L2 artifact reproduction passes.
- L4: collapse execution into the single `tools/arcanum` command surface, preserve adapter selection and discovery, and remove or shim `tools/arcanum-runtime-run`.
- L5: select the default runtime adapter during install and expose post-install interchange.

Schema discipline is part of each layer's acceptance evidence, not a separate layer: required fields, inline enums, stable paths, provenance, and validation grades must remain checkable as implementation proceeds.

## Handoff Artifacts

- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Work-pack: `WORK-PACK.md`
- Execution pack: `EXECUTION-PACK.md`
- Runtime schemas: `RUNTIME-SCHEMAS.md`
- Runtime adapter pattern: `RUNTIME-ADAPTER-PATTERN.md`
- Codex adapter design: `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- Adapter contract decisions: `ADAPTER-CONTRACT-DECISIONS.md`
- Schema discipline integration: `SCHEMA-DISCIPLINE-INTEGRATION.md`
- Runtime command artifact reproduction: `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`
- Single command surface refresh: `SINGLE-COMMAND-SURFACE-REFRESH.md`
- Runtime adapter surface refresh: `RUNTIME-ADAPTER-SURFACE-REFRESH.md`
- Install runtime selection refresh: `INSTALL-RUNTIME-SELECTION-REFRESH.md`
- Plan transport: `PLAN-TRANSPORT.md`

## Validation Summary

The minimum acceptance path is:

```bash
tools/arcanum-runtime-run --adapter dry-run --handoff <fixture>/RUNTIME-HANDOFF.md --run-dir <tmp-run>
jq empty <tmp-run>/RUN.json
jq empty <tmp-run>/STATUS.json
jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' <tmp-run>/RUN.json
jq -e '.schema_version == "arcanum.runtime.run.v1"' <tmp-run>/RUN.json
jq -e '.schema_version == "arcanum.runtime.status.v1"' <tmp-run>/STATUS.json
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output <tmp-output> invoke "define runtime smoke"
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output /tmp/arcanum-runtime-invoke-design-output.md invoke "<artifact-producing invoke design fixture request>"
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --output /tmp/arcanum-one-tool-output.md invoke "define runtime smoke"
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter dry-run
tools/arcanum --exec --adapter dry-run --output /tmp/arcanum-dry-run-output.md invoke "define runtime smoke"
tools/bootstrap_arcanum.sh --target /tmp/arcanum-install-runtime-selection --runtime codex --default-adapter codex-exec --dry-run
tools/bootstrap_arcanum.sh --target /tmp/arcanum-install-runtime-selection --runtime codex --default-adapter codex-exec --force
jq empty /tmp/arcanum-install-runtime-selection/.arcanum/runtime/config.json
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter dry-run
arcana/refine/development/run-validation-fixtures.sh
```

The current execution target is `SWU-RUNTIME-008`, followed by `SWU-RUNTIME-009`.

## Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: trigger if `SWU-RUNTIME-004.5` returns only response prose without creating command-owned invoke design artifacts, or if `SWU-RUNTIME-008` collapses to a Codex-only execution path.
- RECOMMENDATION: continue task-session at `SWU-RUNTIME-008`, then `SWU-RUNTIME-009`.
- DEDUPE_KEY: invoke-plan-durable-runtime-20260525T165111Z
