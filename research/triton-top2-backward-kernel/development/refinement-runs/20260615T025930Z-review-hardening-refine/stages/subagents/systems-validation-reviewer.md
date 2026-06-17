# Systems Validation Reviewer Receipt

- agent_id: `systems-validation-reviewer-<runtime-agent-id>`
- role_id: `systems-validation-reviewer`
- spawn_status: `spawned`
- join_status: `completed`
- close_status: `closed`
- dispatch_id: `refine-20260615T025930Z-review-hardening`
- step_id(s): `stage-1-context-builder`, `stage-4-research-decision`, `stage-6-invoke-design`, `stage-9-invoke-plan`, `stage-10-final-synthesis`
- capability_ref: `subagent:systems-validation-reviewer`
- status: `flag`
- validation_result: `systems evidence is usable for fixed-mask W7 and CAP2 W6/W7 smoke claims, but not yet strong enough for a promoted CAP2 zero-allocation acceptance claim or broad performance claim`

## Artifacts

- `research/triton-top2-backward-kernel/TRITON-BENCHMARK-REPORT.md`
- `research/triton-top2-backward-kernel/CAP2-W6-PARITY-REPORT.md`
- `research/triton-top2-backward-kernel/WORK-PACK.md`
- `research/triton-top2-backward-kernel/tests/test_router_triton.py`
- `research/triton-top2-backward-kernel/reference/router_triton.py`
- `research/triton-top2-backward-kernel/scripts/benchmark_triton_paths.py`
- `research/projects/mars/papers/triton-top2-backward-kernel/DATA-APPENDIX.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`

## Evidence Paths

- RunPod readiness:
  `research/triton-top2-backward-kernel/development/task-sessions/20260614T063208Z-runpod-cuda-probe/RUNPOD-CUDA-PROBE-PASS.md`
- W6 CAP2 reference/Triton parity:
  `research/triton-top2-backward-kernel/CAP2-W6-PARITY-REPORT.md`
- W6 task plan and execution notes:
  `research/triton-top2-backward-kernel/development/invoke-runs/20260614T072729Z-w6-cap2-exact-backward-spec/WORK-PACK-W6-CAP2.md`
- W7 benchmark result:
  `research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/RESULT.md`
- Raw benchmark JSON:
  `research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/benchmark.json`
- Benchmark markdown artifact:
  `research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/BENCHMARK.md`
- Paper data appendix:
  `research/projects/mars/papers/triton-top2-backward-kernel/DATA-APPENDIX.md`
- Paper evidence manifest:
  `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`

## Systems Findings

Fixed-mask W7 evidence is the strongest systems claim currently available.
`WORK-PACK.md` records `TASK-W7-001` as `pass-runpod` for zero-allocation checks,
with fixed-mask kernels reusing preallocated outputs and no measured CUDA
allocation increase after warm-up. `TASK-W7-002` is also `pass-runpod` for FP16
inputs with FP32 outputs and `rtol=2e-3, atol=2e-3`.

CAP2 systems evidence is real but weaker. `CAP2-W6-PARITY-REPORT.md` closes W6
for fixed-load backward parity and explicitly says it does not claim CAP2
zero-allocation behavior. `tests/test_router_triton.py` contains
`test_cap2_backward_reuses_preallocated_outputs`, which verifies returned
buffers reuse caller-provided output pointers. That is useful wrapper evidence,
but it is not the same acceptance level as the fixed-mask memory-stat test.

The benchmark is reproducible enough as a smoke benchmark. `TRITON-BENCHMARK-REPORT.md`
and `DATA-APPENDIX.md` record the RunPod environment as NVIDIA RTX PRO 4000
Blackwell, PyTorch `2.8.0+cu128`, CUDA `12.8`, warmup `10`, iterations `50`, and
two sizes: `T=128,E=8,D=64` and `T=512,E=16,D=128`. The script is
`scripts/benchmark_triton_paths.py`; it already uses preallocated outputs for
both fixed-mask and CAP2 measured paths.

The benchmark should not be promoted beyond case-study timing. The raw data only
covers two sizes, one GPU, FP32 inputs, one seed, one run, and no memory
telemetry. It supports "the tested paths run on the recorded RunPod GPU" and
"CAP2 is slower than fixed-mask on the two smoke sizes," not production
optimization, general scaling, or hardware-independent performance.

