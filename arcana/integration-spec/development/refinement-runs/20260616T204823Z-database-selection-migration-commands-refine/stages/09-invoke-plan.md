# Invoke Plan: Next Routes

Status: pass
Owner capability: invoke
Mode: plan

## Recommended Sequence

1. Extend the next L0 `INTEGRATION-BOUNDARY-DISCIPLINE.md` with the two records from this run.
2. Fill one concrete example: payment database selection plus migration command profile.
3. Add failing fixtures before validator work.
4. Add tool-specific profile cards only after the generic profile stabilizes.
5. Route `integrations.md` and formula validator work after examples prove stable.

## Minimum Example

Payment service:

- `CreatePayment` writes local payment state.
- Provider webhook updates eventual status.
- Relational store is local authority for payment ledger.
- Cache is non-authoritative and invalidated by payment state changes.
- Search or analytics projection is derived and rebuildable.
- Migration command profile blocks production reset/clean/drop.
- Deployment uses reviewed migration artifacts, drift/status validation, lock policy, dry-run or SQL plan, expand/contract compatibility, and roll-forward plan.

## Fixture Candidates

- pass: relational local authority with reviewed migration deploy.
- pass: cache with TTL, invalidation, stale-read policy, and reconciliation.
- flag: polyglot store without operational ownership.
- flag: checksum mismatch with repair proposed but no owner approval.
- flag: irreversible rollback with unclear recovery limits.
- block: missing source-of-truth role.
- block: search/vector/analytics store treated as primary authority without decision.
- block: production reset/clean/drop.
- block: destructive migration without approval, backup/restore, and affected-row/object estimate.
- block: lock release without owner evidence.
- block: runtime receipt promoted as DomainSpec truth.
