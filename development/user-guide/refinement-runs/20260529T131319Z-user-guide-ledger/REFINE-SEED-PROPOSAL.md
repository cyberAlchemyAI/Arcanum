# Refine Seed Proposal: User Ledger And Guide

## Target

`development/user-guide/`

## Raw Operator Intent

Create a new part of the Arcanum framework and a family of sigils and spells around `User` and `Guide`.

The `User` function should behave as a ledger for user profile, prior experiences, vocabulary preferences, analogy/metaphor preferences, clarification history, and mastered definitions. `Guide` should use that ledger to help a user arrive at understanding across domains, from concrete examples to meta-level primitives and abstractions.

## Refinement Objective

Design the first non-executed refinement package for a candidate `User` / `Guide` capability family that:

- preserves user learning evidence in a governed ledger,
- lets Guide adapt vocabulary and analogies from observed clarification attempts,
- turns solved blockers and confirmed clarifications into ledger updates,
- seeds a CyberAlchemy installation game that elicits prior experience and domain fluency,
- supports cross-domain explanation such as sales-to-software, software-to-science, and music-to-construction,
- keeps mastered definitions in a user glossary over time,
- avoids canonical sigil, spell, registry, command, or runtime mutation during this refine run.

## Write Scope

This run may write only under:

- `development/user-guide/refinement-runs/20260529T131319Z-user-guide-ledger/`

This run must not create canonical `arcana/user`, `spells/guide`, registry entries, install scripts, runtime hooks, or persistent user memory schemas. Those are recommended next routes only.

## Source Context

| Source | Use |
| --- | --- |
| User request, 2026-05-29 | Primary intent for User, Guide, install game, glossary, and cross-domain explanation. |
| `development/craft/CRAFT-RECURSIVE-LEDGER-DEFINE.md` | Reference model for a ledger that is larger than a work-pack. |
| `development/craft/CRAFT-MVP-DESIGN.md` | Reference model for YAML schema authority plus Markdown fixture boundaries. |
| `development/craft/CRAFT-LEDGER-SCHEMA.yml` | Reference model for row families, lifecycle states, relations, and validation rules. |
| `development/craft/LEDGER.md` | Current example of a human-readable recursive ledger fixture. |
| `formulae/dispatch-spec/TECHNIQUE-CATALOG.md` | Technique vocabulary for dispatch route shape. |

## Research Mode

`bounded-research`

Rationale: the user explicitly asked to research techniques for this learning/guide behavior. Research is bounded to transferable learning-science and adaptive-tutoring concepts and cannot override local Arcanum ownership boundaries.

## Preset

`full`

## Done Criteria

- The run has a seed, dispatch route, runtime handoff, manifest, evidence index, stage evidence, and final result.
- The dispatch route preserves the canonical ten-stage refine loop.
- The route validates against the local dispatch schema when possible.
- Stage evidence records either pass/flag/block and concrete artifact paths.
- The final synthesis names the selected coherent unit, rejected alternatives, candidate sigils/spells, learning techniques, ledger row families, install-game shape, validation gates, and next routes.
- Canonical mutation remains out of scope.

## Planned Stage Configuration

| Stage | Owner | Mode | Expected Output |
| --- | --- | --- | --- |
| Context Builder evidence baseline | `context-builder` | standard | `stages/01-context-builder.md` |
| Invoke Define | `invoke` | define | `stages/02-invoke-define.md` |
| Interrogation refine-review | `interrogation` | refine-review | `stages/03-interrogation-refine-review.md` |
| Research decision | `refine` | bounded-research | `stages/04-research-decision.md` |
| Distill | `distill` | standard | `stages/05-distill.md` |
| Invoke Redefine / Design | `invoke` | design | `stages/06-invoke-design.md` |
| Interrogation refine-design-review | `interrogation` | refine-design-review | `stages/07-interrogation-design-review.md` |
| Distill Repair | `distill` | validate | `stages/08-distill-repair.md` |
| Invoke Plan | `invoke` | plan | `stages/09-invoke-plan.md` |
| Final Interrogation and Synthesis | `interrogation` + `refine` | refine-final | `stages/10-final-interrogation-and-synthesis.md`, `RESULT.md` |

## Initial Hypothesis

The smallest coherent unit is not the whole Guide system. It is a `User Learning Ledger` plus `Guide Interaction Receipt` contract:

```text
Guide section attempt
  -> adaptation used
  -> user response / blocker resolution / clarification confirmation
  -> mastery or partial-mastery evidence
  -> User ledger update
  -> glossary entry or residue
```

The CyberAlchemy install game should be the first onboarding spell candidate because it creates the initial profile without pretending the system already knows the user.
