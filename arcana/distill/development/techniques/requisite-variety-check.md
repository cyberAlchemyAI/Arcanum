# TechniqueSpec: Requisite Variety Check

```text
technique_id: requisite_variety_check
display_name: Requisite Variety Check
type: check
phase: balance and final synthesis
hook: after_balancer_pass, before_verdict
activation: condition
```

## Trigger Conditions

- The Balancer suspects overbuilding.
- The Balancer suspects underbuilding or brittle minimalism.
- External variation is visible: actors, policies, integrations, volume, contexts, failure modes.
- The unit's internal mechanisms seem too weak or too elaborate for the target context.

## Allowed Inputs

- `RunFrame.target_context`
- `RunFrame.constraints`
- `CandidateUnit.inputs`
- `CandidateUnit.outputs`
- `Evolution profile trace`
- `Balancer objections`

## Questions

- What external variety will hit this unit?
- What internal variety can the unit use to respond?
- Is the unit underfit, overfit, or proportionate?
- What is the smallest adjustment that restores fit?

## Emits

```text
technique_id
external_variety
internal_variety
fit_verdict: underfit | overfit | proportionate
smallest_adjustment
decision: pass | flag | block
```

## Verdict Rules

- Pass: internal variety is proportionate to external variety.
- Flag: fit is close but needs a named guardrail or deferred mechanism.
- Block: the unit cannot handle known external variety, or it includes unjustified mechanisms.

## Failure Behavior

Adjust the selected unit, record overfit or underfit tension, or route blocker ambiguity to Decision-Gate.

## Anti-Patterns

- Using this check to justify broad abstraction without concrete external variety.
- Ignoring known variation because it feels like future scale.
