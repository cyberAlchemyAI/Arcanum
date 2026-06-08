---
name: MOGT Harness 002 Context Pack
description: Strict local context for SWU-MOGT-HARNESS-002.
created: 2026-06-08
coverage: pass
---

# MOGT Harness 002 Context Pack

## Selected Unit

`SWU-MOGT-HARNESS-002` from `research/mogt-agentic-conversation/development/WORK-PACK.md`.

Objective: define runtime decision receipt and scenario/policy-regime fixture
format for first-wave dry-run fixture needs.

## Source Evidence

- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-001-RESULT.md`
- `research/mogt-agentic-conversation/experiments/schema/mogt-run.schema.json`
- `research/mogt-agentic-conversation/tools/validate-mogt-run-jsonl.py`
- `research/mogt-agentic-conversation/module-formulae/formal-runtime-definition.md`
- `research/mogt-agentic-conversation/module-formulae/runtime-decision-receipt.md`
- `research/mogt-agentic-conversation/module-formulae/operations.md`
- `research/mogt-agentic-conversation/module-formulae/flows-policies.md`
- `research/mogt-agentic-conversation/module-formulae/refresh-runs/20260608T035526Z-runtime-definition-refresh/REFRESH-REPORT.md`

## Required Output

Create fixture examples that instantiate `RuntimeDecisionReceipt` for:

- heuristic;
- weighted-sum;
- Pareto-guided;
- bargaining-guided.

Each fixture must map to `MOGTRunRow` fields and cover E1, E2, or E4 first-wave
evidence needs without claiming live experiment support.

## Required Fixture Content

Each runtime fixture example must include:

- candidate actions;
- feasible actions;
- blocked actions;
- objective vectors;
- selected action;
- principal tradeoff;
- policy trace;
- runtime status;
- token, latency, turn, and tool-call overhead.

## Write Scope

- `research/mogt-agentic-conversation/development/fixtures/`
- `research/mogt-agentic-conversation/experiments/*/context.md` only if fixture references need clarification.
- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-002-RESULT.md`

## Guardrails

- Do not run live experiments.
- Do not update `research/mogt-agentic-conversation/results/MOGT-EVIDENCE-STATUS.md` to supported or partially supported.
- Do not rewrite paper result sections.
- Do not mutate canonical Experiment Harness, Dispatch Spec, Whisper, Refine, Invoke, Research Tower, or Research Evidence Harness contracts.

## Verification Surface

The runtime result must show:

1. Fixture files exist for the four policy regimes.
2. Fixture examples can be converted into or validated as `MOGTRunRow` rows using the local validator.
3. The result records exact commands and outputs.
4. The result states that evidence remains synthetic fixture evidence only.
