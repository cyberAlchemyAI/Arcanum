# MOGT Inventory Index

Purpose: index the MOGT inventory chain from authority selection to extracted knowledge to raw provenance.

## Chain-Covered Library Entries

| Source ID                             | Reference ID                        | Context                        | Library File                                                 | Raw Provenance                                                  | Acquisition Mode | Status        | Notes                                                              |
| ------------------------------------- | ----------------------------------- | ------------------------------ | ------------------------------------------------------------ | --------------------------------------------------------------- | ---------------- | ------------- | ------------------------------------------------------------------ |
| PAPER-WU-2024-AUTOGEN                 | REF-WU-2024-AUTOGEN                 | Agentic conversation prior art | `inventory/library/PAPER-WU-2024-AUTOGEN.md`                 | `inventory/raw/PAPER-WU-2024-AUTOGEN/README.md`                 | web-retrieved    | library-grade | open-access orchestration prior art with captured abstract excerpt |
| PAPER-LIU-2024-AGENTBENCH             | REF-LIU-2024-AGENTBENCH             | Agentic conversation prior art | `inventory/library/PAPER-LIU-2024-AGENTBENCH.md`             | `inventory/raw/PAPER-LIU-2024-AGENTBENCH/README.md`             | web-retrieved    | library-grade | open-access evaluation prior art with captured abstract excerpt    |
| PAPER-DU-2023-MULTIAGENT-DEBATE       | REF-DU-2023-MULTIAGENT-DEBATE       | Agentic conversation prior art | `inventory/library/PAPER-DU-2023-MULTIAGENT-DEBATE.md`       | `inventory/raw/PAPER-DU-2023-MULTIAGENT-DEBATE/README.md`       | web-retrieved    | library-grade | open-access debate prior art with captured abstract excerpt        |
| PAPER-LEWIS-2017-DEAL-OR-NO-DEAL      | REF-LEWIS-2017-DEAL-OR-NO-DEAL      | Agentic conversation prior art | `inventory/library/PAPER-LEWIS-2017-DEAL-OR-NO-DEAL.md`      | `inventory/raw/PAPER-LEWIS-2017-DEAL-OR-NO-DEAL/README.md`      | web-retrieved    | library-grade | open-access negotiation prior art with captured abstract excerpt   |
| PAPER-GUO-2024-LLM-MULTIAGENTS-SURVEY | REF-GUO-2024-LLM-MULTIAGENTS-SURVEY | Agentic conversation prior art | `inventory/library/PAPER-GUO-2024-LLM-MULTIAGENTS-SURVEY.md` | `inventory/raw/PAPER-GUO-2024-LLM-MULTIAGENTS-SURVEY/README.md` | web-retrieved    | library-grade | open-access survey prior art with captured abstract excerpt        |
| REPORT-DOSHI-VELEZ-KIM-2017           | REF-DOSHI-VELEZ-KIM-2017            | MOGT methodology and theory    | `inventory/library/REPORT-DOSHI-VELEZ-KIM-2017.md`           | `inventory/raw/REPORT-DOSHI-VELEZ-KIM-2017/README.md`           | web-retrieved    | library-grade | open-access evaluation authority with captured abstract excerpt    |

## Awaiting Raw-Backed Library Entries

| Source ID                 | Reference ID            | Context                     | Current Rollup                         | Status       | Notes                                                              |
| ------------------------- | ----------------------- | --------------------------- | -------------------------------------- | ------------ | ------------------------------------------------------------------ |
| PAPER-WOHLIN-2012         | REF-WOHLIN-2012         | MOGT methodology and theory | `inventory/methodology-authorities.md` | awaiting-raw | paywalled methodology authority                                    |
| PAPER-DEB-2001            | REF-DEB-2001            | MOGT methodology and theory | `inventory/theory-baseline.md`         | awaiting-raw | paywalled theory authority                                         |
| BOOK-KEENEY-RAIFFA-1976   | REF-KEENEY-RAIFFA-1976  | MOGT methodology and theory | `inventory/theory-baseline.md`         | awaiting-raw | paywalled theory authority                                         |
| PAPER-MARLER-2010         | REF-MARLER-2010         | MOGT methodology and theory | `inventory/theory-baseline.md`         | awaiting-raw | scope still being normalized and raw content not preserved locally |
| PAPER-WALKER-1997         | REF-WALKER-1997         | MOGT methodology and theory | `inventory/methodology-authorities.md` | awaiting-raw | open retrieval not yet preserved in this pass                      |
| BOOK-JAIN-1991            | REF-JAIN-1991           | MOGT methodology and theory | `inventory/methodology-authorities.md` | awaiting-raw | paywalled measurement authority                                    |
| PAPER-HART-STAVELAND-1988 | REF-HART-STAVELAND-1988 | MOGT methodology and theory | `inventory/methodology-authorities.md` | awaiting-raw | paywalled workload authority                                       |
| PAPER-WOOLDRIDGE-2009     | REF-WOOLDRIDGE-2009     | MOGT methodology and theory | `inventory/theory-baseline.md`         | awaiting-raw | second-wave theory source                                          |
| PAPER-NASH-1950           | REF-NASH-1950           | MOGT methodology and theory | `inventory/theory-baseline.md`         | awaiting-raw | second-wave theory source                                          |

## Thematic Rollup Views

| Context                        | Artifact                                      | Role                      | Status  | Notes                                                                                                        |
| ------------------------------ | --------------------------------------------- | ------------------------- | ------- | ------------------------------------------------------------------------------------------------------------ |
| MOGT methodology and theory    | `inventory/methodology-authorities.md`        | secondary thematic rollup | partial | some open sources now have per-source backing; several book and paywalled sources still await raw provenance |
| MOGT methodology and theory    | `inventory/theory-baseline.md`                | secondary thematic rollup | partial | still mostly planning-oriented until raw-backed entries are added                                            |
| Agentic conversation prior art | `inventory/agentic-conversation-prior-art.md` | secondary thematic rollup | backed  | first-wave prior-art pack now backed by per-source library entries                                           |

## Usage Notes

1. Use `inventory/library/<source-id>.md` as the content authority for extracted knowledge.
2. Use `inventory/raw/<source-id>/...` as the provenance base for that extracted knowledge.
3. Use thematic rollups for fast human orientation only.
4. Keep source IDs synchronized with `sources/SOURCE-CATALOG.md` and `sources/REFERENCE-LEDGER.md`.
5. When web retrieval is not possible, request raw files from the user and record the dependency in `inventory/raw/NEEDS-USER-RAW.md`.
