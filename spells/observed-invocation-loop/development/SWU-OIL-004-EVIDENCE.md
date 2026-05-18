# SWU-OIL-004 Evidence

## Scope

- Parent task: T-002
- Goal: delegate experiment harness observation to the generic observer.
- Write scope: `arcana/experiment-harness/scripts/observe-harness.sh`

## Implemented Behavior

- Experiment harness still owns report parsing.
- Experiment harness now assembles an invocation envelope with:
  - `run_id`,
  - `session_id`,
  - legacy `sigil`,
  - generic `capability.id`,
  - generic `capability.kind`,
  - execution status,
  - validation evidence,
  - quality and workflow gap fields.
- Experiment harness now calls `framework/observability/scripts/observe-invocation.sh` for append, dedupe, threshold, mirror, hook operation, and reflection-state behavior.
- Experiment harness preserves compatibility output fields:
  - `OBSERVATION`
  - `LEDGER`
  - `PER_SIGIL_LEDGER`
  - `REFLECTION_TRIGGER`
  - `RECOMMENDATION`
  - `RUN_ID`
  - `DEDUPE_KEY`

## Verification

Commands run:

```bash
bash -n arcana/experiment-harness/scripts/observe-harness.sh
```

Focused fixture checked:

- first observation returns `OBSERVATION=recorded`,
- second observation returns `OBSERVATION=skipped`,
- threshold trigger is emitted through generic observer,
- central ledger has exactly one row,
- `by-sigil/experiment-harness.jsonl` has exactly one row,
- `by-capability/sigil/experiment-harness.jsonl` has exactly one row,
- reflection state updates `by_capability.sigil.experiment-harness`.

Result:

```text
SWU_OIL_004_FOCUSED=pass
FIRST=recorded
SECOND=skipped
TRIGGER=usage-threshold
```

Full experiment harness phase gates:

```bash
arcana/experiment-harness/development/run-phase-gates.sh
```

Result:

```text
Phase 0: pass
Phase 1: pass
Phase 2: pass
Phase 3: pass
Phase 4: pass
Phase 5: pass
Phase 6: pass
Phase 7: pass
REPORT=arcana/experiment-harness/development/runs/20260518T120123Z.md
```

## Status

- SWU status: complete
- Parent task status: complete
- Next SWU: SWU-OIL-005
