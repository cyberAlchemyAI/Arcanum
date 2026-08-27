# Sigil Observability

This repository-local package stores Arcanum command, sigil, and spell telemetry plus reflection state.

- signals/sigil-invocations.jsonl is the central append-only invocation ledger.
- by-sigil/ and by-capability/ are rebuildable lookup indexes that point to central ledger rows.
- hooks/ stores hook operation evidence.
- subagents-strategy/subagents-dispatch.yaml stores append-only confirmed dispatch and close rows; the registrar creates it lazily.
- runs/ stores pending and completed observer envelopes.
- reflections/ can hold future reflection reports.
