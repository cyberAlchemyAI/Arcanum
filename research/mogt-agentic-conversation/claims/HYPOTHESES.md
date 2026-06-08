# Hypotheses

## Hypothesis Register

| ID  | Hypothesis                                                                                                           | Decision It Informs                                                       | Confidence | Status   |
| --- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------- | -------- |
| H1  | Explicit objective vectors increase decision traceability without degrading acceptance quality.                      | whether to add objective-vector logging and scoring to the orchestrator   | medium     | proposed |
| H2  | Pareto-aware arbitration reduces dominated decisions compared with heuristic or weighted-sum baselines.              | whether to invest in Pareto-front decision logic                          | medium     | proposed |
| H3  | Negotiation policies grounded in game-theoretic stability cues reduce unresolved conflict and turn cycling.          | whether disagreement handling should become a first-class policy module   | low        | proposed |
| H4  | Benefits from multi-objective and game-theoretic policies remain worthwhile only within a bounded overhead envelope. | whether the approach is operationally feasible beyond research prototypes | medium     | proposed |

## Hypothesis Details

### H1 - Traceable Tradeoff Decisions

- Statement: Explicit objective vectors and per-turn tradeoff logging increase reviewer traceability coverage relative to implicit heuristic arbitration while preserving acceptable decision quality.
- Related proposition: P1
- Decision owner: orchestration architect
- Expected signal: higher traceability coverage and higher reviewer agreement on why a decision was taken
- Data needed: benchmark conversation episodes with blinded reviewer scoring and policy traces
- Existing evidence: none
- Why this might be true: explicit objectives externalize the decision rationale and reduce post hoc reconstruction
- Strongest counterargument: better explanations can be added to heuristics without changing the decision policy itself
- Key confounders: model explanation quality, reviewer fatigue, scenario difficulty
- Disconfirming result: traceability improves but reviewer-rated decision quality or acceptance falls materially
- Protocol readiness: ready

### H2 - Pareto-Aware Arbitration Quality

- Statement: Pareto-aware or dominance-aware selection chooses fewer dominated actions and yields better multi-objective outcomes than single-score heuristic arbitration.
- Related proposition: P2
- Decision owner: orchestration architect
- Expected signal: lower dominated-selection rate and lower regret against ex post reviewer frontier judgments
- Data needed: comparable scenario set with policy variants and objective-score annotations
- Existing evidence: none
- Why this might be true: Pareto filtering prevents policies from choosing options that are clearly worse on all relevant objectives
- Strongest counterargument: objective estimates are noisy, so Pareto reasoning may amplify measurement error rather than improve decisions
- Key confounders: objective calibration quality, policy prompt wording, scenario heterogeneity
- Disconfirming result: Pareto-aware policies show no advantage or increase regret under blinded review
- Protocol readiness: ready

### H3 - Negotiation Stability Under Conflict

- Statement: Game-theoretic negotiation policies reduce oscillation and unresolved disagreement when specialist agents hold partially conflicting preferences.
- Related proposition: P3
- Decision owner: evaluation owner
- Expected signal: fewer cyclic disagreements, fewer escalations, and faster convergence to bounded-turn decisions
- Data needed: structured conflict scenarios with role-specific utility asymmetries and turn-level traces
- Existing evidence: none
- Why this might be true: stability-aware negotiation gives agents a disciplined mechanism for concessions and escalation thresholds
- Strongest counterargument: added negotiation steps only create more chatter and do not change the underlying model behavior
- Key confounders: role prompt strength, fixed versus adaptive concessions, scenario ambiguity
- Disconfirming result: conflict resolution takes more turns without materially reducing unresolved outcomes
- Protocol readiness: needs refinement

### H4 - Practical Feasibility Envelope

- Statement: The approach is only viable if objective dimensionality and deliberation rounds stay within a bounded token, latency, and human-review overhead envelope.
- Related proposition: P4
- Decision owner: research operator
- Expected signal: a clear breakpoint after which marginal quality gains are outweighed by overhead growth
- Data needed: cost, latency, and reviewer burden data across increasing objective counts and negotiation depth
- Existing evidence: none
- Why this might be true: more objectives and more bargaining steps improve deliberation only up to a point before overhead dominates
- Strongest counterargument: high-capability models absorb added reasoning cheaply enough that the overhead concern is overstated
- Key confounders: model selection, caching, prompt compression, scenario reuse
- Disconfirming result: quality keeps improving meaningfully with no practical overhead cliff in the tested range
- Protocol readiness: ready

## Prioritization

| Hypothesis ID | Decision Urgency | Test Cost | Expected Learning | Priority |
| ------------- | ---------------- | --------- | ----------------- | -------- |
| H1            | high             | medium    | high              | now      |
| H2            | high             | medium    | high              | now      |
| H3            | medium           | medium    | medium            | later    |
| H4            | high             | low       | high              | now      |
