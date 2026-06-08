# Experiment Candidates

## Candidate Register

| ID   | Hypothesis | Method Shape | Primary Signal               | Feasibility | Priority |
| ---- | ---------- | ------------ | ---------------------------- | ----------- | -------- |
| EX-1 | H1         | comparison   | traceability coverage        | high        | now      |
| EX-2 | H2         | comparison   | dominated-selection rate     | high        | now      |
| EX-3 | H3         | intervention | convergence rate             | medium      | later    |
| EX-4 | H4         | observation  | overhead acceptability ratio | high        | now      |

## Candidate Details

### EX-1 - Tradeoff Traceability Baseline

- Linked hypothesis: H1
- Decision owner: orchestration architect
- Research question: do explicit objective vectors make conversation decisions materially easier to inspect and justify?
- Method shape: comparison
- Unit of analysis: conversation decision episode
- Data source candidates: benchmark decision scenarios with policy traces and blinded reviewers
- Primary signal: traceability coverage
- Secondary signals: reviewer agreement, decision acceptance score
- Expected effect or finding: objective-vector traces outperform heuristic traces on reviewer reconstruction
- Strongest rival explanation: better logging alone explains any gain
- Disconfirming outcome: traceability coverage does not improve or reviewer-rated quality falls sharply
- Feasibility blockers: benchmark corpus and review rubric not yet finalized
- Minimum gate path: G1 measurable traceability criteria, G2 method + theory sources pinned, G3 review rubric inventorized, G4 trace schema validated
- Recommended next step: design first benchmark corpus and dry-run protocol

### EX-2 - Pareto Arbitration Quality

- Linked hypothesis: H2
- Decision owner: orchestration architect
- Research question: does Pareto-aware arbitration choose better actions than heuristic or weighted-sum baselines?
- Method shape: comparison
- Unit of analysis: policy-scored decision episode
- Data source candidates: replayable benchmark scenarios with annotated objective vectors
- Primary signal: dominated-selection rate
- Secondary signals: decision quality score, frontier regret
- Expected effect or finding: Pareto-aware policies select fewer dominated actions and maintain or improve reviewer quality
- Strongest rival explanation: objective scores are too noisy for Pareto reasoning to help
- Disconfirming outcome: no quality advantage over baselines under blinded review
- Feasibility blockers: objective scoring rubric still needs calibration
- Minimum gate path: G1 objective definitions explicit, G2 optimization sources pinned, G3 benchmark inventory ready, G4 run schema validated
- Recommended next step: refine protocol and benchmark objective scoring

### EX-3 - Negotiation Stability Under Conflict

- Linked hypothesis: H3
- Decision owner: evaluation owner
- Research question: do negotiation policies reduce unresolved disagreement when agent roles have conflicting preferences?
- Method shape: intervention
- Unit of analysis: contested turn sequence
- Data source candidates: synthetic conflict scenarios with role-specific utility asymmetries
- Primary signal: conflict resolution convergence rate
- Secondary signals: escalation count, cycle count, turn count
- Expected effect or finding: negotiation policies reduce cycling and unresolved escalation
- Strongest rival explanation: the extra negotiation steps create cost without changing the underlying decision quality
- Disconfirming outcome: more turns and no improvement in convergence
- Feasibility blockers: first-wave negotiation mechanism still needs selection
- Minimum gate path: G1 conflict and stability criteria explicit, G2 bargaining sources pinned, G3 scenario inventory ready, G4 turn-level telemetry validated
- Recommended next step: choose one negotiation mechanism for the first protocol draft

### EX-4 - Overhead Feasibility Envelope

- Linked hypothesis: H4
- Decision owner: research operator
- Research question: at what point do objective count and negotiation depth make the approach operationally unattractive?
- Method shape: observation
- Unit of analysis: policy run
- Data source candidates: replay runs instrumented with token, latency, and reviewer-burden signals
- Primary signal: overhead acceptability ratio
- Secondary signals: decision quality score, latency, token cost
- Expected effect or finding: a bounded operating region exists where gains remain worthwhile
- Strongest rival explanation: overhead is negligible relative to the quality improvement
- Disconfirming outcome: no practical overhead breakpoint appears in the tested range
- Feasibility blockers: telemetry collection is defined but not yet exercised
- Minimum gate path: G1 acceptable-threshold policy explicit, G2 signal-baseline source pinned, G3 measurement inventory ready, G4 telemetry rows validated
- Recommended next step: pair this experiment with E2 once the quality baseline is stable

## Sequencing Notes

1. Prefer experiments that best differentiate between explicit-objective and heuristic baselines.
2. Avoid promoting negotiation-heavy experiments before the simpler policy comparisons are stable.
3. Do not promote a candidate to live execution until the disconfirming outcome and acceptable overhead thresholds are explicit.
