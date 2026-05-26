# Task Session Context Pack: TASK-VERIFY

## Scope

- Task: `TASK-VERIFY`
- Objective: audit reproducibility, traceability, and work-pack closure after TASK-001 through TASK-005.
- Write scope: closure audit artifacts, task-session evidence, and status synchronization in work-pack/layering/wave records.

## Controlling Sources

- `WORK-PACK.md`: `TASK-VERIFY` is the recommended next execution after TASK-005.
- `work-pack/EXECUTION-PACK.md`: W3 includes `TASK-VERIFY` as a verification exemption after report/dashboard implementation.
- `work-pack/waves/W3.md`: W3 implementation is complete and closure audit remains.
- `IMPLEMENTATION-LAYERING.md`: remaining work is closure verification after dashboard-ready evidence.
- `artifacts/campaign-report-smoke/campaign-report.json`: persisted report read model.
- `artifacts/dashboard-api-smoke/dashboard-data.json`: persisted dashboard-ready read model.
- `artifacts/swebench-lite-official-smoke/score-result.json`: official SWE-bench score artifact.
- `artifacts/smellbench-official-smoke/score-result.json`: SmellBench score artifact.
- `artifacts/perfcodebench-official-smoke/score-result.json`: PerfCodeBench score artifact.

## Constraints

- Do not recompute benchmark outcomes.
- Do not infer resolution status outside official/upstream-derived score files.
- Re-run only deterministic tests and report/dashboard artifact generation.
- Any invalid JSON, missing score artifact, or non-zero evidence gap blocks closeout.
- Keep status synchronization scoped to closure state.

## Decisions

Selected option: run a closure-only audit that validates persisted evidence and regenerates report/API artifacts.

Rationale: this proves the work-pack can be replayed through the operator-facing layer without regrading benchmark outcomes or expanding scope into new benchmark coverage.

## Gate Result

Gate passed. TASK-001 through TASK-005 are marked complete, W3 implementation artifacts exist, and the remaining work is a bounded verification and synchronization pass.
