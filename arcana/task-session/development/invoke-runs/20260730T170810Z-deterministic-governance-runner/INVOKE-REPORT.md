# Invoke Report: Deterministic Task Session Governance Runner

Run: `20260730T170810Z-deterministic-governance-runner`  
Modes: Define -> Design -> Plan  
Result: `PASS` for lifecycle review; implementation not started

## Outcome

The package defines a deterministic Task Session governance runner as an update to
the existing sigil. It is a bounded, checkpointed CLI—not a daemon—and composes
existing policy, admission, continuation, Invoke, and observation owners.

The initial “one script” idea became a high-complexity implementation graph because
safe write application, crash recovery, and owner hooks require distinct acceptance
boundaries. The plan keeps each boundary small and provides useful prototype
frontiers before the whole graph is complete.

## Principal decision

Productionize the current pure governance evaluator first. Do not build the
mutation-capable controller until policy parity and closed envelope contracts pass.

## Design selection

Fixed-point `pass`. Selected concerns:

- authority/trust;
- state/event;
- persistence/concurrency;
- integration/versioning;
- rollout;
- privacy/data lifecycle;
- operator UX;
- validation.

Performance remains recommended rather than required because “faster” is not yet
measured.

## Plan

- 1 lifecycle SWU plus 10 implementation SWUs;
- four ordered layers;
- first selected SWU: `SWU-TSGR-000`;
- first implementation SWU: read-only/new-path `SWU-TSGR-001`;
- final output: bounded opt-in pilot verdict;
- canonical docs, generated mirrors, publication, and promotion deferred.

## Validation

- Design fixed-point validator: pass.
- Plan package validator: pass.
- Dispatch Spec: pass, no flags.
- Independent Standard Distill: initial block repaired, digest flag repaired, final
  pass.
- Existing Task Session suites: 25/25 policy, 11/11 nearest, 23/23 admission.
- Continuation Router: 6/6.
- JSON and scoped whitespace checks: pass.

## Open dependency

Continuation Router does not currently expose a production launcher. TSGR-008 blocks
until the readiness receipt defined in `OWNER-READINESS.md` exists. This does not
block lifecycle review or earlier prototype units.

## Mutation and publication statement

Only this new Invoke planning package was authored. Existing dirty canonical Task
Session changes were not normalized or overwritten. No runtime implementation,
generated mirror, commit, push, publication, deployment, or promotion occurred.

## Next

Sigil Development should review `SIGIL-DEVELOPMENT-HANDOFF.md` and decide
`SWU-TSGR-000`.

