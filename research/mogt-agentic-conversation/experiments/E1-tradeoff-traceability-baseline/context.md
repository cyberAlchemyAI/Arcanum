# Context Bundle: E1

Tier: foundation
Primary claims: MOGT-C1

## 1. Scope and Claim Target

- Decision question: do explicit objective vectors improve decision traceability without harming acceptance quality?
- Primary claim target: MOGT-C1
- Secondary claim target: MOGT-C4

## 2. Source Role Matrix

| Source ID         | Entry Type     | Role                                        | Authority Level | Version Pin             |
| ----------------- | -------------- | ------------------------------------------- | --------------- | ----------------------- |
| PAPER-WOHLIN-2012 | paper-abstract | methodology baseline                        | primary         | book:springer-2012      |
| PAPER-MARLER-2010 | paper-abstract | theory for explicit multi-objective framing | primary         | paper:marler-arora-2010 |

## 3. Normalized Terminology Map

| Canonical Term        | Source Aliases                                     | Operational Meaning                                                    |
| --------------------- | -------------------------------------------------- | ---------------------------------------------------------------------- |
| objective vector      | utility vector, score tuple, tradeoff profile      | explicit list of active decision objectives for a candidate action     |
| traceability coverage | explanation recoverability, rationale completeness | reviewer can reconstruct objectives, tradeoff, and final action reason |
| policy regime         | baseline, intervention                             | the arbitration rule used for the run                                  |

## 4. Metric Definition Map

| Metric                | Definition                                                       | Source Field(s)            |
| --------------------- | ---------------------------------------------------------------- | -------------------------- |
| traceability_coverage | fraction of reviewed episodes with full rationale reconstruction | reviewer rubric, trace log |
| acceptance_score      | reviewer-rated acceptability of the selected action              | reviewer rubric            |
| reviewer_agreement    | agreement across reviewers on rationale reconstruction           | reviewer labels            |

## 5. Conflict Log and Resolution Decisions

| Conflict ID | Conflict Type | Resolution                                                              | Status |
| ----------- | ------------- | ----------------------------------------------------------------------- | ------ |
| E1-C1       | construct     | separate explanation recoverability from decision quality in the rubric | draft  |

## 6. Open Risks and Follow-Up Actions

1. Finalize a benchmark scenario set with comparable difficulty.
2. Define a reviewer rubric that does not reward verbosity alone.
