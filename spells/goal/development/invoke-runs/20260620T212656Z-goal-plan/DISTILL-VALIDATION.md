# Distill Validation: Goal Spell Plan

## Distill Result

- Target context: `arcanum/spells/goal` plan-mode handoff after define and
  design artifacts.
- Objective and output artifact: produce a medium-complexity implementation
  plan, implementation layering artifact, work-pack, execution pack, dispatch
  boundary, and SWU contracts.
- Mode and budget: Validate; single Balancer-led pass with repair decisions
  folded into the work-pack.
- Proposal tracks: one track, because the user requested `/invoke plan` on an
  already selected spell package.
- Recursive rounds: 1 / 1.
- Verdict: pass.

## Role Conversation Trace

| Role | Claim Or Objection | Reconciliation |
| --- | --- | --- |
| Proposer | Plan the full L0-L3 route so later runtime work has explicit sequence and gates. | Accepted, because the design already names runtime and evidence gaps. |
| Balancer | Full route could invite premature implementation before Spellcraft validation. | Repaired by making `SWU-GOAL-001` the selected unit and gating all runtime SWUs behind W0. |
| Balancer | Medium split artifacts can duplicate task/SWU authority. | Repaired by keeping `WORK-PACK.md` as source of truth, waves as choreography, and task files as local SWU contracts. |
| Balancer | Craft ledger/view sync is tempting but protected. | Repaired by making it a staged proposal SWU, not an active ledger mutation. |

## Current Smallest Coherent Unit

`SWU-GOAL-001`: Spellcraft validation of the source/design/plan packet.

Responsibility: decide whether the packet is coherent enough for runtime SWUs
or needs named refinement before execution.

## Optimization Point

`SWU-GOAL-001` is small enough to execute without runtime mutation and large
enough to protect the lifecycle boundary. Splitting smaller would only review
individual documents without proving whether they recompose into a valid spell
packet.

## Concept Layer Map

| Layer | Unit | Recomposition Target |
| --- | --- | --- |
| L0 | Spellcraft validation and staged sync proposal. | Accepted lifecycle packet for `goal`. |
| L1 | Read-only runtime skeleton. | Fail-closed control spine. |
| L2 | Delegation, receipt, audit, staging. | Router-only goal behavior with proposal-before-apply. |
| L3 | Approval, telemetry, experiments, generated readiness. | Reusable draft spell evidence. |

## Technique Pack Trace

| Technique | Outcome |
| --- | --- |
| abstraction-level guard | Pass; plan stays at SWU/task/wave level, not source implementation. |
| recomposition proof | Pass; each wave maps back to the design control spine. |
| evolution profile | Pass; generated runtime packaging waits for evidence. |
| frame-expiry note | If Spellcraft changes the design contracts, this plan must refresh before runtime work. |
| navigable result check | Pass; `WORK-PACK.md` selects one start SWU and links task contracts. |

## Closure And Recomposition Proof

- Closure: `SWU-GOAL-001` has one owner, one objective, explicit inputs,
  acceptance evidence, and a reviewable validation surface.
- Recomposition: accepted W0 unlocks W1, W1 unlocks W2, W2 unlocks W3, and W3
  produces the reusable behavior evidence the README says is required before
  registry readiness.

## Deferred Complexity

- Runtime code or generated package authoring is deferred.
- Active Craft ledger mutation is deferred behind a staged proposal and approval.
- Schema relocation is deferred to Spellcraft validation.
- Registry readiness is deferred until Experiment Harness evidence exists.

## Tension Ledger

| Tension | Status | Route |
| --- | --- | --- |
| Plan should be executable but not mutation-capable yet. | resolved | Select `SWU-GOAL-001`, gate runtime SWUs. |
| Public schema exists but design schemas live in an Invoke run. | owned gap | Spellcraft decision during W0. |
| Craft view may lag authored files. | owned gap | Staged sync proposal, not direct mutation. |
| Runtime success could be mistaken for reusable evidence. | guardrail | Experiment Harness remains separate W3 owner. |

## Premortem

Likely failure reason: a future run skips W0 and starts implementing generated
or runtime behavior directly from the plan.

Guardrail: `WORK-PACK.md` marks W0 active, all runtime SWUs dependency-gated,
and generated surfaces as installer-only.

## Frame Expiry Note

Refresh this plan if Spellcraft changes the source contract, moves schema
authority, rejects a design contract, or approves a different lifecycle owner.

## Navigation Guide

Start at `WORK-PACK.md`, then open
`work-pack/tasks/TASK-GOAL-SPELLCRAFT-VALIDATE.md` and execute
`SWU-GOAL-001`. Use `PLAN-DISPATCH.json` for route boundaries and
`IMPLEMENTATION-LAYERING.md` for promotion decisions.

## Next Route

`spellcraft`
