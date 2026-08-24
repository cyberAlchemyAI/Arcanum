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
Every stage invocation must also carry the exact normalized execution-
projection path in its argument vector or fixed environment. A manifest-only
projection reference does not prove that the consumer used the finalized
projection.

The stage-to-consumer relation is canonical and closed:

| Stage | Canonical consumer |
| --- | --- |
| Invoke material validation | `arcanum/spells/invoke/scripts/material_package_validator.py` |
| Invoke file-bound handoff | `arcanum/spells/invoke/scripts/refresh_material_handoff.py` |
| Work Pack Readiness | `arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py` |
| Task Session Until Blocker preflight | `arcanum/spells/task-session-until-blocker/scripts/run_chain.py` |
| Task Session fast entry | `arcanum/arcana/task-session/scripts/fast_execution_entry_guard.py` |
| Task Session mutation admission | `arcanum/arcana/task-session/scripts/verify-mutation-readiness.py` |
| Task Session governance runner | Exact normalized runner: canonical source, `.agents`, or `.claude` Task Session package |
| precloseout | `arcanum/arcana/task-session/scripts/plan-once-material-controller.py` |
| Invoke closeout | `arcanum/spells/invoke/schemas/precloseout-refresh-closeout-receipt.schema.json` |
| Task Session terminalization | `arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json` |
| continuity | `arcanum/arcana/continuation-router/scripts/work_pack_route.py` |

Executable consumers run directly except for the Task Session governance
runner's generic prepare regression and the two JSON-schema consumers whose
exact bytes cannot execute themselves. The deterministic adapter binds its
own exact bytes, the real consumer, the exact normalized projection, and the
stage-specific invocation. For governance it executes the real runner's
projection-bound request inside an isolated repository, requires `ticketed`
with the exact selected-route partition in ticket provenance, verifies that
the admission remains unconsumed and every route path is unchanged, and stops
before executor launch. For the schema stages it loads and schema-checks the
consumer. A generic, no-op, consumer-ignoring, or unbound adapter blocks.
The three governance runner paths form a closed deployment-surface set. The
exercised exact ref must still equal the normalized runner ref; hash equality
between a different path is not accepted as an identity substitution.

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

For a mutation-capable Work Pack, the normalized projection also binds one
typed Task Session closeout contract. It includes the byte-current precloseout,
Invoke owner, final terminal, continuity, and Continuation Router schema refs,
plus the declared Invoke owner-receipt identity. A legacy flat closeout binding
is read-only historical compatibility; it cannot satisfy this gate.

The public integration fixture constructs the real Task Session governance
request, reaches the runner's no-mutation `prepare`/`ticketed` boundary, checks
that the exact closeout contract survives into the ticket, validates a
project-local-path Invoke owner receipt, and runs the installed precloseout,
terminal, and continuity contract validators.

## Request-emission gate

`emit-request` is the only v2 request-generation operation. It requires a
passing closure receipt, a passing independent-review receipt, and an adoption
receipt whose cross-capability regression passed. All four artifacts must bind
the same manifest and closure-graph digest. The output is exclusively created;
an existing request is never overwritten.

Before any new or regenerated mutation-capable request is presented, the
ordinary Invoke path must run `validate-request` over the emitted artifact.
That validator admits only the v2 schema and rechecks the passing closure,
independent-review, and adoption bindings. A direct base request, historical v1
request, or hand-authored wrapper is not an alternate emission path.

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
