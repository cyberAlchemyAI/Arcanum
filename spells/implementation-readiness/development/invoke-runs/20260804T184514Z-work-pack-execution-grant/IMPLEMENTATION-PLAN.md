# Implementation Plan

## Objective

Make a direct request to run or finish an exact Work Pack sufficient to perform
its declared internal tool and capability routes, while continuing until the
captured frontier completes or a real blocker appears.

## Existing implementation to reuse

Do not rebuild these capabilities:

- Plan Semantic Manifest and `selected-unit-at-task-session` audit profile;
- selected-unit selection receipt and semantic drift checking;
- Invoke material package validation;
- Task Session live target baselines and single-use admission;
- Continuation Router owner ranking, one-hop dispatch, cycle detection, and
  joined owner receipt;
- Task Session Until Blocker finite-frontier sequencing.

## Delivery slices

### Slice A — Execution contract

Add versioned schemas and a deterministic validator for:

- `ExecutionPolicy` embedded or referenced by a Work Pack;
- `AllowedRoutesProjection` containing exact per-frontier route tuples;
- `ExecutionEntryProjection` emitted by Invoke Plan/readiness closeout;
- `ExecutionIntentBinding` produced automatically from direct execution intent.

The validator must reject:

- unknown or unbounded frontier;
- empty or escaping write scope;
- missing validation or stop classes;
- contradictory entry state and next route;
- a binding whose Work Pack semantic digest has changed;
- automatic policy that includes a stop-class effect.
- undeclared capability/mode/target, expanded write scope, changed effect
  class, missing typed input, mismatched expected receipt, or stale route
  digest.

### Slice B — Plan and readiness production

Update Invoke Plan and Work Pack Readiness Audit so:

- new plans recommend `selected-unit-at-task-session`;
- Plan outputs one execution-entry state;
- Plan outputs a canonical allowed-routes digest and exact route tuples;
- `next_route` equals the actual next owner;
- expected material absence is `selection-ready`, not Refresh drift;
- real semantic drift names Invoke Refresh;
- no Plan routes to Task Session when a prerequisite is unresolved.

### Slice C — Work-Pack-bound routing

Extend Continuation Router with two authorization sources:

1. `work-pack-binding` — enough for a matching in-scope internal owner route;
2. `ad-hoc` — retains current exact authorization behavior outside a binding.

The Router validates the complete digest-bound capability, mode, target, write,
effect, input, expected-receipt, and stop-policy tuple. It does not ask for
`--authorize-route` when all are bound by the active Work Pack.

### Slice D — Outer loop

Upgrade Implementation Readiness from a three-stage sketch to the actual
controller:

1. resolve Work Pack and series intent;
2. produce the execution intent binding;
3. classify entry;
4. run/join one owner hop as necessary;
5. invoke one fresh Task Session;
6. join closeout and select the next declared frontier unit;
7. repeat within the captured budget;
8. stop at completion or a stop-class decision.

The controller may automatically decide tools, internal routes, reversible
fallbacks, and declared retries. It records those decisions in the run receipt.

### Slice E — Fast Task Session guard

Before Context Builder:

1. read exact Work Pack identity;
2. read the execution-entry projection and current binding;
3. compare selected unit/frontier identity;
4. return `proceed`, `route-owner`, or `block`.

If `route-owner`, Task Session performs no deep context build, material audit,
or mutation admission. The outer loop consumes the result and invokes the
owner. Validate a deterministic maximum read set; report wall time only as
observability, not a portable correctness threshold.

### Slice F — Series continuation

Extend Task Session Until Blocker to accept a joined pre-execution owner receipt
and start a fresh Task Session for the same selected unit. Preserve one-hop and
one-unit receipts, cycle fingerprints, frontier bounds, and closeout joins.

### Slice G — Integration and adoption

Create a public fixture Work Pack with:

- a declared plan-once path;
- a mechanical owner prerequisite;
- one selected material-bound task;
- one successor;
- a semantic-drift negative case;
- external/destructive/authority stop cases.

Prove:

- one direct execution intent;
- no per-hop route authorization prompts;
- no pre-execution Refresh for expected material absence;
- automatic Refresh for real semantic drift;
- fresh Task Session resumption after the owner receipt;
- unchanged live mutation safety checks;
- complete generated-package sync.

## Migration

1. Land additive schemas and validator.
2. Add execution-entry output without changing legacy routing.
3. Add Work-Pack-bound Router mode while retaining ad hoc behavior.
4. Add outer loop and fast guard behind the new execution policy.
5. Run cross-capability fixtures.
6. Recommend the policy in new Invoke Work Packs.
7. Evaluate default adoption after one public-safe canary and generated parity.

## Stop conditions

Implementation stops if:

- the execution binding cannot be bounded to one Work Pack/frontier;
- the Work Pack cannot produce a closed allowed-routes projection;
- automatic policy could cover a stop-class effect;
- a capability would need to impersonate another owner;
- a route can bypass live target/validation/admission checks;
- a blocked Task Session would be recursively resumed;
- a fixture needs private consuming-project content;
- an existing unrelated dirty change overlaps a planned source target without
  an exact baseline and owner decision.

## Evidence and claim policy

Fixtures prove control flow and boundary enforcement only. A successful run
does not authorize promotion, release, deployment, or production use.
