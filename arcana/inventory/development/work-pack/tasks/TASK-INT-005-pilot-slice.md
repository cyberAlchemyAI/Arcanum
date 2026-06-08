---
module: inventory-interface-link-index
version: current
status: blocked
updatedAt: 2026-06-05
docType: task
task: TASK-INT-005
---

# TASK-INT-005: First Interface-Driven Pilot Slice

## Goal

Use the new interface/index/link contract on one bounded pilot slice.

## Depends On

- TASK-INT-001
- TASK-INT-002
- TASK-INT-003
- TASK-INT-004

## Recommended Pilot

```text
sigils-library-arcanum-authority
```

## Write Scope

```text
arcana/inventory/development/pilot/interface-link-index/
```

## Outputs

- `target-confirmation.md`
- `cards.json`
- `index.json`
- `retrieval.json`
- `COVERAGE.md`
- local index examples needed by validator

## Stop Condition

Do not decide canonical authority. Record evidence, conflict, and next owner.
