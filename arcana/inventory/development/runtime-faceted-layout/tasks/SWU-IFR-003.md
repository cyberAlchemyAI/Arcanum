# SWU-IFR-003: Sequential Apply Observation

## Behavior

Apply already-validated candidate bytes sequentially and report exact
success, write failure, or postwrite mismatch.

## Algorithm

1. Reconfirm baseline target digests immediately before writing.
2. Write declared projections in order and record every attempt.
3. Re-read all targets even after failure.
4. Set `committed=true` only when all candidate digests are observed.
5. Otherwise set `committed=false`,
   `possible_partial_mutation=true`, and `repair_required=true`.
6. Never claim rollback, transactionality, or atomic commit.

## Exact Write Scope

```text
arcana/inventory/bin/inventory
arcana/inventory/lib/inventory-update.cjs
arcana/inventory/test/append-apply.test.cjs
arcana/inventory/test/fixtures/append-apply/
```

Use isolated fixture targets only.

## Done

- baseline drift blocks before write;
- applied means every exact candidate digest is observed;
- first-write, second-write, and postwrite-alteration failures are distinct;
- failure receipts expose possible partial mutation and repair residue.

## Validation

```sh
node --test arcana/inventory/test/append-apply.test.cjs
```

Expected receipt: `inventory.append-apply-result.v1`.

Passing successor: `SWU-IFR-004`.
