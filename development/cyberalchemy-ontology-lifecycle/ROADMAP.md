---
title: CyberAlchemy Ontology Lifecycle Roadmap
status: plan-ready
task: CAOL-008
route: invoke-plan-plus-implementation-layering
createdAt: 2026-05-23
updatedAt: 2026-05-24
---

# Roadmap

## Status

CAOL-008 converts the repaired candidate architecture into an operationalization plan. It does not execute implementation work, mutate canonical ontology/runtime files, or promote candidate definitions.

Planning baseline:

- [ONTOLOGY-ARCHITECTURE.md](ONTOLOGY-ARCHITECTURE.md): PromotionRecord-centered candidate architecture.
- [PROMOTION-LIFECYCLE.md](PROMOTION-LIFECYCLE.md): PromotionRecord-centered lifecycle and gates.
- [INTERROGATION-VERDICT.md](INTERROGATION-VERDICT.md): CAOL-007 pass-with-review-items.
- [CONCEPT-TOURNAMENT.md](CONCEPT-TOURNAMENT.md): selected smallest coherent model.

## Roadmap Phases

| Phase | Goal | Main Deliverables | Exit Evidence |
| --- | --- | --- | --- |
| P0 Evidence Baseline | Preserve strict local evidence and source map. | `CONTEXT-HANDOFF.md`, `context-pack.json`, `SOURCE-MAP.md`. | Completed in CAOL-001. |
| P1 Definition Baseline | Stabilize candidate terms and distinctions. | `DEFINITIONS-GLOSSARY.md`, CAOL-002 sections in `INTERROGATION-VERDICT.md`. | Completed in CAOL-002/003. |
| P2 Research And Tournament | Add external pressure and choose a smallest coherent model. | `external-research-appendix.md`, `CONCEPT-TOURNAMENT.md`. | Completed in CAOL-004/005. |
| P3 Candidate Design | Produce architecture/lifecycle around the selected model. | `ONTOLOGY-ARCHITECTURE.md`, `PROMOTION-LIFECYCLE.md`. | Completed in CAOL-006/007. |
| P4 First Working Slice | Prove the model can evaluate one PromotionRecord without canonical mutation. | [FIRST-WORKING-SLICE.md](FIRST-WORKING-SLICE.md), review-only PromotionRecord fixture, validation checklist. | Next execution route after CAOL-008. |
| P5 Governance Hardening | Normalize schema, owners, validation templates, and threshold defaults. | PromotionRecord schema/template, owner matrix decisions, bridge-validation template, signal threshold defaults. | CAOL-008/next approved tasks. |
| P6 Operational Integration | Connect accepted model to ontology-vault/harness, context-builder, observability, and DomainSpec/AEO routes. | Adapter specs, harness checks, evidence fixtures, route-impact checks. | Only after user accepts candidate design. |
| P7 Publish And Final Audit | Explain model and close the architecture package. | `SUBSTACK-ARTICLE.md`, final package README, final interrogation. | CAOL-009/010. |

## Implementation Layering

Target: CyberAlchemy operational ontology proof slice.

Current state: candidate architecture and lifecycle are authored; no implementation exists.

Primary operator: future Arcanum/Codex agent or human reviewer deciding whether an observed run should create a governed ontology candidate.

Primary constraint: no canonical mutation before model acceptance.

### Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Operator Outcome | Risk Reduced | Main Cost Drivers | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 POC | After this layer, we know whether a PromotionRecord can represent one observed operational lesson with evidence, confidence, owner, and bridge status. | One review-only PromotionRecord fixture plus validation checklist. | Reviewer can inspect one complete candidate without touching canonical files. | Proves model closure and catches schema gaps. | Artifact authoring and review checklist. | Continue if fixture validates without false authority or signal truth. |
| L1 Repeatability | After this layer, we know whether the same template handles three source types. | Three fixtures: source/inventory evidence, ReviewableSignal, LifecycleEvidenceEnvelope. | Reviewer can compare promotion paths across evidence types. | Reduces adapter-shape ambiguity. | Fixture authoring, threshold defaults, owner mapping. | Harden if all fixtures use one PromotionRecord shape. |
| L2 Governance | After this layer, we know whether gates and owners prevent unsafe promotion. | Review-owner matrix with decision examples and bridge-validation evidence templates. | Reviewer can see which owner/gate blocks each risky transition. | Reduces vague-gate and commitment-confidence risk. | Decision review and template maintenance. | Integrate only if owner/gate coverage is explicit. |
| L3 Integration | After this layer, we know whether accepted artifacts can plug into ontology-vault/harness and observability routes. | Adapter specs and harness-ready validation pack. | Future agents can generate context packs and run validation without broad rediscovery. | Reduces operationalization and drift risk. | Connector docs, validation fixtures, harness tests. | Route to ontology-vault/harness only after acceptance. |

