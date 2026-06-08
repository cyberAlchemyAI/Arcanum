# Methodology Profile: E2 Pareto Arbitration Quality

Status: draft
Version: 0.1.0

## Identity

- experiment_id: E2
- bundle_path: `experiments/E2-pareto-arbitration-quality/`
- tier: foundation
- owner: mars-research-scientist

## Framework Selection

- primary_framework: Wohlin-style controlled comparison
- measurement_model: GQM with benchmark objective annotations
- triangulation_policy: required reviewer scoring plus dominance classification

## Analysis Commitments

- required_steps:
  - run heuristic, weighted-sum, and Pareto-aware regimes on matched scenarios
  - classify chosen actions as dominated or frontier members
  - compare decision quality and regret across regimes
  - evaluate success criteria and claim impact
- optional_steps:
  - sensitivity analysis across objective-set sizes
  - scenario-family subgroup analysis
- confidence_and_effect_policy: descriptive effect sizes with scenario-level comparison tables

## Validity Threat Plan

- internal_validity: hold scenario inputs fixed across policy regimes
- external_validity: test across multiple scenario families before broader adoption claims
- construct_validity: objective scoring rubric must be stable enough for dominance classification
- conclusion_validity: do not treat small frontier gains as meaningful without agreement from reviewers

## Claim Adjudication Policy

- evidence_strength_levels: strong | moderate | weak | insufficient | contradicted
- status_levels: supported | partially supported | insufficient evidence | contradicted
- upgrade_rule: require improvement on dominated-selection rate plus stable or better reviewer quality
- downgrade_rule: downgrade if objective-noise sensitivity invalidates frontier judgments

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

- `experiments/E2-pareto-arbitration-quality/protocol.md`
- `experiments/E2-pareto-arbitration-quality/sources.md`
- `experiments/E2-pareto-arbitration-quality/results/*.md`
- `protocols/MOGT-PROTOCOL-CHECKLIST.md`
