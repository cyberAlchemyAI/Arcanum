# CUDA Runner Plan - Triton Top2 Backward Challenge

Status: free-first-paid-fallback-ready
Date: 2026-06-12

## Objective

Make a real CUDA-capable runner available for Triton kernel validation without
confusing CPU PyTorch readiness with GPU kernel readiness.

## Current Evidence

Local machine:

- Docker is installed: `Docker version 28.0.1`.
- Docker runtime list contains `runc`, but no NVIDIA runtime.
- `nvidia-smi` is unavailable.
- `nvcc` is unavailable.
- Local tower `.venv` has CPU-only PyTorch: `torch 2.12.0+cpu`, CUDA `False`.
- Triton is not installed in the tower `.venv`.
- A task-session for `TASK-W0-007` confirmed no local NVIDIA device/runtime and
  recorded a decision gate at
  `development/task-sessions/20260612T135008Z-w0-007-cuda-runner-selection/DECISION-GATE.md`.
- Follow-up selected the free hosted notebook path. See `FREE-CUDA-RUNNER-KIT.md`.
- Refine refresh added `GOOGLE-COLAB-POC.md` and
  `PAID-CUDA-RUNNER-FALLBACK.md`.

Conclusion: local CPU work can continue, but W5-W7 require either a properly
configured local NVIDIA runtime or a separate GPU host/container.

## Runner Options

| Option | Description | When To Choose | Blockers |
| --- | --- | --- | --- |
| Local NVIDIA Docker | Use this machine with NVIDIA drivers plus NVIDIA Container Toolkit. | Choose only if the host has an NVIDIA GPU and driver support can be installed. | Requires host GPU, driver, `nvidia-smi`, and Docker NVIDIA runtime. |
| Remote GPU Host | Use an existing SSH-accessible GPU machine. | Choose if a trusted GPU box already exists. | Requires SSH access, Python/uv, CUDA driver, and workspace transfer or git checkout. |
| Cloud GPU Instance | Rent a small CUDA-capable instance for validation. | Choose if no local/remote GPU exists. | Requires account, budget approval, region/GPU choice, and teardown discipline. |
| Managed Notebook | Use Colab/Kaggle/Runpod-style notebook for early Triton smoke. | Choose for fast prototype validation only. | Harder to preserve repo evidence and repeatable task-session artifacts. |

Selected path:

1. Use free Kaggle or Google Colab for PoC and first Triton correctness smoke.
2. Use RunPod paid on-demand GPU as fallback if free availability blocks twice or
   final benchmark evidence needs repeatability.

## Required Runner Contract

A runner is accepted only when all commands pass on the runner:

```sh
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
python -c "import triton; print(triton.__version__)"
nvidia-smi
```

For this project, the runner must also be able to execute:

```sh
cd research/triton-top2-backward-kernel
python -m pytest tests -v
```

## New Work-Pack Tasks

| Task ID | Purpose | Done Criteria |
| --- | --- | --- |
| `TASK-W0-007` | Select and prepare a CUDA runner path. | A chosen runner option, access method, setup commands, cost/approval state, and teardown rule are recorded. |
| `TASK-W0-008` | Validate CUDA/Triton runner readiness. | Torch CUDA, Triton import, `nvidia-smi`, and project pytest pass on the selected runner, or exact blocker is recorded. |
| `TASK-W0-009` | Provision paid on-demand CUDA runner. | Provider, GPU type, spending cap, setup commands, validation output, and teardown evidence are recorded. |

## Recommended Next Route

Run `FREE-CUDA-RUNNER-KIT.md` on Kaggle or Google Colab and paste the
`scripts/cuda_runner_probe.py` output back into the task-session evidence for
`TASK-W0-008`.

If free runner availability fails twice, run `TASK-W0-009` with the paid fallback
in `PAID-CUDA-RUNNER-FALLBACK.md`.

Do not start W5 Triton implementation until `TASK-W0-008` passes.
