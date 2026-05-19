# TASK-CLO-005: Define Observability And Reflection

## Goal

Define how meaningful Concept Layer Optimizer executions emit telemetry and trigger reflection.

## Layer

L2 Runtime And Observability

## Micro-Layers

- L2.3 Signal Schema
- L4.1 Reflection Signals

## Source Contracts

- [../../SIGIL-HANDOFF.md](../../SIGIL-HANDOFF.md)
- [../../MODE-TECHNIQUE-SURFACE-DESIGN.md](../../MODE-TECHNIQUE-SURFACE-DESIGN.md)
- [../../../../sigil-development/SKILL.md](../../../../sigil-development/SKILL.md)
- [.arcanum/observability/README.md](../../../../../.arcanum/observability/README.md)

## Inputs

- validation findings from TASK-CLO-004,
- existing Arcanum observability conventions,
- Concept Layer Optimizer output contract,
- reflection needs from sigil-development.

## Output Artifacts

- `arcana/concept-layer-optimizer/templates/usage-telemetry.md`
- reflection threshold documentation in README, SKILL, or templates

## Implementation Steps

1. Define what counts as a meaningful Concept Layer Optimizer execution.
2. Define signal fields for objective-output confirmation, target context, mode, budget, recursive rounds, techniques used, verdict, drift, and navigation closeout.
3. Define which gaps are invoke-owned versus target-artifact-owned when the sigil is used through invoke.
4. Define reflection thresholds for repeated drift, blocked runs, technique overuse, navigation failures, and missing evolution profiles.
5. Map each signal to a review question so telemetry is useful rather than decorative.
6. Link the telemetry template from the README/SKILL only after those package files exist.

## Edge Cases

- Do not collect telemetry that cannot drive a review or maintenance action.
- Do not make observability mandatory for manual use when the local observer is unavailable.
- Do not conflate a blocked target artifact with an invoke or sigil failure.
- Reflection triggers should not automatically mutate the sigil.

## Smallest Working Units

| SWU | Micro-Layer | Work | Acceptance |
| --- | --- | --- | --- |
| SWU-CLO-010 | L2.3 | Define usage telemetry. | Meaningful execution and signal fields are named. |
| SWU-CLO-011 | L4.1 | Define reflection thresholds. | Manual, threshold, drift, navigation, and gap triggers are documented. |

## Verification

```bash
rg -n "meaningful execution|signal|objective-output|verdict|reflection|threshold" arcana/concept-layer-optimizer
```

## Done When

- Usage telemetry template or section exists.
- Reflection triggers align with sigil-development.
- Observability can distinguish invoke gaps from target-artifact gaps when applicable.
