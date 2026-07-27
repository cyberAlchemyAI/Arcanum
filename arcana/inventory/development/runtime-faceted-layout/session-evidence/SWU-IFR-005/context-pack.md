# Context Pack: SWU-IFR-005

## Selection

- selected unit: `SWU-IFR-005`
- dependency: `SWU-IFR-004`, pass
- layer: L2 exact facet projections

## Exact Implementation Scope

```text
arcana/inventory/lib/inventory-update.cjs
arcana/inventory/scripts/validate-index-json.sh
arcana/inventory/scripts/validate_projection_conformance.py
arcana/inventory/templates/index.json
arcana/inventory/templates/index.md
arcana/inventory/test/facet-projection.test.cjs
arcana/inventory/test/fixtures/facet-projection/
```

## Obligations

- derive exact `by_namespace`, `by_record_class`, and `by_concept`;
- keep legacy records in existing maps and out of facet maps;
- preserve canonical entry order in every bucket;
- independently reconstruct admission and map equality in the validator;
- keep human path/type agreement blocking.

## Compatibility Decision

Legacy indexes with no faceted entries may omit the three maps. Once a faceted
entry or facet map exists, all three maps are required and exact. New templates
declare all three empty maps.

## Exclusions

- ontology or definition relations
- legacy migration
- generated runtime synchronization
- release or publication

## Readiness

- context: pass
- dependency: pass
- mutation scope: exact
