---
module: inventory-whole-arcanum
version: 0.1.0
status: blocked-pending-decision
updatedAt: 2026-06-03
docType: work-pack
---

# WORK-PACK: Live Arcanum Inventory Test

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | blocked-pending-decision |
| complexity | medium |
| outputMode | single-file |
| planRef | `LIVE-ARCANUM-TEST-PLAN.md` |
| decisionRef | `decisions/DECISION-LIVE-ARCANUM-TEST.md` |
| activeLayerWindow | L0 |
| nextExecutableSWU | none until `B-LAT-001` is resolved |
| nextRoute | decision-gate, then task-session |

## Objective

Run one continuous Inventory-first test inside Arcanum and produce reuse evidence
that decides what Inventory still lacks before broader promotion.

## Task Board

| Task | Goal | Layer | Status |
| --- | --- | --- | --- |
| TASK-LAT-001 | Select the first live Arcanum task lane. | L0 | blocked |
| TASK-LAT-002 | Build Inventory-first retrieval packet for selected lane. | L1 | pending |
| TASK-LAT-003 | Execute one bounded task-session SWU using the retrieval packet. | L2 | pending |
| TASK-LAT-004 | Synthesize reuse evidence and promotion signal. | L3 | pending |

## SWU Manifest

| SWU | Parent | Goal | Dependencies | Write Scope | Validation |
| --- | --- | --- | --- | --- | --- |
| SWU-LAT-001 | TASK-LAT-001 | Resolve first task lane and acceptance metric. | none | `decisions/DECISION-LIVE-ARCANUM-TEST.md` | decision-gate result PASS |
| SWU-LAT-002 | TASK-LAT-002 | Query cards and EvidenceSets before broad source search. | SWU-LAT-001 | `task-session/live-arcanum-test-*-CONTEXT.md` | query commands recorded with selected/excluded cards |
| SWU-LAT-003 | TASK-LAT-003 | Execute one selected bounded task. | SWU-LAT-002 | selected by lane | task-specific validation plus whole-inventory validation |
| SWU-LAT-004 | TASK-LAT-004 | Record reuse evidence and next Inventory gaps. | SWU-LAT-003 | `task-session/live-arcanum-test-*-RESULT.md` | result includes cards used, gaps, and EvidenceSet recommendation |

## Completion Criteria

- The first task lane is explicitly selected.
- The run starts from Inventory cards/EvidenceSets before broad `rg`.
- Fallback searches are recorded as gaps, not hidden.
- One bounded task-session result exists.
- The whole-inventory validator still passes after the run.
- EvidenceSets remain candidate-level unless a later explicit promotion decision exists.

## Blockers

| ID | Blocking Scope | Status | Resolution |
| --- | --- | --- | --- |
| B-LAT-001 | TASK-LAT-001 through TASK-LAT-004 | open | User selects first task lane in `DECISION-LIVE-ARCANUM-TEST.md`. |

## Deferred Decisions

- EvidenceSet promotion after one run: deferred until reuse evidence is available.
- Human UI: deferred.
- Exhaustive card coverage: deferred; missing cards become backlog evidence.

## Recommended Next Step

Resolve `B-LAT-001` by selecting one task lane. Recommendation: **C. EvidenceSet
reuse lane**.
