## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/design.md`
- Outputs: `RUNTIME-ADAPTER-PATTERN.md`, `CODEX-RUNTIME-ADAPTER-DESIGN.md`, `RUNTIME-ADAPTER-DESIGN-TRANSPORT.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: architecture companion design for runtime adapter family.
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Work-pack: `WORK-PACK.md`
- Decisions: add new runtimes through a stable adapter pattern; keep runtime runner generic; make selected runtime properties explicit before execution.
- Unresolved gaps: none blocking for design; future adapters need their own property profiles.
- Next route: plan

## Purpose

Define the pattern for adding new runtime adapters to Arcanum's durable runtime interface.

The pattern must make every selected runtime explainable before it can execute work:

- runtime properties,
- execution layers,
- runner-script integration,
- state and isolation behavior,
- result and error semantics,
- validation expectations.

## Context View

Arcanum orchestrators should not know how each runtime works. They should create generic durable handoffs and receive durable evidence. Runtime-specific behavior belongs in adapters.

```text
orchestrator -> RUNTIME-HANDOFF.md -> tools/arcanum --exec --adapter <adapter-id> -> adapter -> runtime-specific execution
```

The adapter pattern is the boundary that lets Arcanum add a runtime without changing refine, task-session, or other orchestrators.

## High-Level Structure View

Each runtime adapter has four design artifacts:

```text
framework/runtime/adapters/<adapter-id>/
  README.md
  RUNTIME-PROFILE.md
  TRANSLATOR.md
  VALIDATION.md
```

Recommended for v1 if implementation prefers fewer files:

```text
framework/runtime/adapters/<adapter-id>.md
```

with the same sections.

## Runtime Adapter Profile

Every adapter must define:

| Field | Meaning |
| --- | --- |
| `adapter_id` | Stable id used by `tools/arcanum --exec --adapter <adapter-id>`. |
| `runtime_kind` | `model`, `shell`, `local-agent`, `remote-agent`, `dry-run`, or future kind. |
| `execution_mode` | synchronous, durable-local, remote-async, simulated, or hybrid. |
| `state_model` | stateless, run-local state, shared-readonly config, external state. |
| `isolation_model` | process sandbox, filesystem isolation, runtime home isolation, none. |
| `input_shape` | What translator gives the adapter. |
| `output_shape` | What adapter returns to the runner. |
| `failure_model` | Difference between blocked, failed, flagged, and passed. |
| `capabilities` | What this runtime can do. |
| `limitations` | What this runtime must not be used for. |
| `validation_surface` | Commands or evidence that prove adapter behavior. |

## Execution Layers

The adapter pattern has six execution layers:

| Layer | Owner | Purpose |
| --- | --- | --- |
| L0 Handoff | Orchestrator | Defines objective, scope, inputs, validation, and adapter preference. |
| L1 Runtime Run | Runner | Creates durable run folder, status, events, lock, and result paths. |
| L2 Translation | Adapter translator | Converts generic handoff into runtime-specific request. |
| L3 Preparation | Adapter | Prepares runtime-specific state, environment, credentials, config, and isolation. |
| L4 Execution | Adapter | Runs the runtime command/API/simulation. |
| L5 Capture | Runner + adapter | Normalizes result, status, events, blocked reason, and artifacts. |

This layering is important: adding a runtime should usually implement only L2-L4, while L1 and L5 stay stable in the runner.

## Low-Level Components View

### Adapter Registry

`tools/arcanum` should resolve adapter ids through an explicit dispatch table.

Minimum command surface:

```bash
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter <adapter-id>
tools/arcanum --exec --adapter <adapter-id> --output <path> <command> <request>
```

V1 shell shape:

```bash
case "$adapter_id" in
  dry-run)
    run_adapter_dry_run
    ;;
  codex-exec)
    run_adapter_codex_exec
    ;;
  *)
    block_unknown_adapter
    ;;
