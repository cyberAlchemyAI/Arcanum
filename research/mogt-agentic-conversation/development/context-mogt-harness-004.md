---
name: MOGT Harness 004 Context Pack
description: Strict local context for SWU-MOGT-HARNESS-004.
created: 2026-06-08
coverage: pass
---

# MOGT Harness 004 Context Pack

## Selected Unit

`SWU-MOGT-HARNESS-004` from `research/mogt-agentic-conversation/development/WORK-PACK.md`.

Objective: implement result-summary generation from validated fixture JSONL.

## Source Evidence

- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-001-RESULT.md`
- `research/mogt-agentic-conversation/experiments/schema/mogt-run.schema.json`
- `research/mogt-agentic-conversation/tools/validate-mogt-run-jsonl.py`
- `research/mogt-agentic-conversation/development/fixtures/mogt-run-valid.jsonl`
- `arcana/research-evidence-harness/templates/result-summary.md`
- `research/mogt-agentic-conversation/module-formulae/runtime-decision-receipt.md`

## Required Output

Create a summary-generation path that reads validated fixture JSONL and writes a
dry-run result summary. The summary must include:

- protocol deviations;
- raw data location;
- summary statistics;
- success-criteria evaluation;
- claim-impact recommendation;
- next-step recommendation;
- explicit dry-run fixture evidence boundary.

## Write Scope

- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/experiments/*/results/`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-004-RESULT.md`

## Guardrails

- Do not run live experiments.
- Do not update MOGT evidence status to supported or partially supported.
- Do not rewrite paper results from fixture-only summaries.
- If the calculator from SWU-MOGT-HARNESS-003 is unavailable, use the local
  validated fixture fields and record the gap.

## Verification Surface

The runtime result must show:

1. A result summary is generated from validated fixture JSONL.
2. The summary distinguishes synthetic fixture evidence from live experiment evidence.
3. The summary includes claim-impact and next-step recommendations.
4. Exact commands and outputs are recorded.
