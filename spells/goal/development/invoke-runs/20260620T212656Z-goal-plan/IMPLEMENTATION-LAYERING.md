---
artifact_id: GOAL-PLAN-LAYERING-001
artifact_type: invoke-plan-implementation-layering
target: arcanum/spells/goal
invoke_mode: plan
status: draft
owner: spellcraft
created_at: 2026-06-20
---

# Implementation Layering: Goal Spell

## Purpose

Define the layer boundaries for making `arcanum/spells/goal` executable without
collapsing lifecycle validation, runtime implementation, source mutation, and
reusable promotion evidence into one unsafe step.

This artifact is the governance lens for the work-pack. It does not execute
runtime work, mutate the Craft ledger, generate host runtime surfaces, promote
schemas, commit, push, publish, or move a parent gitlink.

## Target And Scope

- Target: `arcanum/spells/goal`
- Scope: draft reusable spell package
- Current state: source contract, public decision-profile schema, define-stage
  spec, definitions, and design bundle exist; runtime implementation and
  reusable behavior evidence remain future work.

## Layer Boundary Rule

Each layer answers: "After this layer, we know whether ...".

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (Lifecycle validation) | After this layer, we know whether the goal source, define/design artifacts, and plan are coherent enough for lifecycle work. | Spellcraft validation of the source/design/plan packet plus a staged Craft sync proposal. | README, public schema, define run, design run, this plan, source authority boundaries. | Runtime skeleton, dispatch execution, active ledger mutation, generated packages. | Spellcraft validation report or explicit refinement block; staged proposal for stale Craft rows if needed. | Continue to L1 only when Spellcraft accepts or repairs the packet. |
| L1 (Read-only runtime skeleton) | After this layer, we know whether the spell can bind a goal, read a frontier, classify risk, and return a non-mutating result. | One read-only loop over a fixture or selected Craft scope that emits `Goal Loop Result` with no source writes. | Goal bind, frontier snapshot, neutral decision-profile defaults, risk classifier, read-only result contract. | Delegated execution, staged deltas, approval apply, gap discovery, reusable validation matrix. | Fixture or reviewable result showing protected and unknown work stops before mutation. | Continue to L2 when read-only behavior is deterministic and fail-closed. |
| L2 (Delegation and staged proposals) | After this layer, we know whether eligible nodes can route through owners, join terminal receipts, audit evidence, and stage deltas without applying them. | One approved low-risk node route with terminal receipt and staged-delta output. | Dispatch route adapter, receipt closeout, audit gate, staged delta creation, no-active-mutation guard. | Approval-token apply, gap discovery loops, generated package, registry readiness. | Route validation, terminal receipt, audit verdict, staged delta shape check. | Continue to L3 when staging cannot bypass approval and open lanes cannot close as success. |
| L3 (Approval, evidence, and generated readiness) | After this layer, we know whether protected apply, telemetry, gap discovery, and reusable validation evidence can support a generated runtime package. | One approval-token path plus low/medium/protected-mutation validation scenarios. | Decision record linkage, approved Craft apply boundary, gap discovery termination, proportionality guard, telemetry, Experiment Harness evidence, runtime installer dry run. | Registry status change or publication unless separately approved. | Experiment Harness report, approval-token validation, telemetry evidence, installer dry-run result. | Package or defer; registry readiness remains blocked until evidence passes. |

## Non Regression Guardrails

- Public spell artifacts must never contain filled decision-profile data.
- Unknown risk remains a protected stop.
- Delegated lanes must return terminal receipts before audit.
- Source-changing progress remains staged until a batch-specific approval token
  and durable decision record exist.
- Runtime success and reusable behavior proof remain separate evidence classes.
- Generated host surfaces are produced by the runtime installer, not
  hand-authored inside this plan.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether the current source/design/plan packet is
  accepted by `spellcraft` or needs refinement before runtime SWUs.
- Major deferred scope: read-only runtime skeleton, delegation/staging runtime,
  approval apply, Experiment Harness evidence, generated runtime packages.
