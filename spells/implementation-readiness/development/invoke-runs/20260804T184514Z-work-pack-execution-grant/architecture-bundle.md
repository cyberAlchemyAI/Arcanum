# Architecture Bundle

## View 1 — Context

The user interacts with one outer-loop surface: `implementation-readiness`.
The Work Pack describes what may be done, how far the loop may progress, which
owners/tools may be used, and what must stop. Internal capabilities remain
separate owners behind that surface.

```text
direct execution intent + exact Work Pack
                  |
                  v
       implementation-readiness
         /        |          \
   readiness   owner hops   task sessions
      audit       router       one unit
```

## View 2 — High-level structure

1. **Plan producer** — Invoke Plan emits a coherent Work Pack, Plan Semantic
   Manifest profile, execution policy, and execution-entry projection.
2. **Outer-loop controller** — Implementation Readiness binds execution intent,
   classifies decisions, invokes owners, and stops only on declared boundaries.
3. **Plan readiness owner** — Work Pack Readiness Audit proves semantic plan
   identity and ready frontier without requiring future material.
4. **One-hop router** — Continuation Router invokes one declared owner and joins
   the receipt. A Work-Pack binding replaces per-route authorization.
5. **Unit executor** — Task Session performs a cheap entry guard, then owns one
   admitted unit and its live validation.
6. **Series controller** — Task Session Until Blocker advances across fresh
   unit sessions when series intent is present.

## View 3 — Low-level components

| Component | Input | Output | Key rule |
| --- | --- | --- | --- |
| `ExecutionPolicy` | Plan decisions and risk boundaries | automatic/stop decision classes | embedded in Work Pack |
| `ExecutionEntryProjection` | plan readiness and prerequisite state | one exact entry state and owner | cannot contradict `next_route` |
| `AllowedRoutesProjection` | exact plan owner edges | digest-bound capability/mode/target/scope/effect/input/receipt tuples | route membership, not user approval |
| `ExecutionIntentBinding` | direct execution request + Work Pack and allowed-route digests | bounded run evidence | created automatically, no user ceremony |
| Fast prerequisite guard | entry projection + current identity | `proceed`, `route-owner`, or `block` | runs before full context build |
| Router grant matcher | intent binding + candidate owner route | `matched`, `outside-scope`, or `ad-hoc` | no exact route prompt for matched routes |
| Outer-loop reducer | owner and Task Session receipts | continue/stop decision | one hop/session at a time |
| Decision classifier | proposed action + policy | automatic or stop | tool choice is automatic by default |

## View 4 — Workflow process

```text
1. Resolve exact Work Pack and direct execution intent.
2. Bind intent to Work Pack semantic identity and finite frontier.
3. Read the execution-entry projection.
4. If semantic audit is needed, run its owner and join the receipt.
5. If selection/material production is needed, run declared owners and join.
6. Start one fresh Task Session for the selected unit.
7. Validate and close the unit through existing owner closeout.
8. If series intent and one successor exists, repeat from step 3.
9. Stop on frontier completion or a stop-class decision.
```

No step asks for authorization merely because it calls a different internal
tool or capability.

## View 5 — Decision and state flow

```text
unbound
  -> bound-to-work-pack
  -> entry-classified
       -> owner-prerequisite -> owner-receipt-joined -> entry-classified
       -> selection-ready    -> selected/materialized -> task-ready
       -> task-ready         -> one-unit-running -> unit-closed
       -> blocked            -> user/owner decision
  -> frontier-complete
```

Transitions are automatic when they preserve the Work Pack identity, frontier,
allowed-route digest, scope, owner contract, and safety class. A changed
semantic plan or frontier starts a new binding; a changed interchangeable tool
implementation inside one declared interface does not.

## View 6 — Dependency and interface

| Producer | Consumer | Interface |
| --- | --- | --- |
| Invoke Plan | Implementation Readiness | Work Pack, execution policy, entry projection, semantic-manifest route |
| Work Pack Readiness Audit | Implementation Readiness | Plan Semantic Manifest and ready frontier |
| Implementation Readiness | Continuation Router | execution binding, exact owner inputs, expected receipt |
| Continuation Router | owner capability | one bounded owner invocation |
| owner capability | Implementation Readiness | joined terminal owner receipt and returned route |
| Implementation Readiness | Task Session | selected unit, strict execution contract, current material/admission evidence |
| Task Session | series controller | terminal receipt, closeout receipt, unique successor |

## Authority and safety split

| Concern | Owner |
| --- | --- |
| Plan meaning and declared scope | Invoke/Work Pack owner |
| User-facing loop and decision class | Implementation Readiness |
| Semantic readiness | Work Pack Readiness Audit |
| One owner handoff and receipt join | Continuation Router |
| One unit's mutation and validation | Task Session |
| Finite series progression | Task Session Until Blocker |
| Product/authority/external decision | user or named lifecycle owner |

The execution binding permits action only inside already-declared Work Pack
semantics. It cannot promote evidence, expand scope, weaken validation, or turn
an internal route into an external side effect.

## Failure and recovery

| Failure | Response |
| --- | --- |
| Missing or stale execution-entry projection | rebuild through Invoke Plan or readiness owner; no Task Session deep audit |
| Real semantic plan drift | automatic Invoke Refresh owner hop; join and reclassify |
| Missing selected-unit material | run declared producer; do not rerun semantic audit |
| Owner receipt blocks | stop with its smallest unblock action |
| Route not declared by Work Pack | classify against decision policy; stop if scope/meaning changes |
| Target, write, effect, input, or receipt tuple mismatch | block as outside the bound route |
| Stale or replayed binding after semantic/frontier change | invalidate and create a new binding from current direct intent |
| Target baseline or validation drift | Task Session blocks before mutation |
| Repeated owner/session fingerprint | cycle block |
| External/destructive/authority action | stop and request the real decision |

## Migration and rollout decisions

- Preserve strict legacy readiness profiles.
- Recommend `selected-unit-at-task-session` for newly authored Work Packs.
- Add the fast guard before changing default outer-loop behavior.
- Keep ad hoc Router authorization for unbound continuations during migration.
- Introduce fixture-backed deprecation of per-hop authorization only for
  Work-Pack-bound routes.
- Do not make the new profile the universal default until current canonical and
  generated-package parity passes.

## Design risks

- A vague Work Pack could become an overly broad execution grant. Mitigation:
  refuse binding without finite frontier, normalized writes, validation, and
  stop policy.
- Dynamic routing could hide a product choice. Mitigation: decision classifier
  distinguishes tool mechanics from semantic outcome.
- The outer loop could recurse forever. Mitigation: one-hop joins, stable
  fingerprints, finite budget, and no recursive Task Session.
- Exact route authorization removal could weaken ad hoc safety. Mitigation:
  remove it only when a current Work-Pack binding matches the complete
  digest-bound allowed-route tuple.
- Performance claims could become wall-clock fragile. Mitigation: validate a
  deterministic read/phase budget and separately report observed duration.

## Design evidence ceiling

Authored design only until deterministic Design selection, implementation, and
fixtures return their own receipts.
