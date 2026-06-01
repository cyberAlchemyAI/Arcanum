# Interrogation: Invoke Refresh

## Target

`invoke refresh` mode proposal and implementation plan.

## Verdict

`pass with constraints`

The proposal is useful and belongs in invoke, but only if refresh remains a typed evidence-to-artifact-delta mode. If it becomes a broad "rerun invoke and rewrite the pack" command, it will blur lifecycle ownership and make artifacts less trustworthy.

## Challenge Findings

| Finding | Severity | Evidence | Required Response |
| --- | --- | --- | --- |
| Refresh could become silent mutation. | high | Existing design includes `apply-approved`; root invoke forbids silent upstream mutation. | Default to proposal-only and require explicit approval plus declared scope for apply. |
| Refresh could overclaim evidence. | high | Existing benchmark lesson says setup proof is not score proof. | Delta model must include confidence and mutation safety; blockers update before completion claims. |
| Refresh could duplicate workflow-reflect. | medium | Handoff mode routes felt workflow gaps to `workflow-reflect`. | Refresh updates artifacts from evidence; workflow-reflect analyzes workflow quality gaps. |
| Refresh could duplicate task-session. | medium | Task-session owns bounded execution. | Refresh must not run tasks; it can only update task/work-pack state from inspectable outputs. |
| No-op behavior must be first-class. | medium | Re-running sessions often produces no new artifact state. | Add no-op phase status and fixture. |
| Fixture coverage must precede routing. | high | Invoke validation runner gates existing modes through fixtures. | Add pass, flag, block, and no-op fixtures before command routing is promoted. |

## Gate Questions

| Question | Answer |
| --- | --- |
| Does refresh need a new mode contract? | Yes. It has distinct inputs, gates, statuses, and outputs. |
| Should refresh be part of `handoff`? | No. Handoff moves selected context into a new thread; refresh updates current artifacts from evidence. |
| Should refresh apply changes by default? | No. Proposal-only is the safe default. |
| Should refresh support no-op? | Yes. No-op prevents forced churn and records that artifacts are already current. |

## Required Repairs Applied

- Add explicit `proposal-only` default.
- Add no-op status and fixture.
- Add artifact drift flag fixture.
- Add refresh-specific template family.
- Add validation runner checks before promotion.

## Residual Risk

Refresh may still be tempting to use as an execution shortcut. The contract and fixtures should keep repeating that refresh is artifact-state synthesis, not task execution.
