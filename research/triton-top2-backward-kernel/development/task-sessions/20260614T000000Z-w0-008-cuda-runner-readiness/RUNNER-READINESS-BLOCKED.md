# TASK-W0-008 CUDA Runner Readiness Evidence

Status: BLOCK
Recorded: 2026-06-14
Scope: local substitute probe for `TASK-W0-008`

## Task

`TASK-W0-008 | W0 | Validate CUDA/Triton runner readiness`

Dependency `TASK-W0-007` is satisfied as `pass-free-runner-kit`: the selected
path is a free hosted CUDA notebook runner using `FREE-CUDA-RUNNER-KIT.md`.

## Acceptance Contract

The runner can only pass when all of these are true on an NVIDIA CUDA runner:

```text
torch.cuda.is_available() == True
triton imports
nvidia-smi runs
project pytest passes
```

## Local Environment Probe

Local device surface:

```text
which nvidia-smi -> not found
which nvcc -> not found
ls /dev/nvidia* -> no entries
ls /dev/dxg -> /dev/dxg exists
ls /usr/lib/wsl/lib/libcuda.so* -> no entries
```

System Python probe:

```text
$ python3 scripts/cuda_runner_probe.py
BLOCK: torch import failed: No module named 'torch'
```

Tower `.venv` probe:

```text
$ .venv/bin/python scripts/cuda_runner_probe.py
python 3.12.3 (main, Mar 23 2026, 19:04:32) [GCC 13.3.0]
torch 2.12.0+cpu
torch.cuda.is_available False
triton_available False
nvidia-smi None
BLOCK: CUDA is not available to PyTorch
```

Environment smoke test:

```text
$ .venv/bin/python -m pytest tests/test_environment.py -q
s..                                                                      [100%]
2 passed, 1 skipped in 2.73s
```

## Verdict

This local environment is not an NVIDIA CUDA/Triton runner. It cannot satisfy
`TASK-W0-008` because PyTorch is CPU-only in the tower `.venv`, Triton is not
importable, `nvidia-smi` is absent, `nvcc` is absent, and no `/dev/nvidia*`
device or WSL `libcuda.so` surface is available.

Do not mark `TASK-W0-008` complete from this evidence.

## Exact Unblock Actions

1. Run `FREE-CUDA-RUNNER-KIT.md` on Kaggle Notebook with GPU accelerator.
2. From the tower root on the hosted runner, run:

```sh
bash scripts/free_cuda_runner_bootstrap.sh
python scripts/cuda_runner_probe.py
```

3. Paste or commit the full successful probe output into a new
   `TASK-W0-008` evidence artifact.
4. If Kaggle lacks GPU availability, repeat the same kit on Google Colab free
   GPU runtime, then SageMaker Studio Lab if available.
5. If two free hosted attempts fail because no GPU is allocated or the runtime
   is unstable, proceed to `TASK-W0-009` using `PAID-CUDA-RUNNER-FALLBACK.md`.
