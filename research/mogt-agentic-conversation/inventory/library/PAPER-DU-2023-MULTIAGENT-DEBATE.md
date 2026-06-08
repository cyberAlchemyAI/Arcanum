# Improving Factuality and Reasoning through Multiagent Debate — Inventory Library Entry

**Source ID:** `PAPER-DU-2023-MULTIAGENT-DEBATE`
**Reference ID:** `REF-DU-2023-MULTIAGENT-DEBATE`
**Entry Type:** `paper-abstract`
**Acquisition Mode:** `web-retrieved`
**Raw Content Paths:** `inventory/raw/PAPER-DU-2023-MULTIAGENT-DEBATE/README.md`
**Extraction Date:** `2026-04-28`
**Experiments:** `E2, E3, E4`
**Status:** `library-grade`

## Bibliographic Record

| Field       | Value                                                                   |
| ----------- | ----------------------------------------------------------------------- |
| Citation    | Du et al. Improving Factuality and Reasoning through Multiagent Debate. |
| URL         | `https://arxiv.org/abs/2305.14325v1`                                    |
| Pin         | `arxiv:2305.14325v1`                                                    |
| Access Mode | open web retrieval                                                      |

## Raw-Backed Content

### Captured Source Content

The raw provenance file preserves the abstract excerpt describing multiple language model instances proposing and debating individual responses over multiple rounds to reach a common final answer, with reported gains in reasoning and factuality.

## Extracted Constructs

| Construct                                  | Why It Matters                                                                                                        | Experiments | Raw Anchor                                                |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- | ----------- | --------------------------------------------------------- |
| multi-round debate between agents          | provides a concrete mechanism for disagreement exposure before final selection                                        | E2, E3, E4  | `inventory/raw/PAPER-DU-2023-MULTIAGENT-DEBATE/README.md` |
| critique and revision loops                | helps MOGT model bounded deliberation rather than one-shot voting                                                     | E3          | `inventory/raw/PAPER-DU-2023-MULTIAGENT-DEBATE/README.md` |
| common final answer after debate           | supports convergence-oriented evaluation for conversational coordination                                              | E3, E4      | `inventory/raw/PAPER-DU-2023-MULTIAGENT-DEBATE/README.md` |
| factuality and reasoning improvement claim | motivates comparison of deliberative regimes, but remains a source-specific empirical claim rather than a MOGT result | E2, E3      | `inventory/raw/PAPER-DU-2023-MULTIAGENT-DEBATE/README.md` |

## Cautions And Limits

- Debate is narrower than full negotiation and should not be treated as a complete bargaining model.
- The abstract argues for improved reasoning, but MOGT still needs explicit episode-level metrics and overhead measurement.

## Reuse Notes

- Use this source to justify bounded deliberation and disagreement-surfacing designs.
- Do not let it stand in for negotiation-specific authorities when E3 hardening begins.
