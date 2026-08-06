# Fixture: strategy-carried-confirmation-medium

## Request

Continue a governed review dispatch whose complete material strategy was
explicitly confirmed. The form owner then canonicalized key ordering, added
derived `n` values and digest-bound predicted-disagreement records that encode
the already-presented anti-bias choices. The sheet SHA-256 changed.

## Inputs

- Prior confirmation: explicit and complete.
- Prior and current material-strategy projections: deterministic match.
- Mechanical changes: key ordering, derived counts, current evidence records.
- Material changes: none.
- Current readiness: pass with a new exact digest and no ledger mutation.
- Current tension gate: independent PASS/PASS on the new digest.
- Equivalence validator: pass with a durable receipt.

## Required Behavior

- Treat the old readiness digest and tension receipts as stale machine evidence.
- Rerun readiness and both independent tension checks on the current bytes.
- Preserve the material-equivalence receipt.
- Carry the prior human confirmation and attach it to the current digest for
  registration.
- Do not ask the human to reconfirm solely because bytes changed.
- Require reconfirmation if any material field changed or equivalence were
  unknown.
