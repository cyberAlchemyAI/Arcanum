# Governed Candidate Bundle: Branch-Aware Ontology Schema

Status: published candidate
Published: 2026-06-01
Lifecycle owner: Ontology Vault development
Promotion boundary: governed candidate bundle, with canonical `promotion_record` record-kind semantics

## Purpose

This bundle is the published candidate surface for the branch-aware ontology schema.

It collects the validated development schema, JSON Schema candidate, fixtures, validators, validation report, and promotion-boundary decision into one stable reference point for future ontology work.

Published candidate means:

- the bundle may be referenced by future ontology development sessions;
- the schema is coherent enough for candidate validation and follow-up planning;
- the bundle is still not a final canonical Ontology Vault template or required external-system contract;
- `promotion_record` is canonical as an Ontology Vault record-kind / governance decision shape, while companion templates and separate schemas remain candidate or deferred surfaces.

## Source Decision

Decision gate:

```text
decision-gates/OVS-GATE-001-promotion-boundary.md
```

Selected option:

```text
promote-governed-candidate-bundle
```

Decision effect:

- carry the validated development surface forward as one coherent candidate package;
- keep final canonical templates behind later, narrower gates;
- keep Inventory and structured-action-schema as evidence or handoff surfaces, not ontology authorities;
- keep DomainSpec, CyberAlchemy, and future systems as separate owner-scoped adoption paths.

Follow-up decision:

```text
decision-gates/OVS-GATE-002-promotion-record-companion-boundary.md
```

Selected option:

```text
promotion-record-canonical-record-kind
```

Decision effect:

- promote `promotion_record` as the canonical Ontology Vault record-kind for owner-routed promotion decisions;
- keep the development JSON Schema as a candidate validation surface;
- keep companion templates and separate schemas behind later gates;
- use GoldenQuill as the canonical applied reference for grant-domain adaptation while preserving local owner boundaries.

## Bundle Contents

| Artifact | Role | Status |
| --- | --- | --- |
| `../BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md` | Human-readable candidate schema and rules. | published candidate |
| `schema/branch-aware-ontology-candidate.schema.yml` | Development JSON Schema candidate. | published candidate |
| `fixtures/valid/` | Positive examples across branch, axis, profile, and cross-system pressure cases. | validated |
| `fixtures/invalid/` | Targeted invalid examples for boundary and rule failures. | validated |
| `tests/validate_branch_schema.py` | Deterministic fixture validator. | validated development tool |
| `tests/validate_branch_json_schema.py` | JSON Schema fixture validator. | validated development tool |
| `VALIDATION-REPORT.md` | Validation verdict, coverage, gaps, and boundary check. | pass |
| `decision-gates/OVS-GATE-001-promotion-boundary.md` | Promotion-boundary decision record. | pass |
| `decision-gates/OVS-GATE-002-promotion-record-companion-boundary.md` | PromotionRecord record-kind and companion boundary decision record. | pass |
| `WORK-PACK.md` | Work history, execution evidence, current gaps, and next gates. | refreshed |

## Published Candidate Boundaries

Allowed use:

- cite this bundle as the current branch-aware ontology candidate;
- use its fixtures and validators for future ontology schema checks;
- design follow-up candidate templates from this evidence;
- prepare DomainSpec or other system-owned handoffs from this evidence;
- open narrower gates for canonical template adoption, PromotionRecord companion work, or external-system adoption;
- treat `record_kind: promotion_record` as the canonical ontology-governance decision shape.

Disallowed use:

- treat this bundle as final canonical Ontology Vault schema;
- mutate canonical Ontology Vault templates from this bundle without a later gate;
- treat the development JSON Schema candidate as a final governed schema;
- require Inventory to emit these fields;
- mutate structured-action-schema;
- mutate DomainSpec or CyberAlchemy source packages;
- require future systems to adopt the fields;
- treat `meaning` as the irreversible long-term global label without governance review.

## Current Candidate Model

Branch discriminator:

```text
branch_context.primary = meaning | system | operational | bridge
```

Record kinds:

```text
ontology_entry | promotion_record | evidence_input | bridge_validation
```

Canonical record-kind:

- `promotion_record`: canonical Ontology Vault governance decision record about one primary claim or relation. It carries evidence pointers, target owner or relation, review gate, confidence split, contradiction path, and rollback, retirement, or supersession path. It does not replace the owner artifact.

Core axes:

- `record_kind`: record family shape.
- `lifecycle_status`: maturity and permitted reliance.
- `claim_role`: semantic role played by the claim.
- `governance_outcome`: accepted policy, constitution, or axiom consequence.
- `bridge_outcome`: cross-branch validation outcome.

Cross-system pressure:

- Arcanum examples validate the ontology development path.
- CyberAlchemy PromotionRecord validates as `record_kind: promotion_record`.
- DomainSpec validates as a boundary-preserving bridge pressure fixture.
- Future-system fixture validates portability shape only and remains placeholder-level.
- GoldenQuill provides the canonical applied grant-domain reference: local `PromotionCandidate` and `OntologyVaultProjection` objects adapt into PromotionRecord-compatible owner decisions without making GoldenQuill the global ontology authority.

## Validation Commands

```bash
jq empty arcana/ontology-vault/development/schema-validation-plan/fixtures/valid/*.json arcana/ontology-vault/development/schema-validation-plan/fixtures/invalid/*.json
python3 arcana/ontology-vault/development/schema-validation-plan/tests/validate_branch_schema.py
python3 arcana/ontology-vault/development/schema-validation-plan/tests/validate_branch_json_schema.py
tools/validate-artifact-constitution.sh
```

Current validation status:

```text
branch-schema-fixtures: PASS
branch-json-schema-fixtures: PASS
Artifact Constitution: PASS with unrelated generated-artifact warnings
```

## Remaining Gates

| Gate | Purpose | Status |
| --- | --- | --- |
| OVS-GATE-002 | Decide PromotionRecord companion and canonical record-kind boundary. | pass |
| OVS-GATE-003 | Decide DomainSpec handoff route. | pending |
| Template promotion gate | Decide whether candidate profiles become authoring templates. | pending |
| Label governance gate | Decide whether `meaning` remains the long-term global branch label. | deferred |

## Next Route

Recommended next route:

```text
task-session: create GoldenQuill L0 PromotionRecord compatibility fixtures, or decision-gate OVS-GATE-003 for DomainSpec handoff
```

If ontology template promotion is the immediate goal, open a narrower template promotion gate first. Do not mutate canonical templates from this bundle alone.
