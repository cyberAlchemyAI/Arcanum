---
module: inventory-whole-arcanum
version: 0.1.0
status: pass
updatedAt: 2026-05-31
docType: refine-gap-check
refinePreset: compact
research: no-research
---

# Refine Gap Check: Finish Whole-Arcanum Inventory Implementation

## Verdict

No blocker-level design gap is visible before continuing implementation.

The remaining gaps are execution gaps already represented in the work-pack:

- `SWU-WAI-005`: governance cards,
- `SWU-WAI-006`: lifecycle cards,
- `SWU-WAI-007`: cross-pilot EvidenceSet,
- `SWU-WAI-008` through `SWU-WAI-010`: expanded capability-family waves,
- `SWU-WAI-011` and `SWU-WAI-012`: operational readiness.

## Current Evidence

| Area | Status | Evidence |
| --- | --- | --- |
| Source boundary | pass | `source-manifest.json`, `SOURCE-POLICY.md`, `TASK-WAI-001-RESULT.md` |
| Slice validation shape | pass | decision option B selected; `validate-evidence-card-slice.sh` exists |
| Inventory self-slice | pass | four-card self-slice plus retrieval fixture and candidate EvidenceSet |
| Governance/lifecycle pilot | pending implementation | `TASK-WAI-003` is ready and has explicit source anchors |
| L2 expansion | blocked by W1 by design | `TASK-WAI-004` waits for W1 evidence |
| L3 readiness | blocked by W2 by design | `TASK-WAI-005` waits for W2 coverage |

## Remaining Gaps

| Gap | Severity | Classification | Handling |
| --- | --- | --- | --- |
| Governance-card minimum is not explicit in task file | low | assumption | Use two minimum cards: Artifact Constitution and Schema Constitution. |
| Lifecycle-card minimum is not explicit in task file | low | assumption | Use three minimum cards: Invoke plan/refresh boundary, Refine discovery boundary, and Task Session execution boundary. |
| Cross-pilot EvidenceSet depends on governance and lifecycle cards | medium | dependency | Run after `SWU-WAI-005` and `SWU-WAI-006`. |
| L2 family expansion could become too broad | medium | planned gate | Keep family slices selector-backed; record selector gaps instead of broad full-file ingestion. |
| EvidenceSet promotion remains deferred | low | deferred decision | Revisit only after repeated task-session reuse across multiple slices. |
| Human UI remains deferred | low | deferred decision | Revisit only when shell plus `jq` reports become hard to inspect. |

## Refined Execution Route

1. Run `SWU-WAI-005` for governance cards.
2. Run `SWU-WAI-006` for lifecycle cards.
3. Run `SWU-WAI-007` for the cross-pilot EvidenceSet.
4. If W1 validates, open L2 family expansion.
5. Stop at first validation failure, unresolved source authority conflict, or
   selector that requires broad full-file ingestion.

## Decision-Gate Recommendation

Return `PASS`.

There are no visible blocker-level multi-option decisions. The remaining
judgments can be handled as recorded assumptions in task-session execution.
