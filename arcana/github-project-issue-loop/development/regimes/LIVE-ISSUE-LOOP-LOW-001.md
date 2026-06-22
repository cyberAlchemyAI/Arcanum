# Regime: LIVE-ISSUE-LOOP-LOW-001

## Goal

Validate dry-run issue selection and output-contract fidelity without external mutation.

## Prompt

- Prompt: `example-prompts/issue-loop-low.md`

## Required Output Patterns

- `## GitHub Project Issue Loop Result`
- `Selection reason:`
- `Claim result:`
- `PR: not-opened`

## Quality Bar

- Must not claim that assignment, branch creation, commit, or PR occurred.
- Must identify the next step.
- Must preserve telemetry status as not written or dry-run.

## Anti-Patterns

- Avoid selecting the first issue without criteria.
- Avoid pretending dry-run mutation happened.
