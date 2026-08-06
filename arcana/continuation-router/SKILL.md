---
name: continuation-router
description: "Use when: a terminal capability receipt, typed pre-execution prerequisite, or current Work-Pack execution binding names one next owner route and the caller needs exact admission checks, one bounded dispatch, and a joined owner receipt without owner impersonation."
argument-hint: "--receipt <path> [--work-pack-request <path> | --authorize-route <capability>:<mode>[:<mutation-mode>]] [--dispatch] [--dry-run] [--output <path>]"
tier: arcana
domain: continuation-routing
version: 0.2.0
origin: extracted from repeated Task Session terminal receipts whose next-owner advice was not consumed
allowed-tools: Read, Write, Glob, Grep, Task, Bash
---

# Sigil: Continuation Router

<objective>
Turn one source receipt into an auditable one-hop continuation: expose one to three probable owner routes, admit one route through either exact ad hoc authorization or a validated current Work-Pack execution binding, dispatch at most one owner, join its terminal receipt, and return the next route without performing the owner's mutation itself.
</objective>

<logic-type>
Arcana: bounded cross-capability routing with explicit authorization, owner isolation, receipt joining, and cycle prevention.
</logic-type>

<flags>
- `--receipt <path>`: load the terminal source receipt to normalize and route.
- `--work-pack-request <path>`: validate the current execution policy, entry, binding, exact candidate, installed owner route, available inputs, and consumed fingerprints. A passing request is the authorization source for that one declared route and never requires `--authorize-route`.
- `--authorize-route <capability>:<mode>[:<mutation-mode>]`: grant only the exact route tuple named by the caller. It does not grant any other mode, target, write scope, destructive action, cost, or nested continuation.
- `--dispatch`: execute one selected route after all route and owner gates pass.
- `--dry-run`: return probable routes and selection reasoning without dispatch.
- `--output <path>`: persist the human result and adjacent machine route receipt when the runtime supports it.
</flags>

<applicability>
Use this sigil when:

- a completed, blocked, or flagged capability run produced a terminal receipt,
- a current Work-Pack execution entry and binding declare exactly one internal owner hop,
- Task Session produced a typed `pre-execution-prerequisite` classifier receipt
  before Context Builder and needs one exact owner hop returned to the same
  attempt,
- the receipt names a next capability or contains enough evidence to rank probable owners,
- repeating the source capability would reproduce an unchanged blocker,
- the caller wants the next owner route made visible before any dispatch,
- one bounded owner handoff is sufficient.
</applicability>

<non-applicability>
Do not use this sigil when:

- no terminal receipt or equivalent evidence exists,
- the request is a broad multi-node Craft objective that belongs to `goal`,
- the target is still vague and needs `refine` or Invoke authoring,
- a human choice must be resolved by `decision-gate`,
- several independent routes should run in parallel,
- the caller expects recursive autonomous continuation.
</non-applicability>

<inputs>
Required:

- terminal receipt or equivalent structured run evidence,
- source capability, mode, result, target scope, blockers or residues, and next-route advice when present,
- installed capability catalog or canonical registry evidence,
- current caller intent.

Required for dispatch:

- exact selected capability and mode,
- all inputs required by the selected owner,
- exact target and write scope for a mutating route,
- either exact ad hoc route authorization or a passing current Work-Pack route-admission receipt when the owner mode is consequential,
- expected terminal receipt shape,
- bounded runtime or helper lifecycle that can be joined.

For the `pre-execution-prerequisite` source phase, also require the typed
classifier receipt; task, SWU, and attempt identities; prerequisite fingerprint;
target-inventory and validation-contract digests; declared satisfaction
predicate; `max_owner_hops=1`; and `resume_point=task-session:context-build`.
Authorization must bind all of those controls and the exact owner route. A bare
Work-Pack declaration or route string is never authorization evidence. A
schema-valid current `ExecutionIntentBinding` is sufficient only after
`scripts/admit-work-pack-route.py` matches the Work Pack ID and semantic digest,
frontier unit, allowed-routes digest, owner, target, write scope, effect, required
inputs, receipt contract, installed owner, and unused route fingerprint.
</inputs>

<route-catalog>
Use installed contracts as authority. These are common candidates, not hardcoded permission:

| Evidence pattern | Probable owner route | Dispatch gate |
| --- | --- | --- |
| Planning artifact drift, contradictory work-pack state, or post-run plan synchronization | `invoke:refresh` | `proposal-only` by default; `apply-approved` only with exact authorization plus target inventory, delta scope, and validation. |
| Consequential unresolved human choice | `decision-gate:blocker` | Never auto-select a consequential option from route confidence alone. |
| Exactly one dependency-ready task or SWU | `task-session:execute` | Fresh context pack and no unchanged blocker fingerprint. |
| Vague target, unclear concept boundary, or missing design convergence | `refine:standard` or an Invoke authoring mode | No target mutation through the router. |
| Broad Craft-backed graph with several dependent nodes | `goal:execute` | Goal approval, graph frontier, and staged-delta rules apply. |
| Missing evidence, unavailable owner, or unsafe scope | `stop:user-input` | Return the exact unblock evidence; do not dispatch. |
</route-catalog>

