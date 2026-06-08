---
module: inventory-interface-link-index
version: current
status: interface-link-index-ready-for-task-session
updatedAt: 2026-06-05
docType: work-pack
---

# WORK-PACK: Inventory Interface, Linking, And Indexing

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Design refresh complete; execution can start with TASK-INT-001. |
| complexity | medium | Skill contract, templates, validators, and pilot slice. |
| outputMode | split | Existing task-session pattern applies; new task files can be added as work starts. |
| architectureRef | `ARCHITECTURE.md` | Active architecture. |
| implementationPlanRef | `IMPLEMENTATION-PLAN.md` | Active plan. |
| activeLayerWindow | L0-L3 | Interface contract through readiness sync. |
| readinessProfile | interface-link-index-ready-for-task-session | Ready for bounded implementation, not feature-complete. |

## Objective Summary

Implement Inventory's user-facing interface and JSON/Markdown index substrate
before continuing any broad inventorization work.

Primary objective:

```text
Calling $inventory should infer what to inventorize, ask for confirmation, then write a bounded Inventory slice and update lookup indexes.
```

## Active Scope

In scope:

- default/no-mode `$inventory` behavior,
- target inference and confirmation proposal,
- status/explain/continue interface views,
- JSON index templates,
- linking discipline,
- validator extensions,
- first interface-driven pilot slice.

Out of scope:

- whole-Arcanum inventorization continuation,
- whole-`domainspec-core` tagging continuation,
- database/vector/search UI,
- ontology/definition promotion,
- source mutation inside submodules.

Archived reference roots:

```text
archive/domainspec-core-research-20260605/
archive/whole-arcanum-research-20260605/
```

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-INT-001 | Default interface contract exists. | L0 | none | SKILL/README grep checks |
| S-INT-002 | Target proposal and interface templates exist. | L0 | S-INT-001 | template presence/review |
| S-INT-003 | JSON index/link templates exist. | L1 | S-INT-001 | `jq empty` examples |
| S-INT-004 | Validator checks link/index discipline. | L2 | S-INT-003 | validator run |
| S-INT-005 | First interface-driven pilot slice exists. | L2 | S-INT-001..004 | cards/index/retrieval/coverage pass |
| S-INT-006 | Pack readiness and docs synchronized. | L3 | S-INT-005 | readiness review |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-INT-001 | Update Inventory SKILL/README with auto interface, target inference, and confirmation behavior. | L0 | medium | `INTERFACE-ARCHITECTURE.md` | ready | not-started |
| TASK-INT-002 | Add target proposal and chat-view templates. | L0 | medium | `INTERFACE-ARCHITECTURE.md` | ready-after-001 | not-started |
| TASK-INT-003 | Add selector/link/backlink/traceability/gap/query/projection index templates. | L1 | medium | `INDEX-TECHNIQUE-RESEARCH.md`, `LINKING-DISCIPLINE.md` | ready-after-001 | not-started |
| TASK-INT-004 | Extend validator for link/index discipline. | L2 | medium | TASK-INT-003 | blocked-by-003 | not-started |
| TASK-INT-005 | Create first interface-driven pilot slice. | L2 | medium | TASK-INT-001..004 | blocked-by-004 | not-started |
| TASK-INT-006 | Sync readiness/docs and next-route handoff. | L3 | low | TASK-INT-005 | blocked-by-005 | not-started |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Write Scope | Done Criteria | Validation Surface | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-INT-001 | TASK-INT-001 | `INTERFACE-ARCHITECTURE.md`, `arcana/inventory/SKILL.md` | `arcana/inventory/SKILL.md`, `arcana/inventory/README.md` | auto interface and confirmation flow documented | `rg -n "auto|target inference|confirmation|status|explain"` | ready |
| SWU-INT-002 | TASK-INT-002 | `INTERFACE-ARCHITECTURE.md` | `arcana/inventory/templates/` | target proposal and view templates added | file presence and grep | blocked |
| SWU-INT-003 | TASK-INT-003 | `INDEX-TECHNIQUE-RESEARCH.md`, `LINKING-DISCIPLINE.md` | `arcana/inventory/templates/` | JSON index templates added | `jq empty` examples | blocked |
| SWU-INT-004 | TASK-INT-004 | index templates, validator script | `arcana/inventory/scripts/` | validator checks edge vocabulary and refs | validator run | blocked |
| SWU-INT-005 | TASK-INT-005 | pilot target decision | `arcana/inventory/development/pilot/interface-link-index/` | first interface-driven slice exists | slice validation | blocked |
| SWU-INT-006 | TASK-INT-006 | all prior outputs | development docs | readiness and work-pack synced | readiness review | blocked |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| B-INT-PILOT-TARGET | pilot | First pilot target must be confirmed before slice mutation. | operator/inventory | Recommend Arcanum vs Sigils Library Authority after interface templates exist. |
| B-INDEX-SCHEMA | templates | Index templates are designed but not yet production templates. | inventory | Execute TASK-INT-003. |
| B-AUTO-SKILL-CONTRACT | skill | `$inventory` default behavior is not yet in SKILL.md. | inventory | Execute TASK-INT-001 first. |

## Gate Checks

1. Run exactly one SWU at a time.
2. Do not start pilot slice until auto interface and index templates exist.
3. Do not continue archived whole-Arcanum or whole-repo tracks as active work.
4. Do not write inside submodules during interface MVP.
5. Do not promote tags to definitions or links to ontology relations.
6. Keep JSON as machine index and Markdown as human explanation.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-05 | Refreshed active development pack around Inventory interface, linking, and indexing; archived whole-Arcanum and whole-repo research roots. | Codex |
