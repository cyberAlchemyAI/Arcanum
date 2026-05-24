# Refine Context Pack

## Task

Create the initial development package for a new Arcana sigil named `refine`.

## Mode

- Context mode: lean
- Handoff type: local development evidence
- Strict coverage: pass for initial design package

## Obligation Coverage

| Obligation | Status | Evidence |
| --- | --- | --- |
| Define the relationship between `refine` and Task Session. | covered | `arcana/task-session/SKILL.md`, `arcana/task-session/README.md` |
| Keep refinement loop mechanics in one contract instead of duplicating them across execution docs. | covered | `arcana/refine/REFINEMENT-LOOP.md` |
| Default later execution to Codex Goal while preserving strict handoff gates. | covered | `arcana/task-session/runtime-adapters/codex-goal.md`, `transmutations/codex-goal-profile/SKILL.md` |
| Route final sigil lifecycle ownership through Sigil Development. | covered | `arcana/sigil-development/SKILL.md` |
| Offer research before refinement and keep research bounded. | covered | `REFINEMENT-LOOP.md` Research Bounds and one-loop unit |
| Produce a seed package before mutation-capable Task Session execution. | covered | `spells/invoke/templates/work-pack.md`, Task Session work-pack contract |

## Included Context

- `arcana/task-session/SKILL.md`
  - Task Session owns selected task/SWU execution, context packs, decisions, gates, runtime selection, validation, and evidence sync.
  - It requires a bounded task or work-pack before mutation-capable execution.
- `arcana/refine/REFINEMENT-LOOP.md`
  - The loop contract owns the refinement phase order, loop limits, research bounds, mutation guard, and report obligations.
  - The one-loop unit now includes Context Builder, Invoke Define, Interrogation, Research Offer, Distill, Invoke Redefine plus Design/Plan, and lifecycle handoff or synthesis.
- `arcana/task-session/runtime-adapters/codex-goal.md`
  - Codex Goal is a runtime adapter, not Task Session identity.
  - It blocks without a selected task/SWU, bounded write scope, done criteria, validation, handoff pack Markdown, JSON/index, and strict coverage.
- `transmutations/codex-goal-profile/SKILL.md`
  - Converts one selected task/SWU into a native Codex Goal profile with outcome, verification, constraints, boundaries, iteration policy, and blocked stop condition.
- `arcana/sigil-development/SKILL.md`
  - Sigil Development owns sigil contract mutation, examples, experiment evidence, observability, reflection, and promotion readiness.
- `spells/invoke/templates/work-pack.md`
  - Work-packs are the executable planning dashboard: objective, tasks, SWUs, validation, blockers, gates, and execution handoff.

## Controlling Constraints

- `refine` must not become a second Task Session.
- `refine` must not copy the loop mechanics outside `REFINEMENT-LOOP.md`.
- `refine` must not silently fall back from Codex Goal to local execution.
- Research is offered by `refine`, but bounded by `REFINEMENT-LOOP.md`.
- Seed artifacts are proposal-first and only written after user confirmation.
- Sigil Development owns final reusable sigil lifecycle.

## Gap Status

No blocker prevents creating the initial `refine` development package. Runtime use of `refine` remains gated by future examples and experiment evidence.
