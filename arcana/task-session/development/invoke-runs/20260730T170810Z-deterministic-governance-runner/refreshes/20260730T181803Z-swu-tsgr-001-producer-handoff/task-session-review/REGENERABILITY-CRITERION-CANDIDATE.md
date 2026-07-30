# Candidate: Deterministic Regenerability as Decision Evidence

Status: proposal for a later governance-policy work pack; not active policy.

## Proposed criterion

A change may receive lower decision friction when it is easy to regenerate, but
regenerability is evidence of reversibility rather than sufficient proof that the
decision is nonconsequential.

An automatic selection may be considered only when all of these conditions hold:

1. the exact target set is closed, bounded, and already declared;
2. the producer command, producer version, inputs, output digests, and validation
   surface are bound in current receipts;
3. regeneration is deterministic and a rerun or exact-byte restoration check exists;
4. canonical source authority remains intact and generated material does not replace
   an unrecorded source of truth;
5. the operation causes no destructive data loss, public publication, promotion,
   deployment, spending, security/privacy effect, external side effect, or acceptance
   of policy or risk;
6. current owner, authority, publication, dependency, and dirty-overlap gates pass;
7. rollback or regeneration remains possible inside the same declared scope; and
8. post-apply validation is mandatory and can falsify the claimed regeneration.

If any condition is absent, the decision remains consequential or unresolved and
routes through Decision Gate.

## Application to TSGR-APPLY-001

The criterion supports the classification `reversible`, but it does not retroactively
bypass the existing public-canonical apply gate. The user's explicit approval resolves
that gate; Invoke material validation and Task Session mutation admission still control
the five canonical writes.

## Suggested owner route

Route a later bounded policy SWU through `invoke:refresh:proposal-only`, then the
Decision Gate and Task Session lifecycle owners. Do not edit the live decision policy
inside `SWU-TSGR-001`.
