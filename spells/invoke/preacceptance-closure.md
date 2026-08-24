# Invoke Preacceptance Closure

## Purpose

`preacceptance-closure` is the Spellcraft-owned admission boundary for an
Invoke owner-acceptance request. It proves that finalized staged bytes can be
consumed by the declared downstream capability chain before the request is
shown to an owner.

It does not accept a candidate, apply a postimage, authorize Task Session,
advance a lifecycle state, publish, or create an external effect. Exact owner
acceptance remains a separate final decision.

## Canonical contracts

- `schemas/preacceptance-closure-manifest-v1.schema.json`
- `schemas/preacceptance-closure-receipt-v1.schema.json`
- `schemas/preacceptance-closure-review-v1.schema.json`
- `schemas/preacceptance-closure-adoption-v1.schema.json`
- `schemas/owner-acceptance-request-v2.schema.json`
- `scripts/preacceptance_closure.py`

## Required closure

One manifest binds final postimages and their live baselines, one normalized
execution projection, exact runner bytes and invocation, schema and locator
identities, disjoint write partitions, admitted frontier, routes, one-request
budget, risk ceiling, runtime-receipt derivation rules, requested effect, and
one reflection-adoption receipt.

Each stage binds both its executable test driver and the downstream runner it
actually exercises. Indirect harnesses must pass that exercised-runner path in
the argument vector or fixed environment; inherited environment alone is not
an identity binding. Required fixture, schema, family, and environment values
are part of the invocation digest, and a missing value must stop at that stage.

The deterministic runner executes these real consumer boundaries in order:

1. Invoke material validation;
2. Invoke file-bound handoff;
3. Work Pack Readiness;
4. Task Session Until Blocker preflight;
5. Task Session fast entry;
6. Task Session mutation admission;
7. Task Session governance runner;
8. precloseout;
9. Invoke closeout;
10. Task Session terminalization; and
11. continuity.

The complete rehearsal runs twice in separate temporary roots. Any skipped,
reordered, identity-mismatched, schema-invalid, non-deterministic, or
repository-mutating stage blocks. Protected inputs and repository state must
remain byte-identical.

## Request-emission gate

`emit-request` is the only v2 request-generation operation. It requires a
passing closure receipt, a passing independent-review receipt, and an adoption
receipt whose cross-capability regression passed. All four artifacts must bind
the same manifest and closure-graph digest. The output is exclusively created;
an existing request is never overwritten.

An emitted request remains `authority_effect: none`. It asks the lifecycle
owner for a decision; it is not that decision.

## Compatibility

Historical v1 requests remain readable historical records. They do not become
v2 closure evidence and cannot be reinterpreted as request-emission-ready.
New or regenerated exact owner requests use the v2 wrapper. A semantic, owner,
target, postimage, runner, route, write, budget, risk, schema, or successor
change invalidates the closure and requires a fresh manifest, rehearsal,
independent review, and request.

## Ownership and exclusions

Spellcraft owns admission of this cross-capability closure for the Invoke
spell. Invoke, WPRA, Task Session Until Blocker, Task Session, Continuation
Router, validators, Inventory, observability, projections, status files, and
cursors may submit evidence but cannot admit the closure independently.

No mutable current-state projection is introduced. The manifest and receipts
are immutable evidence. Public fixtures are synthetic and project-agnostic.
