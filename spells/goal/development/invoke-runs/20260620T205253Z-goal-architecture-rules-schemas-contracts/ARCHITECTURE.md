---
artifact_id: GOAL-ARCH-001
artifact_type: invoke-design-architecture
target: arcanum/spells/goal
invoke_mode: design
status: draft
owner: spellcraft
source_define_run: ../20260620T202601Z-goal-spec-definitions/SPEC.md
created_at: 2026-06-20
---

# Goal Spell Architecture

## Purpose

This architecture bundle turns the `goal` spell source contract and define-stage
spec into a design-stage view set. It defines how the spell composes existing
Arcanum capabilities, which rules protect source authority, which schemas shape
handoff artifacts, and which contracts gate later runtime implementation.

This is not runtime implementation, generated host packaging, promotion
evidence, publication, commit, push, PR creation, or parent gitlink movement.

## View 1 - Context

`goal` is a draft reusable spell at `arcanum/spells/goal/`. It advances a
bounded goal over a Craft-backed work graph while preserving source authority
and owner boundaries.

| Boundary | In Scope | Out Of Scope |
| --- | --- | --- |
| Work graph | Read frontier, blockers, gaps, candidate SWUs. | Inventing work outside the selected Craft scope. |
| Delegation | Route to existing owners and collect receipts. | Reimplementing delegated sigil internals. |
| Mutation | Stage proposed deltas and promote only after approval. | Direct active-ledger mutation. |
| Profile policy | Validate public profile shape and neutral defaults. | Shipping filled private runtime profiles. |
| Lifecycle | Draft source contract, design artifacts, future validation. | Promotion without Experiment Harness evidence. |

Primary consumers:

- `spellcraft`, for lifecycle validation and future promotion review.
- `task-session`, for bounded runtime SWU execution.
- `experiment-harness`, for reusable behavior proof.
- `runtime installer`, for generated host surfaces after source validation.

## View 2 - High-Level Structure

```text
User goal
  -> goal bind
  -> Craft frontier snapshot
  -> risk classifier
  -> owner and technique selector
  -> dispatch-spec route validation
  -> delegated owner execution
  -> receipt join
  -> audit gate
  -> staged delta
  -> approval token
  -> Craft apply and validation
  -> telemetry and next route
```

Architectural principle: `goal` owns routing, guards, staged proposal discipline,
and stop behavior. It delegates capability-specific work to owners.

## View 3 - Low-Level Components

| Component | Owner | Input | Output | Contract |
| --- | --- | --- | --- | --- |
| Goal binder | `goal` | User intent, candidate scope. | Bound scope or block. | Source authority contract. |
| Frontier reader | `goal` + `arcana/craft` | Bound Craft scope. | Frontier snapshot. | Frontier snapshot schema. |
| Risk classifier | `goal` | Frontier node and decision policy. | Risk tier and stop flag. | Risk classification rules. |
| Owner selector | `goal` + `dispatch-spec` | Node, risk tier, capability map. | Dispatch route. | Dispatch route contract. |
| Delegated executor | Owner capability | Route and scoped inputs. | Execution receipt. | Execution receipt schema. |
| Audit gate | `goal` + review owner | Receipt, done criteria, validation. | Accepted, flagged, vetoed, or blocked verdict. | Audit contract. |
| Staging engine | `goal` | Accepted progress requiring source change. | Staged delta. | Staged delta schema. |
| Approval gate | `decision-gate` + user | Staged batch. | Approval token or deferral. | Approval token schema. |
| Promotion adapter | `arcana/craft` | Approved batch. | Applied mutation or validation block. | Promotion contract. |
| Telemetry emitter | Observability capabilities | Round state and result. | Spell signal. | Telemetry signal schema. |

## View 4 - Workflow Process