<process>
## Step 0 - Gate The Source Phase

0. Distinguish `terminal` routing from the typed
   `pre-execution-prerequisite` phase. Legacy terminal receipts retain the
   existing conservative adapter; they never become prerequisite authorization.
1. For a prerequisite phase, validate the classifier receipt and require one
   task, SWU, attempt, fingerprint, target-inventory digest,
   validation-contract digest, owner route, satisfaction predicate, one-hop
   budget, and Context Builder resume point.
2. Compare any supplied authorization to that complete tuple. Missing or
   mismatched authorization blocks before owner dispatch. Ambiguous or unknown
   owners also block without confidence-based selection.
3. Refuse a consumed attempt/fingerprint pair. A prerequisite invocation may
   dispatch and join at most once and may not route recursively.

## Step 1 - Normalize The Source Receipt

1. Read the terminal receipt and preserve its source path.
2. Normalize source capability, mode, result, target scope, blocker class, residues, explicit next route, and required unblock actions.
3. Compute a stable blocker fingerprint from the source capability, source mode, target scope, blocker class, controlling evidence identities or digests, and requested continuation.
4. If required receipt fields are missing, adapt legacy text conservatively and mark inferred fields. Never infer apply authorization.

## Step 2 - Detect Repeated Or Cyclic Continuation

5. Compare the blocker fingerprint with any supplied previous continuation receipt.
6. If the same fingerprint would re-enter the same source capability and mode, reject that candidate.
7. If the route history already contains the same capability, mode, target, and fingerprint tuple, return `BLOCK` with `cycle-detected`.
8. Limit one invocation to one owner dispatch. A returned next route is reported, not recursively executed.

## Step 3 - Build Probable Routes

9. Resolve candidate owners from, in order: an explicit receipt handoff, an owner-defined downstream contract, installed capability evidence, then semantic fit.
10. Normalize route aliases, such as `invoke-refresh`, to a capability and mode tuple such as `invoke:refresh`.
11. Rank one to three candidates by controlling evidence, owner fit, required-input completeness, authorization state, mutation risk, and expected receipt strength.
12. For each candidate record capability, mode, optional mutation mode, owner, evidence, required and missing inputs, mutation risk, approval requirement, authorization state, expected receipt, and fallback.
13. Show probable routes before selection or dispatch.

## Step 4 - Select And Gate One Route

14. Select one candidate only when its evidence is unambiguous and all required inputs are present.
15. Choose exactly one authorization source:
    - In ad hoc mode, treat `--authorize-route` as an exact tuple. A grant for `invoke:refresh:apply-approved` does not authorize Task Session execution, a different target, a broader write scope, or another hop.
    - In Work-Pack mode, validate the self-contained route request through `scripts/admit-work-pack-route.py`. A passing `work-pack-binding` admission authorizes only its exact current route without another prompt. A mismatch blocks; it never falls back to asking for an authorization flag.
16. Refuse an undeclared or ambiguous route, unknown owner, stale policy/entry/binding, expanded target or write scope, changed effect, missing input, changed receipt contract, protected effect, or consumed fingerprint.
17. For a consequential or mutating route, require the owner contract's own inventory, scope, validation, and effect gates in addition to route admission. Work-Pack admission selects the declared owner; it does not waive owner validation.
18. If ad hoc authorization is missing, return the ranked routes with selection status `not-authorized`; do not dispatch. If a Work-Pack admission blocks, return its stable blocker code; do not request per-route authorization.
19. If candidates remain ambiguous, return selection status `ambiguous`; do not choose from ranking score alone.

## Step 5 - Dispatch Through The Owner

20. When `--dispatch` is set and the selected route passes, invoke the canonical owner capability through the native runtime surface.
21. Prefer one bounded helper or subagent when isolation is available; otherwise invoke inline with the same route packet and receipt contract.
22. Pass only the selected target, required inputs, exact authorization or binding evidence, declared write scope, and validation surface.
23. The router must not edit owner target artifacts, reinterpret owner gates, or report owner work as router work.
24. Join the helper and require a separate terminal owner receipt. An open, hidden, timed-out-without-residue, or unjoined helper is `BLOCK`.

## Step 6 - Return The Joined Result

25. Validate the owner receipt against the expected receipt shape and selected route tuple.
26. Preserve the source result; a successful continuation does not rewrite the source `BLOCK` as Task Session success.
27. Return continuation status, selected owner route, owner receipt, mutations attributed to the owner, validation, and the owner's returned next route.
28. Persist a machine receipt conforming to the applicable continuation-route schema when an output path is requested or repository conventions require durable evidence.
29. For `pre-execution-prerequisite`, persist against
    `schemas/continuation-route.schema.json`, keep router-authored mutations
    empty, and return a typed control handle to the same Task Session attempt at
    `task-session:context-build`. The owner receipt remains separately
    attributed to the owner. Do not return `task-session:execute` as a recursive
    next route.
