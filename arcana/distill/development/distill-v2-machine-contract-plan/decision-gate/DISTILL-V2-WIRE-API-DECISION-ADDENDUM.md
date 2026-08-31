# Distill v2 Wire/API Decision Addendum

- Addendum ID: `DISTILL-V2-WIRE-API-DECISION-ADDENDUM-2026-08-27`
- Status: independent review PASS
- Authority effect: none
- Parent decision: `DISTILL-V2-DECISION-GATE-2026-08-27`
- Owner confirmation: `DISTILL-V2-WIRE-API-OWNER-CONFIRMATION-2026-08-27`
- Independent review: `DISTILL-V2-WIRE-API-DECISION-REVIEW-001`

## Confirmed selections

- D11: lowercase snake_case canonical machine tokens; prose and historical spellings are mappings, not accepted v2 writer values.
- D12: `cross_level_confusion` is a JSON boolean; prose `yes`/`no` maps to true/false only.
- D13: `phases` and `hooks` are unique non-empty arrays whose members preserve canonical lifecycle order.
- D14: `https://arcanum.dev/schemas/distill/{hyphenated-artifact}/2-0-0` identities with local `#/$defs/{snake_case_definition}` fragments and cross-schema `{target_schema_id}#/$defs/{snake_case_definition}` references.
- D15: exact per-artifact `distill.{snake_case_artifact}.v2` version constants.
- D16: the enumerated Distill-owned identity fields use the end-of-input-safe lowercase ASCII snake_case grammar in the machine addendum.
- D17: calendar-valid `YYYY-MM-DDTHH:MM:SSZ` only, including years `0001` through `9999`; no offsets or fractional seconds.

The machine addendum contains the exact eight-schema identity/version table, prose-to-wire mappings, seven admissibility request/receipt bindings, and authority ceiling.

## Claim ceiling

This resolves D11-D17 for contract repair. It does not authorize contract mutation, schema authoring, implementation, publication, deployment, promotion, or external effects.

## Next state

Prepare a separately bounded immutable R2 contract candidate that binds the reviewed addendum digest. Preserve the old contract and Review 004 unchanged, obtain a new independent R2 review, and do not author schemas or execute implementation from this decision receipt alone.
