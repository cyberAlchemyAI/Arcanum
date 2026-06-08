# Methodology Profile: E3 Negotiation Stability Under Conflict

Status: draft
Version: 0.1.0

## Identity

- experiment_id: E3
- bundle_path: `experiments/E3-negotiation-stability-under-conflict/`
- tier: foundation
- owner: mars-research-scientist

## Framework Selection

- primary_framework: controlled intervention experiment
- measurement_model: GQM with turn-level conflict telemetry
- triangulation_policy: required telemetry plus reviewer classification of resolution quality

## Analysis Commitments

- required_steps:
  - define contested scenarios with role-specific preferences
  - compare baseline disagreement handling to a negotiation-enabled regime
  - measure turn count, cycle count, escalation count, and convergence
  - evaluate success criteria and claim impact
- optional_steps:
  - subgroup analysis by conflict severity
  - qualitative coding of failure modes
- confidence_and_effect_policy: descriptive comparison with explicit stability thresholds

## Validity Threat Plan

- internal_validity: keep role prompts and scenario content fixed across regimes
- external_validity: do not generalize beyond bounded disagreement scenarios until more regimes are tested
- construct_validity: separate fast convergence from low-quality forced agreement
- conclusion_validity: require both stability and acceptable resolution quality

## Claim Adjudication Policy

- evidence_strength_levels: strong | moderate | weak | insufficient | contradicted
- status_levels: supported | partially supported | insufficient evidence | contradicted
- upgrade_rule: require improved convergence plus non-degraded reviewer resolution quality
- downgrade_rule: downgrade if extra turns accumulate without better conflict handling

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

| Deviation | Rationale      | Impact   | Approval |
| --------- | -------------- | -------- | -------- |
| none yet  | baseline draft | none yet | n/a      |

## Related Artifacts

- `experiments/E3-negotiation-stability-under-conflict/protocol.md`
- `experiments/E3-negotiation-stability-under-conflict/sources.md`
- `experiments/E3-negotiation-stability-under-conflict/results/*.md`
- `protocols/MOGT-PROTOCOL-CHECKLIST.md`