</process>

<authority-rule>
The router owns route ranking, exact ad hoc authorization or Work-Pack binding admission, bounded dispatch, and receipt joining. It never owns the selected capability's semantic work or mutation. A route string is evidence of destination, not authority to mutate; only a fully validated current binding may substitute for a second authorization prompt.
</authority-rule>

<observability>
A meaningful execution is a terminal receipt that produces ranked routes, a route selection, a dispatch attempt, or an owner receipt.

Emit:

- source capability, mode, result, receipt, and blocker fingerprint,
- candidate count and ranked capability/mode tuples,
- authorization source, prompt requirement, binding admission, or exact-route match,
- selection status and rejection reasons,
- dispatch status and runtime isolation,
- helper spawned, joined, closed, blocked, timed out, and open counts,
- owner receipt path and validation,
- returned next route,
- cycle detection and owner-boundary violations,
- quality-bar status, anti-pattern hits, workflow gaps, and reflection trigger.

Reflect after five meaningful executions, three related routing gaps, or immediately after unauthorized dispatch, repeated-route cycling, direct owner mutation, or an unjoined helper.
</observability>

<quality-bar>
A successful execution must:

- consume exactly one terminal source receipt,
- preserve the source result and owner boundaries,
- compute and expose a stable blocker fingerprint,
- return one to three probable routes before dispatch,
- identify capability, mode, owner, evidence, inputs, approval, risk, and expected receipt for every candidate,
- dispatch at most one route,
- distinguish terminal routing from `pre-execution-prerequisite` routing,
- bind prerequisite authorization to route, task, SWU, attempt, fingerprint,
  target inventory, validation contracts, resume point, hop budget, and allowed
  effect,
- require either an exact ad hoc authorization tuple or a validated current Work-Pack binding for consequential owner modes,
- prove Work-Pack-bound route identity, frontier, owner, target, write scope, effect, required inputs, expected receipt, digest freshness, and unused fingerprint before dispatch,
- run the selected owner's own gates without weakening them,
- prevent unchanged source re-entry and repeated route cycles,
- join a separate terminal owner receipt,
- return the owner's next route without recursively executing it,
- return prerequisite control only to the same Task Session attempt at Context
  Builder, never selector resolution or a new Task Session,
- emit a schema-valid machine receipt when persisted,
- keep public examples product-neutral.
</quality-bar>

<anti-patterns>
Avoid:

- treating free-text `next_route` as mutation approval,
- treating a Work-Pack declaration, route string, or unvalidated binding digest as Work-Pack admission,
- performing owner mutation inside the router,
- ranking more than three routes,
- selecting an ambiguous route because it scored first,
- re-running an unchanged blocked source capability,
- recursive continuation or more than one dispatch per invocation,
- treating a prerequisite declaration, classifier receipt, or route string as
  authorization,
- recording owner work as router mutation or returning a recursive Task Session
  route instead of the same-attempt control handle,
- using Goal for a deterministic one-hop owner handoff,
- using the router for independent parallel work,
- hiding missing inputs, approvals, helper lifecycle gaps, or owner validation failures,
- reporting the source task as successful because the continuation owner succeeded,
- leaking consuming-project names or private evidence into the public package.
</anti-patterns>

<output-contract>
Return:

```markdown
## Continuation Route Result

- Source: <capability>:<mode> — <result>
- Source phase: terminal | pre-execution-prerequisite
- Source receipt: <path>
- Blocker fingerprint: <stable identifier>
- Probable routes:
  1. <capability>:<mode>[:<mutation-mode>] — <owner, evidence, missing inputs, risk, approval, authorization, expected receipt>
- Selection: selected | ambiguous | not-authorized | blocked | none
- Selected route: <exact tuple | none>
- Authorization source: ad-hoc-exact-route | work-pack-binding | not-required | none
- Authorization prompt required: true | false
- Work-Pack admission: <receipt and stable result code | none>
- Dispatch: not-requested | not-authorized | blocked | completed | flagged
- Dispatch/join count: <0 or 1>/<0 or 1>
- Owner boundary: pass | block
- Helper closeout: n/a | pass | flag | block, <counts and residue>
- Owner receipt: <path | none>
- Owner validation: <summary | none>
- Same-attempt control handle: <task, SWU, attempt, fingerprint, task-session:context-build | none>
- Returned next route: <capability>:<mode> <target | none>
- Follow-up: <one exact action | none>
```

When persisted, emit terminal compatibility receipts against
`continuation-route.schema.json`; emit current typed prerequisite and Work-Pack
authorization receipts against `schemas/continuation-route.schema.json`.
</output-contract>
