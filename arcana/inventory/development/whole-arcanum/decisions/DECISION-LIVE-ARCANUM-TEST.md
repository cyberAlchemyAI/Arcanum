---
module: inventory-whole-arcanum
version: 0.1.0
status: block
updatedAt: 2026-06-03
docType: decision-record
decisionGate: live-arcanum-test
---

# Decision Gate: Live Arcanum Inventory Test

## Target Scope

Choose the first real Arcanum task lane for testing whole-Arcanum Inventory as
the first context source before broad source search.

## Consequential Work Blocked

- `TASK-LAT-002`: Inventory-first retrieval packet.
- `TASK-LAT-003`: one bounded task-session SWU.
- `TASK-LAT-004`: reuse evidence and promotion signal.

## Blocker Decision

### B-LAT-001: Which lane should the first live test use?

| Option | Benefit | Cost Or Risk | When To Choose | Downstream Impact |
| --- | --- | --- | --- | --- |
| A. Native runtime/install lane | Verifies the latest command-surface removal and native package install story. | May mostly duplicate existing temp install smoke. | Choose if the priority is cross-repository confidence. | Produces install-readiness evidence, less EvidenceSet evidence. |
| B. Missing-card expansion lane | Directly improves coverage by turning a missing area into cards. | Can drift into broad ingestion. | Choose if the priority is more inventory content. | Produces backlog/card evidence, less promotion evidence. |
| C. EvidenceSet reuse lane | Tests the main remaining promotion gate by using a candidate EvidenceSet before execution. | Requires strict non-promotion language after one run. | Choose if the priority is deciding whether EvidenceSets actually help. | Produces the strongest first reuse signal. |
| D. Cross-sigil boundary lane | Exercises Arcanum’s dispersed knowledge across invoke/refine/task-session/context-builder. | Highest complexity and fallback-search risk. | Choose if the priority is stress-testing real Arcanum complexity. | Produces rich but noisier evidence. |

## Recommendation

Select **C. EvidenceSet reuse lane**.

Rationale: the package already validates and native install smoke already
passes. The real unresolved promotion question is whether candidate EvidenceSets
help agents make and execute bounded decisions. Option C tests that directly
while keeping promotion deferred until evidence exists.

## Current Gate Result

- Result: BLOCK
- Decisions resolved: 0
- Blockers remaining: 1
- Decision artifact: `arcana/inventory/development/whole-arcanum/decisions/DECISION-LIVE-ARCANUM-TEST.md`
- Deferred decisions: EvidenceSet promotion, human UI, exhaustive card coverage
- Assumptions recorded: none
- Validation: context artifacts read; no mutation-capable task-session should proceed until B-LAT-001 is resolved
- Next step: user selects A, B, C, or D; recommended C
