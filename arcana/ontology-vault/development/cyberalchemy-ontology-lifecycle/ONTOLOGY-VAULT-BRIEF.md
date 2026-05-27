# Ontology Vault Development Brief From CAOL

Status: candidate development brief
Date: 2026-05-27

## Objective

Map the CyberAlchemy Ontology Lifecycle package into the current Ontology Vault development track.

The immediate target is not to promote CAOL. The target is to use CAOL as a strong pressure test for:

- branch-aware ontology schema,
- PromotionRecord schema/template,
- bridge validation,
- operational branch governance,
- owner and gate rules,
- evidence confidence versus commitment confidence.

## Alignment With Current Ontology Vault Development

| Current Ontology Vault artifact | CAOL contribution | Development implication |
| --- | --- | --- |
| `BRANCH-AWARE-ONTOLOGY-CANDIDATE.md` | Operational Ontology candidate, bridge validation, promotion lifecycle. | Use CAOL as validation evidence for branch shape and operational context rules. |
| `BRANCH-NAMING-DISTILL.md` | Existing CAOL uses Business/System/Bridge language. | Treat `business` as a local alias for candidate `meaning`; do not force migration yet. |
| `BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` | PromotionRecord schema, ReviewableSignal, LifecycleEvidenceEnvelope. | Add or validate promotion/change-record concepts against the schema. |
| `DURABLE-SESSION-CONTEXT.md` | Candidate/promoted separation, no canonical mutation. | Preserve ontology-development-only session boundary. |

## Branch Mapping

| CAOL term | Current candidate branch mapping | Notes |
| --- | --- | --- |
| Business Ontology | `meaning` with local alias `business` | Candidate rename from `proposition` to `meaning` should preserve `business` as alias. |
| System Ontology | `system` | CAOL system evidence includes components, runtime surfaces, tests, adapters, capability contracts. |
| Operational Ontology | `operational` | Candidate top-level discriminator value with mandatory operating context. |
| Bridge Ontology | `bridge` | CAOL bridge validation outcomes should harden bridge schema. |
| ReviewableSignal | `bridge` or `operational` evidence input | Never truth by itself. |
| InventoryEvidence / SourceSelector | `bridge` evidence input | Inventory remains non-authority. |
| LifecycleEvidenceEnvelope | `bridge` or `system` evidence input | Especially useful for DomainSpec/AEO examples. |
| UserDecision | `meaning`, `operational`, or `bridge` evidence input depending on claim | Requires owner, scope, rationale, rejected alternatives. |
| PromotionRecord | `bridge` governance/change object or companion record | Should record a governed change to one claim, not replace ontology entry. |

## Candidate Schema Pressure

The current branch-aware schema candidate defines entries and edges. CAOL adds a pressure to separate:

- ontology entry,
- promotion/change record,
- evidence input,
- bridge validation result.

Candidate adjustment to test:

```yaml
record_kind: ontology_entry | promotion_record | evidence_input | bridge_validation
```

or keep separate templates:

```text
branch-aware-ontology-entry
promotion-record
bridge-validation
reviewable-signal
lifecycle-evidence-envelope
```

Do not decide this by theory alone. Validate with the CAOL first-slice scenario.

## PromotionRecord Boundary For Ontology Vault

CAOL boundary:

- one primary claim,
- source/evidence pointers,
- provenance,
- branch target,
- confidence split,
- review owner,
- gate result,
- use scope,
- contradiction path,
- rollback/retirement,
- route impact,
- bridge validation when needed.

Ontology Vault adaptation:

- PromotionRecord is likely a `bridge` or governance companion artifact.
- It should be required for promotion, contradiction, retirement, policy, constitution, or axiom decisions.
- It should not be required for every low-risk candidate map entry.
- It should not carry full source excerpts or raw telemetry.

## Bridge Validation Outcomes

CAOL defines:

| Outcome | Ontology meaning |
| --- | --- |
| `aligned` | Evidence supports relation across branches. |
| `partial` | Evidence supports a narrower claim or scope. |
| `drift` | Behavior diverges from meaning, system contract, or operational expectation. |
| `insufficient` | Evidence does not yet prove alignment. |
| `contradicted` | Evidence actively challenges the claim. |

Ontology Vault should test these outcomes against existing bridge edge types:

- `realized_by`
- `observed_by`
- `tested_by`
- `drifts_from`
- `operationalizes`
- `contradicted_by`
- `traced_to`

## First Validation Scenario

Use CAOL's first working slice:

```text
An Arcanum invoke/task-session style run produces enough reviewed evidence to propose an operational lesson:
future ontology lifecycle runs should require a context-builder handoff before synthesis.
```

For Ontology Vault, the scenario should validate:

- `meaning` branch role for the lifecycle rule or method claim,
- `system` branch role for Invoke/Task Session/Context Builder machinery,
- `operational` branch role for the situated CAOL run lesson,
- `bridge` role for the PromotionRecord and validation relation,
- evidence confidence and commitment confidence separation,
- ReviewableSignal as review input only,
- circular-authority guard if Arcanum is using Arcanum to improve Arcanum.

## Decisions Not Yet Made

| Decision | Current stance |
| --- | --- |
| Does Operational Ontology become canonical fourth branch? | Candidate only; validate as `operational` with required context. |
| Is `meaning` accepted over `proposition` or `business`? | Candidate label; preserve `business` alias for CAOL evidence. |
| Is PromotionRecord embedded or standalone? | Test standalone companion first. |
| Are bridge validation outcomes canonical? | Candidate; validate against examples. |
| Are axiom/constitution definitions canonical? | No; keep as candidate role semantics. |
| Do ReviewableSignals feed commitment confidence? | No; they affect evidence confidence only unless review owner explicitly commits. |

## Recommended Next Validation

Create a review-only Ontology Vault validation fixture under this package:

```text
arcana/ontology-vault/development/cyberalchemy-ontology-lifecycle/fixtures/CAOL-PROMOTION-RECORD-001.md
arcana/ontology-vault/development/cyberalchemy-ontology-lifecycle/fixtures/CAOL-PROMOTION-RECORD-001.validation.md
```

Do not mutate canonical Ontology Vault templates until this fixture validates.
