# Regime: LIVE-SIGIL-NEW-001

## Goal

Validate that `refine` can run the refinement loop from `arcana/refine/REFINEMENT-LOOP.md` for a new-sigil idea and move from seed proposal into final refinement evidence through dispatch-spec route validation and native capability or approved subagent stage receipts.

## Prompt

- Prompt: `example-prompts/sigil-new-low.md`

## Required Output Patterns

- `## .+Result|# .+Result`
- `Status:|Validation:|Phase status:`
- `Final synthesis|final synthesis|Final refinement|final refinement|dispatch-spec|REFINE-DISPATCH`
- `Refinement Loop Evidence|Executed refinement loop stages`
- `Context Builder evidence baseline|Invoke Define|Interrogation refine-review|Research decision|Distill Repair|Invoke Plan|Final Interrogation`
- `Run manifest|Evidence index|Dispatch route|REFINE-DISPATCH|Runtime handoff|RUNTIME-HANDOFF|refinement-runs`

## Quality Bar

- Output must satisfy the target contract at `arcana/refine/SKILL.md`.
- Output must keep lifecycle and execution routes outside the refine loop.
- Output must be a real artifact body, not a save-summary.
- Output must include final refinement evidence, not only a route proposal.
- Output must include loop-stage evidence from `arcana/refine/REFINEMENT-LOOP.md`; planned stage names alone are not enough.
- Output must point to a materialized target-local run manifest and evidence index.
- If final native receipt proof did not happen, output must say `Status: flag` or `Status: block` and explain which dispatch validation or native runtime-backed stages are missing.

## Anti-Patterns

- Avoid accepting empty output or a summary that only says a file was saved.
- Avoid replacing sigil-development judgment with Experiment Harness mechanics.
- Avoid treating a seed proposal or route proposal as completed refinement evidence.
- Avoid treating Task Session or Sigil Development as a refine loop stage.
- Avoid creating the finished `arcana/x-ray` sigil during this experiment.

## Observability

- Attempt telemetry should record profile id sigil-development, lifecycle owner sigil-development, quality, anti-patterns, workflow gaps, and reflection trigger.

## Lessons To Capture

- Missing output sections.
- Prompt ambiguity.
- Observer gaps.
- Profile drift from the target contract.
