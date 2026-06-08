# Execution Pack: {module-name}

## Purpose

Execution-first planning manifest for medium and high complexity work.

This file can stay single-document for small scope or split into waves and task files for larger scope.

## Planning Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| planningGateStatus | pass or block | Must be pass before mutation-capable stages. |
| complexity | low, medium, or high | Current complexity level. |
| baselineWave | W0 | Mandatory first wave for medium or high complexity. |
| activePlanRef | {path} | Current wave or plan reference. |
| workPackManifest | {path} | Usually ../work-pack.md as the standalone invoke companion template. |
| layeringArtifact | {path} | Usually ../implementation-layering.md as the standalone invoke companion template. |
| activeLayerWindow | L0, L1, L2, or L3 | Primary layer focus for current execution slice. |
| lastPlannedAt | {iso-timestamp} | Last planning update time. |
| readinessProfile | pilot, release-candidate, production | Completion target profile. |

## Task Board

| Task ID | Goal | Layer | Complexity | Waves | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-A | {goal summary} | L0, L1, L2, or L3 | medium | W1, W2 | ready | not-started |
| TASK-VERIFY | Completion verification | L2 or L3 | high | W3+ | ready-after-implementation | not-started |
| TASK-AUDIT-ALIGNMENT | Contract alignment audit | L2 or L3 | high | W3+ | ready-after-mutation | not-started |
| TASK-AUDIT-LAYERING | Boundary layering audit | L2 or L3 | high | W3+ | ready-after-mutation | not-started |
| TASK-SIGNAL-ALIGNMENT | Alignment signal obligation | L2 or L3 | medium | W3+ | ready-after-docs | not-started |
| TASK-SIGNAL-LAYERING | Layering signal obligation | L2 or L3 | medium | W3+ | ready-after-docs | not-started |

## Closure Obligations

Apply these obligations when this execution pack is created:

1. Always include one completion verification task.
2. If any mutation-capable stage is planned, include alignment and layering audits.
3. If all mutation-capable stages are skipped, include alignment and layering signal obligations instead of audits.
4. If any closure task returns flag or block, add remediation tasks without deleting original obligations.

## Layering Alignment

- `layeringArtifact` must reference a valid layering file before medium/high mutation-capable work starts.
- Every wave objective must map to one or more layer IDs from the layering artifact.
- If a wave includes tasks across multiple layers, record why the boundary merge is acceptable.
- Block promotion when a planned task has no layer mapping or contradicts deferred scope from the active layer.

## Work-Pack Integration

- `workPackManifest` must reference a valid work-pack artifact before execution starts.
- Task IDs in this execution pack must match task IDs declared in the work-pack manifest.
- Wave assignments in execution-pack must satisfy work-pack output mode and gate expectations.
- Wave entries should reference SWU IDs when SWUs exist; the execution-pack schedules SWUs but does not redefine them.
- Parallel SWU execution is allowed only when dependencies are satisfied and write scopes are disjoint or an explicit merge plan exists.
- If work-pack and execution-pack diverge on task IDs, layer assignments, or blockers, set planning gate to block until reconciled.

## Design-Guided Task Directives

For each mutation-capable task, map source contracts to implementation directives.

| Task ID | Source Contracts | Coverage IDs | Architecture References | Implementation Directive | Verification Evidence |
| --- | --- | --- | --- | --- | --- |
| TASK-A | operations.md; concept-model.md; interfaces.md | R1, C1, WF-01, concept-id | {architecture references} | Keep rules and calculations pure, isolate adapters, and preserve boundary direction. | {test ids and command outputs} |

Directive requirements:

- Coverage IDs must reference exact identifiers from source contracts.
- Architecture references must include boundary and dependency rules.
- If interface-experience stage is planned, include at least one interface contract reference.
- If alignment or layering findings exist, directives must include closure steps for both.

## Required Links

Single-document mode:

- Keep this file only when scope stays reviewable.

Split mode:

- shared/context.md
- shared/cross-task-gaps.md
- shared/cross-task-decisions.md
- shared/traceability.md
- tasks/TASK-A.md
- waves/W0.md
- waves/W1.md

## Wave Status Board

| Wave | Objective | Entry Gate | Exit Gate | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| W0 | Baseline architecture and stage coverage lock | Execution pack exists | Baseline and stage matrix locked | not-started | {links} |
| W1 | First implementation wave | W0 pass | Wave objective complete | not-started | {links} |

## Delivery Stage Coverage

Keep all canonical stages listed, even when skipped.

| Stage | Required | Wave Mapping | Status | Evidence | Skip Reason |
| --- | --- | --- | --- | --- | --- |
| discover | yes | W0 | not-started | {links} | {optional} |
| design-baseline | yes | W0 | not-started | {links} | {optional} |
| specification | yes | W1+ | not-started | {links} | {optional} |
| scenarios | yes | W1+ | not-started | {links} | {optional} |
| tests | yes | W1+ | not-started | {links} | {optional} |
| implementation | yes | W1+ | not-started | {links} | {optional} |
| interface-experience | yes | W1+ | skipped | {links} | {optional} |
| telemetry-spec | yes | W2+ | not-started | {links} | {optional} |
| telemetry-instrument | yes | W2+ | not-started | {links} | {optional} |
| telemetry-verify | yes | W2+ | not-started | {links} | {optional} |
| deployment | yes | W2+ | skipped | {links} | {optional} |
| concept-index-sync | yes | W2+ | not-started | {links} | {optional} |
| readiness-review | yes | W3+ | not-started | {links} | {optional} |
| completion-verify | yes | W3+ | not-started | {links} | {optional} |
| audit-alignment | yes | W3+ | not-started | {links} | {optional} |
| audit-layering | yes | W3+ | not-started | {links} | {optional} |

When interface-experience is not skipped, evidence must include the interface contract and supporting experience references.

When all mutation-capable stages are skipped, mark audit stages as skipped with explicit reasons and enforce signal obligations.

## Decision Lock Summary

| Decision ID | Scope | Status | Selected Option | Source | Date |
| --- | --- | --- | --- | --- | --- |
| D-001 | task or cross-task | selected | {option} | {source} | {date} |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-001 | task or cross-task | {blocked item} | {owner} | {unblock action} | {date} |

## Notes

- Task files should include gaps, questions, and decision lock sections.
- Medium and high complexity plans should include source coverage and architecture directives.
- W0 is mandatory before mutation-capable stages for medium and high complexity.
- If planningGateStatus is block, do not execute mutation-capable stages.
- Keep layer mappings synchronized with implementation-layering decisions whenever scope changes.
- Keep execution-pack synchronized with work-pack manifest updates whenever task or wave scope changes.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| {date} | Initial execution pack created | {name} |
