# Decision TSGR-APPLY-001: Apply SWU-TSGR-001

## Question

May Invoke materialize and Task Session apply exactly the five validated
`SWU-TSGR-001` public Arcanum files?

This is consequential because it creates canonical implementation files. It is
reversible and bounded, but Task Session cannot auto-select it.

## Option 1 — approve exact five-path apply

- Benefit: unblocks material-package validation, mutation admission, canonical
  implementation, and live SWU validation.
- Cost/risk: creates five public canonical Task Session files.
- Safeguards: targets are currently absent; staged digests are fixed; owner,
  authority, publication class, validation, and allowed writes are receipt-bound.
- Excluded: existing dirty files, generated mirrors, publication, promotion, commit,
  deployment, and `SWU-TSGR-002`.
- Downstream: Invoke builds one exact apply-approved package; Task Session must still
  obtain `admissionVerdict=admit` before writing.

Select with:

`approve SWU-TSGR-001 exact five-path apply`

## Option 2 — defer and keep staged

- Benefit: preserves the validated producer package with no canonical mutation.
- Cost/risk: `SWU-TSGR-001` and the whole work pack remain blocked.
- Downstream: resume only while source, staged-byte, and absent-target identities
  remain exact; otherwise rebuild the producer receipt.

Select with:

`defer SWU-TSGR-001 apply`

## Explain / more context

Ask for `explain TSGR-APPLY-001`. This does not resolve the gate.

## Current record

- Result: `PASS`
- Selected option: `approve-exact-five-path-apply`
- Recommendation: Option 1, because the staged package satisfies every current
  producer acceptance check and the apply remains separately guarded by Invoke and
  Task Session.
- Source of decision: the current user explicitly answered `approved` and clarified
  that easy deterministic regeneration should reduce decision friction.
- Recorded at: `2026-07-30T19:22:55Z`.
- Decision rationale: approve the exact five-path apply because the targets are
  absent, staged bytes and validation evidence are digest-bound, the scope is
  reversible and bounded, and Task Session still requires a fresh mutation-admission
  receipt immediately before the first canonical write.
- Regenerability treatment: accepted as evidence of reversibility, not as ambient
  mutation authority. A separate criterion candidate records when future workflows
  may safely auto-select such decisions.
- Remaining blockers after Option 1: material package validation and Task Session
  mutation admission.
