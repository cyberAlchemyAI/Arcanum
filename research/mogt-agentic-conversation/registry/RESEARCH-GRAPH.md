# MOGT Research Graph

Purpose: apply the MARS research-artifact taxonomy and typed relationships to the MOGT project so paper sections, foundations, claims, experiments, and authorities can be traced as an explicit graph.

Canonical node and edge semantics come from:

- `implementation/mars/definitions/RESEARCH-TAXONOMY.md`
- `implementation/mars/definitions/RESEARCH-RELATIONSHIPS.md`

This artifact is a project-level graph registry. It does not replace canonical definitions, protocol text, or the traceability matrix.

## Scope Of The Current Graph

Current graph coverage:

- project foundations baseline
- core claims
- experiment and protocol nodes
- planned paper section nodes
- current authority references used by protocols

Not yet represented as completed nodes:

- run-data nodes, because no live runs have executed yet
- analysis-result nodes, because no results have been produced yet
- evidence-status update edges, because no adjudication wave has occurred yet

## Derived Paper Contract Artifacts

The current graph now drives a paper-design pilot for MOGT:

- `papers/PAPER-SPEC.md` derives section registry obligations from `PSEC-*` nodes and their incoming graph links.
- `papers/PAPER-STORIES.md` derives one reviewable writing story per paper section.
- `papers/PAPER-TEST-SPEC.md` derives structural and evidence checks from `anchors`, `cites`, and `synthesizes` obligations.
- `papers/PAPER-REVIEW.md` records the current readiness verdict against those derived obligations.

## Node Inventory

| Node ID                             | Meta-Concept         | Artifact Anchor                                                   | Status                | Notes                                         |
| ----------------------------------- | -------------------- | ----------------------------------------------------------------- | --------------------- | --------------------------------------------- |
| DOM-CTX                             | Domain Context       | `foundations/DOMAIN-CONTEXT.md`                                   | active                | project-level domain framing                  |
| METH-BASELINE                       | Methodology Artifact | `foundations/METHODOLOGY-AND-THEORY.md`                           | active                | project-level methodology and theory baseline |
| CLAIM-C1                            | Claim                | `claims/CLAIMS.md` MOGT-C1                                        | active                | traceability and reviewability claim          |
| CLAIM-C2                            | Claim                | `claims/CLAIMS.md` MOGT-C2                                        | active                | Pareto-aware quality claim                    |
| CLAIM-C3                            | Claim                | `claims/CLAIMS.md` MOGT-C3                                        | active                | negotiation-stability claim                   |
| CLAIM-C4                            | Claim                | `claims/CLAIMS.md` MOGT-C4                                        | active                | operational overhead claim                    |
| EXP-E1                              | Experiment           | `experiments/E1-tradeoff-traceability-baseline/`                  | planned               | first-wave traceability experiment            |
| EXP-E2                              | Experiment           | `experiments/E2-pareto-arbitration-quality/`                      | planned               | first-wave arbitration experiment             |
| EXP-E3                              | Experiment           | `experiments/E3-negotiation-stability-under-conflict/`            | planned               | second-wave negotiation experiment            |
| EXP-E4                              | Experiment           | `experiments/E4-overhead-feasibility-envelope/`                   | planned               | first-wave overhead experiment                |
| PROT-E1                             | Protocol             | `experiments/E1-tradeoff-traceability-baseline/protocol.md`       | active                | tests C1                                      |
| PROT-E2                             | Protocol             | `experiments/E2-pareto-arbitration-quality/protocol.md`           | active                | tests C2                                      |
| PROT-E3                             | Protocol             | `experiments/E3-negotiation-stability-under-conflict/protocol.md` | active                | tests C3                                      |
| PROT-E4                             | Protocol             | `experiments/E4-overhead-feasibility-envelope/protocol.md`        | active                | tests C4                                      |
| PSEC-01                             | Paper Section        | `papers/mogt-agentic-conversation-paper.md` planned section 1     | planned               | motivation and problem framing                |
| PSEC-02                             | Paper Section        | `papers/mogt-agentic-conversation-paper.md` planned section 2     | planned               | canonical definitions and decision model      |
| PSEC-03                             | Paper Section        | `papers/mogt-agentic-conversation-paper.md` planned section 3     | planned               | experimental methodology                      |
| PSEC-04                             | Paper Section        | `papers/mogt-agentic-conversation-paper.md` planned section 4     | planned               | traceability and arbitration results          |
| PSEC-05                             | Paper Section        | `papers/mogt-agentic-conversation-paper.md` planned section 5     | planned               | negotiation stability results                 |
| PSEC-06                             | Paper Section        | `papers/mogt-agentic-conversation-paper.md` planned section 6     | planned               | overhead envelope and adoption guidance       |
| PSEC-07                             | Paper Section        | `papers/mogt-agentic-conversation-paper.md` planned section 7     | planned               | threats to validity and future work           |
| REF-WOHLIN-2012                     | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | methodology authority                         |
| REF-DEB-2001                        | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | Pareto and dominance baseline                 |
| REF-MARLER-2010                     | Reference            | `sources/REFERENCE-LEDGER.md`                                     | pending normalization | weighted-sum comparison authority             |
| REF-KEENEY-RAIFFA-1976              | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | value-tradeoff framing                        |
| REF-DOSHI-VELEZ-KIM-2017            | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | interpretability evaluation framing           |
| REF-WALKER-1997                     | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | dialogue evaluation framing                   |
| REF-JAIN-1991                       | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | overhead measurement discipline               |
| REF-HART-STAVELAND-1988             | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | reviewer workload baseline                    |
| REF-WOOLDRIDGE-2009                 | Reference            | `sources/REFERENCE-LEDGER.md`                                     | pending normalization | multi-agent coordination framing              |
| REF-NASH-1950                       | Reference            | `sources/REFERENCE-LEDGER.md`                                     | pending normalization | bargaining and equilibrium framing            |
| REF-WU-2024-AUTOGEN                 | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | agentic orchestration prior art               |
| REF-LIU-2024-AGENTBENCH             | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | agentic benchmark framing                     |
| REF-DU-2023-MULTIAGENT-DEBATE       | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | debate coordination prior art                 |
| REF-LEWIS-2017-DEAL-OR-NO-DEAL      | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | negotiation dialogue prior art                |
| REF-GUO-2024-LLM-MULTIAGENTS-SURVEY | Reference            | `sources/REFERENCE-LEDGER.md`                                     | active                | landscape and failure-mode survey             |

