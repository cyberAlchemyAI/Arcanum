# Native Dispatch Runner — Define

Status: proposed implementation definition

Machine source: [native-dispatch-runner.contract.json](native-dispatch-runner.contract.json)

## Problem

Arcanum can describe and validate a capability-bound dispatch, and a parent agent can manually follow that dispatch. It does not yet have a callable runtime path that turns one validated dispatch into native `spawn`, `join`, gate, and closeout actions.

That distinction invalidates a common proof shortcut: manually spawning agents and later writing dispatch-shaped receipts proves that native agents can be used, but it does not prove that a dispatch invocation caused those agents to run.

## Objective

Add `orchestrate execute <dispatch.json>` as the single execution entry point for a validated capability-bound dispatch. The path must:

1. validate before execution;
2. check authorization before spawning;
3. compile only currently permitted actions;
4. use the host's native subagent operations;
5. reduce returned receipts into deterministic gate decisions;
6. withhold dependent work on failure;
7. emit complete, validator-backed run evidence.

## Boundary

Dispatch Spec remains the route-shape validator. Orchestrate owns runtime coordination. A bounded capability owns its work and receipt. Humans retain authorization, lifecycle, and promotion decisions.

The implementation is split because the deterministic shell/runtime layer cannot itself call a host-only subagent API:

- a deterministic coordinator compiles actions and reduces receipts;
- a native Orchestrate driver performs those actions through the host API;
- a deterministic evidence layer persists what happened.

## Users and Trigger

The immediate user is a parent agent that already has a Dispatch Spec document and needs native, receipt-gated execution.

```text
dispatch-spec <dispatch.json>             # validate only
orchestrate execute <dispatch.json>        # validate and execute
```

## Required Behaviors

| ID | Behavior | Failure behavior |
| --- | --- | --- |
| NDR-R1 | Validate the dispatch before any runtime action. | Block with validation receipt. |
| NDR-R2 | Resolve execution authorization independently from lifecycle approval. | Enter `authorization_pending`; spawn nothing. |
| NDR-R3 | Compile an exact first-wave action set. | Block on ambiguous roles, dependencies, or scopes. |
| NDR-R4 | Spawn only actions emitted by the coordinator. | Block on absent native host capability. |
| NDR-R5 | Join results to declared role, step, wave, and agent identity. | Reject malformed or mismatched receipts. |
| NDR-R6 | Open a dependent wave only when its gate passes. | Withhold all dependent spawns. |
| NDR-R7 | Record each host action at attempt time. | Treat missing live evidence as failed integration proof. |
| NDR-R8 | Validate the closeout dispatch and result. | Keep run blocked or incomplete. |
| NDR-R9 | Generate installed Orchestrate surfaces from one canonical source. | Fail drift validation. |

## Acceptance Boundary

The feature is complete only when both native canaries begin from the same command and require no bespoke parent spawning instructions:

- failure first: first-wave non-pass receipt, blocking gate, no dependent agent;
- success second: passing first wave, open gate, dependent agent spawned exactly once.

The current manually driven canary is historical evidence that the host tools work. It is not automatic Dispatch Spec integration proof and must be adjudicated as such without rewriting its original records.

## Non-goals

- Cross-host parity in the first implementation layer.
- Full legacy CLI migration.
- Autonomous lifecycle promotion.
- Unbounded recursive subagent spawning.
- Treating Markdown as runtime source.

## Source of Truth

The proposed contract is machine-readable. Markdown explains and plans it; implementation will use structured dispatch, state, action, event, receipt, gate, and result documents as runtime inputs and outputs.

## Open Decisions

No architecture-blocking owner decision remains. Implementation may choose filenames and module boundaries inside the declared write scopes, but it may not collapse validator and executor authority or weaken failure withholding.
