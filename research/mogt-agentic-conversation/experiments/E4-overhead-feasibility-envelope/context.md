# Context Bundle: E4

Tier: foundation
Primary claims: MOGT-C4

## 1. Scope and Claim Target

- Decision question: at what point does added policy complexity make the approach operationally unattractive?
- Primary claim target: MOGT-C4
- Secondary claim target: MOGT-C2

## 2. Source Role Matrix

| Source ID         | Entry Type     | Role                                      | Authority Level | Version Pin             |
| ----------------- | -------------- | ----------------------------------------- | --------------- | ----------------------- |
| PAPER-WOHLIN-2012 | paper-abstract | measurement baseline                      | primary         | book:springer-2012      |
| PAPER-MARLER-2010 | paper-abstract | multi-objective method comparison context | primary         | paper:marler-arora-2010 |

## 3. Normalized Terminology Map

| Canonical Term    | Source Aliases                   | Operational Meaning                                                   |
| ----------------- | -------------------------------- | --------------------------------------------------------------------- |
| overhead envelope | operating region, feasible bound | the maximum acceptable token, latency, and review burden for adoption |
| objective count   | dimensionality                   | number of active objectives in the decision vector                    |
| negotiation depth | rounds, deliberation depth       | number of explicit conflict-resolution turns allowed                  |

## 4. Metric Definition Map

| Metric                       | Definition                                                                          | Source Field(s)                       |
| ---------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------- |
| overhead_acceptability_ratio | fraction of runs inside allowed overhead thresholds                                 | token count, latency, reviewer burden |
| quality_retention            | decision quality relative to simpler baseline regimes                               | reviewer quality score                |
| breakpoint_index             | first tested setting where overhead becomes unacceptable or quality gain disappears | run configuration, metric table       |

## 5. Conflict Log and Resolution Decisions

| Conflict ID | Conflict Type | Resolution                                                                             | Status |
| ----------- | ------------- | -------------------------------------------------------------------------------------- | ------ |
| E4-C1       | threshold     | quality and overhead thresholds must be fixed before analysis to avoid post hoc tuning | draft  |

## 6. Open Risks and Follow-Up Actions

1. Set a project-specific acceptable latency and token budget before live runs.
2. Avoid declaring a breakpoint from too narrow a model or scenario sample.
