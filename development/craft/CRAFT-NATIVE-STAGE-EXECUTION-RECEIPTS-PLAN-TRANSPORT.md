# Plan Transport: Craft Native Stage Execution Receipts

## Invoke Run

| Field | Value |
| --- | --- |
| Mode | plan |
| Target | `development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS` |
| Target owner | Craft development package |
| Output mode | split |
| Complexity | medium |
| Created | 2026-06-01 |

## Source Evidence

| Source | Use |
| --- | --- |
| `development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md/evidence-index.json` | Current receipt blocker evidence. |
| `development/craft/CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-WORK-PACK.md` | Completed prerequisite receipt-semantics repair. |
| `tools/arcanum` | Native Refine implementation surface. |
| `spells/invoke/plan.md` | Planning governance and SWU requirements. |

## Outputs

| Artifact | Role |
| --- | --- |
| `CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-IMPLEMENTATION-LAYERING.md` | L0-L3 layer boundary for the receipt bridge. |
| `CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md` | Executable work-pack and SWU manifest. |
| `CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-EXECUTION-PACK.md` | Wave sequencing. |
| `work-packs/native-stage-execution-receipts/tasks/` | Task-local SWU contracts. |
| `work-packs/native-stage-execution-receipts/waves/` | Layer-mapped wave contracts. |

## Decisions

| Decision | Selected | Reason |
| --- | --- | --- |
| Use a local receipt bridge before broad runtime redesign. | yes | The immediate blocker is missing receipt evidence for prepared native handoffs. |
| Make Task Session or the parent runtime responsible for producing receipts. | yes | The shell wrapper cannot execute model-backed owner-stage reasoning safely by itself. |
| Keep Craft promotion deferred. | yes | This plan repairs validation infrastructure only. |

## Unresolved Gaps

| Gap | Owner | Treatment |
| --- | --- | --- |
| Cross-runtime skill execution interface | Runtime interface thread | Deferred to `ARCANUM-SKILL-RUNTIME-HANDOFF.md`. |
| Receipts for downstream Refine stages | Future receipt work | Start with Context Builder receipt proof, then repeat after the bridge works. |

## Recommended Next Route

```text
$task-session development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md --task CRAFT-NATIVE-RECEIPT-001
```
