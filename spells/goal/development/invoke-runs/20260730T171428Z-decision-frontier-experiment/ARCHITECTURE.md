---
artifact: goal-decision-frontier-experiment-architecture
status: design-validated
selection_status: pass-fixed-point
authority_effect: none
---

# Architecture: Goal Decision Frontier Experiment

## View 1: Context And Ownership

```text
External pattern       Invoke              Craft
(Wayfinder)       ->   candidate map  ->   accepted decision state
                            |                     |
                            v                     v
                         Goal decision-frontier projection
                            |
                   claim / route / reconcile proposal
                            |
              +-------------+-------------+
              |                           |
          HITL owner                  AFK resolver

Decision closure --------------------X--> Task/SWU completion
```

Ownership is intentionally asymmetric:

- Invoke owns authoring and refresh proposals.
- Craft owns accepted durable state.
- Goal owns derived eligibility and control receipts.
- Human or AFK owners supply resolution evidence.
- Task Session owns selected implementation execution.
- Spellcraft owns lifecycle validation of the experiment and any reusable Goal
  behavior.

The experiment replaces every external dependency above with synthetic
fixtures and non-authoritative receipts.

## View 2: Components

| Component | Responsibility | Authority |
| --- | --- | --- |
| Decision Map Validator | validate shape, endpoints, states, routes, and DAG | none |
| Canonicalizer | produce stable JSON bytes and digests | none |
| Frontier Reducer | derive eligibility and exclusion reasons | projection only |
| Claim Simulator | compare-and-set one digest-bound claim | fixture-local only |
| Resolution Validator | validate owner, route, decision ID, and source digest | none |
| Reconciler | stage add/invalidate/supersede/unblock proposals | proposal only |
| Way Clear Evaluator | test the strict terminal predicate | receipt only |
| Boundary Auditor | prove no task/SWU status or canonical source changed | evidence only |

No component writes Craft, Goal's canonical runtime state, or an issue tracker.

## View 3: Information And State

### Decision Map

```text
destination
source_digest
nodes[id, question, state, route, scope, owner]
edges[blocker_id, blocked_id]
```

Allowed experiment states are `open`, `resolved`, `fog`, `out_of_scope`,
`invalidated`, and `superseded`. Claims are separate records:

```text
claim_id
decision_id
source_digest
owner
claimed_at
status
```

Resolution receipts bind the decision and source digest. Reconciliation output
contains proposals plus causal references; it never rewrites the input map.

### Frontier Derivation

For node `n`:

```text
eligible(n) =
  state(n) == open
  AND precise(n)
  AND in_scope(n)
  AND no_active_claim(n, source_digest)
  AND every blocker(n) is resolved or invalidated
```

The reducer emits a stable reason set when any predicate fails. A graph cycle
invalidates the whole frontier computation.

## View 4: Runtime And Sequence

```text
validate map
  -> canonicalize and digest
  -> derive full eligibility projection
  -> choose first stable eligible candidate
  -> compare-and-set claim
  -> route HITL or AFK
  -> validate resolution receipt
  -> stage reconciliation proposal
  -> recompute candidate projection
  -> emit Way Clear only if strict predicate passes
```

A HITL route stops after the claim and route receipt. The experiment has no
model-backed auto-resolution. Any stale digest, cycle, unknown endpoint,
competing claim, or invalid state transition stops before a downstream output.

## View 5: Failure, Recovery, And Concurrency

| Failure | Response | Recovery |
| --- | --- | --- |
| cycle or unknown edge | block frontier | repair fixture and rerun |
| stale source digest | reject claim/resolution | reread current map |
| competing active claim | exclude node | choose another frontier node or stop |
| invalid state transition | reject reconciliation | produce corrected receipt |
| HITL owner unavailable | retain active stop | no automatic fallback |
| output interruption | discard temp output | deterministic rerun |
| canonical source hash drift | fail authority witness | inspect scoped diff; no auto-repair |

L0 uses a single-process, file-backed simulator with atomic replacement. Lease
expiry, distributed locks, and crash recovery are deferred because fixture
evidence cannot justify production concurrency semantics.

## View 6: Validation And Evolution

Validation has four layers:

1. schema and graph mutants;
2. golden reducer, claim, and reconciliation fixtures;
3. cross-boundary assertions for HITL and execution separation;
4. independent closure and canonical-source hash review.

Evolution is gated:

- L0 proves contracts and pure frontier reduction;
- L1 proves claim and reconciliation behavior;
- L2 proves human, terminal, and decision/execution boundaries plus all
  fixtures;
- L3 evaluates evidence and decides whether a separate adapter or canonical
  Design refresh is warranted.

Fixture success permits only a lifecycle decision about further work. It does
not permit direct canonical integration.

## Required Extension: Persistence And Concurrency

The only store is a development fixture store. It is explicitly
`none-development-fixture` authority. The Claim Simulator is its sole writer
and uses exact source-digest compare-and-set. There is no shared service,
network lock, automatic expiration, or production recovery claim.

## Required Extension: Integration And Versioning

Any future adapters would be one-way boundaries:

- Invoke candidate map -> experiment map fixture;
- Craft accepted decision snapshot -> read-only experiment projection fixture;
- experiment Way Clear receipt -> Goal eligibility evidence.

Every artifact carries a schema version. Adapter implementation is excluded
from this work pack because current Craft and Goal contracts do not carry the
candidate claim, fog, and dependency shape. Fixture proof may authorize a
separate Spellcraft-owned Invoke Design refresh; it cannot admit adapter code
directly.

## Required Extension: State And Event Semantics

State transitions require a receipt. Claims, decisions, and execution units
have different identities and histories. Reconciliation produces new proposal
events rather than erasing nodes. The causal chain is:

```text
map digest -> claim -> resolution -> reconciliation proposal -> new map digest
```

## Required Extension: Data Lifecycle

All fixture content is synthetic. Evidence may contain identifiers, hashes,
validation outcomes, and timings only. The implementation task must declare
its bounded session-evidence directory and retain no secrets, private project
prose, prompts, or user content. Cleanup is manual and repository-local for
the experiment; a reusable retention policy is deferred to lifecycle review.

## Required Extension: Validation Contracts

[WITNESS-CONTRACTS.md](WITNESS-CONTRACTS.md) is the authored acceptance
denominator. Expected values are not observed values. Validator output,
fixture receipts, and source hashes must be retained separately and bound to
exact input digests.

## Architecture Decisions

| ID | Decision | Consequence |
| --- | --- | --- |
| ADR-DFE-001 | pure projection before adapters | isolates core semantics |
| ADR-DFE-002 | reason-complete frontier output | eligibility is explainable and testable |
| ADR-DFE-003 | claim is separate from decision state | concurrency does not falsify decision history |
| ADR-DFE-004 | proposal-only reconciliation | ownership stays with Invoke/Craft |
| ADR-DFE-005 | serial layers | avoids overlapping shared-contract writes |
| ADR-DFE-006 | no tracker in the experiment | removes a competing authority path |

## Evidence Ceiling

This architecture is a selected design contract only after the official
denominator and selection validators pass. It does not establish implementation
or runtime behavior.
