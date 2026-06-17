# Context Pack - TASK-W5-001

Task: `TASK-W5-001`

Objective: implement Triton fixed-mask `dW` kernel.

## Controlling Sources

- `WORK-PACK.md`: `TASK-W5-001` is ready after `TASK-W0-008` passed on RunPod.
- `RUNPOD-CUDA-PROBE-PASS.md`: proves an external CUDA/Triton runner exists.
- `scripts/cuda_runner_probe.py`: local runner readiness oracle.
- `reference/router_reference.py`: standard-library manual `dW` and finite-difference oracle.
- `reference/router_torch.py`: PyTorch fixed-mask reference.
- `tests/test_router_reference.py` and `tests/test_router_torch.py`: parity baselines.

## Gate

The task can only pass when a Triton `dW` kernel matches the reference on a CUDA
runner. This local shell is not that runner.

## Local Probe

```text
torch 2.12.0+cpu
torch.cuda.is_available False
triton_available False
nvidia-smi None
BLOCK: CUDA is not available to PyTorch
```

## Verdict

`TASK-W5-001` remains work-pack-ready, but this local task-session cannot execute
or validate it. Run the W5 implementation session on the active RunPod pod or
provide SSH/API access to a live CUDA runner.
