# MOGT Paper Spec

Purpose: give the MOGT paper a contract-first design model before evidence-backed prose writing begins.

Authority model:

- `papers/mogt-agentic-conversation-paper.md` remains the narrative synthesis artifact.
- `registry/RESEARCH-GRAPH.md` remains the typed node and edge authority for section inputs.
- This spec translates that graph into explicit paper-section obligations.

## Paper Objective

Demonstrate, with traceable evidence, whether explicit multi-objective and game-theoretic decision policies improve agentic conversation decisions across traceability, arbitration quality, negotiation stability, and operational feasibility.

## Design Contract

1. The paper must not redefine canonical project semantics from `definitions/DEFINITIONS.md`.
2. Every paper section must map to one or more `PSEC-*` nodes in `registry/RESEARCH-GRAPH.md`.
3. A result section is not publication-ready until it can synthesize both the relevant experiment nodes and the relevant evidence-backed result or status nodes.
4. References cited in narrative prose should already exist as `Reference` nodes in `sources/REFERENCE-LEDGER.md`.
5. When evidence is still pending, the paper may describe intended analysis shape but must not claim empirical support.

## Section Registry

| Section Node | Section Title                            | Synthesis Role                                             | Required Graph Inputs                                                      | Current Readiness | Current Blockers                                                       |
| ------------ | ---------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------- | ----------------- | ---------------------------------------------------------------------- |
| PSEC-01      | Motivation and problem framing           | establish problem, scope, and stakes                       | `DOM-CTX`; `CLAIM-C1`; `CLAIM-C2`; `CLAIM-C3`; `CLAIM-C4`                  | drafted           | none                                                                   |
| PSEC-02      | Canonical definitions and decision model | explain concepts, objective structure, and decision model  | `PSEC-02`; `METH-BASELINE`; `CLAIM-C1`; `CLAIM-C2`; `CLAIM-C3`; `CLAIM-C4` | drafted           | keep wording aligned with canonical definitions during later revisions |
| PSEC-03      | Experimental methodology                 | explain research design and measurement posture            | `PSEC-03`; `METH-BASELINE`; `EXP-E1`; `EXP-E2`; `EXP-E3`; `EXP-E4`         | drafted           | live execution details and empirical reporting remain unavailable      |
| PSEC-04      | Traceability and arbitration results     | synthesize E1/E2 outcomes for C1/C2                        | `PSEC-04`; `CLAIM-C1`; `CLAIM-C2`; `EXP-E1`; `EXP-E2`                      | blocked           | no run data, analysis results, or evidence updates yet                 |
| PSEC-05      | Negotiation stability results            | synthesize E3 outcomes for C3                              | `PSEC-05`; `CLAIM-C3`; `EXP-E3`                                            | blocked           | no run data, analysis results, or evidence updates yet                 |
| PSEC-06      | Overhead envelope and adoption guidance  | synthesize E4 outcomes for C4 and adoption guidance        | `PSEC-06`; `CLAIM-C4`; `EXP-E4`                                            | blocked           | no run data, analysis results, or evidence updates yet                 |
| PSEC-07      | Threats to validity and future work      | record methodological limits, evidence gaps, and next work | `PSEC-07`; methodology and evaluation authorities                          | partial           | empirical threats cannot be closed until first live run                |

## Linked Paper Contract Artifacts

- Story contract: `papers/PAPER-STORIES.md`
- Evidence checks: `papers/PAPER-TEST-SPEC.md`
- Current readiness review: `papers/PAPER-REVIEW.md`

## Pilot Scope

This paper contract is an experimental pilot of the MARS paper-design workflow.

Its immediate job is to make the current paper plan reviewable before MOGT has live evidence.

Its secondary job is to produce real lessons that can be fed back into the MARS framework after the MOGT paper is exercised through live experiment results.
