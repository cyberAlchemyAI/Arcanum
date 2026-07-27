# Context Pack: SWU-IFR-003

## Selection

- selected unit: `SWU-IFR-003`
- dependency: `SWU-IFR-002`, pass
- layer: L2 apply observation

## Exact Implementation Scope

```text
arcana/inventory/bin/inventory
arcana/inventory/lib/inventory-update.cjs
arcana/inventory/test/append-apply.test.cjs
arcana/inventory/test/fixtures/append-apply/
```

## Obligations

- recompute baseline digests immediately before writing;
- write `index.json` then `index.md`;
- observe both targets after every attempt or failure;
- claim `committed=true` only for exact candidate digests;
- expose first-write, second-write, and postwrite mismatch separately;
- make partial mutation and repair requirements explicit;
- use isolated fixtures only.

## Decisions

Failure injection is a library test hook, not a CLI flag. The public command
performs the same sequential algorithm without exposing test controls.

## Exclusions

- atomicity, rollback, journaling, or locking
- live repository Inventory state
- facets or runtime synchronization
- currentness or promotion claims

## Readiness

- context: pass
- dependency: pass
- mutation scope: exact
