# S05 Distill

Status: pass

Selected unit: projection contract before generator implementation.

Alternatives considered:

- JSON-only: good read path, weak human edit support.
- CSV-first: useful for editing, too risky without authority/freshness rules.
- SQLite/service-backed ledger: too much runtime surface for this layer.

Selected route: derived JSON index plus derived CSV projections.

Recomposition proof: the route preserves Craft's existing source-of-truth policy
and can recompose into later generator/import SWUs.
