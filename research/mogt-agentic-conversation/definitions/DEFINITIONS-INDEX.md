# MOGT Definitions Index

Purpose: lookup and traceability index for canonical definitions used by the MOGT research project.

Canonical semantics source: `definitions/DEFINITIONS.md`.

## Definitions Map

| Definition ID | Summary                               | Canonical Artifact(s)                                                                                                                              | Practical Example                                                                           |
| ------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| MOGT-D1       | Agentic conversation decision process | `claims/CLAIMS.md`, `experiments/E1-tradeoff-traceability-baseline/protocol.md`, `experiments/E3-negotiation-stability-under-conflict/protocol.md` | E1 and E3 treat each benchmark decision episode as a bounded conversation decision process. |
| MOGT-D2       | Decision state                        | `experiments/E1-tradeoff-traceability-baseline/context.md`, `experiments/E2-pareto-arbitration-quality/context.md`                                 | E2 compares policy regimes on the same decision state to reduce scenario drift.             |
| MOGT-D3       | Objective vector                      | `claims/HYPOTHESES.md`, `experiments/E1-tradeoff-traceability-baseline/protocol.md`, `experiments/E2-pareto-arbitration-quality/protocol.md`       | E1 and E2 require objective vectors to be explicit in the trace.                            |
| MOGT-D4       | Candidate action set                  | `experiments/E1-tradeoff-traceability-baseline/context.md`, `experiments/E3-negotiation-stability-under-conflict/context.md`                       | A candidate action set includes answer, defer, escalate, and specialist handoff.            |
| MOGT-D5       | Pareto frontier                       | `experiments/E2-pareto-arbitration-quality/protocol.md`, `claims/CLAIMS.md`                                                                        | E2 classifies selections as frontier or dominated actions.                                  |
| MOGT-D6       | Conversation game                     | `experiments/E3-negotiation-stability-under-conflict/protocol.md`, `definitions/INITIAL-DEFINITIONS.md`                                            | E3 models specialist role disagreement as a structured conversation game.                   |
| MOGT-D7       | Negotiation stability                 | `experiments/E3-negotiation-stability-under-conflict/protocol.md`, `claims/HYPOTHESES.md`                                                          | E3 measures bounded-turn convergence and cycle detection.                                   |
| MOGT-D8       | Overhead envelope                     | `experiments/E4-overhead-feasibility-envelope/protocol.md`, `results/MOGT-EVIDENCE-STATUS.md`                                                      | E4 defines the acceptable cost and latency envelope for adoption.                           |
| MOGT-D9       | Policy regime                         | `experiments/EXPERIMENTS.md`, `experiments/E2-pareto-arbitration-quality/protocol.md`, `experiments/E4-overhead-feasibility-envelope/protocol.md`  | Regimes compared include heuristic, weighted-sum, Pareto-guided, and bargaining-guided.     |
| MOGT-M1       | Decision quality score                | `experiments/E2-pareto-arbitration-quality/context.md`, `experiments/E4-overhead-feasibility-envelope/protocol.md`                                 | E2 uses reviewer quality scoring to compare selected actions across regimes.                |
| MOGT-M2       | Traceability coverage                 | `experiments/E1-tradeoff-traceability-baseline/protocol.md`, `claims/HYPOTHESES.md`                                                                | E1 measures whether reviewers can reconstruct the decision rationale from traces.           |
| MOGT-M3       | Conflict resolution convergence rate  | `experiments/E3-negotiation-stability-under-conflict/protocol.md`                                                                                  | E3 reports the proportion of contested episodes that converge inside the turn limit.        |
| MOGT-M4       | Overhead acceptability ratio          | `experiments/E4-overhead-feasibility-envelope/protocol.md`, `results/MOGT-EVIDENCE-STATUS.md`                                                      | E4 treats adoption as viable only when quality and overhead thresholds are both met.        |

## Usage Rules

1. Every protocol must reference at least one MOGT definition ID relevant to its claim.
2. Claim updates must cite both experiment evidence and the affected definition IDs.
3. New project terms should be added here before becoming protocol-critical.
