# Stage 05 — Distill

## Objective and budget

- Target context: public Arcanum readiness and Task Session handoff.
- Output: smallest coherent contract that removes the second audit without weakening mutation admission.
- Mode: `standard`, confirmed by the approved strategy.
- Budget: one proposal track, two reduction rounds, Proposer/Balancer trace, one reconciliation.

## Round 1 — candidate boundary

**Proposer:** make readiness plan-only and leave all material checks to Task Session.

**Balancer objection — authority/safety:** a bare plan-only pass can become stale and Task Session cannot prove it is executing the audited frontier unless the pass is a structured, exact receipt.

**Reconciliation:** revise. The unit is not a status enum; it is a producer/consumer contract: selector-level `PlanSemanticManifest` plus Task Session binding and semantic-drift verification.

## Round 2 — alternatives

| Alternative | Benefit | Failure | Decision |
| --- | --- | --- | --- |
| Keep full-frontier audit and rerun after material production. | Strong current proof. | Duplicates the live Task Session gate and forces refresh choreography for expected timing. | retain as legacy strict mode |
| Produce every material package during readiness. | One passing audit. | Expensive, packages go stale before selection, and readiness acquires producer authority. | reject |
| Whole-file plan receipt plus selected-unit live admission. | Simple exact binding. | Normal closeout changes whole Work Pack/handoff bytes and recreates audit churn. | reject |
| Selector-semantic manifest plus selected-unit live admission. | One reusable plan proof across status-only closeouts and one current mutation proof. | Requires canonical selector normalization and cross-capability digest fixtures. | select |

**Balancer objection — compatibility:** changing v1 meanings in place can break consumers.

**Reconciliation:** use an additive opt-in profile and versioned receipt schema; existing strict behavior is the default.

## Smallest coherent unit

**Two-phase semantic readiness bridge**: one audit-owned semantic manifest and one Task Session consumer check. Splitting the manifest from its consumer would either create an unused artifact or an ungrounded execution check, so both sides form one coherent behavior.

## Recomposition proof

The bridge recomposes into the existing lifecycle without changing owners:

`Invoke Plan → Work Pack Readiness(plan-then-admit) → explicit selection → material producer → Task Session live admission → bounded mutation → existing Invoke Refresh closeout`.

## Evolution and deferred complexity

- Evolution pressure: future execution owners may consume the same receipt.
- Minimal extension boundary: a public versioned receipt schema and explicit consumer validation.
- Deferred: v2 objective-execution projection alignment, automatic producer routing, and multi-unit epochs.

## Premortem

Likely failure: a consumer treats `runtime-pending` as mutation-ready or treats a whole-file status change as semantic drift. Guardrails: manifest constants, selector-value digests, separate status/lifecycle namespaces, Task Session schema requirements, and negative mutation-without-admission plus status-only-change fixtures.

## Verdict

`pass`, subject to the independent Balancer receipt and repair-stage counterexample closure.