### Scope Progression

| Scope Area | L0 Proof | L1 Repeatability | L2 Governance | L3 Integration |
| --- | --- | --- | --- | --- |
| PromotionRecord | One fixture. | Three evidence-source fixtures. | Schema plus gate examples. | Template/spec accepted by ontology-vault route. |
| ReviewableSignal | One optional signal input in L0 fixture. | Dedicated signal fixture. | Threshold defaults. | Observability adapter proposal. |
| LifecycleEvidenceEnvelope | Deferred. | Dedicated AEO/DomainSpec fixture. | Bridge-validation template. | DomainSpec route integration proposal. |
| Owner/Gate Model | One default owner. | Owner mapping across fixtures. | Review-owner matrix decisions. | Decision-gate route. |
| Canonical Mutation | Explicitly excluded. | Explicitly excluded. | Explicitly excluded. | Still gated by user acceptance. |

## First Working Slice

Recommended next layer: L0 POC.

The first working slice is a review-only proof artifact, not code implementation:

1. Create one example PromotionRecord fixture in the planning package.
2. Use an Arcanum operational signal as the motivating scenario, but do not ingest raw telemetry exhaust.
3. Fill required fields: claim, source inputs, provenance, branch target, status, evidence confidence, commitment confidence, review owner, gate result, use scope, contradiction path, rollback/retirement path, route impact, bridge validation.
4. Validate it against the architecture/lifecycle gates.
5. Record whether the model is too broad, too narrow, or missing fields.

Candidate output path:

```text
development/cyberalchemy-ontology-lifecycle/first-slice/promotion-record-fixture.md
```

Do not create canonical ontology entries in `../cyberAlchemy/ontology/` during L0.

## Implementation Plan

| Work ID | Layer | Task | Write Scope | Acceptance Evidence | Validation |
| --- | --- | --- | --- | --- | --- |
| CAOL8-L0-001 | L0 | Create review-only PromotionRecord fixture. | `development/cyberalchemy-ontology-lifecycle/first-slice/` | Fixture has every required PromotionRecord field and no canonical mutation. | Review checklist in `FIRST-WORKING-SLICE.md`. |
| CAOL8-L0-002 | L0 | Create PromotionRecord validation checklist. | `FIRST-WORKING-SLICE.md` or `first-slice/` | Checklist maps every required field to architecture/lifecycle source. | Markdown review plus `rg` marker check. |
| CAOL8-L0-003 | L0 | Run manual review against CAOL-006/007 gates. | package artifacts only | Pass/flag/block record with missing fields. | Reviewer verdict saved in first-slice artifact. |
| CAOL8-L1-001 | L1 | Add two more fixtures for source/inventory and lifecycle-envelope inputs. | `first-slice/fixtures/` | Three fixtures share one shape. | Compare field coverage and adapter source type. |
| CAOL8-L2-001 | L2 | Turn Review Owner Matrix into concrete owner decision table. | planning package only | Each claim type has named owner class and escalation route. | Review against vague-gate risk. |
| CAOL8-L2-002 | L2 | Draft bridge-validation evidence template. | planning package only | Outcomes `aligned`, `partial`, `drift`, `insufficient`, `contradicted` represented. | Template review. |
| CAOL8-L3-001 | L3 | Draft adapter specs for ontology-vault/harness and observability routes. | planning package only | Adapter specs route to lifecycle owners without canonical mutation. | Architecture review and final decision-gate. |

## Validation Strategy

