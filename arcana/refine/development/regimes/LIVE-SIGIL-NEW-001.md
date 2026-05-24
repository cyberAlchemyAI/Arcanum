# Regime: LIVE-SIGIL-NEW-001

## Goal

Validate that `refine` can move a new-sigil idea from seed proposal into final refinement evidence through the Task Session/Codex Goal execution path.

## Prompt

- Prompt: `example-prompts/sigil-new-low.md`

## Required Output Patterns

- `## .+Result|# .+Result`
- `Status:|Validation:|Phase status:`
- `Final refinement|final refinement|Task Session/Codex Goal|Task Session execution`

## Quality Bar

- Output must satisfy the target contract at `arcana/refine/SKILL.md`.
- Output must preserve lifecycle owner boundary: sigil-development.
- Output must be a real artifact body, not a save-summary.
- Output must include final refinement evidence, not only a proposed Task Session route.
- If final Task Session/Codex Goal execution did not happen, output must say `Status: flag` or `Status: block` and explain why the run is preflight-only.

## Anti-Patterns

- Avoid accepting empty output or a summary that only says a file was saved.
- Avoid replacing sigil-development judgment with Experiment Harness mechanics.
- Avoid treating a seed proposal or route proposal as completed refinement evidence.
- Avoid creating the finished `arcana/x-ray` sigil during this experiment.

## Observability

- Attempt telemetry should record profile id sigil-development, lifecycle owner sigil-development, quality, anti-patterns, workflow gaps, and reflection trigger.

## Lessons To Capture

- Missing output sections.
- Prompt ambiguity.
- Observer gaps.
- Profile drift from the target contract.
