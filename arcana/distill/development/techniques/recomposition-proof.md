# TechniqueSpec: Recomposition Proof

```text
technique_id: recomposition_proof
display_name: Recomposition Proof
type: gate
phase: closure and final synthesis
hook: before_accept_split, before_verdict
activation: always
```

## Allowed Inputs

- `ConceptLayer.parent`
- `ConceptLayer.child_units`
- `CandidateUnit.inputs`
- `CandidateUnit.outputs`
- `CandidateUnit.responsibility`
- `TensionEntry[]`

## Questions

- How do the smaller units combine back into the upper layer?
- What coordination is required for recomposition?
- Is any required coordination unnamed hidden glue?
- What would fail if these units could not recompose?

## Emits

```text
technique_id
parent_layer
child_units
recomposition_statement
hidden_glue: none | named | unresolved
failure_if_wrong
decision: pass | flag | block
```

## Verdict Rules

- Pass: the recomposition path is explicit and does not depend on hidden glue.
- Flag: recomposition is plausible but depends on a named deferred mechanism.
- Block: the selected unit cannot explain how it adds back into the upper layer.

## Failure Behavior

Reject the split, merge units, name the missing interface, or route unresolved contradiction to Robot-Talks.

## Anti-Patterns

- Accepting a split because the parts sound tidy.
- Hiding coordination in words like "manager", "adapter", "orchestrator", or "policy" without responsibility.
