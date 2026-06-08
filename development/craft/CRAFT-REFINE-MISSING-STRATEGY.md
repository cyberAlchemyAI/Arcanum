# Craft Refine Missing Strategy

## Purpose

Create a dispatch-backed strategy for refining everything still missing in Craft, surfacing blockers and gaps for decision, building the follow-on work after that decision, and running the first live test.

This is a strategy and preview artifact. It does not execute the full Refine loop, spawn subagents, mutate canonical surfaces, promote Craft, or run the first live test yet.

## Evidence Baseline

| Evidence | Current State |
| --- | --- |
| `development/craft/README.md` | Current verdict is `refine-validation-interrogation-receipt-blocked-promotion-deferred`. |
| `development/craft/SESSION-LEDGER.md` | Next route is a narrow local-skill receipt work-pack for `Interrogation refine-review`. |
| `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json` | Context Builder and Invoke Define are receipt-backed pass evidence; Interrogation refine-review is first block. |
| `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-REFRESH-REPORT.md` | Active Craft receipt workflow uses local skill contracts; command-surface history is evidence only. |
| `development/craft/CRAFT-PROMOTION-READINESS.md` | Craft promotion remains deferred. |

## Selected Strategy

Use a local receipt sequence, not a promotion review:

1. Validate the strategy dispatch.
2. Repair stale blocker text where stage handoff artifacts still say Invoke Define is missing.
3. Preview the full Refine missing-gap route and ask before subagent fanout.
4. Produce or block the `Interrogation refine-review` owner-stage receipt.
5. Refresh research decision only if a local evidence gap appears.
6. X-ray all remaining blockers and gaps into a concrete path-cited ledger.
7. Distill the smallest coherent completion unit.
8. Design the missing-work package.
9. Critique and repair the design.
10. Produce a non-executed work-pack.
11. Present a decision pack.
12. Run the first live test through `task-session` only after an approved ready task exists.

## Subagent Strategy

Dispatch Spec recommends subagents for the later full sweep, but authorization is not granted by this artifact.

| Role | Owns | Why |
| --- | --- | --- |
| `receipt-continuity-auditor` | Remaining owner-stage receipts | Keeps Refine-stage dependency order honest. |
| `craft-gap-auditor` | Craft product/method gaps | Separates method gaps from runtime receipt gaps. |
| `boundary-auditor` | Local skill, command-history, and promotion boundaries | Prevents the old command surface from becoming execution authority again. |
| `live-test-designer` | First live test lane | Ensures the live test is small, meaningful, and evidence-backed. |

Permission prompt:

```text
Approve spawning four local role-bound subagents for the Craft missing-gap sweep before executing the full Refine run?
```

## Blockers And Gaps To Carry Forward

| Item | Classification | Owner | Next Route |
| --- | --- | --- | --- |
| `Interrogation refine-review` lacks owner-stage receipt evidence. | blocker | interrogation | Create or block `receipts/03-interrogation-refine-review.json`. |
| Stage handoff `03-interrogation-refine-review.md` has stale blocked reason. | gap | refine evidence sync | Update during the first receipt work-pack or stale-blocker repair gate. |
| Distill and later stages remain dependency-blocked. | blocker chain | distill / invoke / interrogation | Evaluate only after Interrogation refine-review receipt exists. |
| Full missing-gap inventory is not yet consolidated. | planning gap | refine | Run S5 after strategy approval. |
| First live test is not selected. | decision gap | operator / task-session | Decide after S9/S10 produce a ready work-pack. |
| Craft promotion remains deferred. | boundary | Craft | Keep local; do not promote from this strategy. |

## Dispatch Spec Result

| Field | Value |
| --- | --- |
| Dispatch ID | `craft-refine-missing-strategy-20260605` |
| Dispatch JSON | `development/craft/CRAFT-REFINE-MISSING-STRATEGY-DISPATCH.json` |
| Mode | `mixed` |
| Step count | 12 |
| Subagent strategy | recommended, `requires_user_permission` |
| Promotion guardrail | pass by design; validation below confirms |
| Next route | validate dispatch, then ask for full Refine run/subagent authorization |

## First Live Test Scope

The first live test for this strategy is only a strategy-level dry run:

- validate the dispatch JSON,
- confirm the current evidence still points to `Interrogation refine-review`,
- confirm the stale stage handoff mismatch is detected,
- confirm no build task is executed before approval.

The build/live Craft scenario comes later, after the missing-work work-pack exists.
