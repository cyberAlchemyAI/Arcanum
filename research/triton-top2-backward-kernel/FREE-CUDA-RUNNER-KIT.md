# Free CUDA Runner Kit

Status: ready-external
Date: 2026-06-12

## Local Machine Verdict

This machine is WSL2 on Windows and exposes `/dev/dxg`, but Windows reports:

```text
AMD Radeon(TM) Graphics
```

No NVIDIA CUDA surface is visible in WSL:

- no `nvidia-smi`;
- no `nvcc`;
- no `/dev/nvidia*`;
- no NVIDIA Docker runtime;
- no `libcuda.so` under `/usr/lib/wsl/lib`.

Conclusion: this machine cannot run normal Triton CUDA kernels unless an NVIDIA
GPU is added/enabled on the Windows host with WSL-compatible NVIDIA drivers.

## Selected Free Path

Use a free hosted notebook GPU as the first CUDA runner.

Recommended order:

1. Kaggle Notebook with GPU accelerator.
2. Google Colab free GPU runtime.
3. Amazon SageMaker Studio Lab free GPU, if available.

Kaggle is the preferred free path for this project because it is notebook-based,
has a GPU accelerator setting, and can run shell commands directly from cells.
Colab is a good fallback, but GPU availability and limits are explicitly not
guaranteed.

## Files In This Kit

| File | Purpose |
| --- | --- |
| `scripts/free_cuda_runner_bootstrap.sh` | Installs/checks PyTorch, Triton, pytest, numpy, and hypothesis on a hosted runner. |
| `scripts/cuda_runner_probe.py` | Validates CUDA/Triton readiness and runs the project tests when invoked from the tower root. |
| `notebooks/free_cuda_runner_smoke.ipynb` | Copy/paste notebook for Kaggle or Colab. |

## Kaggle Notebook Steps

1. Create or open a Kaggle notebook.
2. In notebook settings, set accelerator to GPU.
3. Add the project files by one of these methods:
   - upload an archive of `research/triton-top2-backward-kernel`;
   - connect to GitHub and clone the repository if access is available.
4. From the tower root, run:

```sh
bash scripts/free_cuda_runner_bootstrap.sh
python scripts/cuda_runner_probe.py
```

## Colab Steps

1. Open a Colab notebook.
2. Runtime -> Change runtime type -> GPU.
3. Upload/clone the project.
4. From the tower root, run:

```sh
bash scripts/free_cuda_runner_bootstrap.sh
python scripts/cuda_runner_probe.py
```

## Acceptance Contract

The free runner passes only when this succeeds:

```text
torch.cuda.is_available() == True
triton imports
nvidia-smi runs
project pytest passes
```

If the free runner has no GPU available, record that exact output and try the
next free option.
