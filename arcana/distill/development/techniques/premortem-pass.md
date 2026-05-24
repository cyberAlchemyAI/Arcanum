# TechniqueSpec: Premortem Pass

```text
technique_id: premortem_pass
display_name: Premortem Pass
type: closeout
phase: final synthesis
hook: before_verdict
activation: mode-required outside Compact when risk is medium/high
```

## Activation Policy

- Compact: skipped unless user requests it or risk is severe.
- Standard: required.
- Tournament: required after pitch-off.
- Deep: required.
- Validate: required for medium/high-risk designs.

## Allowed Inputs

- `Selected CandidateUnit`
- `Evolution profile trace`
- `Tension ledger`
- `Deferred complexity`
- `Frame-expiry note`

## Prompt

```text
Six months later, this optimization point failed. What was the most likely reason?
```

## Failure Categories

- too small to absorb expected evolution
- too broad to validate
- wrong abstraction level
- hidden coupling
- missing stakeholder boundary
- future scale assumed but not real
- no recomposition path
- unsupported knowledge claim

## Emits

```text
technique_id
likely_failure_reason
failure_category
guardrail_or_adjustment
readiness_effect: unchanged | downgraded-to-flag | downgraded-to-block
decision: pass | flag | block
```

## Verdict Rules

- Pass: the likely failure is acceptable, guarded, or already captured as deferred complexity.
- Flag: the likely failure is plausible but manageable with a guardrail.
- Block: the likely failure undermines closure, recomposition, or proportionate complexity.

## Failure Behavior

Add a guardrail, adjust the unit, downgrade readiness, or route the tension.

## Anti-Patterns

- Producing generic failure guesses.
- Using premortem to reopen all already-settled design choices without new evidence.
