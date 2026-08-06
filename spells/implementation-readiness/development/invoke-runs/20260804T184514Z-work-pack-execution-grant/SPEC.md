# Specification: Work-Pack Execution Grant

## Purpose

Provide a zero-surprise entry from an approved Work Pack to implementation.
The operator authorizes the Work Pack once by directly requesting execution.
The runtime may then choose and invoke the internal owners and tools necessary
to perform that plan, inside the plan's declared scope and stop policy.

## Primary behavior

Given:

1. one exact Work Pack;
2. a direct execution intent such as `run`, `finish`, `continue`, `one go`, or
   `until blocker`;
3. a finite plan frontier, declared owners, write scopes, validation, and stop
   conditions;

the system binds the intent to the current Work Pack semantic identity and
automatically performs in-scope route/tool decisions until:

- the selected frontier completes; or
- a real blocker or stop class is reached.

## Work Pack execution policy

Every execution-ready Work Pack exposes a machine-readable policy with:

```yaml
execution_policy:
  route_policy: automatic-in-scope
  allowed_routes:
    - capability: <installed owner id>
      mode: <owner mode>
      target: <exact target or selector>
      write_scope: [<normalized paths>]
      effect_class: repository-local-reversible
      required_inputs: [<typed input refs>]
      expected_receipt: <receipt contract ref>
  automatic_decisions:
    - internal-tool-selection
    - capability-owner-routing
    - reversible-local-default
    - declared-fallback
    - declared-retry
    - fresh-task-session-resumption
  stop_decisions:
    - product-or-semantic-choice
    - scope-expansion
    - destructive-or-irreversible-effect
    - credentials-or-secret-access
    - external-message-or-network-effect
    - cost-policy-or-risk-acceptance
    - authority-promotion-publication-deployment
    - failed-acceptance-critical-validation
  scope_source: exact-work-pack-and-selected-frontier
  validation_policy: owner-gates-remain-mandatory
```

This is policy embedded in the plan, not another approval receipt that the
operator must create.

`allowed_routes` is the execution graph, not a menu of approvals. Its canonical
digest is part of the Work Pack semantic identity. Mechanical tool selection
may vary inside a route's declared interface, but capability, mode, target,
write scope, effect class, required inputs, and receipt contract may not expand.

## Execution intent binding

At runtime, the outer-loop owner records an `ExecutionIntentBinding` derived
from the direct request. It contains:

- Work Pack ID and semantic digest;
- captured frontier and current selected unit;
- declared write-scope union and validation surface;
- execution mode (`one-unit`, `finite-frontier`, or `until-real-blocker`);
- automatic and stop decision classes from the Work Pack;
- the canonical `allowed_routes_digest` and exact route tuple for the current
  frontier unit;
- source invocation identity and timestamp;
- `authority_effect: bounded-execution-only`.

The binding is audit evidence produced automatically. It is not a second user
approval gate.

## Execution-entry states

An Invoke Plan must emit exactly one of these states:

| State | Meaning | Next owner |
| --- | --- | --- |
| `selection-ready` | Plan semantic manifest is current; material is intentionally produced for the selected unit later. | `implementation-readiness` |
| `owner-prerequisite` | A named owner must repair or materialize a declared prerequisite before selection/admission. | exact owner route |
| `task-ready` | Exact selected unit and current mutation inputs are available. | `task-session` through the outer loop |
| `blocked` | A real plan, scope, semantic, safety, or authority decision is unresolved. | named blocker owner or user |

The Plan must not say `task-session` while also declaring a prerequisite owner
that has not run.

## Decision classes

### Automatic

- choosing an installed internal tool that satisfies a declared interface;
- routing to Invoke, Work Pack Readiness Audit, Continuation Router, Task
  Session, or another owner whose exact tuple is present in `allowed_routes`;
- selecting a reversible local default when the Work Pack names the fallback;
- rebuilding stale generated evidence inside declared output paths;
- retrying once after an owner returns a typed, repairable, in-scope condition;
- resuming a fresh Task Session after a joined prerequisite receipt.

Automatic decisions are recorded in the run receipt, but do not interrupt the
user.

### Stop and ask

- two product behaviors are both valid and the Work Pack does not choose;
- the route requires paths, targets, costs, systems, or actors outside the
  Work Pack;
- destructive or difficult-to-recover mutation;
- credentials, secrets, external communication, non-loopback network effects,
  payment, publication, promotion, deployment, or release;
- accepting a failed acceptance-critical validation;
- changing lifecycle or authority policy;
- ambiguity that changes the intended result rather than merely the tool used.

## Owner rules

- `implementation-readiness` owns the outer loop, execution-intent binding,
  stop classification, and user-facing synthesis.
- Invoke owns Plan/Refresh artifacts and material-package semantics.
- Work Pack Readiness Audit owns semantic-plan readiness projection.
- Continuation Router owns one-hop route ranking, dispatch, and owner receipt
  joining.
- Task Session owns exactly one selected unit, live mutation admission,
  execution, validation, and closeout.
- `task-session-until-blocker` owns finite successor progression when the user
  requests a series.
- No owner may claim another owner's work as its own.

## Compatibility

- New Work Packs use `selected-unit-at-task-session` unless their plan requires
  full-frontier materialization for a named reason.
- Existing strict Work Packs keep their current semantics.
- A legacy pack with a clearly declared prerequisite is classified before
  Context Builder runs and routed immediately.
- Ad hoc Continuation Router calls outside a bound Work Pack may retain exact
  route authorization.
- Generated Codex and Claude mirrors continue to derive from canonical Arcanum
  sources.

## Acceptance

1. A direct `run this Work Pack` request causes no per-tool or per-owner
   authorization prompt for declared, local, reversible work.
2. A plan-declared prerequisite is identified before full context building.
3. A plan-once Work Pack reaches selected-unit admission without a
   pre-execution Refresh.
4. A real semantic drift routes to Invoke Refresh automatically and resumes
   only after a passing joined owner receipt.
5. Task Session still validates exact live targets, baselines, validation
   contracts, and single-use admission before mutation.
6. The outer loop performs one owner hop at a time and uses a fresh Task
   Session; it never recursively re-enters a blocked session.
7. Product choices, scope expansion, destructive/external effects, authority,
   promotion, publication, deployment, and failed critical validation stop.
8. The fast prerequisite path reads only execution-entry evidence and emits a
   route decision before expensive context construction.
9. Legacy ad hoc routing remains fail-closed.
10. Public fixtures contain no consuming-project names or private content.
11. An undeclared capability/mode/target tuple, expanded write scope, changed
    effect class, missing required input, or mismatched receipt contract blocks.
12. A Work Pack semantic/frontier change invalidates the binding before reuse.
13. Repeated owner/session fingerprints cycle-block without recursive dispatch.
14. A declared `REPAIRABLE_OWNER_CONDITION` retries the unchanged owner route
    once within the normal step budget, preserves replay history, requires no
    prompt, and blocks a second retry before another dispatch.

## Claim ceiling

Passing fixtures will prove local deterministic routing, binding, and boundary
enforcement. They will not prove release, deployment, promotion, or correctness
of a consuming project's implementation.
