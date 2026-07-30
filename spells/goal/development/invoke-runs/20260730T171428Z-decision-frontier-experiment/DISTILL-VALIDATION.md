# Plan Distill Validation

## Intent And Budget

- Intent: reduce the decision-frontier experiment into independently
  acceptable units without losing authority or decision/execution boundaries.
- Budget: Standard, assumed because no explicit budget was supplied.
- Role execution: local Proposer/Balancer simulation.
- Delegation: no role fan-out; repository policy requires an approved governed
  dispatch for multiple agents.
- Selection authority: none.

## Proposer Pass

The smallest first proposal was:

> Freeze the candidate schemas, graph invariants, synthetic maps, and
> fail-closed validator before any reducer or stateful behavior exists.

## Balancer Pass

| Pressure | Objection | Disposition |
| --- | --- | --- |
| coherence | schemas without cycle/endpoint mutants are decorative | retain validators and negative fixtures in SWU-DFE-001 |
| atomicity | reducer, claims, reconciliation, HITL, Way Clear, and non-collapse have independently acceptable effects | keep them in separate serial SWUs |
| authority | adapters imply shapes absent from current Craft and Goal contracts | defer all adapter code to a later lifecycle Design refresh |
| human control | automated flow could consume HITL decisions | require an explicit stop witness |
| evidence | deterministic bytes do not prove workflow improvement | defer benefit claim to a later paired experiment |
| closure | decision completion could leak into work status | dedicate DFE-FIX-008 and independent closure |

## Atomicity Result

Seven mutation SWUs remain, each with one primary behavior:

1. validate contracts and graph shape;
2. derive a reason-complete frontier;
3. enforce digest-bound claims;
4. stage reconciliation proposals;
5. enforce the HITL stop;
6. evaluate the strict Way Clear predicate;
7. prove decision closure leaves execution state unchanged.

Two closure-only units reconcile evidence and make a lifecycle decision.

## Implementation Detail Closure

Every mutation task links one execution-detail spec:

- `work-pack/details/CONTRACT.md`;
- `work-pack/details/REDUCER.md`;
- `work-pack/details/CLAIM.md`;
- `work-pack/details/RECONCILE.md`;
- `work-pack/details/BOUNDARY.md`.

Together they define purpose, inputs/outputs, state, stepwise algorithms,
precedence and transition rules, edge cases, failures, and acceptance evidence.
Claim compare-and-set and typed reconciliation actions are no longer deferred
implementation decisions.

## Narrow-First Result

- First candidate: SWU-DFE-001.
- Reversible: yes; development-only schemas, fixtures, and validator.
- Trust gained: malformed graphs cannot reach the reducer.
- Deferred: reducer, claims, reconciliation, adapters, workflow comparison,
  and canonical changes.
- Selected: no.
- Verdict: pass.

## Recomposition Proof

[TRACEABILITY.md](work-pack/shared/TRACEABILITY.md) maps every functional
requirement, invariant, architecture extension, and witness to a unit.

```text
closed contract
  -> pure frontier
  -> claim control
  -> reconciliation
  -> HITL stop
  -> Way Clear
  -> execution non-collapse
  -> independent closure
  -> lifecycle decision
```

Removing any mutation unit leaves at least one named behavior unproved.

## Deferred Complexity

- issue tracker projection and all Invoke/Craft/Goal adapter code;
- distributed leases, expiry, crash recovery, and multi-process locking;
- canonical Craft representation;
- model-backed AFK resolution;
- UI or operator console;
- workflow-benefit thresholds;
- publication, deployment, and production readiness.

## Cycle And Premortem

- Recursive split rounds: 2.
- Cycle guard: no child unit expands back into its parent.
- Highest risks: false frontier eligibility, stale claim admission, hidden
  canonical mutation, HITL bypass, and decision/task collapse.
- Each risk has a negative witness or lifecycle gate.

## Verdict

- Status: pass.
- Blocking planning gaps: none.
- Mutation authorization: none.
- Evidence ceiling: Plan structure and recomposition only.
- Next owner: Spellcraft.
- Child run: `distill-20260730T171429Z-goal-decision-frontier-plan`.
- Runtime evidence: partial because the validated run used local role
  simulation; central telemetry line 442.
- Telemetry residue: the generated Invoke child wrapper resolved a nonexistent
  `.agents/framework` runtime path; the canonical observer recorded the already
  validated envelope directly.
