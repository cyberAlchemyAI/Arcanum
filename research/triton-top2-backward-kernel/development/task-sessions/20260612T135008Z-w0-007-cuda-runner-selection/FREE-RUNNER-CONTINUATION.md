# Free Runner Continuation - W0-007

Status: pass-free-runner-kit
Date: 2026-06-12

## Question Answered

Is there a free option, and can this machine run the GPU path?

## Local Machine Answer

This machine is WSL2 with Windows reporting:

```text
AMD Radeon(TM) Graphics
```

WSL exposes `/dev/dxg`, but no NVIDIA CUDA user-space or device surface:

- no `nvidia-smi`;
- no `nvcc`;
- no `/dev/nvidia*`;
- no NVIDIA Docker runtime;
- no `libcuda.so` under `/usr/lib/wsl/lib`.

Therefore the local machine is not a normal Triton CUDA runner.

## Free Option Selected

Selected free hosted notebook path:

1. Kaggle Notebook with GPU accelerator.
2. Google Colab free GPU runtime as fallback.
3. Amazon SageMaker Studio Lab free GPU as second fallback.

## Kit Added

- `FREE-CUDA-RUNNER-KIT.md`
- `scripts/free_cuda_runner_bootstrap.sh`
- `scripts/cuda_runner_probe.py`
- `notebooks/free_cuda_runner_smoke.ipynb`

## Local Validation

```sh
python3 -m json.tool notebooks/free_cuda_runner_smoke.ipynb
python3 -m py_compile scripts/cuda_runner_probe.py
.venv/bin/python scripts/cuda_runner_probe.py
```

The first two checks pass. The local probe correctly blocks with:

```text
torch.cuda.is_available False
triton_available False
nvidia-smi None
BLOCK: CUDA is not available to PyTorch
```

## Next

Run `TASK-W0-008` on Kaggle/Colab/SageMaker using `FREE-CUDA-RUNNER-KIT.md` and
record the probe output.
