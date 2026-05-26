# TASK-003.5: Add Official SWE-bench Lite Evaluation Path

## Objective

Run real SWE-bench Lite tasks through the official SWE-bench evaluation harness so the benchmark result comes from SWE-bench's own grading surface: prediction JSONL in, Docker-backed official harness run, official result report/logs out.

## Layer And Slice Mapping

- Layer: L1.5
- Slice: S-003.5
- Wave: [W1](../waves/W1.md)

## Source Contracts

- [../../starting-point.md](../../starting-point.md)
- [../../ARCHITECTURE.md](../../ARCHITECTURE.md)
- [SWE-bench Overview](https://www.swebench.com/SWE-bench/)
- [SWE-bench Evaluation Guide](https://www.swebench.com/SWE-bench/guides/evaluation/)
- [SWE-bench Datasets Guide](https://www.swebench.com/SWE-bench/guides/datasets/)
- [SWE-bench Docker Setup Guide](https://www.swebench.com/SWE-bench/guides/docker_setup/)

## Dependencies

- TASK-003 local Docker plumbing evidence.
- Official SWE-bench package installed or otherwise available to `python3`.
- Hugging Face dataset access for `princeton-nlp/SWE-bench_Lite`.
- At least one existing agent patch aligned to a real SWE-bench Lite `instance_id`.

## Implementation Detail

Inputs:

- Existing agent patch artifact paired with a real SWE-bench Lite `instance_id`; use `fixtures/swebench-lite-agent-patches.example.json` as the checked-in contract and `fixtures/swebench-lite-agent-patches.json` as the ignored real input.
- `model_name_or_path` label for the producing adapter.
- Official SWE-bench dataset name `princeton-nlp/SWE-bench_Lite`.
- Docker daemon access.

Outputs:

- Official SWE-bench prediction JSONL with `instance_id`, `model_name_or_path`, and `model_patch`.
- Official harness command record.
- Imported official result report as `official-evaluation-results/results.json`.
- Imported normalized `official-evaluation-results/instance_results.jsonl` derived from official resolved/unresolved IDs when the installed SWE-bench harness emits a current-format report instead of an `evaluation_results/<run_id>` tree.
- Imported per-instance logs when produced by the official harness.
- Local `score-result.json` derived only from official SWE-bench result files.
- Local report that links to official artifacts without regrading them.

Implementation notes:

1. Generate prediction JSONL from agent patch outputs only.
2. Block before evaluation if no real SWE-bench Lite `instance_id` is paired with an agent patch.
3. Use `npm run smoke:swebench:agent:prepare` to select the pinned real Lite instance, write a task brief, and prepare a checkout for the Codex local smoke patch.
4. Run the official harness inside the `swebench-official-runner` container with project files mounted at `/workspace` and `/var/run/docker.sock` mounted for official SWE-bench Docker evaluation.
5. Treat official SWE-bench result files as the source of truth.
6. Do not custom-apply patches, custom-run pytest, infer resolution, or substitute gold/local fixture patches.

## Smallest Working Units

### SWU-HARNESS-006A

- Goal: implement the official SWE-bench prediction and evaluation adapter.
- Dependencies: SWU-HARNESS-006.
- Write scope: official SWE-bench adapter, prediction JSONL writer, smoke command, tests.
- Done criteria: adapter can emit valid prediction JSONL and invoke the documented official harness command.
- Acceptance evidence: unit tests for JSONL shape and block behavior.
- Verification: `npm test`.

### SWU-HARNESS-006B

- Goal: run the first official SWE-bench Lite evaluation smoke.
- Dependencies: SWU-HARNESS-006A, built `swebench-official-runner` image, Docker socket access, instance-aligned agent patch artifact.
- Write scope: official run artifacts and completion evidence only.
- Done criteria: official harness completes with `max_workers=1`, captured official result report/logs, and a local `score-result.json`.
- Acceptance evidence: `artifacts/swebench-lite-official-smoke/score-result.json`, `official-swebench-report.json`, and imported official results.
- Verification: `npm run smoke:swebench:official`.

## Synchronization Rules

TASK-004 must not claim upstream SWE-bench evidence until SWU-HARNESS-006B completes. Local mirror evidence remains Docker plumbing evidence only.

## Completion Evidence

- SWU-HARNESS-006A: implemented. Official prediction JSONL writer, preflight, command builder/invoker, and smoke command are present.
- SWU-HARNESS-006A validation: `npm test` covers the official prediction JSONL shape and missing instance-aligned patch block.
- SWU-HARNESS-006B: completed for real SWE-bench Lite instance `astropy__astropy-14365` with a Codex local smoke patch artifact at `artifacts/swebench-lite-agent-smoke/astropy__astropy-14365/patch.diff`.
- SWU-HARNESS-006B validation: `npm run smoke:swebench:official:build` rebuilt `swebench-official-runner`; `npm run smoke:swebench:official` completed the official SWE-bench harness with `max_workers=1`.
- SWU-HARNESS-006B score evidence: `artifacts/swebench-lite-official-smoke/score-result.json` reports `status: fail`, `resolved: false`, `instanceId: astropy__astropy-14365`, with official refs to `official-evaluation-results/results.json`, `instance_results.jsonl`, and per-instance logs. This is accepted as plumbing proof because the official harness completed and produced an unresolved result rather than an infra-fail.
