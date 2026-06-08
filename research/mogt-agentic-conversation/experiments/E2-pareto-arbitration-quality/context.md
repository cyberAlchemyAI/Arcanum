# Context Bundle: E2

Tier: foundation
Primary claims: MOGT-C2

## 1. Scope and Claim Target

- Decision question: does Pareto-aware arbitration outperform heuristic or weighted-sum baselines on multi-objective decision quality?
- Primary claim target: MOGT-C2
- Secondary claim target: MOGT-C4

## 2. Source Role Matrix

| Source ID         | Entry Type     | Role                                             | Authority Level | Version Pin             |
| ----------------- | -------------- | ------------------------------------------------ | --------------- | ----------------------- |
| PAPER-WOHLIN-2012 | paper-abstract | comparative-experiment methodology               | primary         | book:springer-2012      |
| PAPER-DEB-2001    | paper-abstract | Pareto and multi-objective optimization baseline | primary         | book:deb-2001           |
| PAPER-MARLER-2010 | paper-abstract | practical multi-objective method comparison      | primary         | paper:marler-arora-2010 |

## 3. Normalized Terminology Map

| Canonical Term  | Source Aliases                         | Operational Meaning                                                          |
| --------------- | -------------------------------------- | ---------------------------------------------------------------------------- |
| Pareto frontier | nondominated set, efficient set        | actions not strictly dominated on the active objective vector                |
| regret          | decision regret, opportunity loss      | difference between selected action quality and best reviewed frontier action |
| policy regime   | heuristic, weighted-sum, Pareto-guided | intervention arm under comparison                                            |

## 4. Metric Definition Map

| Metric                   | Definition                                                         | Source Field(s)                      |
| ------------------------ | ------------------------------------------------------------------ | ------------------------------------ |
| dominated_selection_rate | fraction of episodes where the chosen action is strictly dominated | objective annotations, chosen action |
| decision_quality_score   | reviewer-rated quality of the chosen action                        | reviewer rubric                      |
| frontier_regret          | quality gap to the best reviewer-accepted frontier action          | reviewer rubric, frontier labels     |

## 5. Conflict Log and Resolution Decisions

| Conflict ID | Conflict Type | Resolution                                                                         | Status |
| ----------- | ------------- | ---------------------------------------------------------------------------------- | ------ |
| E2-C1       | construct     | keep objective-score derivation visible so dominance classification can be audited | draft  |

## 6. Open Risks and Follow-Up Actions

1. Calibrate objective weights and scales before comparing weighted-sum to Pareto-guided regimes.
2. Prevent benchmark designers from encoding one regime's assumptions into the scenario labels.
