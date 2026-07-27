# SWU-IFR-007: Isolated Installed-Consumer Proof

## Behavior

Reproduce the complete approved runtime in a generic temporary consumer
without mutating the live repository Inventory.

## Required Proof Classes

- package-relative unrelated working directory;
- warning-delta attribution;
- deterministic repeated dry-run;
- zero mutation;
- no-op/conflict;
- apply success and injected partial failure;
- faceted admission and mixed legacy projection;
- runtime sync drift;
- public/private boundary scan.

## Exact Write Scope

```text
arcana/inventory/test/installed-consumer.test.cjs
arcana/inventory/test/fixtures/installed-consumer/
arcana/inventory/development/runtime-faceted-layout/session-evidence/SWU-IFR-007/
```

Forbidden:

- live `.arcanum/inventory/` state;
- private paths or evidence in public Arcanum.

## Validation

```sh
node --test arcana/inventory/test/installed-consumer.test.cjs
```

Expected receipt: `inventory.installed-consumer-proof.v1`.

Passing successor: `TASK-IFR-VERIFY`.