esac
```

Future shape can move each adapter into a sourced file:

```text
framework/runtime/adapters/<adapter-id>.sh
```

but v1 should not add dynamic plugin loading until static adapters are proven.

### Runner Core

Command/runtime core owns:

- argument parsing,
- command resolution,
- adapter selection,
- run directory creation,
- lock handling,
- `RUN.json`,
- `STATUS.json`,
- `events.jsonl`,
- terminal status rules,
- result copy/link policy,
- adapter dispatch,
- closeout.

Adapter owns:

- runtime profile,
- translation,
- state preparation,
- runtime invocation,
- raw logs/artifacts,
- adapter result object.

Runner owns `events.jsonl`. Adapter events are returned as contributions in the adapter result object; the runner validates, normalizes, and appends them.

### Adapter Result Object

Adapters must produce:

```json
{
  "adapter_id": "adapter-id",
  "adapter_status": "passed|flagged|blocked|failed",
  "validation_grade": "contract|adapter-safety|execution|null",
  "exit_code": 0,
  "output_paths": ["requested-output.md"],
  "result_path": null,
  "blocked_reason": null,
  "error_summary": null,
  "state_path": "adapter-state/<adapter-id>",
  "events": []
}
```

Each run also records selected adapter profile evidence through `RUN.json.adapter_profile_path`, normally `artifacts/adapter-profile.json`.

## Workflow Process View

To add a new runtime:

1. Write the runtime profile.
2. Decide whether the runtime is safe for v1 durable local execution.
3. Define translator input and adapter result output.
4. Define state/isolation rules.
5. Add adapter dispatch in `tools/arcanum`.
6. Add fixtures under `framework/runtime/development/fixtures/<adapter-id>/`.
7. Add validation commands and classify them as `contract`, `adapter-safety`, or `execution`.
8. Update `RUNTIME-SCHEMAS.md` only if the generic adapter result contract changes.
9. Do not update refine/task-session unless they need new adapter selection policy.

## Decision Flow View

```text
New runtime proposed
  -> Does it fit generic handoff/result contract?
    no -> design adapter extension, do not implement runtime yet
    yes -> define runtime profile
      -> Can state be isolated per run?
        no -> require explicit risk/legacy adapter profile
        yes -> implement adapter
          -> Does fixture prove pass/block behavior?
            no -> keep adapter experimental
            yes -> allow orchestrators to request adapter
```

## Dependency Interface View

### Stable Runner Inputs

- handoff path,
- run dir,
- adapter id,
- optional output path from compatibility callers.

### Adapter Inputs

- generic handoff content,
- runtime run directory,
- adapter state directory,
- selected environment/config,
- source credential/config references when needed.

### Adapter Outputs

- adapter result object,
- requested command output path,
- adapter logs/artifacts under `artifacts/` or `adapter-state/`,
- status/event contributions.

## Required Design Questions For Any Runtime

Before implementing an adapter, answer:

1. What makes this runtime useful compared with existing adapters?
2. Is it synchronous, async, or hybrid?
3. Does it need credentials, config, network, shell, or filesystem access?
4. What state must be isolated per run?
5. What state may be shared read-only?
6. What does a successful result look like?
7. What does a blocked result look like?
8. What does a failed result look like?
9. Can it produce partial/flagged output?
10. What validation proves it works?

## Anti-Patterns

Avoid:

- making orchestrators call runtime-specific commands directly,
- adding adapter-specific fields to top-level `RUN.json` unless the generic schema genuinely changes,
- sharing mutable runtime state across runs,
- treating dry-run adapter success as proof of execution adapter success,
- adding dynamic adapter discovery before static adapters are validated,
- hiding runtime failure behind a generic `failed` message without blocked reason or error summary.

## Design Handoff

This pattern should be implemented before adding adapters beyond `dry-run` and `codex-exec`. Codex becomes the reference adapter profile.
