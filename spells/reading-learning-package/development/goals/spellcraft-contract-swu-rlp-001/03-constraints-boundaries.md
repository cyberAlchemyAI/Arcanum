# Constraints And Boundaries

## Write Scope

Allowed writes:

- `arcanum/spells/reading-learning-package/README.md`
- narrowly necessary updates inside `arcanum/spells/reading-learning-package/development/` only if they document the contract handoff evidence

Default write target:

- `arcanum/spells/reading-learning-package/README.md`

## Read Scope

Read from the development package and Refine handoff:

- [../../SPELL-HANDOFF.md](../../SPELL-HANDOFF.md)
- [../../DEFINE.md](../../DEFINE.md)
- [../../DESIGN.md](../../DESIGN.md)
- [../../PRESET-INTERVIEW.md](../../PRESET-INTERVIEW.md)
- [../../IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)
- [../../WORK-PACK.md](../../WORK-PACK.md)
- [../../VALIDATION.md](../../VALIDATION.md)
- [../../reading-learning-package.dispatch.json](../../reading-learning-package.dispatch.json)
- [../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RESULT.md](../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RESULT.md)
- [../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RUNTIME-HANDOFF.md](../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RUNTIME-HANDOFF.md)

## Capability Policy

Allowed:

- `spellcraft` for contract creation and review framing.
- `dispatch-spec` only for validating the existing development dispatch.

Not allowed in this goal:

- subagents,
- external research,
- runtime implementation SWUs,
- Task Session execution,
- Experiment Harness fixture creation,
- canonical promotion or registry readiness claims.

## Public Boundary

This lives in public `arcanum`. Do not introduce private parent-repo details, user-private context, local machine paths, or private implementation assumptions into the candidate contract.

## Source Authority

The contract may reference `research-tower`, `whisper`, `structured-interview-kits`, `distill`, and `context-builder` by handle and responsibility. It must not copy their full instructions or imply ownership of their internal lifecycle.
