# Craft Architecture Execution Pack

## Purpose

Coordinate execution order for `CRAFT-ARCHITECTURE-WORK-PACK.md`.

This execution pack schedules waves and SWUs. It does not redefine task contracts and does not execute work.

## Control Fields

| Field | Value |
| --- | --- |
| Source work-pack | `CRAFT-ARCHITECTURE-WORK-PACK.md` |
| Complexity | medium |
| Output mode | split |
| Execution policy | one SWU at a time unless coordinator approves disjoint write scopes |
| Runtime mutation | prohibited |
| Promotion mutation | prohibited |

## Wave Plan

| Wave | Layer | Goal | Tasks | Entry Gate | Exit Evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-packs/craft-architecture/waves/W0.md) | L0 | Verify architecture plan baseline. | CRAFT-ARCH-001 | Work-pack and task contracts exist. | Baseline review passes or records blocker. |
| [W1](work-packs/craft-architecture/waves/W1.md) | L1 | Create validation example suite. | CRAFT-ARCH-002 | W0 passed. | `CRAFT-VALIDATION-EXAMPLES.yml` and `.md` cover EX-001 through EX-010. |
| [W2](work-packs/craft-architecture/waves/W2.md) | L2 | Create validation and recomposition guide. | CRAFT-ARCH-003 | W1 passed. | `CRAFT-VALIDATION.md` can review all examples and architecture rules. |
| [W3](work-packs/craft-architecture/waves/W3.md) | L3 | Review promotion readiness and sync package state. | CRAFT-ARCH-004, CRAFT-ARCH-005 | W2 passed. | Readiness report and package entrypoints agree on next route. |

## Parallelization Boundary

No parallel execution is recommended for the first pass. The example suite feeds validation, validation feeds readiness, and readiness feeds package sync.

If a later coordinator allows parallel execution:

- CRAFT-ARCH-004 and CRAFT-ARCH-005 must not run in parallel because package sync depends on readiness output.
- SWU-CRAFT-ARCH-002, 003, and 004 share the same example-suite files and should remain sequential.
- Read-only baseline review can run independently only before mutation-capable work begins.

## Recommended Route

```text
$task-session development/craft/CRAFT-ARCHITECTURE-WORK-PACK.md --task CRAFT-ARCH-001
```
