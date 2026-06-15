# Stage S05: Distill

## Distill Result

- Target context: Craft canonical package maintenance.
- Objective and output artifact: select the smallest coherent Craft update and prove it recomposes into the existing ledger/index model.
- Mode and budget: standard, two-round role simulation.
- Proposal tracks: 1, parent-run Proposer and Balancer roles.
- Recursive rounds: 2 / 2.
- Verdict: pass.
- Current smallest coherent unit: optional `execution_readiness` index family.
- Next route: invoke design.

## Role Conversation Trace

| Role | Claim Or Objection | Reconciliation |
| --- | --- | --- |
| Proposer | Add a full readiness row family with schema fields on contexts, artifacts, decisions, and next moves. | Too broad; would overfit and risk invalidating existing ledgers. |
| Balancer | Craft's existing pattern is derived indexes pointing back to row IDs and paths. | Prefer optional derived index handles first. |
| Proposer | Include approval, execution mode, product worktree, and blocked scopes because these determine what can run. | Accepted as index handles, not execution proof. |
| Balancer | Product-specific examples could leak private context into public `arcanum`. | Accepted; use public-safe or synthetic fixture coverage only. |

## Concept Layer Map

- Broad layer: cross-sigil execution readiness.
- Craft layer: ledger-visible route memory and status.
- Selected unit: optional readiness indexes derived from existing rows.
- Future execution unit: `SWU-CFR-001`, schema/index contract only.

## Closure And Recomposition Proof

The selected unit closes because it has:

- one responsibility: expose execution-readiness lookup handles;
- named inputs: Invoke work-pack status, SWU IDs, approval record, blocked scopes;
- named output: optional index data in Craft ledgers and status/export views;
- no hidden executor role;
- recomposition path into existing Craft status and link/index rules.

## Deferred Complexity

- automated renderer/index generator;
- direct Invoke readiness block mutation;
- direct Refine non-executable marker mutation;
- generated runtime surface sync before canonical source changes pass.

## Distill Verdict

Pass. The readiness index family is the smallest useful unit for the next Craft maintenance SWU.
