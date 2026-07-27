# TASK-IFR-VERIFY: Recomposition And Closure

Closure-only verification; no implementation source mutation is permitted.

## Checks

1. Every traceability row maps to a passing durable receipt.
2. Every SWU stayed inside its declared write scope.
3. L0-L3 non-regression guarantees remain true.
4. Runtime manifests exclude consumer-owned state.
5. Legacy entries remain valid and unmoved.
6. No atomicity or currentness claim appears.
7. No private path or evidence appears in public Arcanum.
8. Canonical source, generated payload, tests, docs, and observability agree.
9. The preserved interface lane remains explicit and non-current.

## Validation

```sh
node --test arcana/inventory/test/*.test.cjs
bash arcana/inventory/scripts/validate-index-json.sh \
  arcana/inventory/test/fixtures/installed-consumer/index.json
```

Output one final `pass|flag|block` audit receipt with exact evidence, residue,
and next owner. Passing closure does not authorize release or publication.
