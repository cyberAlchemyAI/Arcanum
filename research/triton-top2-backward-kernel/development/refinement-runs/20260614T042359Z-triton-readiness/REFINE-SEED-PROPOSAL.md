# Refine Seed Proposal - Triton Runner Readiness

Run ID: `20260614T042359Z-triton-readiness`
Target: `research/triton-top2-backward-kernel`
Preset: `compact`
Research mode: `no-research`

## Operator Intent

Refine the concrete steps needed to make the project Triton-ready and validate
whether the repository already has enough evidence to prove readiness.

## Current Evidence

- `WORK-PACK.md` marks `TASK-W0-008` as `ready-external`.
- `FREE-CUDA-RUNNER-KIT.md` contains the selected free hosted runner path.
- `scripts/free_cuda_runner_bootstrap.sh` installs/checks PyTorch, Triton,
  pytest, numpy, and hypothesis on a hosted runner.
- `scripts/cuda_runner_probe.py` is the readiness oracle.
- `RUNNER-READINESS-BLOCKED.md` records that the local machine is not an NVIDIA
  CUDA/Triton runner.

## Readiness Proof Contract

Triton runner readiness is proven only by captured output from a real NVIDIA
CUDA runner where all of the following pass:

```text
torch.cuda.is_available() == True
triton imports
nvidia-smi runs
project pytest passes
```

The accepted command is:

```sh
bash scripts/free_cuda_runner_bootstrap.sh
python scripts/cuda_runner_probe.py
```

## Current Verdict

The repository has enough instructions and probe code to test readiness, but it
does not yet have enough evidence to prove readiness. The missing artifact is a
successful `scripts/cuda_runner_probe.py` run from Kaggle, Colab, SageMaker, or a
paid NVIDIA CUDA runner.

## Done Criteria For This Refinement

- All readiness steps are explicit.
- The proof contract is unambiguous.
- Existing evidence is classified as sufficient, insufficient, or blocked.
- The next execution route is clear without claiming CUDA readiness early.
