---
artifact_id: GOAL-EXECUTION-PACK-001
artifact_type: invoke-plan-execution-pack
target: arcanum/spells/goal
status: draft
created_at: 2026-06-20
---

# Execution Pack: Goal Spell

## Purpose

Wave-level execution choreography for the medium-complexity goal spell
work-pack. This file schedules waves and dependencies; it does not redefine
task or SWU contracts.

## Planning Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| planningGateStatus | pass | Ready for W0 lifecycle validation. |
| complexity | medium | Split work-pack with L0-L3 waves. |
| baselineWave | W0 | Spellcraft validation before runtime SWUs. |
| activePlanRef | `WORK-PACK.md` | Canonical executable plan. |
| workPackManifest | `WORK-PACK.md` | Source of task and SWU contracts. |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` | Source of layer decisions. |
| specRef | `../20260620T202601Z-goal-spec-definitions/SPEC.md` | Define-stage source. |
| designRef | `../20260620T205253Z-goal-architecture-rules-schemas-contracts/ARCHITECTURE.md` | Design-stage source. |
| activeLayerWindow | L0 | Start with Spellcraft validation. |
| lastPlannedAt | 2026-06-20T21:26:56Z | Authoring timestamp. |
| readinessProfile | pilot | Draft spell; evidence-gated. |

## Wave Board

| Wave | Layer | Goal | Tasks | Entry Gate | Exit Evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | Validate lifecycle packet and stage source-state sync proposal. | TASK-GOAL-SPELLCRAFT-VALIDATE | Existing define/design/plan artifacts present. | Spellcraft report; staged sync proposal or deferral. |
| [W1](work-pack/waves/W1.md) | L1 | Build read-only bind/frontier/risk/result skeleton. | TASK-GOAL-RUNTIME-SKELETON | W0 accepted or repaired. | Non-mutating Goal Loop Result fixture. |
| [W2](work-pack/waves/W2.md) | L2 | Add delegated route, terminal receipt, audit, and staged delta. | TASK-GOAL-DELEGATION-STAGING | W1 pass. | Dispatch route, receipt, audit verdict, staged delta evidence. |
| [W3](work-pack/waves/W3.md) | L3 | Add approval, gap/budget behavior, reusable evidence, and generated readiness. | TASK-GOAL-APPROVAL-PROMOTION, TASK-GOAL-VERIFY-EVIDENCE | W2 pass. | Approval scenario, experiment report, installer evidence. |

## Parallelization Policy

- W0 is serial and blocks all runtime work.
- W1 is serial because risk classification depends on bound frontier shape.
- W2 may split after SWU-GOAL-005 if route/receipt and audit/staging write
  scopes are disjoint, but the merge must preserve staged-delta authority.
- W3 evidence work may prepare fixture outlines while SWU-GOAL-007 and
  SWU-GOAL-008 run, but Experiment Harness pass evidence requires implemented
  runtime behavior.

## Closure Obligations

- Every task result must update its task file completion evidence.
- Every executed SWU must return the expected result shape from its task file.
- Every source-changing result must remain a staged proposal until approved.
- Any deviation from owner boundaries returns to Spellcraft or Dispatch Spec
  before execution continues.
