# Context Pack: SWU-IFR-001R

## Lifecycle Decision

- mode: Sigil Development update
- decision: Option A, one phase-aware receipt schema
- evidence: `../SWU-IFR-002/decision-gate.md`
- selected unit: `SWU-IFR-001R`
- successor on pass: `SWU-IFR-002`

## Obligations

1. Keep one canonical `inventory.operation-receipt.v1` stream.
2. Model evidence availability explicitly.
3. Require digests only when their evidence was observed.
4. Reject contradictory state/value combinations.
5. Preserve canonical byte and digest rules.

## Exact Implementation Scope

```text
arcana/inventory/schemas/inventory.operation-receipt.v1.schema.json
arcana/inventory/lib/operation-receipt.cjs
arcana/inventory/test/operation-receipt.test.cjs
```

## Exclusions

- append CLI or transition behavior
- consumer Inventory access
- generated runtime synchronization
- sentinel hashes
- release, publication, commit, or push

## Readiness

- lifecycle owner: approved
- decision gate: resolved as Option A
- mutation scope: bounded
- implementation readiness: pass