1. Bind source authority.
2. Read the frontier without source mutation.
3. Classify every node by risk.
4. Stop on protected, unknown, or unapproved mutation work.
5. Build a Dispatch Spec route for eligible work.
6. Delegate to the owner and require terminal receipt closeout.
7. Audit before accepting progress.
8. Convert accepted source-changing progress into a staged delta.
9. Batch staged deltas and wait for approval token.
10. Apply approved batches only through the owning source authority.
11. Emit telemetry and report next route.

## View 5 - Decision Flow

| Decision | Default | Escalates When | Output |
| --- | --- | --- | --- |
| Is scope bound? | Block if ambiguous. | More than one source authority fits. | Bound scope or source-authority block. |
| Is node risk acceptable? | Unknown becomes protected stop. | Node involves mutation, publication, shell, network, commit, push, PR, or promotion. | Risk tier or stop. |
| Which owner handles node? | Use owner-scoped route. | No owner or technique fits. | Dispatch route or route block. |
| Did receipt close? | Block if open. | Owner returns no terminal state. | Receipt or closeout block. |
| Did audit pass? | Veto overrides pass. | Evidence missing or review blocks. | Accepted, flag, block, or veto. |
| Can delta stage? | Stage only, never direct apply. | Proposed change lacks framed diff or validation expectation. | Staged delta or staging block. |
| Can batch apply? | Wait for approval. | Approval token absent or not batch-specific. | Hold, reject, or apply. |
| Can spell promote? | Stay draft. | Reusable behavior proof is absent. | Promotion block. |

## View 6 - Dependency Interface

| Dependency | Interface | Direction | Failure Policy |
| --- | --- | --- | --- |
| `arcana/craft` | Frontier read, source validation, approved apply. | `goal` -> `craft` | Block on unreadable source or failed validation. |
| `formulae/dispatch-spec` | Route shape and technique validation. | `goal` -> `dispatch-spec` | Block on invalid route. |
| `arcana/task-session` | Bounded node execution. | `goal` -> `task-session` | Require receipt and validation evidence. |
| `arcana/decision-gate` | Durable approval decisions. | `goal` -> `decision-gate` | Hold batch without approval record. |
| `spells/observed-invocation-loop` | Wrapped delegated execution. | `goal` -> observed runtime | Block on missing observation envelope when required. |
| Observability package | Spell telemetry. | `goal` -> observability | Report skipped telemetry when unavailable. |
| `experiment-harness` | Reusable behavior validation. | `spellcraft` -> harness | Promotion stays blocked until evidence passes. |

## Architectural Decisions

| ID | Decision | Rationale |
| --- | --- | --- |
| `GOAL-ADR-001` | Keep `goal` router-only. | Avoids redefining delegated sigil contracts. |
| `GOAL-ADR-002` | Stage source changes before approval. | Makes mutation reviewable and reversible before apply. |
| `GOAL-ADR-003` | Treat unknown risk as protected stop. | Preserves fail-closed behavior. |
| `GOAL-ADR-004` | Keep filled decision profiles private. | Public package ships schema and neutral defaults only. |
| `GOAL-ADR-005` | Separate task-session evidence from experiment evidence. | Runtime success does not prove reusable promotion readiness. |

## Design Gaps

| Gap | Owner | Next Route |
| --- | --- | --- |
| Exact runtime implementation of each component. | `task-session` | Select and execute `SWU-GOAL-*` units. |
| Fixture-backed rule enforcement. | `experiment-harness` | Build low, medium, and protected-mutation scenarios. |
| Generated host package. | Runtime installer | Generate after Spellcraft source validation. |
| Public design note migration. | Operator approval | Move only scrubbed public-safe design notes when explicitly approved. |

## Handoff

Next owner: `spellcraft validate`.

Required handoff package:

- `ARCHITECTURE.md`
- `RULES.md`
- `SCHEMAS.md`
- `CONTRACTS.md`
- machine-readable schemas under `schemas/`
- `DISPATCH-TECHNIQUE-TRACE.json`
- `INVOKE-RESULT.md`
