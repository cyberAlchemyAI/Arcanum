---
module: inventory-interface-link-index
version: current
status: blocked
updatedAt: 2026-06-05
docType: task
task: TASK-INT-004
---

# TASK-INT-004: Link And Index Validator

## Goal

Extend Inventory validation to check the new link/index discipline.

## Depends On

- TASK-INT-003

## Write Scope

- `arcana/inventory/scripts/`
- `arcana/inventory/development/VALIDATOR-RUNTIME.md`

## Checks

- source paths exist,
- card refs exist,
- edge vocabulary is controlled,
- backlink index is generated from link index,
- relation-like links include non-authority notice,
- every risk tag has a gap/risk row or closed reason.

## Validation

Run the updated validator against template examples and pilot slice once
available.
