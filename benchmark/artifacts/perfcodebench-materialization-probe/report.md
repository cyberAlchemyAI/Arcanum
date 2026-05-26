# PerfCodeBench Materialization Probe

Status: `completed-materialization-probe`

`SWU-HARNESS-008A.1` materialized a runnable `fast_float_parse` tree and produced a raw runner result at:

`artifacts/perfcodebench-materialization-probe/materialized/results/dry-run-fast-float.json`

The run compiled and executed:

- baseline: `ok`, correctness `true`, median `37134461 ns`
- reference: `ok`, correctness `true`, median `4153688 ns`
- candidate: `ok`, correctness `true`, median `22380209 ns`

The candidate was the runner's dry-run baseline placeholder. This is setup proof only, not a benchmark score.

## Remaining Gate For SWU-HARNESS-008B

`SWU-HARNESS-008B` can proceed only after an agent-produced candidate artifact and an accepted deterministic worker/noise profile exist.

