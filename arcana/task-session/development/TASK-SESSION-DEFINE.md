# Task Session Define Baseline

## Invocation

- Spell: `invoke`
- Mode: `define`
- Target artifact: `task-session`
- Target type: Arcana sigil
- Owner/cycle: `arcana/task-session`
- Source artifacts:
  - `arcana/task-session/README.md`
  - `arcana/task-session/SKILL.md`
  - `arcana/task-session/runtime-adapters/README.md`
  - `arcana/task-session/runtime-adapters/codex-goal.md`
  - `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-OPTIMIZATION.md`
  - `arcana/task-session/development/CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md`
  - `arcana/task-session/development/TASK-SESSION-ARCHITECTURE-DESIGN.md`

## Purpose

Task Session executes one bounded task or SWU end to end with explicit context, trade-offs, gates, validation, evidence synchronization, and optional runtime delegation.

It exists to prevent task execution from drifting into unbounded exploration, silent decision-making, unsupported completion claims, or runtime handoffs that bypass Arcanum governance.

## Problem Statement

Single-task execution often fails in subtle ways:

- the task is selected from a narrow file while controlling architecture or work-pack context is missed,
- agents start mutating before dependencies, blockers, or write scope are clear,
- implementation choices are made silently,
- runtime goals are launched without a compact source context,
- completion is marked without validation or synchronized evidence.

Task Session turns that risky moment into a governed execution loop.

## Scope

Task Session covers:

- resolving exactly one task or SWU,
- building a bounded context pack before decisions, gates, runtime selection, or mutation,
- surfacing meaningful implementation trade-offs,
- blocking on unresolved dependencies, contradictions, weak context, broad write scope, or missing validation,
- executing locally or through a runtime adapter,
- validating against done criteria and context-pack obligations,
- synchronizing task/work-pack evidence after completion,
- reporting a compact auditable result.

Task Session does not cover:

- broad project planning,
- defining new product scope from scratch,
- executing many unrelated tasks in one session,
- promoting reusable spells or sigils,
- replacing native runtime lifecycle ownership,
- treating generated context packs as canonical project documentation.

## Actors

| Actor | Role |
| --- | --- |
| User | Selects or approves the task, resolves blocker decisions, and reviews outcome. |
| Task Session | Orchestrates one bounded execution lifecycle. |
| Context Builder | Produces compact obligation-linked context before execution. |
| Runtime Adapter | Converts safe task-session state into runtime-specific handoff. |
| Codex Goal | Optional runtime that owns continuation after safe goal creation. |
| Work-Pack | Planning source of truth for task/SWU status, dependencies, and evidence. |
| Lifecycle Owner | Reviews reusable spell/sigil validation and promotion readiness after execution. |

## Core Concepts

| Concept | Definition |
| --- | --- |
| Task Session | A governed execution loop for one selected task or SWU. |
| Selected Unit | The single task or SWU that the session is allowed to execute. |
| Context Pack | A compact, selector-level evidence bundle mapped to task obligations. |
| Handoff Pack | A context pack prepared for runtime delegation, emitted as Markdown plus JSON/index, persisted as session evidence, and accepted only when strict obligation coverage passes. |
| Decision Pack | Option cards for unresolved implementation choices. |
| Gate Verdict | The decision to proceed, block, or flag based on dependencies, context, scope, and validation readiness. |
| Runtime Adapter | A boundary that translates gated task-session state into a runtime-specific command or profile. |
| Evidence Sync | Updating task/work-pack records only after validation or accepted substitute evidence exists. |

## Required Behavior

### Scope Resolution

Task Session must resolve exactly one execution unit. If the request points to a work-pack, it must select one explicit task/SWU or the next ready unit when unambiguous.

It must block when:

- no work-pack or task source can be resolved,
- more than one execution unit is implied,
- selected dependencies or blockers cannot be interpreted.

### Context First

Task Session must build a bounded context pack before:

- decision cards,
- gate checks,
- runtime selection,
- runtime-goal handoff,
- file mutation.

The context pack must include source links, task contract, architecture/spec references, dependency rows, blocker rows, write scope, done criteria, validation surface, and known repository conventions when available.

If context is missing, contradictory, stale, or too weak to check the task safely, Task Session must return `BLOCK`.

### Decision And Gate Discipline

Task Session must expose meaningful implementation trade-offs before mutation. It may auto-select only non-blocking or clearly safe choices when `--auto` is set.

Gate checks must cover:

- selected scope,
- dependency readiness,
- blocker state,
- context-pack obligation coverage,
- authority contradictions,
- write-scope boundaries,
- runtime readiness,
- validation availability.

No consequential mutation proceeds when gate status is `BLOCK`.

### Runtime Delegation

Task Session may execute locally or delegate through a runtime adapter.

Runtime delegation must not change ownership:

- runtime owns continuation and implementation work within the handed-off goal,
- Task Session owns task selection, gates, context-pack sufficiency, final evidence review, and synchronization.

For Codex Goal delegation, the handoff is pack-first: the goal receives a session-evidence handoff pack Markdown path and JSON/index path. Broad repository exploration is allowed only for named uncovered obligations or gaps from the pack.

Strict handoff coverage is required: every parsed obligation must be covered by selected evidence or explicitly resolved as not applicable/deferred before delegation. Missing, contradictory, stale, unsafe, missing write-scope, or missing validation obligations return `BLOCK`.

### Validation And Synchronization

Task Session must validate every available done criterion and context-pack obligation. If validation cannot run, it must record why and provide the closest useful substitute.

Task or SWU status may be updated only when evidence supports completion. Runtime completion must be reviewed against the original task contract and context pack before work-pack synchronization.

## Inputs

Expected inputs:

- task reference, task file, or work-pack path,
- optional `--task` or `--swu`,
- task objective and deliverables,
- dependencies and blockers,
- source links,
- architecture/spec references,
- write scope,
- done criteria,
- validation command or reviewable evidence,
- optional runtime id,
- optional `--via goal`.

## Outputs

Task Session returns:

- selected task/SWU,
- context pack summary or blocked reason,
- decisions made,
- gate verdict,
- runtime and adapter if used,
- files updated,
- validation results,
- experiment harness status when applicable,
- synchronized records,
- follow-up items.

For runtime-backed execution, it must also report:

- generated runtime command/profile or blocked fallback,
- handoff pack Markdown and JSON/index artifacts,
- strict coverage status,
- runtime-owned lifecycle boundary,
- extra sources used by the runtime when fallback exploration occurred.

## Invariants

- Exactly one selected unit per task session.
- Context pack before mutation or runtime handoff.
- No mutation on `BLOCK`.
- Runtime adapters cannot override Task Session gates.
- Completion status requires evidence.
- Generated context and handoff packs are session evidence, not canonical planning truth.
- Reusable spell/sigil promotion remains outside Task Session authority.

## Open Definition Gaps

- Implementation still needs to apply the handoff-pack schema across Context Builder, Task Session, Codex Goal Profile, and the Codex Goal adapter.
- Task Session observability still needs structured fields for handoff pack Markdown path, JSON/index path, strict coverage, and fallback-search status.

## Handoff

This define baseline supports the existing design artifacts:

- `TASK-SESSION-ARCHITECTURE-DESIGN.md`
- `CONTEXT-PACK-GOAL-HANDOFF-DESIGN.md`

Recommended next route: `invoke plan` to normalize the existing context-pack work-pack against this define baseline and the architecture design.
