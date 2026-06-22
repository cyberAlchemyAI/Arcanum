---
module: inventory-attachment-hook
runId: 20260621T155620Z-architecture-and-spec
stage: s9-invoke-plan
status: pass
updatedAt: 2026-06-21
docType: invoke-plan-refresh
---

# Invoke Plan Refresh

## Mode

`invoke plan`

## Plan Delta

The prior work-pack remains valid with two refinements:

1. `SWU-IAH-001` must include the repaired Inventory mapping details before
   unlocking downstream sigil/spell guidance.
2. `SWU-IAH-006` must include the observed-invocation generated mirror whenever
   OIL canonical docs change.

## Updated Implementation Order

| Order | SWU | Reason |
| --- | --- | --- |
| 1 | `SWU-IAH-001` | Establish Inventory policy vocabulary, candidate-read-model authority, evidence-card/EvidenceSet mapping, and validation expectations. |
| 2 | `SWU-IAH-002` | Add sigil authoring guidance from the stable Inventory contract. |
| 3 | `SWU-IAH-003` | Add spell authoring guidance from the stable Inventory contract. |
| 4 | `SWU-IAH-004` | Add observed invocation phase insertion, failure semantics, hook-operation rows, and recursion guard. |
| 5 | `SWU-IAH-005` | Add policy/handoff templates and schema/fixture checks. |
| 6 | `SWU-IAH-006` | Regenerate generated runtime mirrors, including OIL mirror when touched. |
| 7 | `SWU-IAH-007` | Run a low-risk attached invocation pilot and prove Inventory lookup value. |

## Acceptance Additions

- Policy absent/disabled skips before envelope validation.
- Idempotency is per selected output.
- Public-boundary inheritance must resolve before public writes.
- EvidenceSets group evidence-card IDs only.
- Attachment operations do not recursively attach themselves.
- Validation includes fixture/schema checks, not only grep anchors.

## Next Route

`task-session` on `SWU-IAH-001`.

## Verdict

`pass`: the implementation plan is still sequential and bounded.
