# Invoke Maintenance Reflection: SWU Atomicity

## Trigger

Manual maintenance followed a recent medium-complexity Invoke plan that passed
structural validation but was rejected during operator review because its SWUs
were too large.

## Observed Signals

- Recent plans consistently populated dependencies, write scope, validation,
  ownership, and Distill verdict fields.
- One plan still mapped each broad coordination task to exactly one SWU.
- Its first SWU bundled semantic structure, desktop layout, mobile navigation,
  state projection, and behavior preservation despite independent acceptance
  checks for those concerns.
- Operator correction arrived after the run had already been recorded as pass,
  exposing a plan-quality false pass rather than a missing-field failure.
- Stronger recent plans kept the first handoff narrow and expanded only after a
  focused trust-building receipt.

## Diagnosis

The Invoke plan contract proved SWU completeness but not SWU atomicity. A row
could satisfy every required field while remaining task-shaped. Distill also
lacked a concrete test for whether plausible child units could pass
independently.

## Applied Improvement

1. Require one primary behavior or decision per SWU.
2. Require one independently reviewable acceptance boundary.
3. Require split analysis with candidate children and retained-boundary rationale.
4. Block task-shaped SWUs that bundle independently verifiable concerns.
5. Require the first selected SWU to be the narrowest reversible trust-building step.
6. Add passing and blocking validation-fixture coverage.

## Validation Target

- Canonical and generated plan contracts remain synchronized.
- The Invoke validation fixture suite passes.
- The blocking fixture rejects a shell + desktop + mobile + mapper first SWU.
- The refreshed target plan reports zero task-shaped SWUs and names one narrow first unit.

## Deferred Improvement

Observability currently records an Invoke result before later operator
corrections are known. A separate maintenance pass should evaluate append-only
post-run correction signals rather than rewriting original run receipts.
