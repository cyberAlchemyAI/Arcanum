# Runtime Handoff

## Objective

Validate that `codex-exec` prepares isolated Codex adapter state and records durable runtime evidence.

## Orchestrator

- `orchestrator_id`: manual
- `orchestrator_run_id`: codex-exec-fixture

## Target

- `target_kind`: manual
- `target_id`: codex-exec-fixture

## Inputs

- `framework/runtime/README.md`
- `framework/runtime/templates/RUNTIME-HANDOFF.md`

## Allowed Write Scope

- `/tmp/arcanum-runtime-codex-exec`

## Expected Outputs

- `RUN.json`
- `HANDOFF.md`
- `STATUS.json`
- `RESULT.md`
- `events.jsonl`
- `artifacts/adapter-profile.json`
- `adapter-state/codex-home/`

## Validation

```bash
tools/arcanum-runtime-run --adapter codex-exec --handoff framework/runtime/development/fixtures/codex-exec/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-codex-exec
jq empty /tmp/arcanum-runtime-codex-exec/RUN.json
jq empty /tmp/arcanum-runtime-codex-exec/STATUS.json
```

## Blocked Conditions

- Codex binary unavailable.
- Required Codex auth/config unavailable.
- Codex backend unavailable before execution can safely begin.
- Run-local adapter state cannot be created.

## Adapter Preference

- `adapter_id`: codex-exec

## Nesting Policy

- `loop_role`: root
- `loop_id`: codex-exec-fixture
- `parent_loop_id`: null
- `parent_run_id`: null
