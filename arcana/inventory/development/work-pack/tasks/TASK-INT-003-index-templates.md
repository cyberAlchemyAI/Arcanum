---
module: inventory-interface-link-index
version: current
status: blocked
updatedAt: 2026-06-05
docType: task
task: TASK-INT-003
---

# TASK-INT-003: Index Templates

## Goal

Add JSON templates for the new index substrate.

## Depends On

- TASK-INT-001

## Write Scope

- `arcana/inventory/templates/`

## Required Templates

- `selector-index.json`
- `link-index.json`
- `backlink-index.json`
- `traceability-matrix.json`
- `gap-risk-index.json`
- `query-pattern-index.json`
- `projection-index.json`

## Validation

```bash
jq empty arcana/inventory/templates/*index*.json
```

Relation-like links must include non-authority language.
