---
module: inventory-whole-arcanum
version: 0.1.0
status: pass
updatedAt: 2026-05-31
docType: decision-record
decisionGate: implementation-completion
---

# Decision Gate: Implementation Completion

## Target Scope

Finish the whole-Arcanum Inventory implementation from the current W1 partial
state.

## Consequential Work Checked

- Continue W1 with governance and lifecycle pilot cards.
- Compose the cross-pilot EvidenceSet.
- Open L2 family expansion only after W1 validation evidence exists.
- Preserve deferred EvidenceSet promotion and human UI decisions.

## Decision Review

| Decision Area | Classification | Gate Result | Rationale |
| --- | --- | --- | --- |
| Governance-card minimum | assumption | pass | Two cards are enough for the proof slice: Artifact Constitution and Schema Constitution. |
| Lifecycle-card minimum | assumption | pass | Three cards cover the execution lifecycle boundary: Invoke, Refine, and Task Session. |
| Cross-pilot EvidenceSet order | dependency | pass | Must run after governance and lifecycle cards exist. |
| EvidenceSet canonical promotion | deferred | pass | Not needed to finish the implementation proof; candidate status remains correct. |
| Human UI | deferred | pass | Agent shell plus `jq` remains the selected runtime surface. |
| L2 broadness risk | planned gate | pass | Existing policy says record selector gaps instead of broad full-file ingestion. |

## Resolved Decisions

No new blocker-level user decision is required.

## Remaining Blockers

None visible.

## Deferred Decisions

| Decision | Status | Revisit Trigger |
| --- | --- | --- |
| EvidenceSet canonical promotion | deferred | After repeated task-session reuse across multiple slices. |
| Human UI | deferred | After shell plus `jq` reports become hard for humans to inspect. |

## Assumptions Recorded

- `SWU-WAI-005` should create at least Artifact Constitution and Schema
  Constitution governance cards.
- `SWU-WAI-006` should create at least Invoke, Refine, and Task Session lifecycle
  cards.
- `SWU-WAI-007` should remain candidate-level and reference only known W1 card
  IDs.
- L2 expansion should not start until W1 cards and the cross-pilot EvidenceSet
  validate.

## Next Step

Proceed to `task-session` on `SWU-WAI-005`.
