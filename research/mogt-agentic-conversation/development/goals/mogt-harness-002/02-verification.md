# Verification

Required verification surface:

- Fixture files exist for heuristic, weighted-sum, Pareto-guided, and bargaining-guided regimes.
- Fixture examples include candidate actions, feasible actions, blocked actions, objective vectors, selected action, principal tradeoff, policy trace, runtime status, and overhead.
- Fixture rows pass the local validator:

```bash
python3 research/mogt-agentic-conversation/tools/validate-mogt-run-jsonl.py <fixture-jsonl>
```

Record exact commands and outputs in the task result.
