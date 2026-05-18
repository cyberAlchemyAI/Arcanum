# SWU-OIL-001 Evidence

## Scope

- Parent task: T-001
- Goal: add generic envelope validation and central ledger append path.
- Write scope: `framework/observability/scripts/observe-invocation.sh`

## Implemented Behavior

- Added `observe-invocation.sh`.
- Accepts `--envelope <path>`.
- Accepts optional `--observability-dir <path>`.
- Validates required envelope fields with `jq`.
- Supports legacy sigil-shaped envelopes.
- Supports capability-shaped envelopes with `capability.id` and `capability.kind`.
- Preserves legacy top-level `sigil` compatibility.
- Appends to `signals/sigil-invocations.jsonl`.
- Mirrors to `by-sigil/<id>.jsonl`.
- Mirrors to `by-capability/<kind>/<id>.jsonl`.

## Deferred To Later SWUs

- Hook operation recording: SWU-OIL-002.
- Dedupe behavior: SWU-OIL-002.
- Threshold evaluation and reflection state updates: SWU-OIL-003.
- Reflection report runner: SWU-OIL-005.

## Verification

Commands run:

```bash
chmod +x framework/observability/scripts/observe-invocation.sh
bash -n framework/observability/scripts/observe-invocation.sh
```

Fixture verification used a temporary observability directory and checked:

- legacy `sigil` envelope appends successfully,
- `capability.kind = spell` envelope appends successfully,
- invalid envelope fails,
- central ledger is created,
- `by-sigil` mirror is created,
- `by-capability/sigil` mirror is created,
- `by-capability/spell` mirror is created.

Result:

```text
SWU_OIL_001_FIXTURES=pass
```

## Status

- SWU status: complete
- Parent task status: in progress
- Next SWU: SWU-OIL-002
