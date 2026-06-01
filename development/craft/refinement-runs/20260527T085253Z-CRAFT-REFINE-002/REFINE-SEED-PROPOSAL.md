# Refine Seed Proposal: CRAFT-REFINE-002

## Target

[../../WORK-PACK.md](../../WORK-PACK.md), task `CRAFT-REFINE-002`.

## Objective

Create [../../CRAFT-RECURSIVE-LEDGER-DESIGN.md](../../CRAFT-RECURSIVE-LEDGER-DESIGN.md), a minimal schema for the recursive ledger shaped by [../../CRAFT-LEDGER-TYPE-EXAMPLES.md](../../CRAFT-LEDGER-TYPE-EXAMPLES.md).

## Scope

In scope:

- context rows,
- artifact rows,
- relation rows,
- typed blocker/gate/enabler rows,
- operational lane fields,
- role-hint fields,
- status and gate values,
- blocker refinement lifecycle,
- validation rules,
- conflict policy,
- future scoring placeholders without scoring weights.

Out of scope:

- runtime command implementation,
- JSON parser or generator,
- priority scoring weights,
- canonical Craft promotion.

## Research Decision

`no-research`

Reason: the task designs from local examples and local Craft contracts.

## Validation Surface

Manual trace from each row family in [../../CRAFT-LEDGER-TYPE-EXAMPLES.md](../../CRAFT-LEDGER-TYPE-EXAMPLES.md) to fields in [../../CRAFT-RECURSIVE-LEDGER-DESIGN.md](../../CRAFT-RECURSIVE-LEDGER-DESIGN.md).
