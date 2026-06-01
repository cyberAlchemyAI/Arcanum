# Guide Handoff

## Recommended Next Route

`spellcraft` for `guide`, after User and Translate L0 evidence exists.

## Start With

Do not start Guide implementation first.

Required prerequisites:

- `user-ledger/SWU-USER-001`
- `translate/SWU-TRANSLATE-002`

Then start:

- `SWU-GUIDE-001`: static `/guide this architecture` route fixture.

## Source Artifacts

- `DEFINE.md`
- `DESIGN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `development/user-guide/refinement-runs/20260529T132348Z-translate-before-guide/RESULT.md`

## Guardrails

- Guide orchestrates; it does not own Translate internals.
- Guide can dispatch research/subagents only through explicit budget/gate rules.
- Guide returns receipts; User owns durable ledger updates.
