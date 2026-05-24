# TechniqueSpec: Cognitive Load Check

```text
technique_id: cognitive_load_check
display_name: Cognitive Load Check
type: check
phase: proposal and balance
hook: after_proposer_pass, after_balancer_pass
activation: condition
```

## Trigger Conditions

- A split creates more than three sibling units.
- A split introduces new coordination roles or rules.
- The Balancer sees naming fragments without clear responsibility.
- The user asked for a compact or simple planning pass.

## Allowed Inputs

- `ConceptLayer.child_units`
- `Role conversation trace`
- `Balancer objections`
- `RunFrame.optimization_goal`

## Questions

- Did this split reduce what the user must hold in mind?
- Did it create more coordination burden than it removed?
- Are the units meaningful chunks or naming fragments?

## Emits

```text
technique_id
before_load_summary
after_load_summary
coordination_burden: lower | same | higher
fragment_risk: low | medium | high
recommended_adjustment
decision: pass | flag | block
```

## Verdict Rules

- Pass: the split lowers or preserves cognitive load while improving closure or recomposition.
- Flag: the split increases load, but the added structure handles a concrete tension.
- Block: the split increases load without improving closure, recomposition, evolution fit, or validation.

## Failure Behavior

Merge units, defer fragments, or reject the split.

## Anti-Patterns

- Equating smaller names with simpler understanding.
- Creating taxonomies before the user needs them.
