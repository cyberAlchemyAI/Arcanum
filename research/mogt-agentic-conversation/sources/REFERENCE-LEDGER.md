# MOGT Reference Ledger

Purpose: operational registry of references used as authority in protocols, analysis, and claim adjudication.

## Context A - MOGT Methodology and Theory

| Reference ID             | Citation (Short)                                                                                             | Authority Level | Usage Scope   | Source ID                   | Pin                               | Status                | Notes                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------------------ | --------------- | ------------- | --------------------------- | --------------------------------- | --------------------- | -------------------------------------------------------------------------------------------- |
| REF-WOHLIN-2012          | Wohlin et al. Experimentation in Software Engineering                                                        | primary         | methodology   | PAPER-WOHLIN-2012           | book:springer-2012                | operationalized       | first-wave foundation methodology authority                                                  |
| REF-DEB-2001             | Deb. Multi-Objective Optimization Using Evolutionary Algorithms                                              | primary         | theory        | PAPER-DEB-2001              | book:deb-2001                     | operationalized       | Pareto-front and dominance baseline for E2 and E4                                            |
| REF-MARLER-2010          | Marler and Arora. The Weighted Sum Method for Multi-Objective Optimization: New Insights                     | supporting      | theory        | PAPER-MARLER-2010           | doi:10.1007/s00158-009-0460-7     | pending normalization | current MOGT wording treated this as a broad survey; resolve intended scope before promotion |
| REF-KEENEY-RAIFFA-1976   | Keeney and Raiffa. Decisions with Multiple Objectives: Preferences and Value Tradeoffs                       | supporting      | theory        | BOOK-KEENEY-RAIFFA-1976     | book:wiley-1976-keeney-raiffa     | operationalized       | objective articulation and value-tradeoff framing for E1 and E2                              |
| REF-DOSHI-VELEZ-KIM-2017 | Doshi-Velez and Kim. Towards A Rigorous Science of Interpretable Machine Learning                            | supporting      | evaluation    | REPORT-DOSHI-VELEZ-KIM-2017 | arxiv:1702.08608v2                | operationalized       | evaluation framing for traceability and explainability rubrics                               |
| REF-WALKER-1997          | Walker et al. PARADISE: A Framework for Evaluating Spoken Dialogue Agents                                    | supporting      | evaluation    | PAPER-WALKER-1997           | doi:10.3115/976909.979652         | operationalized       | dialogue and decision-episode evaluation baseline                                            |
| REF-JAIN-1991            | Jain. The Art of Computer Systems Performance Analysis                                                       | primary         | overhead      | BOOK-JAIN-1991              | book:jain-1991                    | operationalized       | measurement discipline for latency, cost, and breakpoint analysis                            |
| REF-HART-STAVELAND-1988  | Hart and Staveland. Development of NASA-TLX (Task Load Index): Results of Empirical and Theoretical Research | supporting      | human-factors | PAPER-HART-STAVELAND-1988   | doi:10.1016/S0166-4115(08)62386-9 | operationalized       | reviewer workload baseline adapted for evaluation burden                                     |
| REF-WOOLDRIDGE-2009      | Wooldridge. An Introduction to MultiAgent Systems                                                            | supporting      | theory        | PAPER-WOOLDRIDGE-2009       | book:wooldridge-2009              | pending normalization | coordination and agent interaction framing                                                   |
| REF-NASH-1950            | Nash. Equilibrium and bargaining baseline                                                                    | supporting      | theory        | PAPER-NASH-1950             | paper:nash-1950                   | pending normalization | negotiation-stability framing                                                                |

## Context B - Agentic Conversation Prior Art

| Reference ID                        | Citation (Short)                                                                        | Authority Level | Usage Scope          | Source ID                             | Pin                      | Status          | Notes                                                                       |
| ----------------------------------- | --------------------------------------------------------------------------------------- | --------------- | -------------------- | ------------------------------------- | ------------------------ | --------------- | --------------------------------------------------------------------------- |
| REF-WU-2024-AUTOGEN                 | Wu et al. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation      | primary         | agentic-conversation | PAPER-WU-2024-AUTOGEN                 | arxiv:2308.08155v2       | operationalized | orchestration and role-handoff prior art for E1, E3, and E4                 |
| REF-LIU-2024-AGENTBENCH             | Liu et al. AgentBench: Evaluating LLMs as Agents                                        | primary         | evaluation           | PAPER-LIU-2024-AGENTBENCH             | arxiv:2308.03688v3       | operationalized | evaluation framing for agentic decision tasks in E1, E2, and E4             |
| REF-DU-2023-MULTIAGENT-DEBATE       | Du et al. Improving Factuality and Reasoning through Multiagent Debate                  | supporting      | agentic-conversation | PAPER-DU-2023-MULTIAGENT-DEBATE       | arxiv:2305.14325v1       | operationalized | debate-style coordination prior art for E2, E3, and E4                      |
| REF-LEWIS-2017-DEAL-OR-NO-DEAL      | Lewis et al. Deal or No Deal? End-to-End Learning of Negotiation Dialogues              | primary         | negotiation          | PAPER-LEWIS-2017-DEAL-OR-NO-DEAL      | doi:10.18653/v1/D17-1259 | operationalized | negotiation structure and convergence framing for E3 and E4                 |
| REF-GUO-2024-LLM-MULTIAGENTS-SURVEY | Guo et al. Large Language Model based Multi-Agents: A Survey of Progress and Challenges | supporting      | agentic-conversation | PAPER-GUO-2024-LLM-MULTIAGENTS-SURVEY | arxiv:2402.01680v2       | operationalized | landscape map for orchestration, evaluation, and failure modes across E1-E4 |

## Authority Levels

- primary: required to justify protocol criteria or claim update decisions
- supporting: used for triangulation or interpretive support
- fallback: optional backup when primary sources are unavailable

## Status Values

- operationalized: source ID + pin + inventory linkage complete
- pending normalization: citation exists but not yet source-cataloged and fully inventorized
- waived: accepted temporary exception with rationale
