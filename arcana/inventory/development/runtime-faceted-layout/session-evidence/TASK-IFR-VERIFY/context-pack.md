# Context Pack: TASK-IFR-VERIFY

## Selection

- selected unit: `TASK-IFR-VERIFY`
- dependency: `SWU-IFR-007`, pass
- mode: closure-only verification
- implementation mutation: forbidden

## Required Evidence

| Obligation | Evidence surface |
| --- | --- |
| traceability | `TRACEABILITY.md` plus current SWU receipts |
| exact scopes | task files, receipt file lists, scoped Git diff |
| L0-L3 non-regression | complete Node test suite |
| manifest ownership | manifest and runtime-sync negative fixtures |
| legacy preservation | facet admission/projection tests |
| claim boundary | public text scan and receipt residue |
| public/private boundary | installed-consumer boundary test and direct scan |
| source/install agreement | manifest digest validation and isolated sync check |
| observability | invocation ledger run IDs and reflection state |
| deferred lane | root `WORK-PACK.md` lifecycle selection |

## Closure Commands

```sh
node --test arcana/inventory/test/*.test.cjs
bash arcana/inventory/scripts/validate-index-json.sh \
  arcana/inventory/test/fixtures/installed-consumer/index.json
```

## Boundaries

- Passing closure does not authorize release, publication, commit, or push.
- Atomicity, currentness verification, and legacy migration remain excluded.
- Inventory output remains a read model, not semantic or promotion authority.
