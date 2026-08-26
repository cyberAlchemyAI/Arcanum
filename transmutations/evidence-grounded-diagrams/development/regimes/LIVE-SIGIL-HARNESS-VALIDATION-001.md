# Regime: LIVE-SIGIL-HARNESS-VALIDATION-001

## Goal

Validate experiment-harness completeness and evidence usability.

## Prompt

- Prompt: `example-prompts/sigil-harness-validation-complex.md`

## Required Output Patterns

- `Profile validation`
- `Validation`
- `Promotion`

## Quality Bar

- Name NOT_RUN platform checks.
- Require low, medium, and complex coverage.

## Anti-Patterns

- Do not treat missing Bash execution as pass.

## Observability

- Record profile validation, runtime limitations, gaps, and promotion gate.

## Lessons To Capture

- Missing regimes, unusable outputs, and platform-specific blind spots.
