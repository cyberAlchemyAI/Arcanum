# Runtime Handoff: User Ledger And Guide

## Status

`block`

## Objective

Prepare a durable handoff for a future runtime or task-session route that can implement the selected User/Guide refinement unit after approval.

## Dispatch Reference

- Dispatch: `development/user-guide/refinement-runs/20260529T131319Z-user-guide-ledger/REFINE-DISPATCH.json`
- Dispatch ID: `refine-user-guide-ledger-20260529T131319Z`
- Target: `development/user-guide/`

## Runtime Status

Canonical command-backed execution is blocked by local command-surface gaps:

- `dispatch-spec` is not registered as a local Arcanum command.
- `runtime-handoff` is not registered as a local Arcanum command.

The stage artifacts in this run are therefore local refine-owned evidence, not proof that every command-backed stage executed through `tools/arcanum --exec`.

## Adapter Fields

| Field | Value |
| --- | --- |
| adapter | not selected |
| run_folder | `development/user-guide/refinement-runs/20260529T131319Z-user-guide-ledger/` |
| execution_environment | local refine evidence only |
| runtime_owner | future task-session / sigil-development |
| blocked_reason | missing command routes for `dispatch-spec` and `runtime-handoff` |

## Handoff For Next Route

The next route should start from `RESULT.md`, not from the raw user request. The approved next route should decide whether to:

1. run `sigil-development` for a `user-ledger` sigil candidate,
2. run `spellcraft` for a `guide` spell candidate,
3. run `task-session` for a small install-game prototype,
4. or run `invoke` to create Define/Design/Plan artifacts for the whole User/Guide family.

## Protected Context Note

No real user profile record is written by this run. Future runtime work must treat profile, learning, vocabulary, analogy, and mastery evidence as protected local context with explicit visibility and promotion boundaries.
