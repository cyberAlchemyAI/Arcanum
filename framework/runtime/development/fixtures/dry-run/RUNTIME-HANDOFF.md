# Runtime Handoff

## Objective

Validate that the durable runtime runner can create a complete run folder without external execution.

## Orchestrator

- `orchestrator_id`: manual
- `orchestrator_run_id`: dry-run-fixture

## Target

- `target_kind`: manual
- `target_id`: dry-run-fixture

## Inputs

- `framework/runtime/templates/RUNTIME-HANDOFF.md`
- `framework/runtime/templates/RUN.json`
- `framework/runtime/templates/STATUS.json`

## Allowed Write Scope

- `/tmp/arcanum-runtime-dry-run`

## Expected Outputs

- `RUN.json`
- `HANDOFF.md`
- `STATUS.json`
- `RESULT.md`
- `events.jsonl`
- `artifacts/adapter-profile.json`
- `children/`
- `adapter-state/`

## Validation

```bash
tools/arcanum-runtime-run --adapter dry-run --handoff framework/runtime/development/fixtures/dry-run/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-dry-run
jq empty /tmp/arcanum-runtime-dry-run/RUN.json
jq empty /tmp/arcanum-runtime-dry-run/STATUS.json
```

## Blocked Conditions

- Runner unavailable.
- Handoff unreadable.
- Run directory cannot be created.
- Required runtime artifact cannot be written.

## Adapter Preference

- `adapter_id`: dry-run

## Nesting Policy

- `loop_role`: root
- `loop_id`: dry-run-fixture
- `parent_loop_id`: null
- `parent_run_id`: null
