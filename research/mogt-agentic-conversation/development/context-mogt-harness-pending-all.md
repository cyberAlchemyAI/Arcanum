---
name: MOGT Harness Pending-All Context Pack
description: Strict local context for one native Codex goal that executes pending MOGT harness tasks in dependency order.
created: 2026-06-08
coverage: pass
---

# MOGT Harness Pending-All Context Pack

## Selected Unit

Composite execution chain:

1. `SWU-MOGT-HARNESS-002`
2. `SWU-MOGT-HARNESS-003`
3. `SWU-MOGT-HARNESS-004`
4. `SWU-MOGT-HARNESS-005`

`SWU-MOGT-HARNESS-005` is not initially runnable. It becomes runnable only
after task result files for `002`, `003`, and `004` exist.

## Source Work-Pack

- `research/mogt-agentic-conversation/development/WORK-PACK.md`

## Stage Context Packs

Read the stage-specific context pack and index before editing for that stage:

| Stage | Context Pack | Index |
| --- | --- | --- |
| `SWU-MOGT-HARNESS-002` | `research/mogt-agentic-conversation/development/context-mogt-harness-002.md` | `research/mogt-agentic-conversation/development/context-mogt-harness-002.index.json` |
| `SWU-MOGT-HARNESS-003` | `research/mogt-agentic-conversation/development/context-mogt-harness-003.md` | `research/mogt-agentic-conversation/development/context-mogt-harness-003.index.json` |
| `SWU-MOGT-HARNESS-004` | `research/mogt-agentic-conversation/development/context-mogt-harness-004.md` | `research/mogt-agentic-conversation/development/context-mogt-harness-004.index.json` |
| `SWU-MOGT-HARNESS-005` | `research/mogt-agentic-conversation/development/context-mogt-harness-005.md` | `research/mogt-agentic-conversation/development/context-mogt-harness-005.index.json` |

## Stage Goal Packs

Use these stage packs as execution subcontracts:

- `research/mogt-agentic-conversation/development/goals/mogt-harness-002/`
- `research/mogt-agentic-conversation/development/goals/mogt-harness-003/`
- `research/mogt-agentic-conversation/development/goals/mogt-harness-004/`
- `research/mogt-agentic-conversation/development/goals/mogt-harness-005/`

## Dependencies

- `SWU-MOGT-HARNESS-001` is complete.
- `SWU-MOGT-HARNESS-002`, `003`, and `004` are ready.
- `SWU-MOGT-HARNESS-005` is blocked until all three prerequisite result files
  exist:
  - `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-002-RESULT.md`
  - `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-003-RESULT.md`
  - `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-004-RESULT.md`

## Combined Write Scope

- `research/mogt-agentic-conversation/development/fixtures/`
- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/experiments/*/context.md` only if fixture references need clarification
- `research/mogt-agentic-conversation/experiments/*/results/`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-002-RESULT.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-003-RESULT.md`
- `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-004-RESULT.md`
- `research/mogt-agentic-conversation/development/fixture-validation-report.md`

## Combined Guardrails

- Do not run live experiments.
- Do not update `research/mogt-agentic-conversation/results/MOGT-EVIDENCE-STATUS.md` to supported or partially supported.
- Do not rewrite result-facing paper sections.
- Do not mutate canonical Experiment Harness, Dispatch Spec, Whisper, Refine, Invoke, Research Tower, or Research Evidence Harness contracts.
- If a reusable Experiment Harness extension is needed, produce a proposal or handoff rather than direct canonical mutation.
- Use stage context packs first. Extra sources are allowed only for named gaps and must be reported.

## Combined Verification Surface

The final goal report must show:

1. `SWU-MOGT-HARNESS-002` created runtime decision receipt fixtures for the four policy regimes and validated them locally.
2. `SWU-MOGT-HARNESS-003` produced frontier/dominance metric output over a synthetic fixture.
3. `SWU-MOGT-HARNESS-004` generated a fixture-only result summary from validated JSONL.
4. `SWU-MOGT-HARNESS-005` produced the S4 dry-run fixture validation report only after `002-004` result files existed.
5. No live experiments were run.
6. Evidence status and paper result claims were not promoted from synthetic fixture evidence.
