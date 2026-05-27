# Context Pack: General Ontology Lifecycle Material

Status: context-builder selection
Mode: standard
Strict coverage: pass
Date: 2026-05-27

## Task

Copy what is general from `development/cyberalchemy-ontology-lifecycle/` into Ontology Vault development, while leaving particular DomainSpec/AEO material for a separate handoff.

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Preserve general ontology-governance concepts. | covered |
| O2 | Keep CAOL and CyberAlchemy claims candidate-only. | covered |
| O3 | Separate DomainSpec/AEO-specific lifecycle material. | covered |
| O4 | Preserve evidence selectors instead of copying whole files. | covered |
| O5 | Produce handoff-ready context for the particular migration. | covered |

## Included Context

| Source | Selectors | Obligations | Why Included |
| --- | --- | --- | --- |
| `development/cyberalchemy-ontology-lifecycle/README.md` | `Current Verdict`, `Core Model`, `Guardrail` | O1, O2 | Establishes package-complete-but-not-canonical posture and the selected PromotionRecord model. |
| `development/cyberalchemy-ontology-lifecycle/CONCEPT-TOURNAMENT.md` | `Selected model`, `Current Smallest Coherent Unit`, `Closure Test` | O1, O2 | Shows why PromotionRecord is the smallest reusable governance object. |
| `development/cyberalchemy-ontology-lifecycle/ONTOLOGY-ARCHITECTURE.md` | `Design Thesis`, `Ontology Branches`, `PromotionRecord Schema`, `PromotionRecord Boundary`, `Review Owner Matrix`, `Observability-Backed Validation` | O1, O2, O3 | Provides the reusable ontology lifecycle model and explicitly separates signals from truth. |
| `development/cyberalchemy-ontology-lifecycle/PROMOTION-LIFECYCLE.md` | `Lifecycle States`, `Transition Table`, `Confidence And Commitment Gates`, `Evidence Requirements`, `Signal Recurrence And Severity`, `Bridge Validation`, `Operational Use` | O1, O2 | Provides reusable lifecycle gates and validation outcomes. |
| `development/cyberalchemy-ontology-lifecycle/INTERROGATION-VERDICT.md` | `CAOL-007 Architecture And Lifecycle Interrogation`, `Final Verification`, `Residual Review Items` | O1, O2, O5 | Preserves repaired risks and unresolved decisions. |
| `development/cyberalchemy-ontology-lifecycle/FIRST-WORKING-SLICE.md` | `PromotionRecord Fixture Requirements`, `Validation Checklist`, `Promotion Decision` | O1, O5 | Provides a reusable validation shape for one review-only fixture. |
| `development/cyberalchemy-ontology-lifecycle/first-slice/promotion-record-fixture.md` | `PromotionRecord`, `Review Notes` | O1, O2, O5 | Provides a concrete example of the reusable pattern, while its CAOL scope remains particular. |
| `development/cyberalchemy-ontology-lifecycle/first-slice/validation-result.md` | `Checklist`, `Required Field Coverage`, `L1 Readiness` | O1, O5 | Provides validation criteria for the reusable pattern. |
| `development/cyberalchemy-ontology-lifecycle/CONTEXT-HANDOFF.md` | `DomainSpec And AEO Sources`, `Decisions And Working Constraints`, `Contradictions` | O3, O4 | Identifies what belongs to DomainSpec/AEO rather than general Ontology Vault. |
| `development/cyberalchemy-ontology-lifecycle/SOURCE-MAP.md` | `Authority Precedence`, `Coverage By Obligation` | O2, O3, O4 | Preserves evidence authority and source separation. |

## General Extract

The reusable model is:

```text
SourceSelector / InventoryEvidence / ReviewableSignal / LifecycleEvidenceEnvelope / UserDecision
  -> PromotionRecord
  -> Candidate / Premise / Reviewed / PromotedEntry / Policy / Constitution / Axiom / Contradiction / Retirement
```

General rules:

- Promotion is a reviewable, attributable, confidence-bearing decision.
- A PromotionRecord records one claim or decision.
- Source inputs are pointers, not raw dumps.
- Signals are review inputs, not truth.
- Evidence confidence and commitment confidence remain separate.
- Operational use requires visible status, scope, confidence, bridge validation when needed, and contradiction/retirement path.
- Bridge outcomes can be `aligned`, `partial`, `drift`, `insufficient`, or `contradicted`.
- Candidate operational ontology must not look canonical by layout.

## Particular Material For DomainSpec Handoff

These are not general Ontology Vault material:

- DomainSpec/AEO route-stage execution semantics.
- AEO telemetry envelope fields as implementation facts.
- DomainSpec authority map and constitution-specific governance.
- LifecycleEvidenceEnvelope details tied to AEO route/stage/terminal outcomes.
- Software-development-specific fixture scenarios.

They should move through a DomainSpec-owned package or work-pack, not remain as the primary layer inside Ontology Vault development.

## Excluded Candidates

| Candidate | Reason Excluded |
| --- | --- |
| `PRESENTATION.html` | Contributor onboarding artifact; not needed for selector-level general model. |
| `SUBSTACK-ARTICLE.md` | Public explanatory artifact; useful prose but not schema authority. |
| `GOALS.md` | Execution prompt list; not general model evidence. |
| `TASK-STRATEGIES.md` | Route mechanics; not needed for general schema extraction. |
| `external-research-appendix.md` | External pressure only; general model should stay local-evidence anchored for this split. |

## Blockers

None for context selection.

Non-blocking gaps:

- exact canonical branch label remains unresolved,
- operational branch acceptance remains unresolved,
- PromotionRecord standalone versus embedded remains unresolved,
- DomainSpec migration target path is not selected here.
