---
module: inventory-interface-link-index
version: current
status: blocked
updatedAt: 2026-06-05
docType: task
task: TASK-INT-002
---

# TASK-INT-002: Interface Templates

## Goal

Add reusable templates for target inference, confirmation proposals, status
views, and lookup views.

## Depends On

- TASK-INT-001

## Write Scope

- `arcana/inventory/templates/`

## Candidate Templates

- `target-inference.json`
- `target-confirmation.md`
- `inventory-status.md`
- `lookup-result.md`

## Validation

- JSON templates parse when filled with examples.
- Markdown templates include source anchors, write scope, exclusions, and
  non-goals.
