# MOGT Experiment Design & Data Collection Plan

This document indexes the experiments needed to validate whether multi-objective game theory should be incorporated into agentic systems conversation decision processes.

Each experiment maps to a project claim, defines a draft protocol bundle, and establishes the first execution wave for this greenfield project.

---

## Experiment Index

| ID  | Experiment                           | Project Claim                                                        | Priority | Effort | Status      | File                                                      |
| --- | ------------------------------------ | -------------------------------------------------------------------- | -------- | ------ | ----------- | --------------------------------------------------------- |
| E1  | Tradeoff Traceability Baseline       | MOGT-C1 - explicit objectives improve traceability                   | P0       | Medium | not started | [E1](E1-tradeoff-traceability-baseline/protocol.md)       |
| E2  | Pareto Arbitration Quality           | MOGT-C2 - Pareto-aware selection improves multi-objective decisions  | P0       | Medium | not started | [E2](E2-pareto-arbitration-quality/protocol.md)           |
| E3  | Negotiation Stability Under Conflict | MOGT-C3 - game-theoretic negotiation reduces unresolved disagreement | P1       | Medium | not started | [E3](E3-negotiation-stability-under-conflict/protocol.md) |
| E4  | Overhead Feasibility Envelope        | MOGT-C4 - benefits remain within acceptable operational overhead     | P0       | Low    | not started | [E4](E4-overhead-feasibility-envelope/protocol.md)        |

### Results & Data

- Results: `experiments/*/results/` - one or more result summaries per experiment bundle
- Raw data: `experiments/*/data/` - append-only JSONL files per experiment run

---

## Execution Rules

### Data Integrity

1. Raw data only. Store all experiment data as JSONL under the owning bundle's `data/` directory.
2. Session isolation. Each experiment run should use a fresh session or a fully documented replay setup.
3. Ground-truth annotation. Any human review or benchmark adjudication must use a documented rubric.
4. Reproducibility. Record exact model version, temperature, system prompt hash, and policy regime for every run.

### Metadata per Run

Every experiment data point must include:

```json
{
  "experiment_id": "E1",
  "run_id": "uuid",
  "timestamp": "2026-04-27T00:00:00Z",
  "project_id": "mogt-agentic-conversation",
  "policy_regime": "heuristic|weighted-sum|pareto-guided|bargaining-guided",
  "model": "model-id",
  "model_temperature": 0,
  "system_prompt_hash": "sha256:...",
  "operator": "vrondelli"
}
```

### Recommended First-Wave Order

1. E1 - establish whether explicit objective modeling improves traceability.
2. E2 - test whether Pareto-aware arbitration improves quality over heuristic baselines.
3. E4 - determine whether any gains survive operational overhead constraints.
4. E3 - deepen into disagreement and negotiation dynamics after the baseline policy comparison is stable.

### Reporting

After each experiment completes, produce a result summary under the bundle's `results/` directory with:

- protocol deviations
- raw data location
- summary statistics
- success-criteria evaluation
- claim impact recommendation
- next-step recommendation
