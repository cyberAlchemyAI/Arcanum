---
name: MOGT Harness Development Pack
description: Development pack for unblocking MOGT dry-run fixtures after harness feasibility blocked.
created: 2026-06-07
status: fixture-validation-ready
---

# MOGT Harness Development Pack

## Objective

Build the minimum MOGT-local execution and validation surface needed to run S4 dry-run fixtures without claiming live experiment results prematurely.

## Route Owner

This pack is now the seed execution case for the draft `research-evidence-harness` sigil and the draft `publication-research-pipeline` spell.

The route remains MOGT-local until fixture validation proves reusable behavior. The draft sigil/spell do not promote MARS assets or MOGT results into canonical Arcanum authority.

## Blocker Source

`development/HARNESS-FEASIBILITY.md` returned BLOCK because the current Experiment Harness is a spell/sigil lifecycle harness, not yet a research-project experiment runner for MOGT JSONL data, objective vectors, Pareto metrics, reviewer rubrics, and result summaries.

## SWU Manifest

| SWU ID | Parent Task | Status | Objective | Acceptance Evidence |
| --- | --- | --- | --- | --- |
| SWU-MOGT-HARNESS-001 | TASK-MOGT-HARNESS-001 | completed | Define MOGT run JSONL schema and validator. | `TASK-MOGT-HARNESS-001-RESULT.md`; schema, validator, passing fixture, failing fixture, and validation output. |
| SWU-MOGT-HARNESS-002 | TASK-MOGT-HARNESS-002 | completed | Define runtime decision receipt and scenario/policy-regime fixture format for E1/E2/E4. | `TASK-MOGT-HARNESS-002-RESULT.md`; `fixtures/mogt-runtime-decision-receipts.jsonl`; validator pass over 4 rows. |
| SWU-MOGT-HARNESS-003 | TASK-MOGT-HARNESS-003 | completed | Implement objective-vector and Pareto/frontier metric calculator. | `TASK-MOGT-HARNESS-003-RESULT.md`; `tools/calculate-pareto-frontier.py`; `fixtures/mogt-pareto-metrics-e2.json`. |
| SWU-MOGT-HARNESS-004 | TASK-MOGT-HARNESS-004 | completed | Implement result-summary generator. | `TASK-MOGT-HARNESS-004-RESULT.md`; `tools/generate-result-summary.py`; fixture-only summaries under E1, E2, and E4 results folders. |
| SWU-MOGT-HARNESS-005 | TASK-MOGT-HARNESS-005 | completed | Produce S4 dry-run fixture validation report. | `development/fixture-validation-report.md` states fixture-only S4 readiness and evidence boundary. |

## TASK-MOGT-HARNESS-001

### Objective

Define a MOGT experiment-run JSONL schema and validator for S4 dry-run fixtures.

### Capability Route

- Draft sigil owner: `arcana/research-evidence-harness/`
- Draft spell route: `spells/publication-research-pipeline/`
- Context pack: `research/mogt-agentic-conversation/development/context-mogt-harness-001.md`
- Context index: `research/mogt-agentic-conversation/development/context-mogt-harness-001.index.json`

### Write Scope

- `research/mogt-agentic-conversation/experiments/schema/`
- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/development/fixtures/`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`

### Done Criteria

- Schema names required common fields from `development/HARNESS-FEASIBILITY.md`.
- Validator rejects missing run metadata, missing objective vector, missing policy regime, and malformed metric fields.
- At least one passing synthetic fixture and one failing synthetic fixture exist.

### Verification

Run the validator against passing and failing fixtures and record the command output.

### Completion Evidence

- Result: `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-001-RESULT.md`
- Schema: `research/mogt-agentic-conversation/experiments/schema/mogt-run.schema.json`
- Validator: `research/mogt-agentic-conversation/tools/validate-mogt-run-jsonl.py`
- Passing fixture: `research/mogt-agentic-conversation/development/fixtures/mogt-run-valid.jsonl`
- Failing fixture: `research/mogt-agentic-conversation/development/fixtures/mogt-run-invalid.jsonl`

## TASK-MOGT-HARNESS-002

### Objective

Define fixture format for S4 policy-regime dry-runs by instantiating the formal
runtime loop and `RuntimeDecisionReceipt`.

### Write Scope

- `research/mogt-agentic-conversation/development/fixtures/`
- `research/mogt-agentic-conversation/experiments/*/context.md` only if fixture references need clarification.

### Done Criteria

- Fixtures cover heuristic, weighted-sum, Pareto-guided, and bargaining-guided regimes.
- Fixture format maps runtime decision receipts to `MOGTRunRow` fields.
- Runtime fixture examples include candidate actions, feasible/blocked actions,
  objective vectors, selected action, principal tradeoff, policy trace, runtime
  status, and overhead.
- Fixtures do not claim live experiment support.
- Each fixture maps to E1/E2/E4 first-wave evidence needs.

### Completion Evidence

- Result: `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-002-RESULT.md`
- Fixture JSONL: `research/mogt-agentic-conversation/development/fixtures/mogt-runtime-decision-receipts.jsonl`

## TASK-MOGT-HARNESS-003

### Objective

Implement or specify objective-vector and Pareto/frontier metric calculation.

### Write Scope

- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/development/fixtures/`

### Done Criteria

- Synthetic E2-like fixture can classify dominated vs frontier selections.
- Scalarization sensitivity or explicit reason for deferral is recorded.
- Output can be consumed by result-summary generation.

### Completion Evidence

- Result: `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-003-RESULT.md`
- Calculator: `research/mogt-agentic-conversation/tools/calculate-pareto-frontier.py`
- Metrics output: `research/mogt-agentic-conversation/development/fixtures/mogt-pareto-metrics-e2.json`

## TASK-MOGT-HARNESS-004

### Objective

Implement result-summary generation from validated fixture JSONL.

### Write Scope

- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/experiments/*/results/`

### Done Criteria

- Summary includes protocol deviations, raw data location, summary statistics, success-criteria evaluation, claim-impact recommendation, and next-step recommendation.
- Summary distinguishes dry-run fixture evidence from live experiment evidence.

### Completion Evidence

- Result: `research/mogt-agentic-conversation/development/TASK-MOGT-HARNESS-004-RESULT.md`
- Generator: `research/mogt-agentic-conversation/tools/generate-result-summary.py`
- Summaries:
  - `research/mogt-agentic-conversation/experiments/E1-tradeoff-traceability-baseline/results/fixture-result-summary.md`
  - `research/mogt-agentic-conversation/experiments/E2-pareto-arbitration-quality/results/fixture-result-summary.md`
  - `research/mogt-agentic-conversation/experiments/E4-overhead-feasibility-envelope/results/fixture-result-summary.md`

## TASK-MOGT-HARNESS-005

### Objective

Produce S4 dry-run fixture validation report.

### Write Scope

- `research/mogt-agentic-conversation/development/fixture-validation-report.md`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`

### Done Criteria

- Report states whether S4 can proceed.
- Report lists fixture commands and outputs.
- No live experiments are run.

### Completion Evidence

- Report: `research/mogt-agentic-conversation/development/fixture-validation-report.md`

## Guardrails

- Do not update `results/MOGT-EVIDENCE-STATUS.md` to supported or partially supported from dry-run fixtures.
- Do not rewrite result-facing paper sections.
- Do not mutate canonical Experiment Harness, Dispatch Spec, Whisper, Refine, or Invoke contracts.
- If a reusable Experiment Harness extension is needed, produce a proposal/handoff rather than direct canonical mutation.
