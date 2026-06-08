---
module: inventory-interface-link-index
version: current
status: ready
updatedAt: 2026-06-05
docType: task
task: TASK-INT-001
---

# TASK-INT-001: Inventory Auto Interface Contract

## Goal

Update Inventory's production contract so `$inventory` without an explicit mode
starts target inference and confirmation instead of exposing only technical
modes.

## Source Anchors

- `../../INTERFACE-ARCHITECTURE.md`
- `../../LINKING-DISCIPLINE.md`
- `../../../SKILL.md`
- `../../../README.md`

## Write Scope

- `arcana/inventory/SKILL.md`
- `arcana/inventory/README.md`

## Required Changes

- Add `auto` as default/no-mode interface behavior.
- Add target inference process.
- Add confirmation proposal process.
- Add interface modes: `inventorize`, `status`, `continue`, `explain`.
- State JSON + Markdown storage rule.
- Preserve technical modes as internal routes.

## Validation

```bash
rg -n "auto|target inference|confirmation|inventorize|status|continue|explain|JSON|Markdown" arcana/inventory/SKILL.md arcana/inventory/README.md
```

## Done

- User can call `$inventory` conceptually without knowing `install`, `ingest`,
  or `backfill`.
- Mutation remains gated by confirmation.
