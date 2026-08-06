# Implementation Layering

## Layer decisions

| Layer | Behavior | Owned surfaces | Evidence required to advance |
| --- | --- | --- | --- |
| L0 — Contract | Define execution policy, entry projection, intent binding, and decision classes. | `implementation-readiness` schemas/validator and Invoke Plan handoff contract | positive and negative schema/contract fixtures |
| L1 — Route | Let Work-Pack-bound owner hops run without per-route authorization and add the outer-loop reducer. | `continuation-router`, `implementation-readiness` | route fixtures prove matched, outside-scope, ad hoc, and cycle cases |
| L2 — Execute | Classify prerequisites before deep Task Session context and resume through fresh sessions. | `task-session`, `task-session-until-blocker` | fast-guard, admission, one-hop join, and fresh-session fixtures |
| L3 — Integrate | Prove the complete direct-intent route and generated package parity. | cross-capability fixture, docs, generated mirrors | end-to-end causal tests and selective-sync parity |

## Boundary rule

Automation expands **progress**, not **scope**. Every layer must preserve:

- exact Work Pack identity and selected frontier;
- declared writes and validation;
- owner-specific gates and receipts;
- one-hop Continuation Router behavior;
- one-unit Task Session behavior;
- explicit stops for semantic, destructive, external, cost/risk, authority,
  publication, promotion, deployment, and failed-critical-validation choices.

## Promotion rule

- L0 cannot claim routing works.
- L1 cannot claim mutation works.
- L2 cannot claim end-to-end adoption.
- L3 local fixtures do not imply registry release or deployment.

## Validation by layer

### L0

- JSON Schema Draft 2020-12 positive/negative cases.
- Entry-state/next-route consistency validator.
- Work-Pack binding refuses unknown frontier, scope, or stop policy.

### L1

- Work-Pack-bound route needs no `--authorize-route`.
- Same route outside a binding preserves ad hoc authorization behavior.
- Route outside scope blocks.
- Owner receipt must join before progression.

### L2

- Fast guard completes before Context Builder on a declared prerequisite.
- Plan-once path produces no pre-execution Refresh.
- Semantic drift routes to Refresh and resumes through a fresh Task Session.
- Live target, validation, and single-use admission checks remain mandatory.

### L3

- One direct `finish this Work Pack` fixture crosses audit/selection/producer/
  routing/Task Session boundaries without another user authorization prompt.
- Stop-class fixtures halt before effects.
- Canonical and generated packages are byte-consistent after selective sync.

## Dispatch technique trace

- `sequence`: contracts precede routing, execution, and integration.
- `scu_swu_reduction`: each SWU has one independently falsifiable behavior.
- `recomposition_proof`: the eight SWUs recompose into one execution loop.
- `owner_boundary_check`: capabilities keep their existing semantic ownership.
- `approval_semantics_map`: execution intent is separated from consequential
  effect authorization.
- `validation_loop`: every layer has discriminating negative cases.
- `execution_receipt_handoff`: owner and Task Session receipts gate progress.

