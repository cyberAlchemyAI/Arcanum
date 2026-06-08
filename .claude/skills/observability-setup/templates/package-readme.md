# Sigil Observability

This package stores local telemetry for sigil usage in this repository.

## Files

- `config.json` defines storage model and reflection thresholds.
- `reflection-state.json` tracks counters since the last reflection.
- `signals/sigil-invocations.jsonl` is the central append-only invocation ledger.
- `by-sigil/` and `by-capability/` hold rebuildable indexes that point back to central ledger rows.
- `hooks/hook-operations.jsonl` tracks background extraction, observer, append, and dedupe hook work.
- `hooks/failures.jsonl` tracks hook failures without changing primary task results.
- `runs/` stores observed run bundles and checkpoints for long-running work.
- `reflections/` can hold reflection reports.

## Default Model

The default storage model is central-ledger-reference-indexes: use the central ledger as the source of truth and rebuild compact lookup indexes for focused reflection.

## Privacy

Do not store secrets, credentials, tokens, private keys, or unnecessary raw request content in telemetry.

## Loop Guard

Hook operation rows are operational audit data and must not trigger normal sigil observation. Capability telemetry and hook telemetry stay separate.
