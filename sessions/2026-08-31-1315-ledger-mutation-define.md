---
tags: [craft-ledger, ledger-mutation, mutation-protocol, invoke, workflow-cost]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-31T13:15:30-03:00
updated_at: 2026-08-31T13:15:30-03:00
expires: 2026-10-30
decisions_made: true
contradictions_found: true
specs_updated: [runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/SPEC.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session fixes the first mutation protocol boundary, preserves its independent admission evidence, and records a material workflow-cost warning before the operation inventory expands."
---

# Craft ledger mutation Define and workflow cost

## Summary

The session set out to clarify what a model or caller must submit when Craft updates a project ledger and whether Craft reads the authoritative ledger first. Inspection confirmed that the existing Craft contract described source authority but did not provide an automated mutation runner that guaranteed the pre-mutation read. A project-local Craft ledger and human view were created, and the generated Craft package was installed under `.agents`. The input direction was fixed as one versioned request envelope with an operation-discriminated payload rather than unrelated top-level YAML formats for every ledger family. A fresh, revision-bound ledger inspection snapshot is mandatory before proposal, and planning must reread and validate the source before any explicit apply boundary can write. The first supported slice was deliberately limited to `add_gap`; blocker, decision, and other operations remain `UNSUPPORTED` until their payload semantics are defined. Invoke Define v1 produced candidate definitions and a thirteen-file bundle whose independent admission passed all thirteen checks with no authority effect or runtime-readiness claim. The work also exposed and repaired a missing `artifact schema` alias in the canonical definitions index and adapted the installed Invoke package to the repository-local path and Windows publication environment. The operator observed that the add-gap-only Define cycle took 38 minutes, so the Craft ledger now records this as an active operational-cost gap and advances to design with an explicit sequence for schemas, implementation, and workflow simplification.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Craft Ledger Runtime](../runtime/craft-ledger/CRAFT.md) | `is-part-of` | This session advances the project-local context that owns ledger mutation design, gaps, and next moves. |
| [Ledger mutation discovery](../runtime/craft-ledger/docs/features/ledger-mutation/discovery.md) | `refines` | The session closes the discovery's first-operation question as an add-gap-only candidate protocol while preserving later design questions. |
| [Define bundle admission receipt](../runtime/craft-ledger/.invoke/ledger-mutation/define-v1/DEFINE-BUNDLE-ADMISSION-RECEIPT.json) | `derives-from` | The session's Define-pass claim is based on the independent current-state replay and thirteen-check admission result. |

## Open questions

- How much of the observed 38-minute cycle was one-time installation, repository-path, and Windows-publication repair versus recurring per-operation authoring cost?
- Which exact authorization and atomic persistence mechanism will govern `apply` after the schemas and mapping are designed?

## Next steps

1. Design the minimal machine-checkable schemas for the inspection snapshot, common request envelope, `add_gap` payload, plan/apply boundary, and mutation outcome.
2. Define the deterministic mapping between the `add_gap` payload and the existing ledger row, including revision, ID, reference, and candidate validation rules.
3. Implement and verify `inspect`, `plan`, and `apply` only for `add_gap`; keep all other operations explicitly unsupported.
4. Instrument the next lifecycle cycle and remove repeated authoring or admission work before defining blocker, decision, or other payload families.

## Recommendation

Treat the request envelope and validation pipeline as reusable infrastructure, add future operations only as discriminated payload branches, and use measured stage timings from the next cycle to distinguish necessary safeguards from accidental workflow overhead.

## Operator observation

The operator recorded that defining and admitting only `add_gap` took 38 minutes. The scoped Craft ledger preserves this as `GAP-LEDGER-MUTATION-DEFINITION-OVERHEAD` with `flag` severity and `plan` treatment.

## Files touched

- .agents/skills/craft/ARCHITECTURE.md
- .agents/skills/craft/README.md
- .agents/skills/craft/SKILL.md
- .agents/skills/craft/examples/platform-governance-CRAFT.md
- .agents/skills/craft/examples/platform-governance-ledger.yml
- .agents/skills/craft/examples/product-launch-CRAFT.md
- .agents/skills/craft/examples/product-launch-ledger.yml
- .agents/skills/craft/templates/ledger.schema.yml
- .agents/skills/craft/templates/schemas/index.schema.yml
- .agents/skills/craft/templates/schemas/ledger-core.schema.yml
- .agents/skills/invoke/schemas/define-bundle-admission-receipt-v1.schema.json
- .agents/skills/invoke/schemas/define-result-v3.schema.json
- .agents/skills/invoke/schemas/define-semantic-closure-receipt-v1.schema.json
- .agents/skills/invoke/scripts/compile_define_source_v3.py
- .agents/skills/invoke/scripts/define_stage_contract.py
- .agents/skills/invoke/scripts/validate_define_bundle_admission.py
- .agents/skills/invoke/scripts/validate_define_semantic_closure.py
- definitions/DEFINITIONS-INDEX.md
- runtime/craft-ledger/.craft/artifacts/.gitkeep
- runtime/craft-ledger/.craft/ledger.yml
- runtime/craft-ledger/CRAFT.md
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/authoring/CAPABILITY-STATUS-REQUEST.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/authoring/DEFINE-SOURCE-AUTHORING-REQUEST.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/authoring/SEMANTIC-CONTEXT-AUTHORING-REQUEST.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/DEFINE-SEMANTIC-CONTEXT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/DEFINE-TRANSPORT-REPORT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/DEFINITIONS.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/DEFINITIONS.md
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/DISPATCH-TRACE.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/DISTILL-RECEIPT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/GLOSSARY.md
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/IDENTITY-DENOMINATOR-RECEIPT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/INVOKE-DEFINE-STAGE-RECEIPT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/LAYERING-GAP.md
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/SPEC.md
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/bundle/TEMPLATE-SELECTION-RECEIPT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/CAPABILITY-STATUS.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/DEFINE-BUNDLE-ADMISSION-RECEIPT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/source/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/source/DEFINE-SEMANTIC-CONTEXT.json
- runtime/craft-ledger/.invoke/ledger-mutation/define-v1/source/DEFINE-SOURCE.json
- sessions/2026-08-31-1315-ledger-mutation-define.md
