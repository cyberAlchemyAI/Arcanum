# Methodology Profile: E1 Tradeoff Traceability Baseline

Status: draft
Version: 0.1.0

## Identity

- experiment_id: E1
- bundle_path: `experiments/E1-tradeoff-traceability-baseline/`
- tier: foundation
- owner: mars-research-scientist

## Framework Selection

- primary_framework: Wohlin-style comparative experiment
- measurement_model: GQM with blinded reviewer rubric
- triangulation_policy: required reviewer scoring plus telemetry trace inspection

## Analysis Commitments

- required_steps:
  - paired baseline and intervention runs on the same scenario set
  - blinded reviewer reconstruction scoring
  - descriptive comparison of traceability coverage and acceptance scores
  - success-criteria evaluation
- optional_steps:
  - subgroup comparison by scenario difficulty
  - qualitative coding of explanation failure modes
- confidence_and_effect_policy: descriptive effect sizes and reviewer-agreement reporting

## Validity Threat Plan

- internal_validity: keep scenario set fixed across policy regimes and blind reviewers to policy identity
- external_validity: use varied decision scenarios before claiming generalizability
- construct_validity: traceability coverage rubric must distinguish explanation quality from decision quality
- conclusion_validity: do not upgrade claims without repeated improvement across multiple scenarios

## Claim Adjudication Policy

- evidence_strength_levels: strong | moderate | weak | insufficient | contradicted
- status_levels: supported | partially supported | insufficient evidence | contradicted
- upgrade_rule: require threshold pass on traceability coverage and non-inferior decision acceptance
- downgrade_rule: downgrade if quality drops materially or reviewer agreement is unstable

## Reproducibility Requirements

Mandatory metadata fields:

- experiment_id
- run_id
- timestamp
- model
- model_temperature
- system_prompt_hash
- operator

## Deviations

List any approved deviations from baseline methodology.

| Deviation | Rationale      | Impact   | Approval |
| --------- | -------------- | -------- | -------- |
| none yet  | baseline draft | none yet | n/a      |

## Related Artifacts

- `experiments/E1-tradeoff-traceability-baseline/protocol.md`
- `experiments/E1-tradeoff-traceability-baseline/sources.md`
- `experiments/E1-tradeoff-traceability-baseline/results/*.md`
- `protocols/MOGT-PROTOCOL-CHECKLIST.md`
