# SWU-IFR-001R: Phase-Accurate Receipt Repair

## Behavior

Represent observed, partial, unavailable, and not-reached causal evidence in
one canonical operation receipt without sentinel hashes or a second receipt
type.

## Exact Write Scope

```text
arcana/inventory/schemas/inventory.operation-receipt.v1.schema.json
arcana/inventory/lib/operation-receipt.cjs
arcana/inventory/test/operation-receipt.test.cjs
```

## Done

- complete observed receipts preserve L0 byte determinism;
- early tooling, baseline, and request blocks validate without invented values;
- evidence-state/value contradictions fail closed;
- fingerprint and receipt digests remain reproducible;
- no clock or filesystem dependency is introduced.

## Validation

```sh
node --test arcana/inventory/test/operation-receipt.test.cjs
```

Expected receipt: `inventory.operation-receipt-phase-repair-result.v1`.

Passing successor: `SWU-IFR-002`.
