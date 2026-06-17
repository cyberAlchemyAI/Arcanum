# Task Session Result - TASK-W5-001 Bug-Fix Continuation

Status: `pass-runpod`

## Summary

Fixed the first W5 Triton `dW` implementation for the RunPod failure mode:

- Requested tile sizes are now converted to Triton-safe physical dot tiles with minimum size `16`.
- Logical output remains `[E, D]` through existing load/store masks.
- `tl.dot` now uses `input_precision="ieee"` to avoid TF32 drift in the strict FP32 fixture test.
- Added a CPU-side launch-shape test so local validation catches sub-16 requested tiles before the pod loop.

## Files Updated

- `reference/router_triton.py`
- `tests/test_router_triton.py`
- `scripts/free_cuda_runner_bootstrap.sh`
- `<cuda-runner-iteration-command>`

## Local Validation

```sh
.venv/bin/python -m py_compile reference/router_triton.py tests/test_router_triton.py
.venv/bin/python -m pytest tests/test_router_triton.py -q
.venv/bin/python -m pytest tests -q
```

Results:

```text
tests/test_router_triton.py: 2 passed, 3 skipped in 1.96s
full suite: 51 passed, 4 skipped in 2.67s
```

The skipped tests are the CUDA/Triton tests that require the RunPod GPU.

## Runner Bundles

Validated RunPod iteration bundle:

```text
research/triton-top2-backward-kernel/development/runner-bundles/triton-top2-iteration-20260614T071552Z.tar.gz
sha256: 9462ef537e0784fee85ffd49e5268bd50a9028e53ac06fd8378c42c5f3f31e13
```

Final evidence archive:

```text
research/triton-top2-backward-kernel/development/runner-bundles/triton-top2-w5-kernel-bugfix-20260614T070808Z.tar.gz
sha256: 91b73067da35b29c85b0c104a866510d458d5af2e8d09cb08626df83179f78c0
```

## External Validation

RunPod command:

```sh
cd <repo>/research/triton-top2-backward-kernel
<cuda-runner-iteration-command>
```

Result:

```text
CUDA/Triton probe: 55 passed in 4.31s
tests/test_router_triton.py: 5 passed in 2.92s
full suite: 55 passed in 3.73s
PASS: remote CUDA/Triton iteration completed.
```

The first rerun exposed a harness issue, not a kernel issue: remote `tar`
extraction attempted to restore local UID/GID ownership on a filesystem that
does not permit `chown`. The iteration script now extracts with
`--no-same-owner`. The second rerun exposed a bootstrap portability issue:
system Python rejected global pip writes under PEP 668. The bootstrap now
reuses an already-good Python when possible and falls back to a local
`.venv --system-site-packages` when packages must be installed.

## Follow-Up

- `TASK-W5-002`, `TASK-W6-001`, `TASK-W7-001`, and `TASK-W7-002` are now unblocked by `TASK-W5-001`.
- Keep the current non-claims: this is not yet fused full backward, zero allocation, final FP16 policy, or performance evidence.
