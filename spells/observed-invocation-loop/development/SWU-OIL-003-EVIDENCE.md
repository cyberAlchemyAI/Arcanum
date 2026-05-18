# SWU-OIL-003 Evidence

## Scope

- Parent task: T-001
- Goal: add threshold evaluation and reflection counter updates.
- Write scope: `framework/observability/scripts/observe-invocation.sh`

## Implemented Behavior

- Generic observer now reads `.arcanum/observability/config.json` when available.
- Generic observer now reads and updates `.arcanum/observability/reflection-state.json` when available.
- Threshold evaluation occurs before telemetry append, so emitted events carry the final `reflection_trigger` and `recommendation`.
- Duplicate observations skip before reflection state mutation, preserving counters.
- Counters updated:
  - `meaningful_executions`
  - `generated_outputs`
  - `related_workflow_gaps`
  - `severe_workflow_gaps`
  - `quality_bar_failures`
  - `output_contract_drift_events`
- Per-capability state updates:
  - `by_sigil.<id>`
  - `by_capability.<kind>.<id>`
- Machine output now includes:
  - `REFLECTION_TRIGGER`
  - `RECOMMENDATION`
  - `REFLECTION_STATE`

## Deferred To Later SWUs

- Reflection report runner: SWU-OIL-005.
- Experiment harness delegation: SWU-OIL-004.
- Adapter contract and pilots: SWU-OIL-006 and SWU-OIL-007.

## Verification

Commands run:

```bash
bash -n framework/observability/scripts/observe-invocation.sh
```

Fixture verification used temporary observability directories and checked:

- usage threshold emits `REFLECTION_TRIGGER=usage-threshold`,
- usage threshold sets `RECOMMENDATION=reflect-now`,
- reflection state updates meaningful execution and generated output counters,
- per-sigil and per-capability counters update,
- duplicate observation returns `OBSERVATION=skipped`,
- duplicate observation does not update counters,
- severe workflow gap emits `REFLECTION_TRIGGER=severe-gap`,
- severe gap updates severe gap, quality failure, and output drift counters.

Result:

```text
SWU_OIL_003_FIXTURES=pass
USAGE_TRIGGER=usage-threshold
DUPLICATE=skipped
SEVERE_TRIGGER=severe-gap
```

## Status

- SWU status: complete
- Parent task status: complete
- Next SWU: SWU-OIL-004
