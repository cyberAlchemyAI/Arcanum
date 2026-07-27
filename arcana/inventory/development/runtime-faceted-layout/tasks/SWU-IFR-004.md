# SWU-IFR-004: Faceted New-Record Admission

## Behavior

Admit stable namespace-first paths for new faceted records while preserving
every legacy path and validation rule.

New path:

```text
entries/<namespace>/<record-class>/<stable-id>.md
```

## Rules

- `namespace` and `record_class` are single-valued, controlled, and path-safe.
- `concepts` is non-empty, normalized, deduplicated, byte-sorted, and
  multi-valued.
- Stable ID remains independent of the physical path.
- Partial facet metadata, traversal, unknown class, empty concept, normalized
  duplicates, and path mismatch block.
- Tag or concept combinations never create directories.
- Legacy records without facet fields pass unchanged.

## Exact Write Scope

```text
arcana/inventory/templates/index.schema.yml
arcana/inventory/templates/entry.md
arcana/inventory/templates/schema.md
arcana/inventory/lib/inventory-update.cjs
arcana/inventory/test/facet-admission.test.cjs
arcana/inventory/test/fixtures/facet-admission/
```

## Validation

```sh
node --test arcana/inventory/test/facet-admission.test.cjs
```

Expected receipt: `inventory.facet-admission-result.v1`.

Passing successor: `SWU-IFR-005`.
