# TechniqueSpec: Abstraction-Level Guard

```text
technique_id: abstraction_level_guard
display_name: Abstraction-Level Guard
type: classifier
phase: concept mapping and closure
hook: before_layer_split, before_accept_split
activation: always
```

## Allowed Inputs

- `RunFrame.target_context`
- `ConceptLayer.label`
- `ConceptLayer.abstraction_level`
- `CandidateUnit.name`
- `CandidateUnit.responsibility`
- `CandidateUnit.inputs`
- `CandidateUnit.outputs`

## Allowed Labels

- purpose
- value/constraint
- capability
- function
- workflow/process
- policy/rule
- interface
- artifact
- operation

## Questions

- What abstraction level is this layer or unit operating at?
- Is the proposed child unit at the same level, one valid lower level, or an accidental cross-level jump?
- Is the Proposer treating a value as a component, a policy as a workflow, or an operation as a purpose?

## Emits

```text
technique_id
unit_or_layer_id
selected_level
level_rationale
cross_level_confusion: yes | no
decision: pass | flag | block
```

## Verdict Rules

- Pass: every accepted layer and candidate unit has an explicit level, and parent/child levels have a coherent relationship.
- Flag: a level is plausible but weakly justified.
- Block: the split depends on confusing abstraction levels in a way that breaks closure or recomposition.

## Failure Behavior

Reject the split, revise the unit, or return block when no responsible level can be assigned.

## Anti-Patterns

- Using level labels decoratively.
- Splitting a purpose directly into implementation operations without intermediate responsibility.
- Treating a policy, interface, and workflow as interchangeable.
