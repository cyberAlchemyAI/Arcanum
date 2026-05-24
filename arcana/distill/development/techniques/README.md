# Distill Techniques

## Purpose

This directory specifies each technique in the Distill technique pack.

Techniques are not optional plugins. They are named instruments used by the optimizer: some are always-on gates, some are lenses, some are Balancer checks, some are closeout passes, and one is a Tournament mode mechanic.

## Common TechniqueSpec Shape

Each technique file should use this contract:

```text
technique_id: stable id
display_name: human name
type: gate | lens | classifier | mode mechanic | check | closeout
phase: setup | concept mapping | proposal | balance | closure | pitch-off | final synthesis | handoff
hook: one PhaseHook from MODE-TECHNIQUE-SURFACE-DESIGN.md
activation: always | condition | mode-required | risk-required | user-requested
allowed_inputs: state fields the technique may inspect
emits: trace fields the technique must write
pass_condition: when the technique succeeds
flag_condition: when the technique leaves a non-blocking concern
block_condition: when the technique prevents readiness
failure_behavior: pass | flag | block | skip-with-reason | route
```

## Technique Registry

| Technique ID | Name | Type | Hook | Default Activation | Spec |
| --- | --- | --- | --- | --- | --- |
| `abstraction_level_guard` | Abstraction-Level Guard | classifier | `before_layer_split`, `before_accept_split` | always | [abstraction-level-guard.md](abstraction-level-guard.md) |
| `recomposition_proof` | Recomposition Proof | gate | `before_accept_split`, `before_verdict` | always | [recomposition-proof.md](recomposition-proof.md) |
| `evolution_profile` | Evolution Profile | lens | `after_intent_confirmation`, `after_proposer_pass`, `before_verdict` | always when evolution or future scale appears | [evolution-profile.md](evolution-profile.md) |
| `frame_expiry_note` | Frame-Expiry Note | closeout | `before_verdict` | always | [frame-expiry-note.md](frame-expiry-note.md) |
| `cognitive_load_check` | Cognitive Load Check | check | `after_proposer_pass`, `after_balancer_pass` | condition | [cognitive-load-check.md](cognitive-load-check.md) |
| `requisite_variety_check` | Requisite Variety Check | check | `after_balancer_pass`, `before_verdict` | condition | [requisite-variety-check.md](requisite-variety-check.md) |
| `boundary_object_check` | Boundary-Object Check | check | `after_intent_confirmation`, `after_balancer_pass` | condition | [boundary-object-check.md](boundary-object-check.md) |
| `concept_vs_knowledge_status` | Concept-vs-Knowledge Status | classifier | `after_proposer_pass`, `before_accept_split` | condition | [concept-vs-knowledge-status.md](concept-vs-knowledge-status.md) |
| `premortem_pass` | Premortem Pass | closeout | `before_verdict` | mode-required outside Compact when risk is medium/high | [premortem-pass.md](premortem-pass.md) |
| `set_based_tournament` | Set-Based Tournament | mode mechanic | `before_pitch_off` | Tournament mode | [set-based-tournament.md](set-based-tournament.md) |
| `navigable_result_check` | Navigable Result Check | closeout | `before_verdict` | always | [navigable-result-check.md](navigable-result-check.md) |

## Mode Compatibility

| Technique ID | Compact | Standard | Tournament | Deep | Validate |
| --- | --- | --- | --- | --- | --- |
| `abstraction_level_guard` | required | required | required | required | required |
| `recomposition_proof` | required | required | required | required | required |
| `evolution_profile` | required when future scale appears | required | required | required | required when design includes extensibility claims |
| `frame_expiry_note` | required | required | required | required | required |
| `cognitive_load_check` | trigger only | trigger only | trigger only | trigger only | trigger only |
| `requisite_variety_check` | trigger only | trigger only | trigger only | trigger only | trigger only |
| `boundary_object_check` | trigger only | trigger only | trigger only | trigger only | trigger only |
| `concept_vs_knowledge_status` | trigger only | trigger only | trigger only | trigger only | trigger only |
| `premortem_pass` | skipped unless requested | required | required | required | required for medium/high risk |
| `set_based_tournament` | not applicable | not applicable | required | optional only if multiple tracks | not applicable |
| `navigable_result_check` | required | required | required | required | required |

## Trace Aggregation Rules

The technique pack trace should include one row per technique activation:

| Field | Meaning |
| --- | --- |
| technique_id | Stable technique id. |
| hook | Phase hook where the technique ran or was skipped. |
| activation | always, condition, mode-required, risk-required, or user-requested. |
| trigger_summary | Why it ran or why it was skipped. |
| inspected_state | State fields used. |
| emitted_output | Short summary of trace output. |
| decision | pass, flag, block, route, or skipped-with-reason. |
| readiness_effect | unchanged, downgraded-to-flag, downgraded-to-block, or route. |

## Gate Result

- Status: pass
- Reason: The technique index names all included techniques, links each detailed spec, defines compatibility by mode, and preserves shared trace aggregation rules.
