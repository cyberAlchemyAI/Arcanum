# Methodology Profile Contract

Purpose: make methodology selection explicit, versioned, and enforceable before protocol approval.

Scope: all new and modified experiments in this project.

## Contract Rules

| Rule ID | Rule | Enforcement |
|---|---|---|
| MC1 | Every experiment must include `experiments/<experiment-key>/methodology.md`. | G1 blocks if methodology artifact is missing. |
| MC2 | Methodology profile must declare `tier` (`foundation` or `full`) and primary empirical framework. | Protocol review fails if tier/framework are absent. |
| MC3 | Methodology profile must define analysis commitments and validity-threat handling policy. | G1 blocks if analysis or validity commitments are missing. |
| MC4 | Protocol tier and methodology tier must match. | G1 blocks on tier mismatch. |
| MC5 | Method deviations must be declared in protocol and justified before execution. | Execution is blocked until deviation is approved and documented. |

## Required Methodology Fields

- experiment_id
- tier
- primary_framework
- measurement_model
- confidence_and_effect_policy
- validity_threat_plan
- claim_adjudication_policy
- reproducibility_metadata_requirements

## Canonical Path

- `experiments/<experiment-key>/methodology.md`

## Related Artifacts

- `research/projects/mars/definitions/MARS-PIPELINE.md`
- `protocols/MARS-PROTOCOL-CHECKLIST.md`
- `implementation/mars/templates/methodology-profile-template.md`
- `research/projects/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md`
