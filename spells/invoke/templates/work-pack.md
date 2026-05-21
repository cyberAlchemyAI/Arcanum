---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: work-pack
---

# WORK-PACK: {module-name}

## Purpose

Canonical executable plan and execution manifest for invoke planning outputs.

This artifact is the planning entrypoint and source of truth for executable planning. It contains the objective, delivery slices, tasks, SWUs, validation strategy, blockers, gates, current state, and links to waves/task files when split.
It can stay single-file for low complexity or link split waves, task files, and execution-pack artifacts for medium/high complexity.
This template is standalone at invoke scope and is composed by Module Formulae implementation and full profiles.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass or block | Must be pass before mutation-capable execution. |
| complexity | low, medium, or high | Current complexity level. |
| outputMode | single-file or split | Split is required when scope exceeds low complexity. |
| executionPackRef | {path or n/a} | Required for medium/high complexity execution. |
| layeringArtifactRef | {path or n/a} | Should reference implementation-layering.md. |
| activeLayerWindow | L0, L1, L2, L3, or n/a | Primary layer focus for current execution slice. |
| lastUpdatedAt | {iso-timestamp} | Last update time for this work-pack. |
| readinessProfile | pilot, release-candidate, production | Completion target profile. |

## Objective Summary

- Objective: {what this work-pack must deliver}
- Primary inputs: approved design outputs, layering decisions, architecture references
- Success condition: {evidence-based completion condition}

## Planning Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Delivery Boundary | Objective Summary and Slices | Preserve included/excluded scope. |
| Delivery Slices | Task Status Board and Waves | Each slice produces one or more tasks with explicit dependencies. |
| Layer Boundary Decisions | activeLayerWindow and task layer fields | Every task and wave maps to at least one layer decision. |
| Task Decomposition | Task Status Board and task files | Preserve task IDs, dependencies, and owners. |
| Blockers And Risks | Blockers section | Carry blocker IDs and resolution paths forward unchanged. |
| Validation Strategy | Gate checks and evidence references | Reuse validation targets and expected evidence commands. |
| SWU Manifest | Task files and traceability | Every non-exempt SWU keeps dependencies, write scope, done criteria, validation, and execution-owner recommendation. |
| Source Contracts | Task board, SWU manifest, and task files | Link existing source context so workers can navigate without repository search. |

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | {outcome} | L0, L1, L2, or L3 | W0, W1, W2 | {dependencies} | {validation check} |

## Navigability Rule

The work-pack is the coordinator control panel. Link IDs to their contracts when files exist:

- task IDs link to `work-pack/tasks/TASK-*.md`,
- wave IDs link to `work-pack/waves/W*.md` when practical,
- SWU parent tasks link to their task contract,
- source contracts link to existing design, architecture, run-contract, or shared context files.

Keep future write-scope paths as plain text unless the files already exist and linking them improves readability.

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-A](work-pack/tasks/TASK-A.md) | {goal summary} | L0, L1, L2, or L3 | low, medium, high | [W1](work-pack/waves/W1.md), [W2](work-pack/waves/W2.md) | {source contract links} | ready or blocked | not-started, in-progress, completed |
| TASK-VERIFY | Completion verification | L2 or L3 | medium or high | W3+ | {source contract links} | ready-after-implementation | not-started, in-progress, completed |

## Split Task File Contract

When `outputMode = split`, each `work-pack/tasks/TASK-*.md` file must include:

- task objective,
- layer and slice mapping,
- source contracts with links to existing files,
- dependencies,
- blocker/gap state,
- Smallest Working Units,
- for each SWU: dependencies, write scope, done criteria, validation, execution owner, and handoff note,
- synchronization rules,
- completion evidence.

Placeholder task files are not execution-ready. If task files exist but do not include the task-local SWU execution contract, set `workPackGateStatus = block`.

## SWU Execution Handoff

| SWU ID | Parent Task | Source | Dependencies | Write Scope | Done Criteria | Validation | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-{FEATURE-CODE}-001 | [TASK-A](work-pack/tasks/TASK-A.md) | {source contract links} | {dependencies or none} | {paths/modules} | {done criteria} | {command or review check} | subagent, local-fallback, or manual | ready, blocked, or selected |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-001 | task or cross-task | {blocked item} | {owner} | {unblock action} | {date} |

## Required Links

Single-file mode:

- Keep this file as the only planning artifact when scope remains low complexity and reviewable.

Split mode:

- module-formulae/execution-pack.md
- work-pack/shared/context.md
- work-pack/shared/cross-task-gaps.md
- work-pack/shared/cross-task-decisions.md
- work-pack/shared/traceability.md
- work-pack/tasks/TASK-A.md
- work-pack/waves/W0.md
- work-pack/waves/W1.md

## Gate Checks

1. `workPackGateStatus` must be pass before mutation-capable execution.
2. Medium/high complexity requires `executionPackRef` and baseline wave W0.
3. Layer mappings must be consistent with `layeringArtifactRef` deferred scope and promotion decisions.
4. Any unresolved blocker that affects acceptance criteria keeps gate status at block.
5. Any non-exempt SWU missing dependencies, source context, write scope, done criteria, validation, or execution-owner recommendation keeps gate status at block.
6. Any task with multiple SWUs must select one SWU before mutation-capable execution.
7. Parallel SWUs must have disjoint write scopes or an explicit merge plan.

## Handoff To Execution Pack

Use [module-formulae/execution-pack.md](module-formulae/execution-pack.md) for wave-by-wave execution details.

- Low complexity: execution details may remain in this file with `executionPackRef = n/a`.
- Medium/high complexity: generate or update execution-pack and set `executionPackRef`.
- Keep task IDs and layer assignments consistent between work-pack and execution-pack.
- Execution-pack schedules waves and SWUs; it does not redefine task or SWU contracts.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| {date} | Initial work-pack created | {name} |
