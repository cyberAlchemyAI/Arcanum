# Implementation Layering: Task Session Governance Runner

## Layer decision

This is a high-complexity lifecycle update delivered through a narrow active window.
Only L0 is selectable initially. No layer may be skipped because later automation
depends on earlier receipt semantics.

| Layer | Question | SWUs | Promotion evidence |
| --- | --- | --- | --- |
| L0 Contract | Can policy and runner envelopes be evaluated deterministically without implementation mutation? | TSGR-000, 001, 002 | lifecycle acceptance; evaluator parity; schema-negative fixtures |
| L1 Mechanism | Can one run prepare, join execution, reconcile, commit admitted bytes, and resume safely? | TSGR-003, 004, 005, 006 | deterministic prepare; structured executor join; target/write/output reconciliation; atomic commit and crash matrix |
| L2 Integration | Can owner side jobs be invoked and joined without absorbing their semantics? | TSGR-007, 008 | hook protocol fixtures; exact Continuation Router and Invoke route; cursor discrimination |
| L3 Operations | Is the prototype observable and measurably useful enough for an opt-in pilot verdict? | TSGR-009, 010 | observer dedupe; paired experiment; public scan; bounded pilot verdict |

## Promotion rules

- L0 to L1 requires `SWU-TSGR-001` and `SWU-TSGR-002` pass receipts.
- L1 to L2 requires the crash/restart and undeclared-write matrices to pass.
- L2 to L3 requires separate owner receipts to remain visible and joined.
- This work pack can emit only an opt-in pilot verdict. Recommended-path promotion,
  canonical documentation repair, and generated mirror integration require a new
  Sigil Development work pack after `TSGR-EXP-001`.

## Nested layer policy

An SWU may contain internal schema, fixture, and validator steps, but it may not
smuggle a later-layer behavior into its acceptance. In particular:

- L0 writes no implementation target;
- L1 does not implement Continuation Router or Invoke semantics;
- L2 does not claim speed or promotion;
- L3 does not rewrite historical evidence or canonical skill/mirror surfaces.

## Deferrals

- remote services and multi-host coordination;
- recursive until-blocker execution;
- policy changes unrelated to orchestration;
- performance thresholds before paired evidence;
- commit, push, publication, and promotion.
