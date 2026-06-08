---
module: inventory-interface-link-index
version: current
status: ready
updatedAt: 2026-06-05
docType: wave
wave: W-INT-0
---

# Wave W-INT-0: Interface Contract

## Objective

Make `$inventory` default to a clear interface flow: infer target, ask
confirmation, and only then mutate a bounded Inventory slice.

## Entry Gate

- `INTERFACE-ARCHITECTURE.md` exists.
- `WORK-PACK.md` marks `TASK-INT-001` ready.

## Exit Gate

- `arcana/inventory/SKILL.md` documents auto mode, target inference,
  confirmation proposal, status, continue, and explain behavior.
- `arcana/inventory/README.md` explains the interface to humans.

## Tasks

- `TASK-INT-001-interface-contract.md`
