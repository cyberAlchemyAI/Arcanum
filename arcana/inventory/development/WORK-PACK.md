---
module: inventory-lifecycle
version: current
status: runtime-faceted-layout-verified-complete
updatedAt: 2026-07-26
docType: work-pack
---

# WORK-PACK: Inventory Lifecycle Selection And Preserved Interface Lane

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Bounded implementation and terminal closure passed. |
| complexity | medium | Deterministic receipts, append runtime, facets, runtime sync, and isolated proof. |
| outputMode | split | Canonical task files live under `runtime-faceted-layout/tasks/`. |
| architectureRef | `runtime-faceted-layout/WORK-PACK.md` | Accepted generic behavior and sequencing contract. |
| implementationPlanRef | `runtime-faceted-layout/WORK-PACK.md` | Current selected plan. |
| activeLayerWindow | closed | No Task Session unit is selected. |
| readinessProfile | runtime-faceted-layout-verified | Bounded implementation proof, not release authorization. |

## Current Lifecycle Selection

| Field | Value |
| --- | --- |
| selected lane | `runtime-faceted-layout` |
| selected unit | none |
| task contract | terminal closure receipt at `runtime-faceted-layout/session-evidence/TASK-IFR-VERIFY/receipt.json` |
| owner decision | `runtime-faceted-layout/OWNER-ACCEPTANCE.md` |
| execution owner | none active; Sigil Development owns any later selection |
| prior lane | `inventory-interface-link-index`, preserved and deferred |
| prior selected unit | `SWU-INT-001`, no longer current |

The runtime lane supersedes only the current selection. It does not delete,
reject, or claim completion of the interface/link/index lane. Resuming
`SWU-INT-001` requires a later explicit Sigil Development selection receipt.

## Preserved Interface Lane Objective

The remainder of this document preserves the June 2026 interface/link/index
lane as deferred lifecycle evidence. It is not the current Task Session route.

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
| TASK-INT-001 | Update Inventory SKILL/README with auto interface, target inference, and confirmation behavior. | L0 | medium | `INTERFACE-ARCHITECTURE.md` | deferred-by-lifecycle-selection | not-started |
| TASK-INT-002 | Add target proposal and chat-view templates. | L0 | medium | `INTERFACE-ARCHITECTURE.md` | deferred-by-lifecycle-selection | not-started |
| TASK-INT-003 | Add selector/link/backlink/traceability/gap/query/projection index templates. | L1 | medium | `INDEX-TECHNIQUE-RESEARCH.md`, `LINKING-DISCIPLINE.md` | deferred-by-lifecycle-selection | not-started |
| TASK-INT-004 | Extend validator for link/index discipline. | L2 | medium | TASK-INT-003 | deferred-by-lifecycle-selection | not-started |
| TASK-INT-005 | Create first interface-driven pilot slice. | L2 | medium | TASK-INT-001..004 | deferred-by-lifecycle-selection | not-started |
| TASK-INT-006 | Sync readiness/docs and next-route handoff. | L3 | low | TASK-INT-005 | deferred-by-lifecycle-selection | not-started |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Write Scope | Done Criteria | Validation Surface | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-INT-001 | TASK-INT-001 | `INTERFACE-ARCHITECTURE.md`, `arcana/inventory/SKILL.md` | `arcana/inventory/SKILL.md`, `arcana/inventory/README.md` | auto interface and confirmation flow documented | `rg -n "auto|target inference|confirmation|status|explain"` | deferred |
| SWU-INT-002 | TASK-INT-002 | `INTERFACE-ARCHITECTURE.md` | `arcana/inventory/templates/` | target proposal and view templates added | file presence and grep | blocked |
| SWU-INT-003 | TASK-INT-003 | `INDEX-TECHNIQUE-RESEARCH.md`, `LINKING-DISCIPLINE.md` | `arcana/inventory/templates/` | JSON index templates added | `jq empty` examples | blocked |
| SWU-INT-004 | TASK-INT-004 | index templates, validator script | `arcana/inventory/scripts/` | validator checks edge vocabulary and refs | validator run | blocked |
| SWU-INT-005 | TASK-INT-005 | pilot target decision | `arcana/inventory/development/pilot/interface-link-index/` | first interface-driven slice exists | slice validation | blocked |
| SWU-INT-006 | TASK-INT-006 | all prior outputs | development docs | readiness and work-pack synced | readiness review | blocked |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| B-INT-PILOT-TARGET | pilot | First pilot target must be confirmed before slice mutation. | operator/inventory | Resolve only after the interface lane is explicitly reselected. |
| B-INDEX-SCHEMA | templates | Index templates are designed but not yet production templates. | inventory | Execute TASK-INT-003 only after lane reselection and its dependencies. |
| B-AUTO-SKILL-CONTRACT | skill | `$inventory` default behavior is not yet in SKILL.md. | inventory | Execute TASK-INT-001 only after a new lifecycle selection receipt. |

## Gate Checks

1. Run exactly one SWU at a time.
2. No unit is current; do not select `SWU-INT-001` without a new lifecycle
   receipt.
3. Do not start the preserved pilot slice until its interface and index
   templates exist.
4. Do not continue archived whole-Arcanum or whole-repo tracks as active work.
5. Do not write inside unrelated submodules.
6. Do not promote tags to definitions or links to ontology relations.
7. Keep JSON as machine index and Markdown as human explanation.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-05 | Refreshed active development pack around Inventory interface, linking, and indexing; archived whole-Arcanum and whole-repo research roots. | Codex |
| 2026-07-24 | Sigil Development accepted the runtime/faceted-layout lane as the current selection, preserved the interface lane as deferred, and selected `SWU-IFR-001`. | Codex |
| 2026-07-26 | Task Session completed `SWU-IFR-001` with 8/8 receipt-kernel tests and selected only `SWU-IFR-002`. | Codex |
| 2026-07-26 | `SWU-IFR-002` stopped before implementation: preflight block states cannot satisfy mandatory observed-digest fields. No successor selected. | Codex |
| 2026-07-26 | Sigil Development accepted decision Option A and selected the bounded phase-accurate receipt repair `SWU-IFR-001R`. | Codex |
| 2026-07-26 | `SWU-IFR-001R` passed 9/9 tests and JSON Schema meta-validation; `SWU-IFR-002` was reselected. | Codex |
| 2026-07-26 | Resumed `SWU-IFR-002` passed 8/8 no-write transition tests; `SWU-IFR-003` was selected. | Codex |
| 2026-07-26 | `SWU-IFR-003` passed sequential apply and partial-failure observation; `SWU-IFR-004` was selected. | Codex |
| 2026-07-26 | `SWU-IFR-004` passed faceted admission and legacy compatibility; `SWU-IFR-005` was selected. | Codex |
| 2026-07-26 | `SWU-IFR-005` passed exact facet projection and independent validation; `SWU-IFR-006` was selected. | Codex |
| 2026-07-26 | `SWU-IFR-006` passed manifest-bound runtime synchronization and consumer-state protection; `SWU-IFR-007` was selected. | Codex |
| 2026-07-26 | `SWU-IFR-007` passed isolated installed-consumer proof; `TASK-IFR-VERIFY` was selected. | Codex |
| 2026-07-26 | `TASK-IFR-VERIFY` passed recomposition, reflection, and closure; no successor was selected. | Codex |
