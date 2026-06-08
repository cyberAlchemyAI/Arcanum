---
name: MOGT Harness 003 Context Pack
description: Strict local context for SWU-MOGT-HARNESS-003.
created: 2026-06-08
coverage: pass
---

# MOGT Harness 003 Context Pack

## Selected Unit

`SWU-MOGT-HARNESS-003` from `research/mogt-agentic-conversation/development/WORK-PACK.md`.

Objective: implement or specify objective-vector and Pareto/frontier metric
calculation for synthetic MOGT fixture rows.

## Source Evidence

- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-001-RESULT.md`
- `research/mogt-agentic-conversation/experiments/schema/mogt-run.schema.json`
- `research/mogt-agentic-conversation/tools/validate-mogt-run-jsonl.py`
- `research/mogt-agentic-conversation/development/fixtures/mogt-run-valid.jsonl`
- `research/mogt-agentic-conversation/module-formulae/formal-runtime-definition.md`
- `research/mogt-agentic-conversation/module-formulae/runtime-decision-receipt.md`
- `research/mogt-agentic-conversation/module-formulae/operations.md`

## Required Output

Create a calculator or explicit deferral-specification that can classify:

- dominated selections;
- frontier membership;
- dominated candidate actions;
- scalarization sensitivity or the exact reason it is deferred.

The preferred path is a dependency-free local Python tool under the declared
write scope, unless the local codebase already provides a better pattern.

## Write Scope

- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/development/fixtures/`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-003-RESULT.md`

## Guardrails

- Do not run live experiments.
- Do not update MOGT evidence status from synthetic calculator output.
- Do not mutate canonical Arcanum capability contracts.
- Keep calculator output consumable by `SWU-MOGT-HARNESS-004`.

## Verification Surface

The runtime result must show:

1. A synthetic E2-like fixture is processed.
2. Calculator output identifies frontier status and dominated selections.
3. Validator compatibility with the MOGT JSONL row remains intact.
4. Exact commands and outputs are recorded.
