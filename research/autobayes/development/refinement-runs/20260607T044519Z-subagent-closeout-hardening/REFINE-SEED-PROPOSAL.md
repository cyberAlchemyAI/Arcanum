---
profile: autobayes-research
name: Subagent Closeout Hardening Seed
description: Refine seed for hardening subagent lifecycle strategy in Task Session and Dispatch Spec research runs.
type: refine-seed-proposal
status: pass
run_id: 20260607T044519Z-subagent-closeout-hardening
last_updated: 2026-06-07
---

# Refine Seed Proposal

## Target

Harden the AutoBayes research subagent strategy so future Task Session and Dispatch Spec runs can proceed mostly unattended while still proving that spawned subagents were properly joined, closed, or recorded as blocked.

## Operator Intent

Use `refine`, then `invoke` planning, then `codex-goal-profile` so a native Codex Goal can continue the research-learning work.

## Problem Statement

The current AutoBayes research strategy successfully used subagents, but two residues appeared:

- one planned lane was blocked by the runtime thread cap;
- closeout correctness depended on the parent remembering to wait, integrate, and close agents manually.

For full-AFK research, this must become a governed invariant:

```text
every spawned subagent has a lifecycle receipt:
  spawned -> joined | timed_out | blocked | closed
```

The parent task-session result should not pass until that lifecycle ledger is complete.

## Desired Outcome

A non-executed hardening plan plus a ready native Codex `/goal` profile that can continue the AutoBayes research work by implementing the hardening artifacts.

## Write Scope

Allowed:

- `research/autobayes/development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/`
- `research/autobayes/work-pack/`

Deferred until the goal executes:

- canonical `arcana/task-session/`
- canonical `formulae/dispatch-spec/`
- global memory, registry, ontology, or runtime surfaces

## Done Criteria

- Refine run folder exists with seed, dispatch, handoff, manifest, evidence index, and result.
- Dispatch validates with `formulae/dispatch-spec/scripts/validate-dispatch.py`.
- Invoke-style plan exists and names concrete hardening layers.
- Work-pack has a selected SWU with bounded write scope and validation.
- Context handoff pack exists as Markdown plus JSON index.
- Codex goal profile is generated with strict coverage, boundaries, and stop condition.

## Research Mode

`no-research`: existing AutoBayes task-session evidence is sufficient. External research is not needed for this hardening design.

