# Task CRAFT-ARCH-003: Create Validation And Recomposition Guide

## Objective

Create a manual validation guide that can review the example suite and classify Craft evidence without reopening architecture discovery.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L2 |
| Slice | S-ARCH-003 |
| Wave | W2 |
| Complexity | medium |

## Source Contracts

- `development/craft/CRAFT-VALIDATION-EXAMPLES.yml`
- `development/craft/CRAFT-VALIDATION-EXAMPLES.md`
- `development/craft/CRAFT-ARCHITECTURE.md#Dependency And Interface Rules`
- `development/craft/CRAFT-ARCHITECTURE.md#Gate Result`
- `development/craft/LEDGER-VALIDATION.md`

## Dependencies

- CRAFT-ARCH-002 must pass.

## Implementation Detail

Create `development/craft/CRAFT-VALIDATION.md`.

The guide should include:

- validation purpose,
- example-suite coverage table,
- rule checklist for R-001 through R-007,
- recomposition checklist,
- pass/flag/block/waiver/deferred classification rules,
- evidence requirements for later task-session runs,
- explicit non-goals for runtime and promotion mutation.

## Smallest Working Units

### SWU-CRAFT-ARCH-005

Goal: create the validation and recomposition guide.

Dependencies: SWU-CRAFT-ARCH-004.

Write scope:

- `development/craft/CRAFT-VALIDATION.md`

Done criteria:

- Guide covers every example ID EX-001 through EX-010.
- Guide covers architecture rules R-001 through R-007.
- Guide defines recomposition evidence required before a unit can be considered closed.
- Guide keeps scoring, generated indexes, role automation, runtime integration, and promotion out of scope.

Acceptance evidence:

- Manual checklist can classify each example as pass, flag, block, waived, or deferred.

Validation surface:

- `rg -n "EX-001|EX-010|R-001|R-007|recomposition|deferred" development/craft/CRAFT-VALIDATION.md`

Execution owner: subagent.

Handoff note:

Make the guide practical for task-session. It should tell the next worker what to inspect and what evidence is enough.

## Synchronization Rules

Do not rewrite examples unless a validation guide requirement exposes a clear defect. If that happens, record it in the task-session evidence and keep the change scoped.
