# AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation — Inventory Library Entry

**Source ID:** `PAPER-WU-2024-AUTOGEN`
**Reference ID:** `REF-WU-2024-AUTOGEN`
**Entry Type:** `paper-abstract`
**Acquisition Mode:** `web-retrieved`
**Raw Content Paths:** `inventory/raw/PAPER-WU-2024-AUTOGEN/README.md`
**Extraction Date:** `2026-04-28`
**Experiments:** `E1, E3, E4`
**Status:** `library-grade`

## Bibliographic Record

| Field       | Value                                                                               |
| ----------- | ----------------------------------------------------------------------------------- |
| Citation    | Wu et al. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. |
| URL         | `https://arxiv.org/abs/2308.08155v2`                                                |
| Pin         | `arxiv:2308.08155v2`                                                                |
| Access Mode | open web retrieval                                                                  |

## Raw-Backed Content

### Captured Source Content

The raw provenance file preserves the abstract excerpt describing AutoGen as an open-source framework for building LLM applications via multiple conversable agents, with flexible interaction behaviors programmed through natural language and code.

## Extracted Constructs

| Construct                                       | Why It Matters                                                                                       | Experiments | Raw Anchor                                      |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------- | ----------------------------------------------- |
| role-based multi-agent conversation             | gives MOGT a concrete prior-art frame for conversational role interaction                            | E1, E3, E4  | `inventory/raw/PAPER-WU-2024-AUTOGEN/README.md` |
| turn-level orchestration and handoff            | supports the idea that decision episodes can be structured by explicit conversational policies       | E1, E3, E4  | `inventory/raw/PAPER-WU-2024-AUTOGEN/README.md` |
| customizable agent interaction behaviors        | justifies comparing alternative policy regimes rather than treating one orchestration style as fixed | E1, E3, E4  | `inventory/raw/PAPER-WU-2024-AUTOGEN/README.md` |
| inspectable intermediate conversation artifacts | supports MOGT's emphasis on traceability and reviewability                                           | E1          | `inventory/raw/PAPER-WU-2024-AUTOGEN/README.md` |

## Cautions And Limits

- AutoGen is strong orchestration prior art, not a methodology authority for threshold setting.
- The abstract establishes framework breadth and flexibility more strongly than controlled comparative evaluation.

## Reuse Notes

- Use this source to justify why multi-agent conversational orchestration is a legitimate experimental setting for MOGT.
- Do not use it alone to justify empirical success claims about a particular decision policy.
