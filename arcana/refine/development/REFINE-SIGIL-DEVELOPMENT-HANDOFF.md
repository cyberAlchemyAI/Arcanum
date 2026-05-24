# Sigil Development Handoff: Refine

## Handoff Summary

Create the reusable `refine` sigil from this development package.

Lifecycle owner: `sigil-development`

## Source Artifacts

- [REFINE-CONTEXT-PACK.md](REFINE-CONTEXT-PACK.md)
- [REFINE-INVOKE-DEFINE.md](REFINE-INVOKE-DEFINE.md)
- [REFINE-INTERROGATION.md](REFINE-INTERROGATION.md)
- [REFINE-RESEARCH-DECISION.md](REFINE-RESEARCH-DECISION.md)
- [REFINE-DISTILL-REVIEW.md](REFINE-DISTILL-REVIEW.md)
- [REFINE-INVOKE-DESIGN-PLAN.md](REFINE-INVOKE-DESIGN-PLAN.md)
- [WORK-PACK.md](WORK-PACK.md)

## Required Package Files

- `arcana/refine/README.md`
- `arcana/refine/SKILL.md`
- `arcana/refine/examples/seed-proposal.md`
- `arcana/refine/examples/existing-work-pack-preflight.md`
- `arcana/refine/examples/goal-blocked.md`

## Lifecycle Requirements

- Define `refine` as Arcana.
- Preserve Task Session as execution owner.
- Preserve `REFINEMENT-LOOP.md` as loop owner.
- Preserve Codex Goal as default runtime route after strict handoff coverage.
- Require confirmation before writing seed artifacts or delegating.
- Always offer research before running refinement.
- Block unsafe Codex Goal handoff rather than silently falling back.

## Validation Expectations

- Folder structure exists.
- README and SKILL agree on boundaries.
- Examples demonstrate seed proposal and blocked goal handoff.
- Registry links point to `arcana/refine/`.
- Searches show `refine` delegates through `task-session --runtime codex --via goal`.

## Promotion Note

This handoff creates a usable initial sigil package. Promotion readiness still requires later experiment-harness evidence with realistic prompts.
