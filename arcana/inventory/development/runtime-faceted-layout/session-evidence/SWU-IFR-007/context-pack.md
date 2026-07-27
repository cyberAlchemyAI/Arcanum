# Context Pack: SWU-IFR-007

## Selection

- selected unit: `SWU-IFR-007`
- dependency: `SWU-IFR-006`, pass
- layer: L3 installed-consumer proof

## Exact Implementation Scope

```text
arcana/inventory/test/installed-consumer.test.cjs
arcana/inventory/test/fixtures/installed-consumer/
arcana/inventory/development/runtime-faceted-layout/session-evidence/SWU-IFR-007/
```

## Proof Classes

1. manifest install and unrelated working directory;
2. warning-delta attribution;
3. deterministic repeated dry run;
4. zero mutation;
5. identical no-op and conflict;
6. apply success and injected partial failure;
7. faceted admission and mixed legacy projection;
8. runtime sync drift repair;
9. public/private boundary scan.

## Boundaries

- All consumers are generic temporary repositories.
- Installed paths, not canonical module paths, execute runtime behavior.
- The live repository-local `.arcanum/inventory/` is forbidden.
- The proof authorizes closure review only, not release or publication.

## Readiness

- context: pass
- dependency: pass
- mutation scope: exact
