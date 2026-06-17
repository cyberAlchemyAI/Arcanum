# Refine Strategy Proposal Result - Triton Runner Readiness

Status: `strategy-proposal`

The repository has enough to attempt and validate a Triton readiness proof, but
it does not yet contain the evidence required to prove readiness.

## Required Proof

Run this from the tower root on Kaggle, Colab, SageMaker, RunPod, or another
NVIDIA CUDA runner:

```sh
bash scripts/free_cuda_runner_bootstrap.sh
python scripts/cuda_runner_probe.py
```

The proof is accepted only if the probe prints:

```text
PASS: CUDA/Triton runner is ready
```

and the preceding output shows:

```text
torch.cuda.is_available True
triton_available True
nvidia-smi <non-empty path>
project pytest passes
```

## Current Verdict

Current local evidence is a blocker, not a pass. `TASK-W0-008` remains
`ready-external` until successful external runner output is recorded.
