# Plan Distill Validation

## Mode and verdict

- Mode: validate
- Round budget: 2
- Verdict: pass for plan structure
- Mutation handoff: not allowed; no SWU or lifecycle dispatch is authorized

## Role trace

### Proposer

Six sequential units separate data contracts, pure classification, owner routing, guarded resume, authoring adoption, and integration.

### Balancer

The independent contract reviewer raised four material objections:

1. ordinary Context Builder work occurs before declared prerequisite routing;
2. a bare Task Session request cannot currently authorize apply-capable Refresh;
3. more than one prerequisite hop exceeds Continuation Router ownership;
4. wall-clock assertions alone would be flaky and machine-dependent.

### Reconciliation

- Add a typed pre-execution record and classifier before Context Builder.
- Keep bare unauthorized entry fail-closed but fast; accept only exact carried authorization for owner mutation.
- Limit the fast path to one hop and preserve multi-hop work as outer-loop residue.
- Make phase/read instrumentation normative and five seconds an operational SLO only.

## SWU atomicity

| SWU | One primary behavior | Independent acceptance | Further split? |
| --- | --- | --- | --- |
| 001 | versioned prerequisite/classification contracts | schema fixtures | no; schemas are one identity chain |
| 002 | pure early classifier | phase/read-budget fixtures | no; routing is excluded |
| 003 | one-hop prerequisite routing | Router fixtures | no; resume is excluded |
| 004 | joined revalidation and same-attempt resume | stale/replay/resume fixtures | no; Plan adoption is excluded |
| 005 | authoring/entry consistency | Plan/readiness fixtures | no; both surfaces express one immediate-route contract |
| 006 | cross-capability and generated proof | canary/regression/parity receipt | no; this is the recomposition gate |

## First-unit narrowness

`SWU-PEP-001` is the narrowest reversible trust-building step. It creates no runtime behavior and can be validated without dispatching an owner or mutating a consuming project.

## Recomposition proof

The schema is consumed by the classifier; the classifier receipt is consumed by Router; the Router receipt is consumed by Task Session resume; Plan and Implementation Readiness emit the matching entry contract; integration proves both plan-once and genuine-prerequisite paths. Removing any unit leaves an unbound interface or untested owner boundary.

## Premortem

Most likely failure: the “fast path” becomes another full preflight or silently broadens execution intent into apply authority. Guardrails: phase/read budget, exact path equality, one-hop limit, explicit carried authorization, and a canary that proves no Context Builder phase occurred before an unauthorized fast block.

## Evolution profile

Expected evolution includes more prerequisite kinds and additional entrypoint compositions. The smallest extension boundary is the typed prerequisite record plus owner route/satisfaction predicate. Multi-hop DAG orchestration remains separate.

## Navigation

Start with `SWU-PEP-001`. Use `execution.dispatch.json` for lifecycle routing. Read `RESIDUE.md` before `SWU-PEP-004` or `SWU-PEP-005` because authorization semantics become consequential there.
