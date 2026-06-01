# Refine Result: PromotionRecord Companion Boundary And Model Gap Sweep

Status: pass
Preset: standard
Research: no-research

## Recommendation

Use a layered schema model for the first development-only JSON Schema candidate:

1. **Base ontology entry schema**
   - Common fields shared by every branch-aware ontology record.
   - Owns branch context, lifecycle/role/outcome axes, confidence split, evidence pointers, edges, and governance base fields.

2. **Record-kind profiles inside the development JSON Schema**
   - `promotion_record`
   - `bridge_validation`
   - `evidence_input`
   - `ontology_entry`

3. **Companion templates later**
   - Do not create canonical companion templates yet.
   - Do not split separate governed schemas yet.
   - Let the first JSON Schema express record-kind-specific rules as `$defs` or conditional profiles, then promote companion templates only after fixtures prove the profile boundaries.

This avoids both bad extremes:

- one flat schema where `record_kind` becomes decorative and weak;
- premature separate schemas/templates before examples prove the split.

## PromotionRecord Boundary

`promotion_record` should be a record-kind profile before it becomes a companion template.

It is not merely:

- a lifecycle status,
- a claim role,
- a governance outcome,
- a bridge outcome,
- an `entry_type` string.

It is a governed change/proposal/receipt record about one primary ontology claim.

Minimum profile requirements for `record_kind: promotion_record`:

- one primary promoted/proposed claim, represented by `content.claim`;
- one target relation or target claim reference, preferably through `edges[]`;
- source or validation evidence;
- confidence split preserved;
- non-`none` review or validation gate;
- contradiction path;
- rollback, retirement, or supersession path, represented initially as `governance.contradiction_path` or a named blocker;
- no replacement of the base ontology entry record.

## Other Model Gaps To Address Before JSON Schema

| Gap | Severity | Why it matters | Recommendation |
| --- | --- | --- | --- |
| `evidence_input` has no direct fixture | blocker for complete record_kind schema coverage | The enum value exists but is not pressure-tested. | Add one valid and one invalid evidence-input fixture before JSON Schema validation is considered complete. |
| `bridge_validation` profile is implicit | flag | Bridge entries currently rely on branch context and edges; JSON Schema should make bridge validation shape visible. | Add a `bridge_validation` profile requiring bridge scope, bridge alignment confidence, and either edges or explicit evidence-gap role. |
| PromotionRecord target relation is implicit | flag | `content.claim` plus edges works, but a PromotionRecord should be about one primary claim. | Require one primary relation by convention first; consider `primary_target_ref` only if fixtures prove edges are insufficient. |
| `entry_type` remains unconstrained | non-blocking | Domain/system class labels will vary across Arcanum, CyberAlchemy, DomainSpec, and future systems. | Keep `entry_type` as string in the base schema; do not enumerate it in JSON Schema yet. |
| Branch evidence completeness is under-enforced | flag | V4 says bridge entries cite evidence from each connected branch or name gaps, but validator only approximates this. | Strengthen validator/fixtures after JSON Schema candidate, unless a bridge validation fixture fails first. |
| Companion templates are not selected | non-blocking | Templates imply workflow and authoring behavior, not just validation shape. | Defer templates until JSON Schema profiles pass fixtures. |
| DomainSpec-owned package absent | non-blocking external boundary | DomainSpec examples should pressure-test the general model without becoming general mechanics. | Keep as handoff/future package, not a blocker for base JSON Schema. |
| Future-system source absent | non-blocking evidence gap | Placeholder proves portability shape only. | Keep placeholder marked as evidence gap. |

## Rejected Alternatives

| Alternative | Verdict | Reason |
| --- | --- | --- |
| Flat base schema only | rejected | It repeats the `record_kind` problem by making the discriminator visible but weak. |
| Separate governed schemas now | rejected | Too early; it would freeze boundaries before fixture evidence distinguishes profiles from templates. |
| PromotionRecord as canonical template now | rejected | Template authority is a later governance decision and would exceed this development package. |
| Remove `evidence_input` until later | rejected | Keeping it exposes a real fixture gap that should be tested before JSON Schema completion. |

## Refined Next Route

Run an invoke plan or task-session for a new pre-JSON-schema profile coverage step:

```text
OVS-PROFILE-001: define development-only record-kind profiles and add missing evidence_input coverage before JSON Schema generation
```

Suggested SWUs:

| SWU | Goal | Done criteria |
| --- | --- | --- |
| OVS-PROFILE-001 | Add a short profile-boundary section to the schema candidate for `ontology_entry`, `promotion_record`, `bridge_validation`, and `evidence_input`. | Candidate remains non-canonical and names profile rules without creating companion templates. |
| OVS-PROFILE-002 | Add valid/invalid `evidence_input` fixtures. | Validator has direct coverage for the currently untested enum value. |
| OVS-PROFILE-003 | Add profile checks to the deterministic validator. | `promotion_record`, `bridge_validation`, and `evidence_input` profile boundaries are checked. |
| OVS-PROFILE-004 | Refresh validation report and work-pack. | Report states whether JSON Schema generation is ready or still flagged. |

Only after those pass should `OVS-JSON-001` generate the first development-only JSON Schema candidate.

## Final Boundary

PromotionRecord should not block JSON Schema as a separate canonical schema/template. It should block JSON Schema only until its **development profile** is explicit and fixture-backed.

The clean next shape is:

```text
base entry schema + record_kind profiles first
JSON Schema candidate second
companion templates/schemas later, only if profiles prove they need independent ownership
```
