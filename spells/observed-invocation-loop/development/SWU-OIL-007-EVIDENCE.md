# SWU-OIL-007 Evidence

## Scope

- Parent task: T-005
- Goal: add hook-driven local adapter pilot.
- Write scope: `framework/observability/scripts/run-observed-adapter-pilot.sh`

## Implemented Behavior

- Added deterministic adapter pilot script.
- The script assembles adapter closeout envelopes for:
  - skill: `arcanum-orchestrate`
  - sigil: `signal-observer`
  - spell: `invoke`
- The script calls `observe-invocation.sh` as the adapter closeout path.
- The pilot validates central telemetry rows and `by-capability` mirrors for all three kinds.
- The pilot does not rely on an agent-authored/manual observer call after the fact.

## Verification

Commands run:

```bash
chmod +x framework/observability/scripts/run-observed-adapter-pilot.sh
bash -n framework/observability/scripts/run-observed-adapter-pilot.sh
framework/observability/scripts/run-observed-adapter-pilot.sh --observability-dir <temp-dir>
```

Fixture verification checked:

- central ledger has exactly three rows,
- `by-capability/skill/arcanum-orchestrate.jsonl` exists,
- `by-capability/sigil/signal-observer.jsonl` exists,
- `by-capability/spell/invoke.jsonl` exists,
- reflection state records each pilot capability under `by_capability`.

Result:

```text
SWU_OIL_007_PILOT=pass
```

## Status

- SWU status: complete
- Parent task status: complete
- Next SWU: SWU-OIL-008
