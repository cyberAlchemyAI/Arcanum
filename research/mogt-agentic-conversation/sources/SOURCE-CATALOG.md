# MOGT Source Catalog

Purpose: track candidate and selected authority sources for the MOGT project before experiment-specific source bundles are finalized.

## Context A - MOGT Methodology and Theory

| Source ID                   | Kind          | Short Label                            | Relevance | Access            | Pin                               | Status    | Notes                                                                                         |
| --------------------------- | ------------- | -------------------------------------- | --------- | ----------------- | --------------------------------- | --------- | --------------------------------------------------------------------------------------------- |
| PAPER-WOHLIN-2012           | methodology   | Wohlin experimentation handbook        | high      | paywalled         | book:springer-2012                | selected  | baseline empirical software engineering method authority; inventory linked                    |
| PAPER-DEB-2001              | theory        | Deb multi-objective optimization       | high      | paywalled         | book:deb-2001                     | selected  | Pareto-front and dominance baseline for E2 and E4; inventory linked                           |
| PAPER-MARLER-2010           | theory        | Marler and Arora weighted-sum insights | high      | paywalled         | doi:10.1007/s00158-009-0460-7     | candidate | keep as candidate until the 2004 survey versus 2010 weighted-sum scope is resolved explicitly |
| BOOK-KEENEY-RAIFFA-1976     | theory        | Keeney and Raiffa value tradeoffs      | high      | paywalled         | book:wiley-1976-keeney-raiffa     | selected  | objective structuring and value-tradeoff authority for E1 and E2                              |
| REPORT-DOSHI-VELEZ-KIM-2017 | evaluation    | interpretability evaluation report     | high      | accessible open   | arxiv:1702.08608v2                | selected  | rigorous evaluation framing for traceability and explainability rubrics                       |
| PAPER-WALKER-1997           | evaluation    | PARADISE dialogue evaluation           | high      | accessible open   | doi:10.3115/976909.979652         | selected  | dialogue and decision-episode evaluation baseline for acceptance and task-cost tradeoffs      |
| BOOK-JAIN-1991              | overhead      | performance analysis handbook          | high      | paywalled         | book:jain-1991                    | selected  | overhead, latency, and measurement-discipline baseline for E4                                 |
| PAPER-HART-STAVELAND-1988   | human-factors | NASA-TLX workload baseline             | medium    | paywalled         | doi:10.1016/S0166-4115(08)62386-9 | selected  | reviewer-burden and subjective workload instrument for E4                                     |
| PAPER-WOOLDRIDGE-2009       | theory        | Wooldridge multiagent systems          | medium    | pending retrieval | book:wooldridge-2009              | candidate | multi-agent coordination framing                                                              |
| PAPER-NASH-1950             | theory        | Nash bargaining / equilibrium baseline | medium    | pending retrieval | paper:nash-1950                   | candidate | game-theoretic stability reference                                                            |

## Context B - Agentic Conversation Prior Art

| Source ID                             | Kind                 | Short Label                           | Relevance | Access          | Pin                      | Status   | Notes                                                                         |
| ------------------------------------- | -------------------- | ------------------------------------- | --------- | --------------- | ------------------------ | -------- | ----------------------------------------------------------------------------- |
| PAPER-WU-2024-AUTOGEN                 | agentic-conversation | AutoGen multi-agent conversation      | high      | accessible open | arxiv:2308.08155v2       | selected | orchestration and role-handoff prior art for E1, E3, and E4                   |
| PAPER-LIU-2024-AGENTBENCH             | evaluation           | AgentBench agent evaluation           | high      | accessible open | arxiv:2308.03688v3       | selected | benchmark and evaluation framing for agentic decision tasks in E1, E2, and E4 |
| PAPER-DU-2023-MULTIAGENT-DEBATE       | agentic-conversation | Multiagent Debate                     | medium    | accessible open | arxiv:2305.14325v1       | selected | debate-style coordination prior art for E2, E3, and E4                        |
| PAPER-LEWIS-2017-DEAL-OR-NO-DEAL      | negotiation          | Deal or No Deal negotiation dialogues | high      | accessible open | doi:10.18653/v1/D17-1259 | selected | negotiation and convergence framing for E3 and E4                             |
| PAPER-GUO-2024-LLM-MULTIAGENTS-SURVEY | survey               | LLM-based multi-agents survey         | high      | accessible open | arxiv:2402.01680v2       | selected | landscape map for orchestration, evaluation, and failure modes across E1-E4   |

## Normalization Notes

1. MOGT references are organized into two contexts: `MOGT methodology and theory` and `agentic conversation prior art`.
2. `PAPER-MARLER-2010` is pinned to the weighted-sum paper, not a general survey. Keep it for E2 and E4 when discussing weighted-sum baselines or weighted-sum failure modes.
3. If MOGT needs broader method-family framing beyond weighted-sum itself, add the Marler and Arora survey as a separate source rather than overloading `PAPER-MARLER-2010`.
4. Agentic-conversation prior art should guide policy-regime design, orchestration assumptions, and external-validity framing; it should not replace the methodology and theory authorities used for protocol thresholds and claim updates.

## Selection Rules

1. Promote a source to `selected` only when it has a stable pin and a clear usage scope.
2. Any source used as protocol authority must also appear in `sources/REFERENCE-LEDGER.md`.
3. Prefer sources that define concepts in a reusable way rather than only reporting one-off task performance.
