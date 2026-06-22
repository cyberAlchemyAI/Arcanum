# Refine Seed Proposal

## Target

- Target package: `arcanum/spells/reading-learning-package/development/`
- Primary artifact under review: [WORK-PACK.md](../../WORK-PACK.md)
- Supporting artifacts: [DEFINE.md](../../DEFINE.md), [DESIGN.md](../../DESIGN.md), [IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md), [PRESET-INTERVIEW.md](../../PRESET-INTERVIEW.md), [SPELL-HANDOFF.md](../../SPELL-HANDOFF.md), [VALIDATION.md](../../VALIDATION.md), [INVOKE-RESULT.md](../../INVOKE-RESULT.md), [reading-learning-package.dispatch.json](../../reading-learning-package.dispatch.json)

## Raw Intent

Review the current plan for gaps before implementation so the reading-learning-package spell can move into the right implementation route without smuggling unresolved assumptions into canonical spell work.

## Desired Outcome

Produce an implementation-readiness review that classifies the plan as one of:

- `implementation-ready`
- `repair-needed`
- `blocked`

The review must name every blocking or repair-worthy gap with its source artifact, owner, and next action.

## Scope

In scope:

- Verify whether the work-pack is complete enough to implement.
- Check that `research-tower` and `whisper` ownership boundaries are preserved.
- Check that the preset interview is concrete enough to create user-tailored presets from examples rather than from generic answers.
- Check that PDF composition has an implementable renderer strategy, validation surface, and fallback behavior.
- Check that the spellcraft handoff is clear enough to install or defer the canonical spell.

Out of scope before confirmation:

- Running the full refinement loop.
- Installing the spell under a canonical runtime surface.
- Creating renderer code, templates, or CLI adapters.
- Launching subagents.
- Running external research.

## Preset And Research Mode

- Refine preset: `standard`
- Research mode: `research-if-gap-appears`
- Research gate: any external research must pause for explicit approval and cite the gap that makes it necessary.

## Proposed Route

1. Build a context pack from the package artifacts.
2. Re-run Invoke-style define/design/plan checks against the package.
3. Use Interrogation-style review passes to identify missing decisions, weak artifact contracts, and implementation blockers.
4. Distill the smallest repair unit if gaps exist.
5. Produce a final review result and runtime handoff.

## Subagent Strategy

No subagents are proposed for the initial plan review. The target is narrow and source-local enough for a native sequential refine loop. If the review discovers independent contested lanes, a later route can ask for approval to spawn role-bound agents with receipts.

## Stop Point

This seed is a strategy proposal only. Runtime-backed stages start only after explicit operator confirmation.
