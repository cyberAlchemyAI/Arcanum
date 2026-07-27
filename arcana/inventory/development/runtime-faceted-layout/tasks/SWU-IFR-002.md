# SWU-IFR-002: No-Write Append Transition

## Behavior

Compute a complete baseline-to-candidate append receipt from any working
directory while proving zero consumer mutation.

## Algorithm

1. Resolve runtime root from the executable and verify required members.
2. Read and digest the exact baseline `index.json` and `index.md`.
3. Run the complete baseline validator.
4. Normalize the candidate record.
5. Return identical no-op or ID conflict when applicable.
6. Stage candidate projections outside consumer targets.
7. Run the complete candidate validator.
8. Derive stable introduced, resolved, and inherited warning sets.
9. Build the canonical receipt and re-prove target digests are unchanged.

Failure precedence:

```text
tooling-unavailable
> baseline-blocked
> invalid-request
> identical-no-op | id-conflict
> candidate-blocked
> dry-run-ready
```

## Exact Write Scope

```text
arcana/inventory/bin/inventory
arcana/inventory/lib/inventory-update.cjs
arcana/inventory/test/append-dry-run.test.cjs
arcana/inventory/test/fixtures/append-dry-run/
```

## Done

- unrelated-CWD execution passes;
- warning delta is exact;
- no-op/conflict/block receipts are deterministic;
- repeated receipts are byte-identical;
- every dry-run outcome proves zero mutation.

## Validation

```sh
node --test arcana/inventory/test/append-dry-run.test.cjs
```

Expected receipt: `inventory.append-dry-run-result.v1`.

Passing successor: `SWU-IFR-003`.
