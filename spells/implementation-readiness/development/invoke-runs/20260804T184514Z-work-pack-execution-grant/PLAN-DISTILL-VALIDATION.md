# Plan Distill Validation

## Objective and output

- Objective: one Work Pack execution instruction carries internal routing until
  completion or a real blocker.
- Output: a split Work Pack with eight one-behavior SWUs and owner-bound gates.
- Mode: validate, standard budget.

## Proposer / Balancer trace

- Proposer: change only Continuation Router authorization.
- Balancer: that would still let Invoke Plan advertise the wrong next route and
  Task Session discover it late.
- Reconciliation: include Plan projection and fast entry guard.
- Proposer: let Task Session dispatch and resume itself.
- Balancer: that collapses owner routing and creates recursive session risk.
- Reconciliation: make Implementation Readiness the outer loop and keep fresh
  Task Sessions.
- Proposer: create a new approval/grant receipt.
- Balancer: that recreates the ceremony the user rejected.
- Reconciliation: Work Pack policy plus direct execution intent is sufficient;
  the runtime binding is automatic audit evidence.

## Smallest coherent unit

`SWU-WPEG-001` is the smallest trust-building unit: it defines and validates
the data boundary without changing routing or mutation behavior.

## Atomicity review

- 001: one schema/validator behavior.
- 002: one Plan projection behavior.
- 003: one Router admission behavior.
- 004: one outer-loop behavior.
- 005: one Task Session entry-guard behavior.
- 006: one fresh-session resumption behavior.
- 007: one end-to-end causal proof behavior.
- 008: one packaging/parity behavior.

No SWU combines independently reviewable UI, product, runtime, deployment, or
authority changes.

## Recomposition proof

001 defines the bounded policy; 002 emits it; 003 consumes it for owner hops;
004 coordinates the hops; 005 prevents expensive wrong-owner entry; 006
resumes safely; 007 proves the resulting loop; 008 makes canonical/generated
surfaces consistent. Removing any unit leaves one acceptance criterion
unproven.

## Evolution profile

The design can later support other outer-loop owners by consuming the same
entry/binding contracts. It deliberately does not create a general policy
engine or permit dynamic scope expansion.

## Premortem

Most likely failure: the execution binding becomes a broad ambient permission.
Guardrail: require exact Work Pack semantic identity, finite frontier, declared
writes/validation, canonical allowed-routes digest, complete matched owner-route
tuple, stop classes, and live Task Session admission.

## Verdict

Pass. The plan is implementation-ready after explicit selection through the
target lifecycle owner; Plan evidence remains pending until fixtures execute.
