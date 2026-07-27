# Context Pack: SWU-IFR-006

## Selection

- selected unit: `SWU-IFR-006`
- dependencies: apply observation and facet projection, pass
- layer: L3 runtime distribution

## Exact Implementation Scope

```text
arcana/inventory/runtime-manifest.json
arcana/inventory/scripts/sync-runtime.sh
arcana/inventory/test/runtime-sync.test.cjs
arcana/inventory/test/fixtures/runtime-sync/
arcana/inventory/SKILL.md
arcana/inventory/README.md
arcana/inventory/templates/package-readme.md
```

## Managed Set

- complete `bin/`, `lib/`, and `schemas/` trees;
- `scripts/validate-index-json.sh`;
- `scripts/validate_projection_conformance.py`;
- `runtime-manifest.json`.

## Forbidden Consumer Set

`entries/`, `queries/`, `raw/`, `receipts/`, `index.json`, `index.md`,
`schema.md`, `tags.md`, and `log.md`.

## Decisions

- Check mode reports sorted missing, drifted, and extra-managed paths without
  writing.
- Apply copies manifest members, removes only extras inside fully managed
  roots, writes the manifest, and then rechecks.
- The canonical manifest never self-hashes; its bundle digest binds its member
  list, and the manifest file is copied as the distribution contract.

## Exclusions

- consumer state mutation
- installed-consumer behavioral proof
- release, publication, commit, or push

## Readiness

- context: pass
- dependency: pass
- mutation scope: exact
