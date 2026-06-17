# Task Session Context - W0-007 CUDA Runner Selection

Date: 2026-06-12
Work pack: `research/triton-top2-backward-kernel/WORK-PACK.md`
Task: `TASK-W0-007`
SWU: `SWU-W0-007`

## Controlling Context

- `CUDA-RUNNER-PLAN.md` defines the runner options and acceptance contract.
- `TASK-W0-006` proved the local tower environment is CPU-only.
- Docker exists locally, but Docker runtime inspection exposes `runc`, not an
  NVIDIA runtime.
- No local NVIDIA device or CUDA command surface is visible.

## Local Diagnostics

Observed:

- `/dev/nvidia*`: absent.
- `nvidia-smi`: absent.
- `nvcc`: absent.
- `nvidia-container-runtime`: absent.
- `nvidia-ctk`: absent.
- Docker: installed.
- Docker runtimes: `runc` only.
- SSH/rsync/GitHub CLI: available.

## Write Scope

- task-session evidence;
- decision gate artifact;
- work-pack status synchronization.

No system driver installation, cloud provisioning, paid resource creation, or
remote-host mutation is authorized by this task session.

## Gate

`TASK-W0-007` cannot pass until a CUDA runner path is selected and any access,
budget, or system-driver approval is resolved.