| Validation Surface | What It Proves | Method |
| --- | --- | --- |
| Required field coverage | PromotionRecord can close over one claim. | Checklist against [ONTOLOGY-ARCHITECTURE.md](ONTOLOGY-ARCHITECTURE.md#promotionrecord-schema). |
| Boundary check | PromotionRecord is not an everything object. | Confirm one primary claim, no raw telemetry/source dumps, no unrelated bundled claims. |
| Confidence split | Evidence and commitment confidence do not collapse. | Separate rationale fields in fixture. |
| Signal truth guard | ReviewableSignal does not become truth. | Signal input affects evidence confidence only. |
| Owner/gate clarity | Review cannot proceed with unknown owner. | Owner matrix mapping. |
| Bridge validation | Operational use waits for bridge outcome. | Fixture outcome is `aligned`, `partial`, `drift`, `insufficient`, or `contradicted`. |
| Canonical mutation guard | Planning package remains isolated. | `git status --short -- development/cyberalchemy-ontology-lifecycle` plus no edits outside approved package. |

## Plan Interrogation

| Risk | Finding | Repair |
| --- | --- | --- |
| Premature implementation | Original temptation would be to build adapters or mutate ontology files. | L0 is review-only fixture and checklist. |
| Missing validation | A plan without field/checklist proof would not show model closure. | Added validation strategy and first-slice checklist requirement. |
| Canonical mutation risk | Operationalization could drift into `../cyberAlchemy/ontology/` or runtime assets. | All first-slice writes stay under the planning package. |
| First slice too large | Full adapter suite is larger than needed. | L0 proves one PromotionRecord only. |
| Owner ambiguity | Concrete named owners are not accepted yet. | L0 uses owner class; L2 routes named owner decisions. |

## Next Work

Smallest next continuation goal:

```text
/goal Execute the CAOL-008 L0 first working slice.

Read development/cyberalchemy-ontology-lifecycle/FIRST-WORKING-SLICE.md first. Create only review-only first-slice artifacts under development/cyberalchemy-ontology-lifecycle/first-slice/. Do not mutate canonical ontology/runtime files. Produce one PromotionRecord fixture and validate it against the checklist.
```

## CAOL-008 Gate

| Gate | Result | Evidence |
| --- | --- | --- |
| Roadmap has phases | pass | Roadmap Phases table. |
| Next work named | pass | First Working Slice and Next Work sections. |
| Implementation layering included | pass | L0-L3 layer decision table and scope progression. |
| Validation strategy included | pass | Validation Strategy table. |
| First working slice included | pass | L0 POC details and [FIRST-WORKING-SLICE.md](FIRST-WORKING-SLICE.md). |
| No canonical mutation without acceptance | pass | All planned write scope stays under `development/cyberalchemy-ontology-lifecycle/`. |

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: CAOL planning package
- Phase status: pass
- Mode contract: `spells/invoke/plan.md`
- Outputs: [ROADMAP.md](ROADMAP.md), [FIRST-WORKING-SLICE.md](FIRST-WORKING-SLICE.md)
- Implementation layering: included in this roadmap
- Work-pack: lightweight package-local plan, no execution work-pack mutation
- Decisions: L0 is review-only PromotionRecord fixture; canonical mutation excluded
- Unresolved gaps: concrete owner names, signal threshold defaults, bridge evidence template details, Operational Ontology acceptance route
- Next route: CAOL-009 article synthesis or optional L0 first-slice execution if user chooses to run it before article work

## Observability Closeout

- `OBSERVATION`: CAOL-008 turned the repaired architecture into a layered operationalization plan and first-slice handoff.
- `LEDGER`: Updated [ROADMAP.md](ROADMAP.md), created [FIRST-WORKING-SLICE.md](FIRST-WORKING-SLICE.md), updated [TASKS.md](TASKS.md), and updated [index.json](index.json).
- `REFLECTION_TRIGGER`: no runtime reflection; this is planning output.
- `RECOMMENDATION`: run optional L0 first-slice proof before canonical acceptance, or proceed to CAOL-009 article synthesis with this caveat.
- `DEDUPE_KEY`: `caol-008-roadmap-first-slice-2026-05-24`
