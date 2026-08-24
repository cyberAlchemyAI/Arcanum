# Invoke Ontology Index

- Profile: `profile.json`
- Sources: `sources.json`
- Business view: `views/business.json`
- System view: `views/system.json`
- Bridge view: `views/bridge.json`
- Residue: `residue.json`
- Operation composition: `extensions/operation-composition.json`
- Preserved identities and schema amendments: `migration/preserved-identities.json`
- Source re-grounding and exact line-slice bindings: `migration/preserved-identities.json#source_regroundings` and `#evidence_selector_binding`
- Validation history: `history/legacy-validation.json`

## Business concept model

Every business node uses `invoke-business-node/public-contract-v2` and carries an exact `concept` object with `name`, `role`, `meaning`, and `plain_language`. Top-level `label` and `role` remain compatibility projections required by the shared public node contract; the validator requires them to equal `concept.name` and `concept.role`.

The concept text is a public candidate explanation bounded by the node's existing evidence and obligations. It is not canonical definition authority. The atomic v1-to-v2 migration witness is `migration/preserved-identities.json#schema_amendments/0`.

## Stable nodes

- `B-AUTHORING` — Governed Intent Authoring (business)
- `B-DEFINE-BASELINE` — Definition Baseline (business)
- `B-PLAN-READY-DESIGN` — Plan-Ready Design (business)
- `B-EXECUTABLE-PLAN` — Executable Plan (business)
- `B-CONTINUITY` — Bounded Session Continuity (business)
- `B-EVIDENCE-REFRESH` — Evidence-Bounded Refresh (business)
- `B-NON-COLLAPSE` — Readiness Non-Collapse Rule (business)
- `B-NARROW-FIRST` — Narrow-First Policy (business)
- `B-DOWNSTREAM-OWNER` — Downstream Lifecycle Owner (business)
- `S-MODE-ROUTER` — Invoke Mode Router (system)
- `S-DEFINE-PACK` — Define Artifact Pack (system)
- `S-DESIGN-PIPELINE` — Design Pipeline (system)
- `S-PLAN-PACK` — Plan Artifact Pack (system)
- `S-HANDOFF-PACK` — Handoff Artifact Pack (system)
- `S-REFRESH-PIPELINE` — Refresh Pipeline (system)
- `S-CAPABILITY-RESOLVER` — Capability Resolver (system)
- `S-VALIDATION-SURFACE` — Validation Surface (system)
- `S-DISPATCH-TRACE` — Dispatch Trace (system)

## Stable relations

- `BR-AUTHORING-DEFINE` — B-AUTHORING produces B-DEFINE-BASELINE (business)
- `BR-DEFINE-DESIGN` — B-DEFINE-BASELINE precedes B-PLAN-READY-DESIGN (business)
- `BR-DESIGN-PLAN` — B-PLAN-READY-DESIGN precedes B-EXECUTABLE-PLAN (business)
- `BR-AUTHORING-CONTINUITY` — B-AUTHORING includes B-CONTINUITY (business)
- `BR-AUTHORING-REFRESH` — B-AUTHORING includes B-EVIDENCE-REFRESH (business)
- `BR-AUTHORING-NON-COLLAPSE` — B-AUTHORING governed_by B-NON-COLLAPSE (business)
- `BR-PLAN-NARROW-FIRST` — B-EXECUTABLE-PLAN governed_by B-NARROW-FIRST (business)
- `BR-AUTHORING-OWNER` — B-AUTHORING hands_off_to B-DOWNSTREAM-OWNER (business)
- `SR-ROUTER-DEFINE` — S-MODE-ROUTER selects S-DEFINE-PACK (system)
- `SR-ROUTER-DESIGN` — S-MODE-ROUTER selects S-DESIGN-PIPELINE (system)
- `SR-ROUTER-PLAN` — S-MODE-ROUTER selects S-PLAN-PACK (system)
- `SR-ROUTER-HANDOFF` — S-MODE-ROUTER selects S-HANDOFF-PACK (system)
- `SR-ROUTER-REFRESH` — S-MODE-ROUTER selects S-REFRESH-PIPELINE (system)
- `SR-DEFINE-DESIGN` — S-DEFINE-PACK feeds S-DESIGN-PIPELINE (system)
- `SR-DESIGN-PLAN` — S-DESIGN-PIPELINE feeds S-PLAN-PACK (system)
- `SR-DESIGN-VALIDATION` — S-DESIGN-PIPELINE validated_by S-VALIDATION-SURFACE (system)
- `SR-PLAN-VALIDATION` — S-PLAN-PACK validated_by S-VALIDATION-SURFACE (system)
- `SR-REFRESH-VALIDATION` — S-REFRESH-PIPELINE validated_by S-VALIDATION-SURFACE (system)
- `SR-ROUTER-DISPATCH` — S-MODE-ROUTER emits S-DISPATCH-TRACE (system)
- `SR-ROUTER-RESOLVER` — S-MODE-ROUTER status_reported_by S-CAPABILITY-RESOLVER (system)
- `E-AUTHORING-ROUTER` — B-AUTHORING realized_by S-MODE-ROUTER (bridge)
- `E-DEFINE-PACK` — B-DEFINE-BASELINE realized_by S-DEFINE-PACK (bridge)
- `E-DESIGN-PIPELINE` — B-PLAN-READY-DESIGN realized_by S-DESIGN-PIPELINE (bridge)
- `E-PLAN-PACK` — B-EXECUTABLE-PLAN realized_by S-PLAN-PACK (bridge)
- `E-CONTINUITY-HANDOFF` — B-CONTINUITY realized_by S-HANDOFF-PACK (bridge)
- `E-REFRESH-PIPELINE` — B-EVIDENCE-REFRESH realized_by S-REFRESH-PIPELINE (bridge)
- `E-NON-COLLAPSE-RESOLVER` — B-NON-COLLAPSE realized_by S-CAPABILITY-RESOLVER (bridge)
- `E-NARROW-FIRST-VALIDATION` — B-NARROW-FIRST tested_by S-VALIDATION-SURFACE (bridge)
- `E-AUTHORING-DISPATCH` — B-AUTHORING constrained_by S-DISPATCH-TRACE (bridge)
