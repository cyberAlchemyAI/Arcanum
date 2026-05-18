# SWU-OIL-005 Evidence

## Scope

- Parent task: T-003
- Goal: add deterministic reflection report runner from signal ledger.
- Write scope: `framework/observability/scripts/reflect-invocation-signals.sh`

## Implemented Behavior

- Added `reflect-invocation-signals.sh`.
- Supports:
  - `--all`
  - `--capability <id>`
  - `--kind skill|sigil|spell`
  - `--since <iso-date>`
  - `--min-signals <n>`
  - `--dry-run`
  - `--observability-dir <path>`
- Reads `.arcanum/observability/signals/sigil-invocations.jsonl`.
- Filters by capability, kind, and timestamp.
- Skips when signal count is below `--min-signals`.
- Skips when no threshold-backed reflection evidence exists.
- Writes reflection reports under `.arcanum/observability/reflections/`.
- Updates `reflection-state.json` only after report write succeeds.
- Does not edit observed capabilities.

## Machine Output

The runner prints:

```text
REFLECTION=written|skipped|failed
REASON=<threshold-hit|manual|insufficient-signals|invalid-ledger|...>
SIGNALS_ANALYZED=<n>
THRESHOLDS_TRIGGERED=<csv-or-none>
REPORT=<path-or-n/a>
STATE=updated|unchanged|unavailable
```

## Verification

Commands run:

```bash
chmod +x framework/observability/scripts/reflect-invocation-signals.sh
bash -n framework/observability/scripts/reflect-invocation-signals.sh
```

Fixture verification checked:

- threshold-backed signal writes a reflection report,
- report file exists and is non-empty,
- reflection state `last_reflection_at` updates after report write,
- insufficient signals return `REFLECTION=skipped` and `REASON=insufficient-signals`,
- dry run returns `REFLECTION=skipped` and `REASON=dry-run`,
- dry run writes no report,
- malformed JSONL returns `REFLECTION=failed` and `REASON=invalid-ledger`.

Result:

```text
SWU_OIL_005_FIXTURES=pass
WRITE=written
INSUFFICIENT=insufficient-signals
DRY=dry-run
```

## Status

- SWU status: complete
- Parent task status: complete
- Next SWU: SWU-OIL-006
