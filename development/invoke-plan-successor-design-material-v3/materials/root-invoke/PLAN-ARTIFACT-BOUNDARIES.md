# Invoke Plan Artifact Boundaries

Status: runtime contract for invoke plan outputs.

## Purpose

Invoke plan should produce planning artifacts that are distinct, navigable, and execution-ready without duplicating the same responsibility across `WORK-PACK.md`, `work-pack/waves/*`, and `work-pack/tasks/*`.

The main failure to avoid is a plan where multiple artifacts claim to own the same tasks and SWUs. The canonical executable hierarchy should be:

```text
IMPLEMENTATION-LAYERING.md
  governance lens over the work

WORK-PACK.md
  canonical executable plan and current state
    -> work-pack/waves/W*.md
      -> work-pack/tasks/TASK-*.md
        -> SWUs
```

## Artifact Boundary Summary

| Artifact | Owns | Does Not Own |
| --- | --- | --- |
| `IMPLEMENTATION-LAYERING.md` | Layer decision questions, L0-L3 boundaries, promotion evidence, deferrals, nested layer policy. It is the governance lens over waves. | Task execution details, task status tracking, or SWU implementation contracts. |
| `WORK-PACK.md` | Canonical executable plan: objective, delivery slices, task/SWU manifest, validation strategy, blocker board, gate status, output mode, active layer window, required links, and current state. | Deep task-local detail when split task files exist; layer philosophy that belongs in implementation-layering. |
| `work-pack/shared/*` | Shared execution context: source contracts, traceability, cross-task decisions/gaps, global assumptions. | Task-specific instructions that belong in task files. |
| `work-pack/tasks/TASK-*.md` | One task's executable contract: objective, parent slice/layer, SWUs, dependencies, write scope, done criteria, validation, subagent handoff, synchronization notes. | Global plan rationale or unrelated task status. |
| `work-pack/waves/W*.md` | Execution ordering: wave goal, layer mapping, entry gate, included tasks/SWUs, dependency order, parallelization boundaries, exit evidence. | Detailed implementation specs that belong to tasks/SWUs. |
| `EXECUTION-PACK.md` | Cross-task execution choreography for medium/high complexity: waves, stage coverage, closure obligations, parallelization boundaries. | Source-of-truth task specs or SWU definitions. |

## Boundary Rules

1. `WORK-PACK.md` is the source of truth for executable planning and current execution readiness.
2. `IMPLEMENTATION-LAYERING.md` is the source of truth for layer governance and promotion evidence.
3. Waves must respect implementation layering: each wave names its layer, layer question, promotion evidence, and exit gate.
4. Tasks must belong to one or more waves.
5. SWUs must belong to exactly one task.
6. Split task files are required to be useful execution contracts, not placeholders.
7. If `WORK-PACK.md`, wave files, and task files disagree, `workPackGateStatus` must be `block` until reconciled.
8. Execution status belongs in work-pack and task/wave files.
9. Work-pack tables must be navigable: task-board task IDs should link to task contracts when task files exist, and SWU manifest rows should link to the parent task contract and source contract or local context needed to execute the SWU.

## SWU Responsibility

Invoke plan owns SWU execution contracts.

For every non-exempt SWU, invoke plan must provide:

- SWU ID,
- parent task with task-contract link when a task file exists,
- objective,
- dependencies,
- explicit write scope,
- source contract or context link,
- done criteria,
- acceptance evidence,
- validation command or reviewable check,
- expected execution owner: `subagent`, `local-fallback`, or `manual`,
- handoff note containing the exact context a worker or subagent needs.

This allows later `goal`, `task-session`, or runtime subagents to execute one SWU without reopening design discovery.

## Subagent Handoff Contract

When a runtime supports subagents, each SWU is the preferred subagent boundary.

Each subagent should receive exactly:

- one SWU ID,
- parent task ID,
- objective,
- write scope,
- dependencies,
- done criteria,
- validation command or reviewable check,
- source contract links,
- known blockers/gaps that affect that SWU,
- expected return shape.

Expected return shape:

```yaml
swu_id: <id>
result: pass | flag | block | interrupted
files_touched:
  - <path>
validation:
  - <command or review check and result>
blockers:
  - <blocker or none>
handoff_note: <what the parent coordinator needs next>
```

If subagents are unavailable, the same SWU contract is used by `task-session` or a labeled local fallback.

## Split Work-Pack Minimum Useful Content

Each `work-pack/tasks/TASK-*.md` file must include:

- task objective,
- layer and slice mapping,
- source contracts,
- dependencies,
- blocker/gap state,
- SWU list,
- for each SWU: write scope, done criteria, validation, and subagent handoff,
- synchronization rules,
- completion evidence.

An empty task file that only repeats a task title is not execution-ready.

## Navigability Pattern

`WORK-PACK.md` should behave like a coordinator control panel. An agent should be able to scan status, open the task contract, then follow the source context without searching the repository.

Use this pattern when paths exist:

- task board task IDs link to `work-pack/tasks/TASK-*.md`,
- wave names link to `work-pack/waves/W*.md` when the table names waves,
- SWU manifest parent tasks link to `work-pack/tasks/TASK-*.md`,
- SWU manifest source contracts link to existing design, run-contract, architecture, or shared context files,
- write-scope paths stay plain text when they are future outputs or numerous paths, and may be linked only when doing so does not make the table unreadable.

## Execution Readiness Gate

Mutation-capable execution is blocked when:

- an SWU lacks dependencies, write scope, done criteria, or validation,
- an SWU lacks source context or task-contract navigation needed for execution,
- a task with multiple SWUs is handed off without selecting one SWU,
- task files are placeholders,
- work-pack gate status is not pass,
- wave order conflicts with dependencies,
- parallel SWUs have overlapping write scopes without an explicit merge plan.
