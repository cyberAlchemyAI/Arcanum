# SWU-OIL-002 Evidence

## Scope

- Parent task: T-001
- Goal: add hook operation and dedupe behavior to the generic observer.
- Write scope: `framework/observability/scripts/observe-invocation.sh`

## Implemented Behavior

- Generic observer now records hook operations through `record-hook-operation.sh`.
- Each observation records a `started` hook row.
- Successful telemetry append records a completed `append` hook row.
- Duplicate observation for the same target run and observer version records a skipped `append` hook row.
- Duplicate observation does not append a second central telemetry row.
- Duplicate observation does not append duplicate `by-sigil` or `by-capability` rows.
- Hook operation rows carry `observe:false` through the hook recorder.

## Dedupe Key

The dedupe key uses:

```text
<target-run-id>:signal-observer:<observer-version>
```

`target-run-id` comes from `run_id`, `id`, or `target_run_id` when present. When no run id exists, the observer derives a stable fallback from session, capability, timestamp, and envelope path.

## Deferred To Later SWUs

- Threshold evaluation and reflection state updates: SWU-OIL-003.
- Reflection report runner: SWU-OIL-005.

## Verification

Commands run:

```bash
bash -n framework/observability/scripts/observe-invocation.sh
```

Fixture verification used a temporary observability directory and checked:

- first observation returns `OBSERVATION=recorded`,
- second observation with same envelope and observer version returns `OBSERVATION=skipped`,
- central ledger has exactly one row,
- `by-capability/spell/invoke.jsonl` has exactly one row,
- `by-sigil/invoke.jsonl` has exactly one row,
- hook operations include started/completed/skipped rows with `observe:false`,
- dedupe ledger has exactly one row.

Result:

```text
SWU_OIL_002_FIXTURES=pass
FIRST=recorded
SECOND=skipped
```

## Status

- SWU status: complete
- Parent task status: in progress
- Next SWU: SWU-OIL-003
