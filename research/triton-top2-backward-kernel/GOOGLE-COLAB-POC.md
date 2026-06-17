# Google Colab CUDA PoC

Status: ready-external
Date: 2026-06-12

## Purpose

Use Google Colab as a free or low-friction CUDA PoC runner for the Triton
challenge.

Colab is enough for:

- checking that CUDA is available;
- checking that Triton imports;
- running the existing project tests;
- running first Triton kernel smoke tests later.

Colab is not enough for:

- guaranteed GPU availability;
- guaranteed GPU model;
- final repeatable performance benchmark claims.

## Colab Setup

1. Open Google Colab.
2. Runtime -> Change runtime type -> GPU.
3. Upload the `research/triton-top2-backward-kernel` folder or clone the repo if
   repo access is available.
4. Open or recreate the cells from:

```text
notebooks/free_cuda_runner_smoke.ipynb
```

## Minimal Cells

From the tower root:

```python
!bash scripts/free_cuda_runner_bootstrap.sh
!python scripts/cuda_runner_probe.py
```

## Expected Pass

The probe must end with:

```text
PASS: CUDA/Triton runner is ready
```

If it instead says CUDA is unavailable, switch Colab runtime to GPU or try the
Kaggle path.

## Paid Google Fallback

Google Colab Pay As You Go can be used if free GPU access is unavailable. The
current public pricing page lists `$9.99` for `100 Compute Units`, but compute
unit consumption and GPU type are dynamic. Use this only if convenience matters
more than exact hourly pricing.
