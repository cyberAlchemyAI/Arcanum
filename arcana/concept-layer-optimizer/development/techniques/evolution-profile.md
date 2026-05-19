# TechniqueSpec: Evolution Profile

```text
technique_id: evolution_profile
display_name: Evolution Profile
type: lens
phase: setup, proposal, final synthesis
hook: after_intent_confirmation, after_proposer_pass, before_verdict
activation: always when future scale, extensibility, or open-endedness appears
```

## Allowed Inputs

- `RunFrame.target_context`
- `RunFrame.constraints`
- `CandidateUnit.responsibility`
- `CandidateUnit.evolution_profile`
- `Balancer objections`

## Evolution Pressure Categories

- variants
- new actors
- volume or performance growth
- new integrations
- policy or rule growth
- migration or replacement pressure
- governance or review pressure
- learning uncertainty
- none known yet

## Questions

- What type of evolution is likely for this solution?
- Is the future pressure concrete, likely but vague, or unknown?
- What is the smallest extension boundary that prevents brittle minimalism?
- What heavier mechanism should be deferred?

## Emits

```text
technique_id
evolution_categories
confidence: concrete | likely-vague | unknown
smallest_extension_boundary
deferred_mechanism
decision: pass | flag | block
```

## Verdict Rules

- Pass: the evolution pressure is named or explicitly unknown, and the selected unit stays proportionate.
- Flag: evolution is likely but vague; preserve a boundary and defer mechanism.
- Block: the design requires an unconfirmed evolution profile to be responsible.

## Failure Behavior

Ask one blocker question if the profile affects readiness; otherwise record deferred complexity.

## Anti-Patterns

- Treating every possible future as current scope.
- Treating open-endedness as optional when concrete evolution pressure is already visible.