## Edge Inventory

| Source Node   | Edge        | Target Node                         | Evidence Anchor                                                   | Status  |
| ------------- | ----------- | ----------------------------------- | ----------------------------------------------------------------- | ------- |
| DOM-CTX       | frames      | CLAIM-C1                            | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | frames      | CLAIM-C2                            | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | frames      | CLAIM-C3                            | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | frames      | CLAIM-C4                            | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | frames      | EXP-E1                              | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | frames      | EXP-E2                              | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | frames      | EXP-E3                              | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | frames      | EXP-E4                              | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | cites       | REF-WU-2024-AUTOGEN                 | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | cites       | REF-LIU-2024-AGENTBENCH             | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | cites       | REF-DU-2023-MULTIAGENT-DEBATE       | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | cites       | REF-LEWIS-2017-DEAL-OR-NO-DEAL      | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| DOM-CTX       | cites       | REF-GUO-2024-LLM-MULTIAGENTS-SURVEY | `foundations/DOMAIN-CONTEXT.md`                                   | active  |
| METH-BASELINE | anchors     | PROT-E1                             | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | anchors     | PROT-E2                             | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | anchors     | PROT-E3                             | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | anchors     | PROT-E4                             | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | anchors     | PSEC-02                             | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| METH-BASELINE | anchors     | PSEC-03                             | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| METH-BASELINE | cites       | REF-WOHLIN-2012                     | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | cites       | REF-DEB-2001                        | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | cites       | REF-MARLER-2010                     | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | cites       | REF-KEENEY-RAIFFA-1976              | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | cites       | REF-DOSHI-VELEZ-KIM-2017            | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | cites       | REF-WALKER-1997                     | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | cites       | REF-JAIN-1991                       | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| METH-BASELINE | cites       | REF-HART-STAVELAND-1988             | `foundations/METHODOLOGY-AND-THEORY.md`                           | active  |
| EXP-E1        | tests       | CLAIM-C1                            | `experiments/E1-tradeoff-traceability-baseline/protocol.md`       | active  |
| EXP-E2        | tests       | CLAIM-C2                            | `experiments/E2-pareto-arbitration-quality/protocol.md`           | active  |
| EXP-E3        | tests       | CLAIM-C3                            | `experiments/E3-negotiation-stability-under-conflict/protocol.md` | active  |
| EXP-E4        | tests       | CLAIM-C4                            | `experiments/E4-overhead-feasibility-envelope/protocol.md`        | active  |
| PROT-E1       | cites       | REF-WOHLIN-2012                     | `experiments/E1-tradeoff-traceability-baseline/protocol.md`       | active  |
| PROT-E1       | cites       | REF-KEENEY-RAIFFA-1976              | `experiments/E1-tradeoff-traceability-baseline/protocol.md`       | active  |
| PROT-E1       | cites       | REF-DOSHI-VELEZ-KIM-2017            | `experiments/E1-tradeoff-traceability-baseline/protocol.md`       | active  |
| PROT-E1       | cites       | REF-WALKER-1997                     | `experiments/E1-tradeoff-traceability-baseline/protocol.md`       | active  |
| PROT-E2       | cites       | REF-WOHLIN-2012                     | `experiments/E2-pareto-arbitration-quality/protocol.md`           | active  |
| PROT-E2       | cites       | REF-DEB-2001                        | `experiments/E2-pareto-arbitration-quality/protocol.md`           | active  |
| PROT-E2       | cites       | REF-KEENEY-RAIFFA-1976              | `experiments/E2-pareto-arbitration-quality/protocol.md`           | active  |
| PROT-E2       | cites       | REF-MARLER-2010                     | `experiments/E2-pareto-arbitration-quality/protocol.md`           | active  |
| PROT-E3       | cites       | REF-WOHLIN-2012                     | `experiments/E3-negotiation-stability-under-conflict/protocol.md` | active  |
| PROT-E3       | cites       | REF-WOOLDRIDGE-2009                 | `experiments/E3-negotiation-stability-under-conflict/protocol.md` | active  |
| PROT-E3       | cites       | REF-NASH-1950                       | `experiments/E3-negotiation-stability-under-conflict/protocol.md` | active  |
| PROT-E4       | cites       | REF-WOHLIN-2012                     | `experiments/E4-overhead-feasibility-envelope/protocol.md`        | active  |
| PROT-E4       | cites       | REF-JAIN-1991                       | `experiments/E4-overhead-feasibility-envelope/protocol.md`        | active  |
| PROT-E4       | cites       | REF-HART-STAVELAND-1988             | `experiments/E4-overhead-feasibility-envelope/protocol.md`        | active  |
| PROT-E4       | cites       | REF-WALKER-1997                     | `experiments/E4-overhead-feasibility-envelope/protocol.md`        | active  |
| PROT-E4       | cites       | REF-MARLER-2010                     | `experiments/E4-overhead-feasibility-envelope/protocol.md`        | active  |
| DOM-CTX       | frames      | PSEC-01                             | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| DOM-CTX       | frames      | PSEC-06                             | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-01       | synthesizes | CLAIM-C1                            | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-01       | synthesizes | CLAIM-C2                            | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-01       | synthesizes | CLAIM-C3                            | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-01       | synthesizes | CLAIM-C4                            | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-02       | synthesizes | CLAIM-C1                            | `registry/TRACEABILITY-MATRIX.md`                                 | planned |
| PSEC-02       | synthesizes | CLAIM-C2                            | `registry/TRACEABILITY-MATRIX.md`                                 | planned |
| PSEC-02       | synthesizes | CLAIM-C3                            | `registry/TRACEABILITY-MATRIX.md`                                 | planned |
| PSEC-02       | synthesizes | CLAIM-C4                            | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-03       | synthesizes | EXP-E1                              | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-03       | synthesizes | EXP-E2                              | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-03       | synthesizes | EXP-E3                              | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-03       | synthesizes | EXP-E4                              | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-04       | synthesizes | CLAIM-C1                            | `registry/TRACEABILITY-MATRIX.md`                                 | planned |
| PSEC-04       | synthesizes | CLAIM-C2                            | `registry/TRACEABILITY-MATRIX.md`                                 | planned |
| PSEC-04       | synthesizes | EXP-E1                              | `experiments/E1-tradeoff-traceability-baseline/protocol.md`       | planned |
| PSEC-04       | synthesizes | EXP-E2                              | `experiments/E2-pareto-arbitration-quality/protocol.md`           | planned |
| PSEC-05       | synthesizes | CLAIM-C3                            | `registry/TRACEABILITY-MATRIX.md`                                 | planned |
| PSEC-05       | synthesizes | EXP-E3                              | `experiments/E3-negotiation-stability-under-conflict/protocol.md` | planned |
| PSEC-06       | synthesizes | CLAIM-C4                            | `registry/TRACEABILITY-MATRIX.md`                                 | planned |
| PSEC-06       | synthesizes | EXP-E4                              | `experiments/E4-overhead-feasibility-envelope/protocol.md`        | planned |
| PSEC-07       | synthesizes | REF-WOHLIN-2012                     | `papers/mogt-agentic-conversation-paper.md`                       | planned |
| PSEC-07       | synthesizes | REF-DOSHI-VELEZ-KIM-2017            | `papers/mogt-agentic-conversation-paper.md`                       | planned |

## Pending Graph Expansion

The following edges should be added after the first live execution wave:

- `EXP-*` `produces` run-data nodes under `experiments/*/data/*.jsonl`
- analysis-result nodes `analyzes` run-data nodes
- analysis-result nodes `updates` `results/MOGT-EVIDENCE-STATUS.md`
- paper sections `synthesizes` concrete result and evidence-status nodes rather than only planned experiment nodes

## Alignment Notes

1. The paper is still a synthesis stub, so all `PSEC-*` nodes are planned rather than evidence-backed narrative sections.
2. `REF-MARLER-2010`, `REF-WOOLDRIDGE-2009`, and `REF-NASH-1950` remain usable as graph nodes, but their normalization status is still incomplete in the authority workflow.
3. The traceability matrix remains the authoritative quick lookup for claim-to-experiment-to-paper mapping; this graph adds typed node and edge semantics on top of that matrix.
