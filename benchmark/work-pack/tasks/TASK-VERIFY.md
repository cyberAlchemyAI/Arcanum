# TASK-VERIFY: Reproducibility And Traceability Closure Audit

## Objective

Verify that the benchmark harness work-pack can be replayed at the reporting layer and that every promoted benchmark score is traceable to persisted evidence.

## Layer And Slice Mapping

- Layer: L0-L3 closure
- Slice: S-001 through S-005
- Wave: [W3](../waves/W3.md)

## Source Contracts

- [../../WORK-PACK.md](../../WORK-PACK.md)
- [../../IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)
- [../EXECUTION-PACK.md](../EXECUTION-PACK.md)
- [../waves/W0.md](../waves/W0.md)
- [../waves/W1.md](../waves/W1.md)
- [../waves/W2.md](../waves/W2.md)
- [../waves/W3.md](../waves/W3.md)

## Dependencies

- TASK-001 through TASK-005 complete.
- Official SWE-bench Lite smoke score artifact exists.
- SmellBench score smoke artifact exists.
- PerfCodeBench score smoke artifact exists.
- Campaign report and dashboard-ready data artifacts exist.

## Implementation Detail

Inputs:

- Persisted benchmark score artifacts.
- Generated campaign report artifact.
- Generated dashboard-ready data artifact.
- Work-pack, wave, task, and layering records.

Outputs:

- Closure context pack and context index.
- Reproducibility and traceability audit report.
- Task-session report and observability envelope.
- Updated work-pack, wave, execution, and layering status records.

Audit rules:

1. Do not recompute benchmark outcomes during closure.
2. Re-run only deterministic reporting/API commands and unit tests.
3. Treat missing score artifacts, invalid JSON, or non-zero evidence gaps as closure blockers.
4. Preserve official benchmark results as benchmark authority; closure may only summarize them.
5. Record any remaining deferred scope as follow-up, not as hidden completion work.

## Closure Checks

- `npm test` passes.
- `npm run report:campaign` regenerates the campaign report.
- `npm run smoke:dashboard-api` regenerates dashboard-ready data.
- Core JSON artifacts parse with `jq empty`.
- Campaign and dashboard summaries agree on total runs and evidence gaps.
- SWE-bench, SmellBench, and PerfCodeBench score artifacts have terminal `status` values and no `infra-fail`.

## Done Criteria

- Closure audit report exists under `artifacts/verification-traceability-audit/`.
- Task-session report exists under `artifacts/task-session-task-verify-report.md`.
- Work-pack records mark `TASK-VERIFY` complete and the work-pack ready for closeout.

## Status

completed-closure-audit

## Verification Result

- `npm test` passed with 10/10 test files.
- `npm run report:campaign` regenerated a six-run report with zero evidence gaps.
- `npm run smoke:dashboard-api` regenerated dashboard data with six runs and zero evidence gaps.
- Core JSON artifacts passed `jq empty`.
- Traceability assertions passed for campaign/dashboard summaries and SWE-bench, SmellBench, and PerfCodeBench score artifacts.

## Completion Evidence

- `artifacts/verification-traceability-audit/report.json`
- `artifacts/verification-traceability-audit/report.md`
- `artifacts/task-session-task-verify-context-pack.md`
- `artifacts/task-session-task-verify-context-index.json`
- `artifacts/task-session-task-verify-report.md`
- `artifacts/task-session-task-verify-envelope.json`
