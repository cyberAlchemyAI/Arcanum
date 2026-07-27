# SWU-IFR-005: Exact Facet Projections

## Behavior

Derive exact non-authoritative machine and human views for namespace, record
class, and concept over mixed legacy/faceted records.

## Outputs

```text
indexes.by_namespace
indexes.by_record_class
indexes.by_concept
```

## Rules

- Legacy records remain in existing maps and are absent from facet maps.
- Each faceted ID appears exactly once per applicable key.
- Array order follows canonical entry order.
- The validator independently rebuilds every map and compares exact equality.
- Human represented paths and classes must agree with the machine index.

## Exact Write Scope

```text
arcana/inventory/lib/inventory-update.cjs
arcana/inventory/scripts/validate-index-json.sh
arcana/inventory/scripts/validate_projection_conformance.py
arcana/inventory/templates/index.json
arcana/inventory/templates/index.md
arcana/inventory/test/facet-projection.test.cjs
arcana/inventory/test/fixtures/facet-projection/
```

## Validation

```sh
node --test arcana/inventory/test/facet-projection.test.cjs
bash arcana/inventory/scripts/validate-index-json.sh \
  arcana/inventory/test/fixtures/facet-projection/index.json
```

Expected receipt: `inventory.facet-projection-result.v1`.

Passing successor: `SWU-IFR-006`.
