# SWU-IFR-006: Manifest-Bound Runtime Sync

## Behavior

Check or synchronize only the generated Inventory runtime payload and prove
consumer-owned state remains outside the managed set.

Managed payload:

```text
bin/
lib/
schemas/
scripts/validate-index-json.sh
scripts/validate_projection_conformance.py
runtime-manifest.json
```

Forbidden managed roots:

```text
entries/
queries/
raw/
receipts/
index.json
index.md
schema.md
tags.md
log.md
```

## Exact Write Scope

```text
arcana/inventory/runtime-manifest.json
arcana/inventory/scripts/sync-runtime.sh
arcana/inventory/test/runtime-sync.test.cjs
arcana/inventory/test/fixtures/runtime-sync/
arcana/inventory/SKILL.md
arcana/inventory/README.md
arcana/inventory/templates/package-readme.md
```

## Done

- check reports exact missing/drifted/extra-managed members and writes nothing;
- apply changes only allowlisted generated members;
- post-sync digests match;
- consumer-owned negative-fixture digests remain unchanged.

## Validation

```sh
node --test arcana/inventory/test/runtime-sync.test.cjs
```

Expected receipt: `inventory.runtime-sync-result.v1`.

Passing successor: `SWU-IFR-007`.
