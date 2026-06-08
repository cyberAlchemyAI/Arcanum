---
name: TASK-MOGT-HARNESS-003 Result
description: Result for SWU-MOGT-HARNESS-003 objective-vector and Pareto/frontier metrics.
created: 2026-06-08
status: pass
selected_unit: SWU-MOGT-HARNESS-003
---

# TASK-MOGT-HARNESS-003 Result

## Verdict

Result: PASS.

`SWU-MOGT-HARNESS-003` produced a dependency-free Pareto/frontier calculator
for MOGT fixture rows and verified it against the synthetic E2 fixture created
by `SWU-MOGT-HARNESS-002`.

## Files Created Or Changed

- `research/mogt-agentic-conversation/tools/calculate-pareto-frontier.py`
- `research/mogt-agentic-conversation/development/fixtures/mogt-pareto-metrics-e2.json`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-003-RESULT.md`

## Metric Definitions

- Dominance: action `b` dominates action `a` when `b` is at least as good on
  all objective-vector dimensions and strictly better on at least one.
- Frontier membership: an action is on the frontier when no other candidate
  dominates it.
- Dominated selection: selected action is dominated by at least one candidate.
- Scalarization sensitivity: equal-weight scalar scores are computed as a
  lightweight sensitivity check over the normalized objective vector.

## Validation Commands

Compile check:

```bash
python3 -m py_compile research/mogt-agentic-conversation/tools/calculate-pareto-frontier.py research/mogt-agentic-conversation/tools/generate-result-summary.py
```

Result: pass.

Calculator command:

```bash
python3 research/mogt-agentic-conversation/tools/calculate-pareto-frontier.py research/mogt-agentic-conversation/development/fixtures/mogt-runtime-decision-receipts.jsonl --experiment E2 --output research/mogt-agentic-conversation/development/fixtures/mogt-pareto-metrics-e2.json
```

Output:

```text
PASS wrote research/mogt-agentic-conversation/development/fixtures/mogt-pareto-metrics-e2.json (1 row(s))
```

Metric excerpt:

```text
selected_action: ask_clarifying_question
selected_frontier_member: true
selected_dominated: false
dominated_actions: guess_without_trace
scalarization_sensitivity: selected_equal_weight_best
```

## Extra Sources

No extra sources outside the composite and stage context packs were required.

## Evidence Boundary

The calculator was verified on synthetic fixture data only. It does not update
publication claims or MOGT evidence status.
