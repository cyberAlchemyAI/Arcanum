# Task CRAFT-ARCH-001: Verify Planning Baseline

## Objective

Confirm that the Craft architecture plan can be executed without reopening design, losing source contracts, or violating runtime/promotion boundaries.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L0 |
| Slice | S-ARCH-001 |
| Wave | W0 |
| Complexity | low |

## Source Contracts

- `development/craft/CRAFT-ARCHITECTURE.md`
- `development/craft/CRAFT-ARCHITECTURE-GLOSSARY-CONSISTENCY.md`
- `development/craft/CRAFT-ARCHITECTURE-DESIGN-TRANSPORT.md`
- `development/craft/CRAFT-ARCHITECTURE-IMPLEMENTATION-LAYERING.md`
- `development/craft/CRAFT-ARCHITECTURE-WORK-PACK.md`
- `development/craft/CRAFT-ARCHITECTURE-EXECUTION-PACK.md`

## Dependencies

None.

## Smallest Working Units

### SWU-CRAFT-ARCH-001

Goal: verify the plan baseline before mutation-capable tasks start.

Dependencies: none.

Write scope:

- Review only.
- Optional task-session evidence folder under `development/craft/task-sessions/`.

Done criteria:

- Required plan artifacts exist.
- Work-pack gate is `pass`.
- Every SWU in the work-pack has dependencies, source anchors, write scope, done criteria, acceptance evidence, validation surface, owner recommendation, and handoff status.
- Runtime, registry, promotion, scoring, index, and role automation boundaries are still explicit.

Acceptance evidence:

- Task-session note or evidence file records baseline pass, flag, or block.

Validation surface:

- Manual review of work-pack and execution-pack contracts.

Execution owner: manual.

Handoff note:

Use this task to catch plan-contract errors before creating validation examples.

## Synchronization Rules

Do not edit architecture source unless a blocker-level defect is found. If a defect is found, record a blocker or patch request instead of silently changing the approved design.
