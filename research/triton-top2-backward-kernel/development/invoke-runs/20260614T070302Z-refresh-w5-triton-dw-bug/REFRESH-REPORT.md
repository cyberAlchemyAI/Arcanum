# Invoke Refresh Report - W5 Triton dW Bug

Mode: `refresh`
Mutation mode: `proposal-only`
Evidence date: `2026-06-14`
Target workflow root: `research/triton-top2-backward-kernel`

## Source Signals

### RS-W5-001-RUNPOD-FAIL

- Type: `blocker_opened`
- Source: `redacted local evidence attachment`
- Target artifacts:
  - `WORK-PACK.md`
  - `reference/router_triton.py`
  - `tests/test_router_triton.py`
  - `development/task-sessions/20260614T-w5-001-triton-dw/RESULT.md`
- Claim: RunPod CUDA validation failed for the first `TASK-W5-001` Triton `dW` implementation.
- Evidence: Full test run reports `50` prior tests passing and `3` Triton fixed-mask `dW` failures.
- Confidence: `high`
- Mutation safety: `safe` for status/report updates; `needs_review` for kernel repair.

### RS-W5-001-TLDOT-MIN-TILE

- Type: `artifact_drift`
- Source: RunPod failure trace in pasted output.
- Target artifacts:
  - `reference/router_triton.py`
  - `tests/test_router_triton.py`
- Claim: The current kernel/test path asks Triton `tl.dot` to compile tiles below the target lower bound.
- Evidence: Triton reports `Input shapes should have M >= 16, N >= 16 and K >= 16` at `acc += tl.dot(tl.trans(dz), x)`.
- Confidence: `high`
- Mutation safety: `safe` for a focused implementation correction.

### RS-W5-001-PRECISION-MISMATCH

- Type: `artifact_drift`
- Source: RunPod failure trace in pasted output.
- Target artifacts:
  - `reference/router_triton.py`
  - `tests/test_router_triton.py`
- Claim: The fixture parity tolerance or accumulation mode is too strict for the current `tl.dot` path on the pod GPU.
- Evidence: The manual fixture mismatch is about `4.2e-05` absolute and `0.0016` relative, while the test expected `rtol=1e-5, atol=1e-6`.
- Confidence: `medium`
- Mutation safety: `needs_review`; decide whether to enforce fp32-accurate accumulation by implementation change or relax only FP16/TF32-specific tolerances.

## Delta Summary

- `blocker_opened`: `TASK-W5-001` has real RunPod failure evidence and must not be promoted to `pass`.
- `artifact_drift`: local CPU-only validation skipped Triton tests, while external validation exposed compile and numeric failures.
- `route_changed`: next route stays `task-session`, but the bounded task should be a bug-fix continuation, not the next W5 task.

## Proposed Changes

1. Preserve `TASK-W5-001` as not passed.
2. Add a blocker note to the W5 task-session result and evidence index.
3. Fix `reference/router_triton.py` so small logical expert/feature sizes do not create sub-16 `tl.dot` compile shapes.
4. Update `tests/test_router_triton.py` to cover small logical shapes through padded/minimum physical tiles, while still comparing only logical output.
5. Decide and document the expected numeric contract:
   - FP32 parity should either disable TF32 or use an honest tolerance.
   - FP16 parity should keep fp32 output and use the existing approximate tolerance lane.
6. Re-run local CPU validation and then use `<cuda-runner-iteration-command>` for RunPod validation.

## Non-Changes

- Do not advance `TASK-W5-002`, W6, or W7 before `TASK-W5-001` passes on RunPod.
- Do not claim zero allocation, fused full backward, or final FP16 performance from this fix.
- Do not mutate `WORK-PACK.md` during this refresh without explicit approval.

## Recommended Task-Session Handoff

Route: `task-session`

Task: `TASK-W5-001 bug-fix continuation`

Inputs:

- `reference/router_triton.py`
- `tests/test_router_triton.py`
- `<cuda-runner-iteration-command>`
- RunPod failure evidence from `redacted local evidence attachment`

Implementation target:

- Repair the Triton `dW = dZ^T @ X` baseline so it passes small logical shapes on the RunPod GPU.

Acceptance:

```sh
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py
.venv/bin/python -m pytest tests -q
<cuda-runner-iteration-command>
```

RunPod acceptance must include:

```sh
/usr/local/bin/python -m pytest tests/test_router_triton.py -q
/usr/local/bin/python -m pytest tests -q
```

## Phase Status

`pass`: the refresh has enough evidence to propose a focused bug-fix route. No target artifacts were mutated.