## Blockers

- CAP2 zero-allocation does not yet have a fixed-mask-style CUDA memory-stat
  acceptance test.
- CAP2 FP16 does not have a dedicated Triton parity/tolerance test. Current FP16
  coverage is fixed-mask W7.
- Benchmark sweep is too small for strong scaling claims: two sizes, one GPU,
  one dtype, one run configuration, and no statistical repeat groups beyond the
  per-run timing iterations.
- Reproducibility metadata is missing several useful fields: GPU driver version,
  Triton version, Python version, git commit, pod image/container identity, and
  exact command output capture for the benchmark run.
- No benchmark validates memory allocation behavior inside the CAP2 measured
  loop with `torch.cuda.reset_peak_memory_stats`.

## Residue

- CAP2 wrapper design already accepts `out_d_z`, `out_d_x_router`, `out_d_h`,
  and `out_d_w`, and the benchmark path passes those buffers. This suggests a
  strong CAP2 zero-allocation acceptance test is feasible without redesigning the
  kernel interface.
- `cap2_row_backward_triton` calls the fixed-mask matrix kernels after the
  row-local CAP2 kernel. A CAP2 memory test must warm up all three kernels before
  measuring, because first-launch compilation/cache behavior is not part of the
  hot-path allocation contract.
- The current CAP2 row-local kernel uses `block_e=max(block_e, e_size)` through
  `_triton_dot_block_size`, so larger `E` sweeps may hit practical Triton block
  limits before matrix kernels do. Scaling tests should include expected-failure
  reporting for unsupported `E`.

## Reroute

Route systems hardening into a new bounded work pack rather than editing paper
claims directly:

- `TASK-SYS-001`: CAP2 zero-allocation acceptance test.
- `TASK-SYS-002`: CAP2 FP16 parity/tolerance test.
- `TASK-SYS-003`: Larger benchmark sweep with environment capture.
- `TASK-SYS-004`: Paper/evidence manifest synchronization after the new systems
  evidence exists.

## Recommended Next Tasks

1. Add `test_cap2_backward_reuses_preallocated_outputs_without_measured_cuda_allocation`.
   Acceptance: warm up `cap2_row_backward_triton` with all four output buffers,
   reset CUDA peak memory stats, run again, assert all returned data pointers
   match provided buffers, `after == before`, and `peak == before`.

2. Add CAP2 FP16 tests separate from fixed-mask FP16 tests.
   Acceptance: run CAP2 with FP16 `x`, `w`, `h`, `load`, and `f` where supported,
   require FP32 outputs, compare against a FP32/manual reference with an explicit
   tolerance budget. If `load`/`f` should remain FP32, document that as the
   mixed-precision contract and test it explicitly.

3. Extend `scripts/benchmark_triton_paths.py` with CLI-selectable sizes and
   dtypes.
   Suggested sweep: `(T,E,D) = (128,8,64)`, `(512,16,128)`,
   `(2048,32,256)`, `(4096,32,512)`, plus one stress size gated by available
   memory. Include `fixed_mask` and `cap2_fixed_load` paths for FP32 and the
   selected FP16/mixed-precision contract.

4. Add benchmark environment capture.
   Acceptance: JSON includes `torch.__version__`, `torch.version.cuda`,
   `triton.__version__`, Python version, `torch.cuda.get_device_name(0)`,
   driver line from `nvidia-smi`, git commit or dirty-state marker, warmup,
   iterations, seed, and command-line arguments.

5. Add memory telemetry to benchmark output without making it the only
   zero-allocation proof.
   Acceptance: for each path/size/dtype, record `memory_allocated_before`,
   `memory_allocated_after`, and `max_memory_allocated_after_reset` after warmup.
   Treat this as supporting data; keep the unit test as the acceptance gate.

6. Update `TRITON-BENCHMARK-REPORT.md`, `DATA-APPENDIX.md`, and
   `EVIDENCE-MANIFEST.md` only after the tests and benchmark sweep pass on the
   GPU runner. The report should continue to separate fixed-mask W7 acceptance
   from CAP2 evidence unless `TASK-SYS-001` passes.
