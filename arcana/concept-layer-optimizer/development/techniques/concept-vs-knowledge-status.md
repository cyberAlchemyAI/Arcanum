# TechniqueSpec: Concept-vs-Knowledge Status

```text
technique_id: concept_vs_knowledge_status
display_name: Concept-vs-Knowledge Status
type: classifier
phase: proposal and closure
hook: after_proposer_pass, before_accept_split
activation: condition
```

## Trigger Conditions

- A candidate unit depends on uncertain domain knowledge.
- The Proposer introduces a novel construct.
- Evidence is missing, contradictory, or only assumed.
- The selected optimization point may depend on a factual claim.

## Allowed Inputs

- `CandidateUnit`
- `Evidence or assumption trace`
- `Existing artifacts`
- `Balancer objections`

## Questions

- Is this unit a concept claim or a knowledge-backed unit?
- What evidence supports it?
- Does missing knowledge block closure, or can it be recorded as a non-blocking assumption?

## Emits

```text
technique_id
unit_id
status: concept-claim | knowledge-backed | mixed
evidence_summary
assumption_summary
decision: pass | flag | block
```

## Verdict Rules

- Pass: knowledge-backed units cite enough evidence, and concept claims are not treated as settled facts.
- Flag: the unit can proceed with an explicit assumption.
- Block: the selected optimization point depends on unsupported knowledge.

## Failure Behavior

Route to research, Decision-Gate, or deferred gap depending on whether the uncertainty blocks readiness.

## Anti-Patterns

- Treating confident language as evidence.
- Blocking on uncertainty that does not affect the current optimization point.
