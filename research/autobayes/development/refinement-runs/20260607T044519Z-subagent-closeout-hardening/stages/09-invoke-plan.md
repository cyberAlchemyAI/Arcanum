---
profile: autobayes-research
name: Invoke Plan - Subagent Closeout Hardening
description: Non-executed implementation plan for hardening subagent lifecycle closeout.
type: invoke-plan
status: pass
last_updated: 2026-06-07
---

# Invoke Plan

## Goal

Enable mostly-AFK AutoBayes research by requiring Task Session and Dispatch Spec subagent strategies to prove that all spawned subagents were properly joined, closed, or safely recorded as residue.

## Plan Layers

### Layer 1 - Research-Local Contract

Add a research-local lifecycle ledger specification to the AutoBayes work-pack.

Deliverables:

- `WORK-PACK.md`
- `tasks/TASK-AB-AFK-001-subagent-closeout-hardening.md`
- context handoff Markdown and JSON index
- native Codex goal profile

### Layer 2 - Task Session Report Shape

Prototype the report language that future Task Session outputs should include:

```text
Subagent closeout: pass | flag | block
Spawned: <n>
Joined: <n>
Closed: <n>
Timed out: <n>
Blocked by cap: <n>
Open without handoff: <n>
```

### Layer 3 - Dispatch Spec Receipt Requirements

Prototype dispatch fields or validation expectations:

```text
subagent_strategy.receipt_requirements includes:
  agent_id
  role_id
  spawn_status
  join_status
  close_status
  residue
  reroute
```

### Layer 4 - Validation

Validate future implementation by replaying against known AutoBayes evidence:

- previous full-mode run with six completed lanes and one blocked lane;
- all-possible-subagents run with six completed lanes and one thread-cap blocked lane.

Expected result:

- completed lanes pass;
- thread-cap residue is accepted only because it is explicit;
- no run passes if an agent remains open without a handoff or closeout.

## Non-Goals

- Do not implement canonical Task Session or Dispatch Spec changes in this refinement run.
- Do not promote AutoBayes research vocabulary into canonical Arcanum vocabulary.
- Do not spawn more research subagents from this plan.

## Recommended Execution Route

Use the generated native Codex goal profile:

```text
research/autobayes/work-pack/goals/TASK-AB-AFK-001-GOAL.md
```

