# Regime: LIVE-SIGIL-UPDATE-001

## Goal

Validate the bundle-lifecycle update against the original contract.

## Prompt

- Prompt: `example-prompts/sigil-update-medium.md`

## Required Output Patterns

- `Sigil Development Result`
- `Files changed`
- `Next lifecycle step`

## Quality Bar

- Distinguish persistence, publication, and promotion.
- Preserve review read-only.

## Anti-Patterns

- Do not rewrite ownership boundaries silently.

## Observability

- Record lifecycle-owner judgment, validation, workflow gaps, and reflection trigger.

## Lessons To Capture

- Contract drift, update ambiguity, and ownership-boundary mistakes.
