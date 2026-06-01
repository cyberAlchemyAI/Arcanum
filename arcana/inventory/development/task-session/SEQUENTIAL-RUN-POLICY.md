# Task Session Sequential Run Policy

## Status

- Status: active
- Updated: 2026-05-29
- Scope: `arcana/inventory/development/WORK-PACK.md`
- Applies to: future Inventory work-pack execution after the completed evidence-card and EvidenceSet candidate tasks.

## Purpose

Run Inventory work-pack tasks one unit at a time until the first blocker or gap appears, then route immediately to `decision-gate` with the accumulated task-session context.

## Execution Rule

Future Inventory task-session execution is sequential-only:

1. Resolve the next ready task or SWU from `WORK-PACK.md`.
2. Build or refresh a bounded task-session context pack for that exact unit.
3. Execute only that unit.
4. Validate the unit against its declared done criteria.
5. Synchronize completion evidence before selecting another unit.
6. Repeat only if the previous unit returned `PASS`.

Do not batch future Inventory SWUs, even when dependencies are satisfied and write scopes appear disjoint. The task-session sigil owns exactly one task/SWU at a time, and this policy keeps the next decision point auditable.

## Stop Conditions

Stop the sequential run before mutation when any of these appears:

- missing task source, write scope, dependency evidence, or validation surface;
- stale or contradictory work-pack status;
- a task decision with more than one viable consequential option;
- a validation failure that cannot be repaired inside the selected unit without changing scope;
- a new blocker, gap, or deferred choice becomes necessary for the next unit.

## Decision Gate Trigger

When a stop condition is a blocker-level choice, run `decision-gate` before further task-session work.

The decision-gate target scope should use the blocked task or SWU ID, for example:

```text
decision-gate inventory-<TASK-or-SWU-ID>
```

The decision-gate context must include:

- the blocked task-session context pack;
- the task-session result or blocked report;
- the relevant `WORK-PACK.md` row;
- source contracts named by the task;
- validation output, if any;
- the exact downstream mutation that is blocked;
- concrete options with trade-offs.

If decision-gate returns `PASS`, resume task-session at the same blocked unit or the next ready unit named by the decision record. If decision-gate returns `BLOCK`, do not mutate and leave the work-pack status unchanged except for recording the blocker.

## Current Inventory State

All known Inventory evidence-card and candidate EvidenceSet tasks through `TASK-008` are complete. The current deferred item, canonical `EvidenceSet` promotion, is not a blocker for completed candidate-schema work. It becomes a decision-gate target only when a future task proposes production promotion, canonical terminology, or downstream behavior that depends on promotion.
