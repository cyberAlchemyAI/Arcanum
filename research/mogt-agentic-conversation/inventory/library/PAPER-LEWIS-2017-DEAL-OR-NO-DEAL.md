# Deal or No Deal? End-to-End Learning of Negotiation Dialogues — Inventory Library Entry

**Source ID:** `PAPER-LEWIS-2017-DEAL-OR-NO-DEAL`
**Reference ID:** `REF-LEWIS-2017-DEAL-OR-NO-DEAL`
**Entry Type:** `paper-abstract`
**Acquisition Mode:** `web-retrieved`
**Raw Content Paths:** `inventory/raw/PAPER-LEWIS-2017-DEAL-OR-NO-DEAL/README.md`
**Extraction Date:** `2026-04-28`
**Experiments:** `E3, E4`
**Status:** `library-grade`

## Bibliographic Record

| Field       | Value                                                                                   |
| ----------- | --------------------------------------------------------------------------------------- |
| Citation    | Lewis et al. Deal or No Deal? End-to-End Learning of Negotiation Dialogues. EMNLP 2017. |
| URL         | `https://aclanthology.org/D17-1259/`                                                    |
| Pin         | `doi:10.18653/v1/D17-1259`                                                              |
| Access Mode | open web retrieval                                                                      |

## Raw-Backed Content

### Captured Source Content

The raw provenance file preserves the ACL Anthology abstract excerpt describing semi-cooperative negotiation, a human-human negotiation dataset, end-to-end negotiation models, and dialogue rollouts that plan ahead by simulating full continuations.

## Extracted Constructs

| Construct                                      | Why It Matters                                                                                    | Experiments | Raw Anchor                                                 |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------- | ----------- | ---------------------------------------------------------- |
| semi-cooperative dialogue setting              | aligns closely with MOGT's contested conversational decision episodes                             | E3, E4      | `inventory/raw/PAPER-LEWIS-2017-DEAL-OR-NO-DEAL/README.md` |
| explicit agreement / no-deal outcome structure | supports measurable convergence and failure outcomes                                              | E3          | `inventory/raw/PAPER-LEWIS-2017-DEAL-OR-NO-DEAL/README.md` |
| hidden reward functions across participants    | motivates role-specific utility asymmetry in negotiation scenarios                                | E3          | `inventory/raw/PAPER-LEWIS-2017-DEAL-OR-NO-DEAL/README.md` |
| planning through simulated dialogue rollouts   | informs how negotiation-enabled regimes might reason about downstream conversational consequences | E3, E4      | `inventory/raw/PAPER-LEWIS-2017-DEAL-OR-NO-DEAL/README.md` |

## Cautions And Limits

- This is pre-LLM negotiation work and should be reused for structure and metrics more than for direct orchestration assumptions.
- MOGT should not assume that its conversational roles have the same utility model as the dataset without explicit adaptation.

## Reuse Notes

- Use this source to design bounded-turn negotiation scenarios, convergence outcomes, and utility-sensitive disagreement tasks.
- Keep the adaptation step explicit when moving from the original bargaining task to LLM-agent conversations.
