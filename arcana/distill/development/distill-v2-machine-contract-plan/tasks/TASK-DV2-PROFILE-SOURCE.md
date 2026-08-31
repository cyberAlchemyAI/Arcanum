# TASK-DV2-PROFILE-SOURCE — Exact Configuration And Input Closure

## SWU-DV2-023

### Objective

Make the profile the single composition authority and bind one normalized
Standard RunFrame to that exact profile without prose fallback.

### Entry

SWU-DV2-022 PASS and unchanged digests for all eight schemas, eleven techniques,
and five modes.

### Write Scope

- `profiles/v2/distill-core-profile-v2.json`
- Standard normalized source positive fixture
- profile/source cross-reference validator and positive/negative fixtures

### Acceptance

- Profile binds exact mode and technique instance refs/digests and the output contract version.
- Source binds exactly one profile, with mode consistency checked by the validator.
- Full input groups, objective/output revision lineage, artifact exact refs, finite
  override rules, and optional non-authoritative evidence context are exercised.
- Drifted ref, unknown technique, profile/source mode mismatch, incomplete RunFrame,
  stale artifact, forbidden override, or evidence-authored verdict rejects.

### Claim Ceiling And Successor

Configuration and normalized-input closure only. No trace/result/finalizer claim.
The only successor is SWU-DV2-024.
