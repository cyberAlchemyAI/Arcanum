# Regime: CEL-LOW-001

## Goal

Validate invariant-preserving structural escalation for one explanatory concept.

## Prompt

- Prompt: `example-prompts/cel-low.md`

## Required Output Patterns

- `## Complexity Example Ladder Result`
- `### Low`
- `### Medium`
- `### Complex`
- `Rungs produced: 3/3`

## Authority Boundary

The ladder explains only; it grants no authority.

## Quality Bar

- The declared required output patterns must be present.
- The stable-identity invariant and authority boundary must remain intact.

## Anti-Patterns

- Do not accept missing declared output patterns.
- Do not turn the example into a recommendation, consent, or authority.

## Observability

- Record the regime ID, validation result, missing patterns, invariant drift, and authority-boundary drift.

## Lessons To Capture

- Missing output sections.
- Prompt ambiguity.
- Required-pattern drift.
- Invariant or authority-boundary drift.
