# Fixture: strategy-carried-confirmation-medium

## Request

Continue a governed review dispatch whose exact sheet was explicitly
confirmed. The form owner then canonicalized key ordering and added derived
`n` values. The sheet SHA-256 changed, and the operator asks whether the old
confirmation can carry.

## Inputs

- Prior confirmation: explicit and complete.
- Mechanical changes: key ordering, derived counts, current evidence records.
- Current readiness: pass with a new exact digest and no ledger mutation.
- Current tension gate: independent PASS/PASS on the new digest.

## Required Behavior

- Treat the old readiness digest and tension receipts as stale machine evidence.
- Rerun readiness and both independent tension checks on the current bytes.
- Treat the prior confirmation as invalid because the exact bytes changed.
- Present the current admitted sheet and require explicit reconfirmation.
- Keep registration and execution blocked until the current digest is
  confirmed.
- Create no material-strategy or equivalence artifact.
