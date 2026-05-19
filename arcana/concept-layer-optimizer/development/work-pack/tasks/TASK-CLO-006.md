# TASK-CLO-006: Add Runtime Command Adapter

## Goal

Add a local command/runtime adapter only after manual validation proves behavior.

## Layer

L2 Runtime And Observability

## Blocker

- B-CLO-001: decide true subagents versus role simulation fallback.

## Implementation Notes

Adapter must:

- read the canonical SKILL,
- preserve output contract,
- support role simulation fallback,
- keep finite rounds,
- record observability closeout when available.

## Smallest Working Units

- SWU-CLO-010: Add runtime adapter.
- SWU-CLO-011: Validate runtime representative run.

## Done When

- Command resolves through `tools/arcanum`.
- Representative run preserves closeout and result contract.
