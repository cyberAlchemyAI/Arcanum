---
artifact_id: GOAL-RULES-001
artifact_type: invoke-design-rules
target: arcanum/spells/goal
status: draft
created_at: 2026-06-20
---

# Goal Spell Rules

## Rule Status

These rules are design-stage contract rules for future implementation. They
define expected behavior and validation surfaces; they do not implement runtime
code by themselves.

## Rule Families

| Family | Purpose |
| --- | --- |
| Authority | Preserve source-of-truth and public/private boundaries. |
| Risk | Keep unapproved or unknown work fail-closed. |
| Routing | Ensure delegated work has an owner, technique, and fallback. |
| Receipt | Prevent hidden open lanes from appearing complete. |
| Audit | Require evidence before accepting progress. |
| Staging | Separate proposals from active mutation. |
| Approval | Bind protected apply operations to explicit decisions. |
| Budget | Prevent overbuilt or runaway loops. |
| Observability | Preserve round and goal evidence. |

## Authority Rules

| Rule | Statement | Violation |
| --- | --- | --- |
| `GOAL-R-AUTH-001` | Bind a source authority before reading or routing work. | Block with `source-authority`. |
| `GOAL-R-AUTH-002` | Do not mutate active Craft ledger rows directly. | Block with `direct-mutation`. |
| `GOAL-R-AUTH-003` | Do not copy filled decision-profile data into public spell files. | Block with `public-private-leak`. |
| `GOAL-R-AUTH-004` | Do not hand-author generated host surfaces such as `SKILL.md`. | Block with `generated-surface`. |
| `GOAL-R-AUTH-005` | Do not commit, push, create PRs, publish, or move gitlinks unless explicitly approved. | Stop with `protected-operation`. |

## Risk Rules

| Rule | Statement | Violation |
| --- | --- | --- |
| `GOAL-R-RISK-001` | Every frontier node must be classified before routing. | Block with `missing-risk-tier`. |
| `GOAL-R-RISK-002` | Unknown risk resolves to protected stop. | Stop with `unknown-risk`. |
| `GOAL-R-RISK-003` | Mutation, shell, network, CI, publication, commit, push, PR, and promotion are protected operations. | Stop with `protected-operation`. |
| `GOAL-R-RISK-004` | Read-only planning, context selection, and staged proposals may route when owner and validation are clear. | Block if owner or validation is missing. |

## Routing Rules

| Rule | Statement | Violation |
| --- | --- | --- |
| `GOAL-R-ROUTE-001` | A routable node must name owner, technique, inputs, receipt fields, and fallback. | Block with `invalid-route`. |
| `GOAL-R-ROUTE-002` | Dispatch Spec validates route shape before delegation. | Block with `route-validation`. |
| `GOAL-R-ROUTE-003` | The spell may not redefine delegated owner internals. | Block with `owner-boundary`. |
| `GOAL-R-ROUTE-004` | Subagents require explicit authorization and terminal closeout. | Block with `subagent-closeout`. |

## Receipt Rules

| Rule | Statement | Violation |
| --- | --- | --- |
| `GOAL-R-REC-001` | Every delegated lane must return a terminal receipt. | Block with `open-lane`. |
| `GOAL-R-REC-002` | A receipt must include status, evidence, validation, files touched when applicable, residue, and reroute. | Flag or block with `receipt-shape`. |
| `GOAL-R-REC-003` | Timed-out lanes need residue and reroute before parent synthesis. | Block with `timeout-open`. |

## Audit Rules

| Rule | Statement | Violation |
| --- | --- | --- |
| `GOAL-R-AUDIT-001` | Audit runs before accepting progress. | Block with `missing-audit`. |
| `GOAL-R-AUDIT-002` | Audit veto overrides apparent success. | Stop with `audit-veto`. |
| `GOAL-R-AUDIT-003` | Evidence weaker than the node done criteria cannot close the node. | Block with `insufficient-evidence`. |

## Staging Rules

| Rule | Statement | Violation |
| --- | --- | --- |
| `GOAL-R-STAGE-001` | Source-changing progress becomes a staged delta first. | Block with `unstaged-change`. |
| `GOAL-R-STAGE-002` | A staged delta must include target, operation, framed diff, validation expectation, and promotion state. | Block with `staged-delta-shape`. |
| `GOAL-R-STAGE-003` | Staged deltas are not active source truth. | Block if treated as applied. |

## Approval Rules

| Rule | Statement | Violation |
| --- | --- | --- |
| `GOAL-R-APPROVE-001` | Protected apply requires an approval token. | Stop with `approval-required`. |
| `GOAL-R-APPROVE-002` | Approval token must bind exact batch, approver, state, and durable decision record. | Block with `approval-token-shape`. |
| `GOAL-R-APPROVE-003` | Approval token is not ambient authority for unrelated operations. | Block with `ambient-approval`. |

## Budget And Gap Rules

| Rule | Statement | Violation |
| --- | --- | --- |
| `GOAL-R-BUDGET-001` | Stop before exceeding turn, token, spawn, or no-progress budgets. | Stop with `budget-ceiling`. |
| `GOAL-R-BUDGET-002` | Gap discovery runs only after the active frontier is empty and the module is enabled. | Block with `early-gap-discovery`. |
| `GOAL-R-BUDGET-003` | Gap discovery dedupes by `(kind, target)` and queues proposals. | Flag or block with `gap-loop`. |

## Observability Rules

| Rule | Statement | Violation |
| --- | --- | --- |
| `GOAL-R-OBS-001` | Emit a round signal when observability is available. | Flag with `telemetry-skipped` when unavailable. |
| `GOAL-R-OBS-002` | Final result reports extra sources outside the pack with the named gap that justified each. | Flag with `missing-extra-source-report`. |
| `GOAL-R-OBS-003` | Task-session runtime evidence and experiment-harness reusable evidence remain distinct. | Block promotion if conflated. |

## Enforcement Order

1. Source authority.
2. Public/private boundary.
3. Risk classification.
4. Route validation.
5. Receipt closeout.
6. Audit.
7. Staging shape.
8. Approval token.
9. Apply validation.
10. Telemetry and final report.
