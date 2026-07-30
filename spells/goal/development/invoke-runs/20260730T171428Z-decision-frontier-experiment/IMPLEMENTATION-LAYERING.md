---
artifact: goal-decision-frontier-experiment-layering
status: plan-authored
active_layer_window: L0
selected_swu: none
---

# Implementation Layering

## Layer Model

| Layer | Outcome | Admitted work | Explicitly excluded | Promotion evidence |
| --- | --- | --- | --- | --- |
| L0 Contract and pure reduction | deterministic validated frontier on synthetic maps | schemas, graph validator, canonicalizer, pure reducer, golden fixtures | claims, reconciliation, adapters, canonical files | DFE-FIX-001, 003, 006, 009 |
| L1 Controlled state transitions | claim and reconciliation semantics | digest CAS simulator, resolution validation, immutable reconciliation proposals | distributed leases, Craft writes, tracker mutation | DFE-FIX-002, 004, 005, 007 |
| L2 Control-boundary proof | HITL, Way Clear, and decision/execution non-collapse | separate boundary reducers and all-witness replay | adapters, canonical contract changes, Task Session execution | DFE-FIX-008, 011, 012 plus full matrix |
| L3 Evidence and lifecycle decision | decide whether an adapter, workflow experiment, or canonical Design refresh is warranted | authority hash, independent closure, Spellcraft review | direct adapter implementation, promotion, publication, production claim | DFE-FIX-010, complete owner receipts, and explicit lifecycle decision |

## Active Window

Only L0 is active for execution eligibility. Even within L0, no SWU is
selected. Later layers are blocked by predecessor owner receipts.

## Authority Boundaries

- The implementation root is development-only.
- Canonical Craft, Goal, Invoke, and Task Session paths remain read-only for
  every planned mutation unit.
- L3 can authorize a new Invoke Design refresh; it cannot directly integrate
  the candidate.
- Fixture evidence supports mechanism behavior only.

## Ordering Rationale

The graph contract must fail closed before a reducer can be trusted. The
reducer must be deterministic before stateful claims are introduced. Claims
must bind the same digest model used by reconciliation. HITL, Way Clear, and
execution non-collapse are separate acceptance boundaries. Cross-capability
adapters are deferred until fixture evidence supports a new Design route.
