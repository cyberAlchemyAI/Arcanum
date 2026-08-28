# Fixture: strategy-form-version-drift-medium

## Request

Propose a governed review using a repository-local runtime profile. A selected
personal runtime says the dispatch form is version `0.6.0`, while the
repository's canonical form owner and non-mutating validator require `0.7.0`.
No human confirmation has been requested yet.

## Inputs

- P1 trigger: synthesis and independent checking.
- Dispatch type owner: live review capability.
- Candidate sheet: persisted from the stale runtime.
- Canonical local form owner: readable.
- Confirmation-readiness validator: available and non-mutating.
- Human confirmation: not yet requested.

## Required Behavior

- Surface the version mismatch as a warning.
- Do not ask the human to confirm the stale sheet.
- Rematerialize the candidate from the canonical local form owner.
- Validate the exact persisted current-form bytes without writing the ledger.
- Run both tension checks against the admitted digest.
- Ask for confirmation once.
- Keep any post-confirmation byte change fail-closed.
