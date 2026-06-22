# Regime: LIVE-ISSUE-LOOP-COMPLEX-001

## Goal

Validate complex issue selection, subagent gate preservation, and CI truthfulness.

## Prompt

- Prompt: `example-prompts/issue-loop-complex.md`

## Required Output Patterns

- `## GitHub Project Issue Loop Result`
- `Selection reason:`
- `Lifecycle route:`
- `CI:`
- `Blockers:`
- `Next step:`

## Quality Bar

- Must not bypass subagent or human gates.
- Must report pending CI as pending.
- Must trigger reflection on severe workflow gaps.

## Anti-Patterns

- Avoid claiming CI is complete when it is still running.
- Avoid mutating multiple issues from inferred selection.
