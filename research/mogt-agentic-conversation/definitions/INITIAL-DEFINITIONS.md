# Initial Definitions

## Terminology

| Term                          | Working Definition                                                                  | Type         | Status | Evidence Type |
| ----------------------------- | ----------------------------------------------------------------------------------- | ------------ | ------ | ------------- |
| agentic conversation decision | a bounded decision episode inside a multi-role agent interaction                    | construct    | draft  | stated        |
| objective vector              | explicit per-action tradeoff representation across active objectives                | construct    | draft  | hypothesized  |
| Pareto-aware arbitration      | policy that filters or ranks candidate actions using nondominance before tie-break  | intervention | draft  | hypothesized  |
| conversation game             | strategic interaction among roles with aligned or partially conflicting preferences | construct    | draft  | hypothesized  |
| negotiation stability         | bounded-turn convergence without repeated conflict cycles                           | metric       | draft  | hypothesized  |
| overhead envelope             | acceptable cost, latency, and review burden bound for policy adoption               | metric       | draft  | stated        |

## Research Constructs

| Construct               | Description                                            | Observable Proxy                                            | Status |
| ----------------------- | ------------------------------------------------------ | ----------------------------------------------------------- | ------ |
| decision traceability   | how inspectable a decision is after the fact           | reviewer reconstruction success                             | draft  |
| multi-objective quality | how well a selected action balances competing goals    | blinded reviewer quality score and dominance classification | draft  |
| disagreement stability  | whether contested conversations converge without churn | turn count, cycle count, escalation count                   | draft  |
| operational feasibility | whether benefits justify additional reasoning cost     | token cost, latency, reviewer burden                        | draft  |

## Candidate Claims And Propositions

| ID  | Type        | Statement                                                                              | Status |
| --- | ----------- | -------------------------------------------------------------------------------------- | ------ |
| P1  | proposition | Explicit objective logging improves ex post reasoning about conversational decisions.  | draft  |
| P2  | proposition | Dominance-aware selection avoids clearly inferior actions in multi-objective settings. | draft  |
| P3  | proposition | Structured negotiation can reduce arbitrary escalation in role conflict.               | draft  |
| H1  | hypothesis  | Objective vectors increase traceability without reducing quality.                      | draft  |
| H2  | hypothesis  | Pareto-aware arbitration improves decision quality over heuristics.                    | draft  |
| H3  | hypothesis  | Negotiation policies reduce unresolved disagreement.                                   | draft  |
| H4  | hypothesis  | Practical gains disappear beyond a bounded overhead envelope.                          | draft  |

## Units Of Analysis

| Unit                    | Why This Unit                                 | Likely Data Source                | Status    |
| ----------------------- | --------------------------------------------- | --------------------------------- | --------- |
| decision episode        | primary object of intervention and evaluation | benchmark conversation trace      | candidate |
| contested turn sequence | captures disagreement dynamics                | conversation log with turn labels | candidate |
| policy run              | needed for cost and latency measurement       | JSONL telemetry row               | candidate |

## Constraints

| Constraint                              | Category  | Impact                                     | Status |
| --------------------------------------- | --------- | ------------------------------------------ | ------ |
| source normalization not complete       | access    | blocks G2 for live execution               | known  |
| no benchmark corpus yet                 | tooling   | delays first empirical run                 | known  |
| objective calibration may be subjective | construct | threatens validity if scoring is unstable  | known  |
| reviewer burden may be high             | cost      | limits feasible sample size in early waves | known  |

## Ambiguities To Resolve

| Topic                 | Why Ambiguous                                                                                         | Resolution Needed                              |
| --------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| default objective set | some experiments may need four objectives while others need five                                      | choose baseline objective family for E1 and E2 |
| negotiation mechanism | multiple candidate mechanisms exist: bargaining, concession schedule, voting, or escalation threshold | select first-wave policy family for E3         |
| benchmark source      | synthetic scenarios and historical traces have different validity tradeoffs                           | define first benchmark corpus strategy         |
