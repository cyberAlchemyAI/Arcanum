---
profile: autobayes-research
name: Invoke Design - Subagent Closeout Hardening
description: Design artifact for adding lifecycle receipt gates to future AutoBayes research runs.
type: invoke-design
status: pass
last_updated: 2026-06-07
---

# Invoke Design

## Smallest Coherent Unit

The smallest useful hardening unit is:

```text
Subagent Lifecycle Ledger + Closeout Gate
```

It does not require changing every subagent strategy immediately. It requires future Task Session and Dispatch Spec research routes to name and check the lifecycle ledger.

## Proposed Artifact Fields

```text
agent_id
role_id
lane_name
spawn_status
spawn_error
join_status
join_timeout_ms
receipt_artifact
close_status
close_error
residue
reroute
```

## Gate Rule

Before Task Session returns `PASS`:

```text
all agents in lifecycle_ledger satisfy:
  spawn_status in [spawned, blocked]
  and if spawned:
    join_status in [completed, timed_out, closed_without_result]
    close_status in [closed, already_closed, not_needed_with_reason]
```

If the gate fails:

- `BLOCK` when an agent is still open and no continuation handoff exists.
- `FLAG` when a lane timed out but is safely recorded as residue.
- `PASS` only when all spawned agents are joined/closed or safely recorded.

## Dispatch Spec Hook

When `subagent_strategy.status` is `recommended` or `required`, the dispatch should name receipt requirements that include subagent lifecycle fields and a closeout gate.

## Task Session Hook

Task Session should include a "subagent closeout" validation line in the final report whenever it spawned or inherited subagents.

