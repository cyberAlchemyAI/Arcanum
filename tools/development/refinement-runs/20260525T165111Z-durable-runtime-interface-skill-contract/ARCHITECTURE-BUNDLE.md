# Architecture Bundle: Durable Arcanum Runtime Interface

## Context View

Arcanum has command and skill surfaces that can orchestrate complex loops, but runtime execution currently leaks through Codex-specific concepts. Refine and task-session need a shared durable runtime substrate.

Key source constraints:

- Refine keeps the canonical ten-stage loop.
- Task-session remains the bounded task/SWU coordinator.
- Codex is allowed only as an adapter.
- Runtime execution must preserve blocked/failure evidence.
- Nested and multiple refinement loops need explicit topology.
- Runtime artifacts should prove lightweight schema discipline through field tiers, inline enums, stable ids/paths, provenance, and small validators.

## High-Level Structure View

```text
refine/task-session/other orchestrator
  -> RUNTIME-HANDOFF.md
  -> tools/arcanum --exec
  -> optional runtime envelope
  -> selected adapter
  -> .arcanum/runtime/runs/<runtime-run-id>/
```

Primary components:

- orchestrator,
- runtime handoff,
- `tools/arcanum` command surface,
- translator,
- adapter,
- adapter profile evidence,
- adapter registry/profile resolver,
- installed runtime configuration,
- schema discipline contract,
- runtime run folder,
- orchestrator manifest/index.

## Low-Level Components View

### `tools/arcanum`

CLI options:

```bash
tools/arcanum --exec --output <path> <command> <request>
tools/arcanum --exec --adapter <adapter-id> --output <path> <command> <request>
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter <adapter-id>
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter <adapter-id>
```

Responsibilities:

- resolve command files,
- build the normal Arcanum command prompt,
- select and resolve a runtime adapter,
- read and update installed runtime defaults,
- run the selected adapter,
- write final command response directly to requested `--output`,
- optionally create runtime envelope evidence,
- write status/events/profile evidence when envelope is enabled,
- emit observed invocation closeout.

`tools/arcanum-runtime-run` is no longer the canonical runtime model. It may remain only as a short-lived compatibility shim while existing fixtures are migrated.

### Runtime Templates

Location:

```text
framework/runtime/templates/
```

Templates:

- `RUNTIME-HANDOFF.md`
- `RUN.json`
- `STATUS.json`

Runtime templates are the first artifact family for schema discipline. They must keep required fields explicit, keep controlled values close to the fields they constrain, and avoid dependencies beyond JSON plus shell/`jq` checks for v1.

### Adapters

V1:

- `dry-run`
- `codex-exec`

Every adapter must have profile evidence. A runtime run records the selected adapter profile through `RUN.json.adapter_profile_path`, normally pointing at `artifacts/adapter-profile.json`.

Adapter execution is split into:

- runtime-specific preflight and translation,
- runtime-specific outcome classification,
- command-surface-owned output capture and optional status/event persistence.

Adapters do not write `events.jsonl` directly in v1.

`codex-exec` is the default adapter for current Codex UI parity only. It must not be treated as the generic runtime behavior. `dry-run` remains the non-Codex proof adapter for the shared execution path.

### Runtime Config

Installed repositories should keep non-secret runtime selection in:

```text
.arcanum/runtime/config.json
```

The config records command surface, default adapter, enabled adapter ids, and profile paths. It must not store auth tokens, copied Codex config, SQLite state, or symlinks to runtime state.

Adapter selection precedence:

1. explicit `--adapter <adapter-id>`,
2. `ARCANUM_RUNTIME_ADAPTER`,
3. `.arcanum/runtime/config.json` default,
4. compatibility fallback from command surface.

### Command Compatibility

`tools/arcanum --exec` is the user-facing and canonical command path. Runtime envelope evidence may be enabled, but the command output remains the requested `--output`; successful command execution should not create a duplicate runtime `RESULT.md`.

### Schema Discipline

Runtime schema discipline is intentionally small:

- required/recommended/optional field tiers live in documentation,
- enum values live inline in `RUNTIME-SCHEMAS.md` and templates,
- generated evidence records provenance paths,
- validation grades state the strength of proof,
- validators stay in shell and `jq` until the runtime family proves it needs a schema library.

## Workflow Process View

1. Orchestrator creates or selects a task/stage.
2. Orchestrator writes `RUNTIME-HANDOFF.md`.
3. Orchestrator calls `tools/arcanum --exec`, optionally with `--adapter <adapter-id>`.
4. `tools/arcanum` optionally creates `.arcanum/runtime/runs/<runtime-run-id>/` envelope evidence.
5. `tools/arcanum` translates handoff for the selected adapter.
6. Adapter executes or blocks.
7. `tools/arcanum` writes requested output, status/events, and artifact references.
8. Orchestrator indexes runtime run evidence.

## Decision Flow View

```text
Is the target executable?
  no -> write blocked status
  yes -> is adapter available?
    no -> write blocked status
    yes -> execute adapter
      pass -> write passed status/result
      recoverable issue -> write flagged status/result
      pre-execution block -> write blocked status with exact reason
      execution failure -> write failed status with error summary
```

Migration flow:

```text
L0 dry-run passes
  -> L1 codex-exec adapter
  -> L2 tools/arcanum feature-flag route
  -> L3 refine/task-session active runtime migration
```

## Dependency Interface View

### Inputs

- handoff path,
- run dir,
- adapter id,
- adapter profile path,
- adapter-specific configuration,
- installed runtime config,
- command metadata for `tools/arcanum --exec` compatibility.

### Outputs

- `RUN.json`,
- `HANDOFF.md`,
- `STATUS.json`,
- adapter profile evidence,
- requested command output path,
- `events.jsonl`,
- adapter artifacts,
- child run folders.

### External Dependencies

- Codex CLI only for `codex-exec`.
- `jq` for validation and JSON generation where available.
- existing `tools/arcanum` command metadata for compatibility.
- no dependency on `knowledge-taxonomy`; it is used as a schema-design precedent only.

## Risks

- Over-migrating historical `/goal` records.
- Making Codex adapter state isolation optional.
- Blurring target-local refine evidence with runtime state.
- Treating dry-run success as proof of Codex adapter success.
- Letting schema discipline sprawl into a universal ontology before the runtime artifact family proves the pattern.

## Design Handoff

Proceed to invoke plan with `IMPLEMENTATION-LAYERING.md` and `WORK-PACK.md`.
