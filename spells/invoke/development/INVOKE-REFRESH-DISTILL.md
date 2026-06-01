# Distill Result: Invoke Refresh

## Target Context

Invoke development needs a new mode that can update existing invoke-authored artifacts from latest session outputs without re-running the whole lifecycle or executing target work.

## Objective And Output Artifact

- Objective: reduce broad "refresh artifacts from session outputs" behavior into the smallest coherent invoke mode.
- Output artifact: mode contract, template family, fixtures, validation wiring, and refreshed development artifacts.

## Mode And Budget

- Mode: standard
- Proposal tracks: one
- Recursive rounds: two completed
- Role execution path: role simulation

## Verdict

pass

## Role Conversation Trace

| Role | Claim Or Objection | Reconciliation |
| --- | --- | --- |
| Proposer | Refresh should inspect latest session outputs and update artifacts. | Accepted with an evidence-to-delta model. |
| Balancer | That is too broad and can become hidden mutation. | Revised into proposal-only default plus apply-approved gate. |
| Proposer | Refresh should handle blockers, routes, status, evidence, drift, and no-op. | Accepted as finite delta classes. |
| Balancer | It may duplicate workflow-reflect or task-session. | Resolved by authority split: refresh updates artifact state; workflow-reflect analyzes workflow gaps; task-session executes work. |

## Current Smallest Coherent Unit

`RefreshSignal -> Delta -> RefreshReport`

Responsibility: turn selected session evidence into typed artifact-state deltas, then produce a report/proposal that can be reviewed or explicitly applied.

## Optimization Point

This unit is small enough to validate with fixtures and large enough to preserve the full user need: new evidence, blockers, resolved blockers, status changes, route changes, artifact drift, and no-op state.

## Concept Layer Map

| Layer | Concept | Status |
| --- | --- | --- |
| Broad frame | Keep workflow artifacts current after sessions. | too broad |
| Invoke mode | `invoke refresh` handles artifact refresh from evidence. | selected frame |
| Smallest unit | `RefreshSignal -> Delta -> RefreshReport`. | implementation unit |
| Deferred scale | Apply-approved mutation, command routing, telemetry promotion. | later layers |

## Technique Pack Trace

| Technique | Activation | Outcome |
| --- | --- | --- |
| abstraction-level guard | Refresh mixed execution, reflection, and artifact update. | Selected artifact-state synthesis level. |
| recomposition proof | Need to show the unit still satisfies the broad request. | Signals and deltas recompose into report/proposal/apply flow. |
| evolution profile | Future refresh types and apply modes are likely. | Keep finite delta classes and extension boundary. |
| frame-expiry note | If refresh must execute target work, this design expires. | Route execution to task-session instead. |
| navigable result check | Need next files and fixtures. | Contract, template, fixtures, runner wiring identified. |
| premortem pass | Triggered by mutation risk. | Main failure: silent overclaiming; guard with proposal-only default and evidence mapping. |

## Closure And Recomposition Proof

The unit closes because it has named inputs, outputs, statuses, and gates:

- input: source evidence plus target artifact inventory,
- transform: classify refresh signals and deltas,
- output: refresh report, patch proposal, or approved changes,
- validation: pass, flag, block, and no-op fixtures.

It recomposes upward into the full mode by adding optional template output, approved mutation, command routing, and observability without changing the central unit.

## Evolution Profile

Expected evolution:

- more delta classes may appear,
- apply-approved may become operational,
- command routing may expose `/invoke refresh`,
- observability may aggregate refresh drift patterns.

Smallest extension boundary:

- add new delta classes only when a fixture demonstrates a distinct artifact-state change.
- keep mutation modes explicit.

## Deferred Complexity

- Direct command routing.
- Automatic patch application.
- Cross-repository refresh.
- Runtime adapter mutation support.
- Observability aggregation dashboards.

## Tension Ledger

| Tension | Resolution |
| --- | --- |
| Update artifacts vs avoid silent mutation. | Proposal-only default; apply-approved requires explicit approval. |
| Refresh vs workflow reflection. | Refresh handles evidence-backed artifact state; reflection handles workflow improvement analysis. |
| Refresh vs task execution. | Refresh never executes tasks. |
| Broad session context vs useful evidence. | Context Builder selects obligation-linked source evidence. |

## Premortem

Likely failure: refresh turns a setup artifact into a completion claim because the latest session "felt successful."

Guardrail: every status or blocker change must cite a refresh signal with confidence and mutation safety.

## Frame Expiry Note

This optimization point expires if the desired command must execute target work, score benchmarks, or perform broad lifecycle redesign. Those should route to `task-session`, external research, or `workflow-reflect`.

## Navigation Guide

Start here:

1. [INVOKE-REFRESH-CONTEXT-PACK.md](INVOKE-REFRESH-CONTEXT-PACK.md)
2. [INVOKE-REFRESH-DEFINE.md](INVOKE-REFRESH-DEFINE.md)
3. [INVOKE-REFRESH-INTERROGATION.md](INVOKE-REFRESH-INTERROGATION.md)
4. [INVOKE-REFRESH-DISTILL.md](INVOKE-REFRESH-DISTILL.md)
5. [../refresh.md](../refresh.md)

Next route: invoke plan for implementation hardening, then task-session for any mutation-capable routing work.
