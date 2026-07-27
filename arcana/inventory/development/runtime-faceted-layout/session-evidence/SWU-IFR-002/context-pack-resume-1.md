# Context Pack: SWU-IFR-002 Resume 1

## Selection

- selected unit: `SWU-IFR-002`
- dependency repair: `SWU-IFR-001R`, pass
- layer: L1
- behavior: complete no-write append transition

## Bound Contracts

- one package-relative CLI;
- canonical phase-aware operation receipt;
- complete projection-conformance validator;
- accepted deterministic updater behavior;
- failure precedence from `tasks/SWU-IFR-002.md`;
- zero consumer mutation for every terminal state.

## Exact Implementation Scope

```text
arcana/inventory/bin/inventory
arcana/inventory/lib/inventory-update.cjs
arcana/inventory/test/append-dry-run.test.cjs
arcana/inventory/test/fixtures/append-dry-run/
```

## Decisions

1. The executable resolves the Inventory root from its own package path.
2. Runtime members are digested before any consumer state read.
3. Candidate validation runs in a temporary repository-shaped copy.
4. Validator reports are path-normalized before hashing.
5. A dry-run write witness is observed with `attempted=false` and equal
   expected/actual baseline digests.
6. Block states return canonical receipts and nonzero process status.

## Exclusions

- apply writes
- live repository Inventory state
- currentness or atomicity claims
- generated runtime synchronization
- facets
- promotion, release, commit, push, or publication

## Readiness

- dependency: pass
- decision gate: resolved
- write scope: exact
- mutation readiness: pass
