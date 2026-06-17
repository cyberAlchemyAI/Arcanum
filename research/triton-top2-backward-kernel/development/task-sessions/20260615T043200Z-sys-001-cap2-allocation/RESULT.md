# Result - SWU-SYS-001 CAP2 CUDA Memory-Stat Allocation Test

Status: `blocked-after-local-validation`

Implemented:

- Added `test_cap2_backward_preallocated_outputs_do_not_increase_measured_allocation` to `tests/test_router_triton.py`.
- The test warms CAP2 kernels, reuses preallocated `d_z`, `d_x_router`, `d_h`, and `d_w` outputs, resets CUDA peak memory stats, reruns the CAP2 backward wrapper, and asserts:
  - returned tensor pointers match the preallocated outputs;
  - `torch.cuda.memory_allocated()` is unchanged;
  - `torch.cuda.max_memory_allocated()` does not exceed the pre-run value.

Validation completed:

- Local focused test command:
  `cd research/triton-top2-backward-kernel && .venv/bin/python -m pytest tests/test_router_triton.py -q`
- Result:
  `2 passed, 14 skipped in 3.60s`

Blocked validation:

- Required RunPod/CUDA validation command:
  `<cuda-runner-iteration-command>`
- Result:
  `ssh: connect to host <redacted-runner-host> port <redacted-runner-port>: Connection refused`
- Bundle produced before the connection failure:
  `development/runner-bundles/triton-top2-iteration-20260615T043156Z.tar.gz`
- Bundle SHA256:
  `cf01af723321397adee9584236106f9969c9419eed6d843c0bf6675329576528`

Next unblocker:

Provide a live CUDA runner SSH host/port or restart the RunPod instance, then rerun:

```bash
cd <repo>/research/triton-top2-backward-kernel
<cuda-runner-iteration-command>
```
