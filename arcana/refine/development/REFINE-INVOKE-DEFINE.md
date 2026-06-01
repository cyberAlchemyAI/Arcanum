# Invoke Define: Refine

> Historical note: this define artifact predates dispatch-route hardening. Current Refine execution evidence requires `REFINE-DISPATCH.json`, dispatch-spec validation, and `RUNTIME-HANDOFF.md`.

## Target

- Sigil name: `refine`
- Tier: Arcana
- Domain: refinement-governance
- Lifecycle owner: `sigil-development`

## Purpose

`refine` creates a governed seed before a refinement task is executed.

It accepts a vague target, folder, idea, design concern, or existing work-pack; proposes the smallest executable refinement seed; offers research; selects a budget preset; asks for confirmation; then routes the approved unit to Task Session using Codex Goal runtime by default.

## Problem It Solves

Users may ask for "full refinement" without an approved work-pack or selected SWU. Task Session already knows how to execute a bounded task, but it should not silently invent one. `refine` fills that pre-execution gap by turning the user's target into a confirmed seed task/work-pack that Task Session can safely consume.

## Non-Goals

- Do not replace Task Session.
- Do not move the refinement loop into Task Session.
- Do not replace Invoke, Interrogation, Distill, or Sigil Development.
- Do not perform implementation work directly.
- Do not run external research without explicit user confirmation.
- Do not fall back from Codex Goal to local Task Session unless the user explicitly asks.

## Relationships

| Capability | Relationship |
| --- | --- |
| Task Session | Execution owner for the approved seed task or SWU. |
| Iterative Refinement profile | Canonical loop owner for phase order, research bounds, pass limits, and synthesis requirements. |
| Codex Goal | Default runtime target after Task Session gates and strict handoff coverage pass. |
| Context Builder | Produces context packs and Codex Goal handoff packs. |
| Invoke | Produces richer define/design/plan artifacts when the seed grows beyond a minimal task. |
| Interrogation | Critiques the seed or design for duplicated authority, missing gates, and unsafe assumptions. |
| Distill | Selects the smallest coherent refinement unit. |
| Sigil Development | Owns reusable sigil lifecycle, examples, observability, validation, and promotion readiness. |

## Initial Definition

`refine` is a seed/preflight controller for refinement runs. Its output is not completed work; its output is an approved, bounded refinement seed and delegation route.

## Definition Verdict

Pass for design. The definition is narrow enough to avoid duplicating Task Session and broad enough to solve the missing seed problem.
