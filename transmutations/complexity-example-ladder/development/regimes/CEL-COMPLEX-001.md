# Regime: CEL-COMPLEX-001

## Goal

Validate authority-neutral decision explanation with dependencies, failure, defer,
and stop.

## Prompt

- Prompt: `example-prompts/cel-complex.md`

## Required Output Patterns

- `## Complexity Example Ladder Result`
- `### Low`
- `### Medium`
- `### Complex`
- `Decision effect: none`
- `BLOCK`

## Authority Boundary

Examples cannot select an option or clear the caller's gate.

## Quality Bar

- The declared required output patterns must be present.
- The blocked gate, continuation states, and authority boundary must remain intact.

## Anti-Patterns

- Do not accept missing declared output patterns or invented product behavior for defer and stop.
- Do not turn the example into a recommendation, consent, selection, or authority.

## Observability

- Record the regime ID, validation result, missing patterns, gate drift, and authority-boundary drift.

## Lessons To Capture

- Missing output sections.
- Prompt ambiguity.
- Required-pattern or continuation-state drift.
- Gate or authority-boundary drift.
