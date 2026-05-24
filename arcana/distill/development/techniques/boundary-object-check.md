# TechniqueSpec: Boundary-Object Check

```text
technique_id: boundary_object_check
display_name: Boundary-Object Check
type: check
phase: setup and balance
hook: after_intent_confirmation, after_balancer_pass
activation: condition
```

## Trigger Conditions

- Multiple teams, roles, institutions, audiences, or disciplines share the concept.
- The same word has different meanings across actors.
- A plan, governance model, diagram, roadmap, or workflow must coordinate local interpretations.

## Allowed Inputs

- `RunFrame.target_context`
- `RunFrame.constraints`
- `ConceptLayer.label`
- `Tension ledger`
- `Role conversation trace`

## Questions

- Who must share this concept?
- What meaning must remain stable across actors?
- What can vary locally without breaking recomposition?
- Which actor owns the unresolved ambiguity?

## Emits

```text
technique_id
actors
stable_shared_meaning
allowed_local_variation
boundary_tension
route_if_unresolved
decision: pass | flag | block
```

## Verdict Rules

- Pass: shared meaning and allowed local variation are explicit enough for the current context.
- Flag: local variation is known but non-blocking.
- Block: stakeholder ambiguity prevents choosing a responsible optimization point.

## Failure Behavior

Route to Robot-Talks for cross-layer or multi-actor investigation, or Decision-Gate for a blocker choice.

## Anti-Patterns

- Forcing all actors into the same internal model when only a stable shared interface is needed.
- Ignoring actor-specific meanings in governance or organizational designs.
