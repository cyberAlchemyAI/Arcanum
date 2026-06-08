# AgentBench: Evaluating LLMs as Agents — Inventory Library Entry

**Source ID:** `PAPER-LIU-2024-AGENTBENCH`
**Reference ID:** `REF-LIU-2024-AGENTBENCH`
**Entry Type:** `paper-abstract`
**Acquisition Mode:** `web-retrieved`
**Raw Content Paths:** `inventory/raw/PAPER-LIU-2024-AGENTBENCH/README.md`
**Extraction Date:** `2026-04-28`
**Experiments:** `E1, E2, E4`
**Status:** `library-grade`

## Bibliographic Record

| Field       | Value                                             |
| ----------- | ------------------------------------------------- |
| Citation    | Liu et al. AgentBench: Evaluating LLMs as Agents. |
| URL         | `https://arxiv.org/abs/2308.03688v3`              |
| Pin         | `arxiv:2308.03688v3`                              |
| Access Mode | open web retrieval                                |

## Raw-Backed Content

### Captured Source Content

The raw provenance file preserves the abstract excerpt describing AgentBench as a multi-dimensional benchmark across eight environments for evaluating LLMs as agents, with explicit discussion of typical failure modes such as weak long-term reasoning, decision-making, and instruction following.

## Extracted Constructs

| Construct                                            | Why It Matters                                                             | Experiments | Raw Anchor                                          |
| ---------------------------------------------------- | -------------------------------------------------------------------------- | ----------- | --------------------------------------------------- |
| benchmark-oriented agent evaluation                  | supports controlled evaluation framing for MOGT decision episodes          | E1, E2, E4  | `inventory/raw/PAPER-LIU-2024-AGENTBENCH/README.md` |
| multi-environment evaluation discipline              | reinforces that policy claims should survive across multiple task families | E1, E2, E4  | `inventory/raw/PAPER-LIU-2024-AGENTBENCH/README.md` |
| failure-mode analysis for agents                     | helps MOGT discuss where conversational policies break down                | E1, E2, E4  | `inventory/raw/PAPER-LIU-2024-AGENTBENCH/README.md` |
| gap between strong commercial and weaker open models | reminds MOGT to separate policy effects from base-model capability effects | E1, E2, E4  | `inventory/raw/PAPER-LIU-2024-AGENTBENCH/README.md` |

## Cautions And Limits

- AgentBench is strongest as an evaluation and benchmark authority, not as a theory source for multi-objective reasoning.
- The abstract points at failure categories, but experiment-specific adaptation is still needed for conversational decision episodes.

## Reuse Notes

- Use this source to justify rigorous evaluation framing and controlled task comparisons.
- Use it to motivate benchmark-style decision tasks rather than unrestricted chat transcripts.
