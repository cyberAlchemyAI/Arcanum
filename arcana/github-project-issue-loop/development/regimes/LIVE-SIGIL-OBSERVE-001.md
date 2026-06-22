# Regime: LIVE-SIGIL-OBSERVE-001

## Goal

Validate Sigil Development observability review behavior.

## Prompt

- Prompt: `example-prompts/sigil-observe-medium.md`

## Required Output Patterns

- `## .+Result|# .+Result`
- `Status:|Validation:|Phase status:`

## Quality Bar

- Output must satisfy the target contract at `arcana/github-project-issue-loop/SKILL.md`.
- Output must preserve lifecycle owner boundary: sigil-development.
- Output must be a real artifact body, not a save-summary.

## Anti-Patterns

- Avoid accepting empty output or a summary that only says a file was saved.
- Avoid replacing sigil-development judgment with Experiment Harness mechanics.

## Observability

- Attempt telemetry should record profile id sigil-development, lifecycle owner sigil-development, quality, anti-patterns, workflow gaps, and reflection trigger.

## Lessons To Capture

- Missing output sections.
- Prompt ambiguity.
- Observer gaps.
- Profile drift from the target contract.
