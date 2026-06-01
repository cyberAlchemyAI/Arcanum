# Runtime Handoff

Schema discipline: keep this handoff as immutable request context. Runtime status, schema version, events, and adapter evidence belong in `RUN.json`, `STATUS.json`, `events.jsonl`, and `artifacts/`.

## Objective

<Describe the work the runtime should execute or validate.>

## Orchestrator

- `orchestrator_id`: manual
- `orchestrator_run_id`: null

## Target

- `target_kind`: manual
- `target_id`: runtime-target

## Inputs

- <Input artifacts or paths.>

## Allowed Write Scope

- <Allowed write paths, or `none` for dry validation.>

## Expected Outputs

- `RESULT.md`

## Validation

- <Validation command or reviewable evidence.>

## Blocked Conditions

- Missing handoff.
- Missing required adapter.
- Missing write scope.
- Missing required runtime inputs.

## Adapter Preference

- `adapter_id`: dry-run

## Nesting Policy

- `loop_role`: root
- `loop_id`: runtime-loop
- `parent_loop_id`: null
- `parent_run_id`: null
