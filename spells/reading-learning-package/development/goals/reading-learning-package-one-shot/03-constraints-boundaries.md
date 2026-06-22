# Constraints And Boundaries

## Write Scope

Allowed writes are limited to:

- `arcanum/spells/reading-learning-package/`

Recommended implementation subpaths:

- `arcanum/spells/reading-learning-package/README.md`
- `arcanum/spells/reading-learning-package/runtime/`
- `arcanum/spells/reading-learning-package/templates/`
- `arcanum/spells/reading-learning-package/fixtures/`
- `arcanum/spells/reading-learning-package/validation/`
- `arcanum/spells/reading-learning-package/development/` only for narrow evidence updates tied to this one-shot profile

## Read Scope

Use the development package and Refine handoff first:

- [../../README.md](../../README.md)
- [../../DEFINE.md](../../DEFINE.md)
- [../../PRESET-INTERVIEW.md](../../PRESET-INTERVIEW.md)
- [../../DESIGN.md](../../DESIGN.md)
- [../../IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)
- [../../WORK-PACK.md](../../WORK-PACK.md)
- [../../SPELL-HANDOFF.md](../../SPELL-HANDOFF.md)
- [../../VALIDATION.md](../../VALIDATION.md)
- [../../reading-learning-package.dispatch.json](../../reading-learning-package.dispatch.json)
- [../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RESULT.md](../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RESULT.md)
- [../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RUNTIME-HANDOFF.md](../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/RUNTIME-HANDOFF.md)
- [../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/evidence-index.json](../../refinement-runs/20260620T034710Z-reading-learning-package-plan-review/evidence-index.json)

## Capability Policy

Allowed capability lanes:

- `spellcraft`: contract creation and final spell readiness review.
- `task-session`: bounded implementation of ordered runtime SWUs.
- `experiment-harness`: local fixture structure and fixture result reporting.
- `decision-gate`: only for blocker-level decisions that cannot be safely defaulted.
- `dispatch-spec`: validation of existing dispatch route shape.

Not allowed:

- subagents unless the operator separately approves them,
- external research unless a blocker-level gap explicitly requires it and the operator approves it,
- mutation outside `arcanum/spells/reading-learning-package/`,
- promotion of generated learning output into canonical source authority,
- copying full `research-tower` or `whisper` skill bodies into this spell.

## Authority Boundaries

- `research-tower` remains source authority.
- `whisper` remains composition authority.
- `reading-learning-package` owns orchestration, package artifacts, source trace, PDF fallback, and validation report.
- Generated PDFs or manuscripts are learning outputs, not source evidence.

## Public Boundary

This lives in public `arcanum`. Use only public-safe synthetic fixtures and repository-local relative paths.
