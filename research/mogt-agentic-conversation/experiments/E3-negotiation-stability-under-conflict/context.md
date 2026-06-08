# Context Bundle: E3

Tier: foundation
Primary claims: MOGT-C3

## 1. Scope and Claim Target

- Decision question: does negotiation-aware disagreement handling reduce unresolved conflict in bounded-turn agent conversations?
- Primary claim target: MOGT-C3
- Secondary claim target: MOGT-C4

## 2. Source Role Matrix

| Source ID             | Entry Type     | Role                                | Authority Level | Version Pin          |
| --------------------- | -------------- | ----------------------------------- | --------------- | -------------------- |
| PAPER-WOHLIN-2012     | paper-abstract | methodology baseline                | primary         | book:springer-2012   |
| PAPER-WOOLDRIDGE-2009 | paper-abstract | multi-agent coordination framing    | supporting      | book:wooldridge-2009 |
| PAPER-NASH-1950       | paper-abstract | bargaining and equilibrium baseline | supporting      | paper:nash-1950      |

## 3. Normalized Terminology Map

| Canonical Term        | Source Aliases                            | Operational Meaning                                             |
| --------------------- | ----------------------------------------- | --------------------------------------------------------------- |
| negotiation stability | convergence, bounded-turn agreement       | resolution without repeated conflict cycles                     |
| escalation            | handoff, override                         | leaving the current agent conversation for external arbitration |
| contested scenario    | disagreement case, conflicting incentives | scenario where roles prefer different actions                   |

## 4. Metric Definition Map

| Metric             | Definition                                                        | Source Field(s)        |
| ------------------ | ----------------------------------------------------------------- | ---------------------- |
| convergence_rate   | fraction of contested episodes that resolve inside the turn limit | turn log, final status |
| cycle_count        | number of repeated conflict loops per episode                     | turn log               |
| resolution_quality | reviewer quality score for the final decision                     | reviewer rubric        |

## 5. Conflict Log and Resolution Decisions

| Conflict ID | Conflict Type | Resolution                                                            | Status |
| ----------- | ------------- | --------------------------------------------------------------------- | ------ |
| E3-C1       | mechanism     | first-wave protocol should use one bounded negotiation mechanism only | draft  |

## 6. Open Risks and Follow-Up Actions

1. Choose one negotiation mechanism before protocol lock.
2. Ensure convergence is not rewarded when it results in low-quality forced decisions.
