# Invoke Maintenance Reflection: Refresh Phase Status

## Trigger

Manual maintenance followed repeated proposal-only Refresh runs whose generated proposals were complete but whose authored phase status was lowered because application or downstream validation still remained.

## Observed Signals

- Invoke had sufficient accumulated execution history for pattern-level reflection.
- Several proposal-only outputs correctly used `pass` for a complete proposal with a gated next route.
- At least two comparable outputs used `flag` even though their only remaining conditions were apply authorization or later lifecycle work.
- A separate flagged example was valid because unresolved artifact authority prevented an exact safe proposal.
- Existing telemetry could report execution and quality as passing while omitting the conflicting authored phase status.

## Diagnosis

Refresh status described two different things at once: whether the current Refresh artifact was complete and whether its next lifecycle route was ready. Blocker lists also mixed authoring ambiguity, apply permission, target work, and audit obligations without a machine-readable scope.

## Applied Improvement

1. Define phase status as completion of the current Refresh artifact.
2. Report handoff readiness independently as ready, gated, deferred, blocked, or not needed.
3. Type blockers as refresh authoring, apply authorization, target lifecycle, or audit.
4. Preserve `pass` for an exact proposal-only artifact even when later gates remain.
5. Require a refresh-authoring blocker before a proposal-only artifact may use `flag` or `block`.
6. Prevent proposal-only validator evidence from authorizing mutation handoff.
7. Add apply-approved pass, proposal-only pass, and downstream-only false-flag controls.
8. Carry phase status, basis, handoff status, and blocker scopes into Refresh observability obligations.

## Validation Evidence

- `run-validation-fixtures.sh` passes all deterministic fixtures, including five Refresh scenarios.
- `run-distill-active-mode-evidence-fixtures.sh` passes 13 checks.
- The machine controls accept an apply-approved pass with mutation handoff.
- The machine controls accept a complete proposal-only pass without mutation handoff.
- The machine controls accept a proposal-only flag when a refresh-authoring blocker remains.
- The machine controls reject a proposal-only flag whose blockers are only apply authorization and target lifecycle.

## Contract Preservation

- Proposal-only remains the default.
- A passing proposal never grants permission to apply it.
- Apply-approved still requires explicit scoped approval and validation.
- No-op remains valid.
- Refresh still does not execute target tasks, downstream lifecycles, or audits.

## Deferred Evidence

No live Refresh stability regime was run for this targeted reflection. Deterministic controls prove the repaired classification and authorization relationships; they do not constitute new promotion evidence for deferred `full` or `validate` modes.

## Decision

Keep the Invoke core workflow. Adopt the targeted Refresh phase-status, blocker-scope, handoff, and observability repair.
