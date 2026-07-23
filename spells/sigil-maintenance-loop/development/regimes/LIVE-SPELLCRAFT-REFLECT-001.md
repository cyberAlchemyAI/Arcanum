# Regime: LIVE-SPELLCRAFT-REFLECT-001

## Goal

Validate Spellcraft observe/reflect behavior.

## Prompt

- Prompt: `example-prompts/spellcraft-reflect-complex.md`

## Required Output Patterns

- `## .+Result|# .+Result`
- `Status:|Validation:|Phase status:`
- `Inventory lookup:`
- `Mutation approval:`

## Quality Bar

- Output must satisfy the target contract at `arcanum/spells/sigil-maintenance-loop/README.md`.
- Output must preserve lifecycle owner boundary: spellcraft.
- Output must preserve the public/private boundary and route consumers through the canonical spell.
- Output must be a real artifact body, not a save-summary.

## Anti-Patterns

- Avoid accepting empty output or a summary that only says a file was saved.
- Avoid replacing spellcraft judgment with Experiment Harness mechanics.

## Observability

- Attempt telemetry should record profile id spellcraft, lifecycle owner spellcraft, quality, anti-patterns, workflow gaps, and reflection trigger.

## Lessons To Capture

- Missing output sections.
- Prompt ambiguity.
- Observer gaps.
- Profile drift from the target contract.
