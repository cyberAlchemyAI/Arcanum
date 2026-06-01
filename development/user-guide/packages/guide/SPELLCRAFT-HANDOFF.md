# Guide Spellcraft Handoff

## Recommended Route

`spellcraft` for `guide-architecture`.

## Readiness

Status: `pass`

Guide now has:

- static route schema,
- static `/guide this architecture` fixture,
- Translate integration contract,
- dispatch governance seed.

First spellcraft target:

- `guide-architecture`

Deferred until spellcraft design:

- runtime dispatch budget defaults,
- allowed callable capabilities in L0.

## Candidate Spell Shape

```text
guide-architecture
  phase 1: frame target and user goal
  phase 2: select context and inspect target
  phase 3: call Translate or flag research need
  phase 4: assemble explanation sequence
  phase 5: ask active evidence prompt
  phase 6: emit guide receipt
```

## Source Artifacts

- `GUIDE-ROUTE-SCHEMA.yml`
- `GUIDE-ROUTE-FIXTURE.md`
- `GUIDE-TRANSLATE-INTEGRATION.md`
- `DISPATCH-GOVERNANCE.md`
- `development/user-guide/packages/user-ledger/USER-LEDGER-SCHEMA.yml`
- `development/user-guide/packages/translate/GUIDE-CALL-CONTRACT.md`

## Spellcraft Decision

Selected target: `guide-architecture`.

Rationale: narrow, fixture-backed, and easiest to validate from the current `/guide this architecture` route fixture. Generalize to `guide` after the architecture slice passes.
