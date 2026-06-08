---
module: inventory-interface-link-index
version: current
status: ready-for-interface-task-session
updatedAt: 2026-06-05
docType: readiness
---

# Readiness: Inventory Interface, Linking, And Indexing

## Status

Design readiness: pass.

Implementation readiness: ready for first bounded task-session.

The active package is not claiming feature completion. It is ready to implement
the interface/link/index MVP.

## Acceptance Checklist

| Gate | Evidence | Status |
| --- | --- | --- |
| Interface architecture exists | `INTERFACE-ARCHITECTURE.md` | pass |
| Index technique research exists | `INDEX-TECHNIQUE-RESEARCH.md` | pass |
| Linking discipline exists | `LINKING-DISCIPLINE.md` | pass |
| Refine synthesis exists | `INTERFACE-REFINE-SYNTHESIS.md` | pass |
| Active architecture refreshed | `ARCHITECTURE.md` | pass |
| Active implementation plan refreshed | `IMPLEMENTATION-PLAN.md` | pass |
| Active work-pack refreshed | `WORK-PACK.md` | pass |
| Scope-specific research archived | `archive/domainspec-core-research-20260605/`, `archive/whole-arcanum-research-20260605/` | pass |
| `$inventory` auto behavior implemented | `arcana/inventory/SKILL.md` | not-started |
| Index templates implemented | `arcana/inventory/templates/` | not-started |
| Validator extended | `arcana/inventory/scripts/` | not-started |
| First interface-driven pilot slice | `development/pilot/interface-link-index/` | not-started |

## Current Next Route

Run `task-session` for:

```text
SWU-INT-001: update Inventory SKILL/README with auto interface, target inference, and confirmation behavior.
```

## Deferred Or Archived Work

| Work | Status | Reason |
| --- | --- | --- |
| whole-Arcanum inventorization | archived | useful evidence, not active interface MVP |
| whole-`domainspec-core` tagging strategy | archived | useful evidence, not active interface MVP |
| human web UI | deferred | chat-first interface should prove behavior first |
| SQLite/vector index | deferred | JSON indexes should prove shape first |
| EvidenceSet canonical promotion | deferred | still candidate-only |

## Readiness Boundary

This package is ready for implementation of the interface/link/index MVP only.
It is not ready to resume broad inventorization until the interface can:

1. infer a target,
2. ask for confirmation,
3. write a bounded slice,
4. update selector/link/tag/gap indexes,
5. show lookup/status/explain output.
