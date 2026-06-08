# MOGT Paper Test Spec

Purpose: define the evidence and structure checks that the MOGT paper must satisfy before it is treated as a publication-ready synthesis artifact.

This is a paper-facing verification contract, not an experiment protocol.

## Structural Checks

| Check ID | Requirement                                                                                 | Source Artifact                                                           | Current Status |
| -------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------- |
| PTEST-01 | The paper declares all planned `PSEC-*` section nodes used by `registry/RESEARCH-GRAPH.md`. | `papers/mogt-agentic-conversation-paper.md`, `registry/RESEARCH-GRAPH.md` | pass           |
| PTEST-02 | The paper spec lists each section's required graph inputs and current blockers.             | `papers/PAPER-SPEC.md`                                                    | pass           |
| PTEST-03 | The paper has section-scoped writing stories aligned to the graph.                          | `papers/PAPER-STORIES.md`                                                 | pass           |
| PTEST-04 | The paper review artifact records a current verdict and open blockers.                      | `papers/PAPER-REVIEW.md`                                                  | pass           |
| PTEST-05 | The paper does not act as the normative definition source.                                  | `papers/mogt-agentic-conversation-paper.md`, `definitions/DEFINITIONS.md` | pass           |

## Section Evidence Checks

| Check ID | Section Node | Evidence Obligation                                                                                                                                  | Source Artifact                                                       | Current Status            |
| -------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------- |
| PTEST-10 | PSEC-01      | Motivation must frame all four claims using project domain context.                                                                                  | `registry/RESEARCH-GRAPH.md`                                          | draft present             |
| PTEST-11 | PSEC-02      | Decision-model section must remain anchored to methodology/theory baseline and synthesize the four core claims without redefining them.              | `registry/RESEARCH-GRAPH.md`, `foundations/METHODOLOGY-AND-THEORY.md` | draft present             |
| PTEST-12 | PSEC-03      | Methodology section must synthesize experiment design across E1-E4 and cite the methodology baseline.                                                | `registry/RESEARCH-GRAPH.md`                                          | draft present             |
| PTEST-13 | PSEC-04      | Traceability and arbitration section must synthesize C1 and C2 plus E1 and E2, and later bind to concrete analysis-result and evidence-status nodes. | `registry/RESEARCH-GRAPH.md`, `results/MOGT-EVIDENCE-STATUS.md`       | blocked pending live runs |
| PTEST-14 | PSEC-05      | Negotiation section must synthesize C3 plus E3, and later bind to concrete analysis-result and evidence-status nodes.                                | `registry/RESEARCH-GRAPH.md`, `results/MOGT-EVIDENCE-STATUS.md`       | blocked pending live runs |
| PTEST-15 | PSEC-06      | Overhead section must synthesize C4 plus E4, and later bind to concrete analysis-result and evidence-status nodes.                                   | `registry/RESEARCH-GRAPH.md`, `results/MOGT-EVIDENCE-STATUS.md`       | blocked pending live runs |
| PTEST-16 | PSEC-07      | Threats section must synthesize methodology or evaluation authorities and explicitly acknowledge current evidence gaps.                              | `registry/RESEARCH-GRAPH.md`, `sources/REFERENCE-LEDGER.md`           | partial                   |

## Dynamic Checks To Activate After First Live Runs

1. Every result-facing section must synthesize at least one `Analysis Result` node.
2. Every empirical conclusion must be traceable to an evidence update in `results/MOGT-EVIDENCE-STATUS.md`.
3. No section may claim support for C1-C4 unless the relevant claim status has been updated from live analysis.
4. If a cited reference remains `pending normalization`, the final paper draft should either normalize it first or explicitly document the waiver.

## Current Blocking Conditions

The paper can be designed now, but it is not ready for evidence-backed publication integration until:

1. E1, E2, E3, and E4 produce live run data and result artifacts.
2. Claim updates land in `results/MOGT-EVIDENCE-STATUS.md`.
3. `registry/RESEARCH-GRAPH.md` is expanded with result and evidence-status nodes.
