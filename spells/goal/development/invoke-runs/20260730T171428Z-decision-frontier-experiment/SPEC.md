---
artifact: goal-decision-frontier-experiment-spec
status: define-pass
target_type: spell-extension-experiment
lifecycle_owner: spellcraft
authority_effect: none
---

# Specification: Goal Decision Frontier Experiment

## 1. Objective

Prove, using synthetic fixtures, whether a decision-discovery DAG can yield a
deterministic, explainable, claim-aware frontier for Goal while Craft remains
the accepted state authority and implementation execution remains outside the
protocol.

## 2. Actors

- **Invoking author:** identifies material ambiguity and authors or refreshes a
  candidate decision map.
- **Craft owner:** accepts durable decision state and relations.
- **Goal controller:** computes eligibility, claims one candidate, and stages
  reconciliation proposals.
- **Human decision owner:** resolves HITL decisions.
- **AFK resolver:** may resolve explicitly routable non-human decisions.
- **Task Session owner:** executes an explicitly selected SWU after this
  experiment's lifecycle gates.
- **Spellcraft owner:** validates reusable spell behavior and any later
  canonical integration.

## 3. Functional Requirements

| ID | Requirement |
| --- | --- |
| FR-01 | Accept a versioned decision-map fixture containing a destination, nodes, dependency edges, state, route, and source digest. |
| FR-02 | Validate identifiers, edge endpoints, acyclicity, state transitions, and route values before computing a frontier. |
| FR-03 | Compute eligibility as `open ∩ blockers-resolved ∩ unclaimed ∩ in-scope ∩ precise`. |
| FR-04 | Emit, for every node, eligibility plus stable exclusion reasons. |
| FR-05 | Exclude fog and out-of-scope nodes from the frontier without deleting them. |
| FR-06 | Claim at most one eligible node using source-digest and compare-and-set semantics; reject stale or competing claims. |
| FR-07 | Preserve an explicit HITL stop; the controller must never auto-resolve a human-owned decision. |
| FR-08 | Accept a resolution receipt and produce a reconciliation proposal that may add, invalidate, supersede, or unblock nodes while preserving history. |
| FR-09 | Emit a Way Clear receipt only when no open precise decision or unresolved fog remains within the destination boundary. |
| FR-10 | Keep decision state distinct from Craft task/SWU completion and from Task Session execution state. |
| FR-11 | Produce byte-identical canonical JSON for repeated identical inputs. |
| FR-12 | Prove source authority remains unchanged by hashing the bounded canonical inputs before and after the experiment. |

## 4. Invariants

1. Craft remains the only accepted durable ledger authority.
2. A decision projection cannot mutate Craft or a tracker.
3. Fog is a question-shaped uncertainty, never an eligible task.
4. Out-of-scope state cannot graduate without an explicit destination redraw.
5. A claim binds the exact source digest; stale claims fail closed.
6. HITL decisions require human resolution evidence.
7. Decision closure never completes a task, SWU, or Goal execution node.
8. Reconciliation is proposal-only until an owning capability accepts it.
9. Identical inputs and claim state produce identical frontier bytes.
10. No fixture or receipt asserts promotion, publication, or production
    readiness.

## 5. State Model

Decision node states:

```text
open -> resolved
open -> invalidated
open -> superseded
fog  -> open        (only with a precise question and owner)
out_of_scope -> open (only after destination redraw)
```

Claims are separate leases over `open` nodes and do not change decision state.
Resolution and reconciliation are separate receipts.

## 6. Inputs And Outputs

Inputs:

- decision-map fixture;
- optional active-claim fixture;
- optional resolution receipt;
- exact source digest.

Outputs:

- validation receipt;
- frontier snapshot with per-node reasons;
- claim receipt or fail-closed rejection;
- reconciliation proposal;
- Way Clear receipt when its strict predicate holds.

All outputs are development evidence and non-authoritative projections.

## 7. Success Criteria

The experiment passes only if all planned witnesses DFE-FIX-001 through
DFE-FIX-012 pass, repeated outputs are byte-identical, canonical source hashes
are unchanged, and an independent closure review confirms the decision versus
execution boundary.

## 8. Non-Goals

- importing or vendoring the upstream Wayfinder skill;
- operating GitHub Issues or another tracker;
- changing canonical Craft, Goal, Invoke, or Task Session contracts;
- implementing a daemon, network service, or shared lock manager;
- selecting or executing an SWU;
- claiming broad workflow improvement from fixture results alone.

## 9. Evidence Ceiling

This specification establishes a testable hypothesis and experiment boundary.
It does not prove the reducer exists, the fixtures pass, or the pattern should
be adopted.

