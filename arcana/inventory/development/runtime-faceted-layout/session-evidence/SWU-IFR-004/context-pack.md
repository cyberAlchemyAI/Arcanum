# Context Pack: SWU-IFR-004

## Selection

- selected unit: `SWU-IFR-004`
- dependencies: `SWU-IFR-002` and lifecycle order after 003, pass
- layer: L2 faceted admission

## Exact Implementation Scope

```text
arcana/inventory/templates/index.schema.yml
arcana/inventory/templates/entry.md
arcana/inventory/templates/schema.md
arcana/inventory/lib/inventory-update.cjs
arcana/inventory/test/facet-admission.test.cjs
arcana/inventory/test/fixtures/facet-admission/
```

## Decisions

- Facet metadata is optional for legacy records and all-or-nothing for new
  faceted records.
- Public code contains generic token rules and default record classes only.
- Allowed namespaces and class extensions come from local index validation
  configuration.
- Concepts normalize to lowercase hyphenated tokens; normalization collisions
  block rather than silently deduplicate.
- The path is derived from namespace, record class, and stable ID only.

## Exclusions

- legacy path migration
- facet-derived indexes
- ontology meaning or promotion
- consumer state outside isolated fixtures

## Readiness

- context: pass
- dependency: pass
- mutation scope: exact
