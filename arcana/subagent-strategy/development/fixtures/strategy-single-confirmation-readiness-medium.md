# Fixture: strategy-single-confirmation-readiness-medium

## Request

Propose a governed research dispatch. The first draft contains two pooled
explorers, a named external final approver, and pairwise disagreement prose in
`STRATEGY.md` rather than the persisted dispatch sheet. The human has not been
asked to confirm.

## Inputs

- P1 trigger: synthesis and parallelism.
- Dispatch type owner: live research capability.
- Canonical form owner: schema `0.8.0`.
- Agent pool: readable; both explorers are eligible and unique.
- First draft final approver: `Independent Maintainer`, not pooled and not a
  singleton auditor group.
- First draft pair evidence: companion-only.
- Tension gate: available.
- Human confirmation: not yet requested.

## Required Behavior

- Block the first draft before tension or confirmation.
- Explain that companion prose cannot satisfy digest-owned pair evidence.
- Replace the arbitrary approver with `parent` or a valid pooled singleton
  auditor.
- Add complete canonical `predicted_disagreements` records to the sheet.
- Revalidate the exact sheet with no ledger mutation.
- Give both tension agents only the sheet bytes, digest, and rubric.
- Preserve both independent verdicts before any checker/reviewer comparison.
- Ask for confirmation exactly once after PASS/PASS.
- Register immediately if the confirmed digest remains unchanged.
- Keep a genuine post-confirmation byte edit fail-closed.
