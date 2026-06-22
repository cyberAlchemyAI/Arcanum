---
module: inventory-attachment-hook
runId: 20260621T155620Z-architecture-and-spec
stage: s8-distill-repair
status: pass
updatedAt: 2026-06-21
docType: distill-repair
---

# Distill Repair

## Selected Repair Unit

`AttachedInventoryHandoff` remains the correct smallest coherent unit.

The repair did not split the concept further; it tightened the boundary around
five implementation-critical edges:

1. per-output idempotency;
2. skip-vs-invalid semantics;
3. recursive attachment prevention;
4. public-boundary inheritance resolution;
5. Inventory record mapping.

## Repairs Applied

| Repair | Artifact |
| --- | --- |
| Added non-authoritative draft notice. | `ARCHITECTURE.md`, `SPEC.md` |
| Corrected runtime order and OIL insertion sequence. | `ARCHITECTURE.md`, `SPEC.md` |
| Moved idempotency to selected outputs. | `ARCHITECTURE.md`, `SPEC.md` |
| Added recursion guard. | `ARCHITECTURE.md`, `SPEC.md` |
| Normalized `promotion_owner`. | `SPEC.md` |
| Added `attachWhen` values. | `SPEC.md` |
| Added weak source-ref behavior. | `SPEC.md` |
| Added evidence-card/EvidenceSet mapping. | `SPEC.md` |
| Added public-boundary inheritance resolution. | `SPEC.md` |
| Tightened validation and mirror scope. | `SPEC.md`, `WORK-PACK.md` |

## Recomposition Proof

The repaired unit still feeds the planned SWUs:

- `SWU-IAH-001`: policy vocabulary, Inventory mapping, candidate-read-model boundary;
- `SWU-IAH-002`: sigil declaration guidance;
- `SWU-IAH-003`: spell declaration guidance;
- `SWU-IAH-004`: observed invocation phase insertion and recursion guard;
- `SWU-IAH-005`: templates and fixtures;
- `SWU-IAH-006`: generated mirror regeneration scope;
- `SWU-IAH-007`: pilot acceptance test.

## Verdict

`pass`: the flags are repaired into implementation criteria.
