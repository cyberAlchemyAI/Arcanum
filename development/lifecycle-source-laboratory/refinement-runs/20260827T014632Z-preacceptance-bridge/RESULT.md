# Refined Result: Plan to Preacceptance Bridge

## Outcome

The bridge cannot truthfully be `Plan source -> preacceptance manifest`. Exact final postimages do not exist at Plan time. The selected architecture is:

```text
validated Plan source
-> isolated candidate materialization
-> exact candidate/material receipt
-> deterministic acceptance-bundle compilation
-> 11 real consumers twice
-> independent review plus enforced adoption
-> exactly one owner request
-> exact acceptance
-> fresh-baseline exact-postimage apply
-> terminal, owner closeout and continuity
```

## Verdict

- Principle: PASS CONDITIONAL.
- Current implementation: BLOCK.
- Refined design and non-executed plan: PASS.
- Implementation authority: none.

## Critical blockers discovered

1. Current preacceptance regression is red because `joined_driver_digest` is required but not produced by the fixture.
2. Plan source v1 stops at WPRA and owns no candidate-finalization contract.
3. Some named consumers are schema or fixture substitutions rather than actual production transformations.
4. Request/response v2/v1 and v3/v2 families are split.
5. Attempt-scoped semantic IDs are not deterministically epoch-derived.

## Closed decisions

- Do not place final hashes or live evidence in the initial Plan source.
- Produce candidate postimages in an isolated, no-canonical-write transaction.
- Compile all deterministic preacceptance artifacts from Plan plus the exact candidate receipt.
- Keep rehearsal, review, adoption, owner decision, selection, admission and live evidence separately owned.
- Publish each deterministic preparation family atomically only after terminal PASS.
- Require actual production transformation consumers at closeout and terminal boundaries.
- Select one request/response family end to end.

## Implementation route

Use the eight ordered units in `IMPLEMENTATION-PLAN.json`, beginning with restoration of the currently red canonical regression. A future Invoke Plan must materialize exact machine contracts and pass WPRA before Task Session can be recommended.

No implementation, owner request, acceptance, selection, admission, SWU execution, Git operation, publication, release, deployment or external effect occurred.
