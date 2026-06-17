$# Tooling Plan - Triton Top2 Backward Challenge

Status: planned
Date: 2026-06-12

## Objective

Add the minimum tools needed to move from the current standard-library oracle to
PyTorch reference parity, formal/math checks, Triton kernel validation, and
zero-allocation/FP16 evidence.

## Current Local Facts

- Python is available: `Python 3.12.3`.
- `pip` is available.
- `uv` is available: `uv 0.9.10`.
- PyTorch CPU is installed in `research/triton-top2-backward-kernel/.venv`.
- pytest, numpy, and hypothesis are installed in the same `.venv`.
- Triton is not installed in the `.venv`.
- No local NVIDIA command surface is visible: `nvidia-smi` and `nvcc` are absent.
- Docker is installed locally, but Docker runtimes currently expose `runc`, not
  an NVIDIA runtime.

## Tooling Layers

| Layer | Purpose | Tools | Local Status |
| --- | --- | --- | --- |
| T0 | Existing no-dependency oracle | Python stdlib `unittest` | ready |
| T1 | CPU reference and TDD | `uv`, venv, `pytest`, `numpy`, `torch` | ready |
| T2 | Gradient rigor | `torch.autograd.gradcheck`, `hypothesis` optional | ready |
| T3 | Formal/math validation | Lean/Lake or proof-note fallback | planned |
| T4 | Triton implementation | `triton`, CUDA-capable PyTorch, NVIDIA GPU runtime | blocked locally |
| T5 | Systems/performance evidence | CUDA memory stats, profiler timing, optional Nsight | blocked locally |

See `CUDA-RUNNER-PLAN.md` for the runner acquisition path.

## Recommended Install Strategy

Create an isolated environment inside the research tower:

```sh
cd research/triton-top2-backward-kernel
uv venv .venv
source .venv/bin/activate
uv pip install pytest numpy hypothesis
```

Then install PyTorch according to the execution target:

```sh
# CPU-only reference path
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
```

For Triton/GPU work, use a machine or container with NVIDIA CUDA support and
install matching PyTorch/Triton wheels there:

```sh
uv pip install torch triton pytest numpy hypothesis
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
python -c "import triton; print(triton.__version__)"
nvidia-smi
```

Do not treat a CPU-only PyTorch install as evidence that Triton kernels are
validated.

## Files To Add

| File | Purpose |
| --- | --- |
| `requirements-cpu.txt` | Minimal CPU reference dependencies: `pytest`, `numpy`, `hypothesis`, CPU PyTorch note. |
| `requirements-gpu.txt` | GPU runner dependencies: `pytest`, `numpy`, `hypothesis`, `torch`, `triton`. |
| `tests/test_environment.py` | Fast environment gate that reports torch/triton/cuda availability without failing unrelated stdlib tests. |
| `development/task-sessions/<run>/RESULT.md` | Evidence from the install/check attempt. |

## Work-Pack Changes

Add a W0 tooling subwave before W1:

| Task ID | Objective | Done Criteria |
| --- | --- | --- |
| `TASK-W0-004` | Add isolated dependency manifests and environment check tests. | requirement files and env test exist. |
| `TASK-W0-005` | Provision CPU reference environment. | PyTorch CPU import and pytest test run succeed, or blocker recorded. |
| `TASK-W0-006` | Provision GPU/Triton runner. | `torch.cuda.is_available()`, Triton import, and `nvidia-smi` succeed, or blocker recorded. |
| `TASK-W0-007` | Select and prepare a CUDA runner path. | A runner option, access method, setup commands, approval/cost state, and teardown rule are recorded. |
| `TASK-W0-008` | Validate CUDA/Triton runner readiness. | Torch CUDA, Triton import, `nvidia-smi`, and project pytest pass on selected runner, or exact blocker recorded. |

## Validation Commands

Always run:

```sh
python3 -m unittest discover -s research/triton-top2-backward-kernel/tests -v
```

After CPU env provisioning:

```sh
cd research/triton-top2-backward-kernel
.venv/bin/python -m pytest tests -v
.venv/bin/python -c "import torch; print(torch.__version__)"
```

After GPU env provisioning:

```sh
cd research/triton-top2-backward-kernel
.venv/bin/python -c "import torch; print(torch.cuda.is_available())"
.venv/bin/python -c "import triton; print(triton.__version__)"
nvidia-smi
```

## Decision Gates

- If CPU PyTorch installs, W1-W3 can proceed locally.
- If GPU/Triton remains unavailable, W5-W7 stay blocked and must run on a GPU
  host/container.
- If dependency install fails, preserve the exact error in a task-session result
  instead of changing math or implementation scope.
- If Lean is unavailable, W4 can proceed with proof-note artifacts and mark Lean
  execution as blocked.

## Next Execution Step

Run a task-session for `TASK-W0-007` if the priority is unblocking GPU/Triton
work. Run `TASK-W1-001` in parallel if the priority is CPU reference progress.
