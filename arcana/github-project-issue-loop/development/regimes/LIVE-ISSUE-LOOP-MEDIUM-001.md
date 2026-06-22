# Regime: LIVE-ISSUE-LOOP-MEDIUM-001

## Goal

Validate the standard issue-claim to PR delivery loop.

## Prompt

- Prompt: `example-prompts/issue-loop-medium.md`

## Required Output Patterns

- `## GitHub Project Issue Loop Result`
- `Lifecycle route:`
- `Branch/commit:`
- `PR:`
- `Validation:`
- `Telemetry:`

## Quality Bar

- Must preserve one-issue scope.
- Must report assignment and project status truthfully.
- Must include validation command status.

## Anti-Patterns

- Avoid always invoking every template when the ticket does not need it.
- Avoid opening a PR without local validation evidence.
