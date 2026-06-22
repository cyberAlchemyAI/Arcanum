# Iteration And Stop Policy

## Iteration Policy

1. Read `handoff-pack.md`, `handoff-index.json`, and `WORK-PACK.md`.
2. Execute W0 first.
3. Continue to W1 only if W0 passes or an accepted repair path is recorded.
4. Continue to W2 only if W1 passes.
5. Continue to W3 only if W2 passes.
6. Attempt one SWU at a time and record a receipt before moving on.
7. Refresh or stop when a task changes source/design/plan contracts enough to
   invalidate the handoff pack.

## Stop Conditions

Stop blocked when:

- W0 Spellcraft validation blocks,
- runtime source/write scope is not selected for a runtime SWU,
- approval token or decision record is missing for protected apply,
- Craft mutation would occur without staged proposal and approval,
- reusable behavior evidence is absent but registry readiness is requested,
- generated-surface ownership is unclear,
- private profile contents would enter public artifacts,
- any SWU lacks a terminal receipt,
- validation cannot prove the current layer.

## Blocked Report Rule

Blocked report must include:

- active wave and SWU,
- blocker reason,
- evidence inspected,
- owner,
- exact unblock action,
- residue,
- reroute,
- whether previous SWUs remain valid.
