# Regime: CEL-MED-001

## Goal

Validate equal comparative option coverage inside shared scenarios.

## Prompt

- Prompt: `example-prompts/cel-medium.md`

## Required Output Patterns

- `## Complexity Example Ladder Result`
- `### Low`
- `### Medium`
- `### Complex`
- `Decision effect: none`

## Authority Boundary

The ladder does not recommend, choose, or change admissibility.

## Quality Bar

- The declared required output patterns must be present.
- Shared-scenario option coverage and the authority boundary must remain intact.

## Anti-Patterns

- Do not accept missing declared output patterns or unequal option coverage.
- Do not turn the example into a recommendation, consent, or authority.

## Observability

- Record the regime ID, validation result, missing patterns, option-coverage drift, and authority-boundary drift.

## Lessons To Capture

- Missing output sections.
- Prompt ambiguity.
- Required-pattern or option-coverage drift.
- Authority-boundary drift.
