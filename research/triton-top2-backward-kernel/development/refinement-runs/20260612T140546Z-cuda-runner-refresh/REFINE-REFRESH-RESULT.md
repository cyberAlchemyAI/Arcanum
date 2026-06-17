# Refine Refresh Result - CUDA Runner Strategy

Status: pass
Date: 2026-06-12

## Target

`research/triton-top2-backward-kernel`

## Refresh Question

Can we use an online NVIDIA GPU, preferably Google/free first, and what is the
cheapest sensible paid fallback?

## Refined Decision

Use a staged runner strategy:

1. Use free hosted notebook GPU first: Kaggle or Google Colab.
2. Use Google Colab PoC if the user wants the simplest Google path.
3. If free availability fails twice or final benchmark evidence needs more
   repeatability, use paid RunPod as the recommended fallback.

## Why This Is Enough

The work does not need a guaranteed GPU for the first PoC. It needs a CUDA runner
that can prove:

```text
torch.cuda.is_available() == True
triton imports
nvidia-smi runs
project pytest passes
```

Final performance claims need a more repeatable runner, so they should not rely
only on a free notebook.

## Outputs

- `GOOGLE-COLAB-POC.md`
- `PAID-CUDA-RUNNER-FALLBACK.md`
- updates to `CUDA-RUNNER-PLAN.md`
- updates to `WORK-PACK.md`

## Next Route

Run `TASK-W0-008` on Google Colab or Kaggle using `FREE-CUDA-RUNNER-KIT.md`.

If free runners fail twice:

```text
TASK-W0-009: Provision paid on-demand CUDA runner.
```
