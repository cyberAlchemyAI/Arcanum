# Final Prior-Art And Novelty Report

Status: `complete-candidate-no-novelty-claim`
Date: 2026-06-14

## Executive Result

The challenge has a validated implementation path for a zero-allocation-style
fixed-mask Triton backward baseline and a selected continuous relaxation,
CAP2-v0, with fixed-load exact-backward parity on RunPod.

The rigorous claim is:

```text
We implemented and validated exact backward for the chosen smooth CAP2-v0
relaxation graph with fixed load, and validated Triton parity for dZ,
dX_router, dH, and dW against a PyTorch/manual reference.
```

The rigorous non-claim is:

```text
We do not claim exact backward through hard Top2, CAP2 novelty, exact 2-sparsity,
dynamic-load gradients, or production-optimized performance.
```

## What Was Built

Reference layer:

- fixed-mask Top2 reference and manual backward;
- PyTorch fixed-mask autograd parity;
- sparsemax baseline;
- normalized ReLU baseline;
- convex sparse top-k PAV mask oracle and custom-autograd parity;
- CAP2-v0 standard-library and PyTorch forward reference;
- CAP2-v0 manual exact backward for the fixed-load smooth graph.

Triton layer:

- fixed-mask `dW = dZ^T @ X`;
- fixed-mask `dX_router = dZ @ W`;
- fixed-mask `dH = A * dY`;
- CAP2 row-local `dZ` and `dH`;
- CAP2 `dX_router` and `dW` through validated matrix kernels.

Validation layer:

- PyTorch gradcheck and finite differences;
- RunPod CUDA/Triton parity tests;
- fixed-mask zero-allocation checks using preallocated outputs;
- fixed-mask FP16 tolerance checks with FP32 outputs;
- fixed-mask vs CAP2 smoke benchmark.

## Prior-Art Positioning

The implemented baselines cover the key families needed to avoid a shallow
claim:

| Family | Local Coverage | Status |
| --- | --- | --- |
| Hard Top2 fixed-mask backward | Manual and PyTorch parity for post-selection graph | pass |
| Sparsemax / entmax family | Sparsemax baseline implemented; entmax remains named but not implemented | partial |
| ReLU / ReMoE-style sparse-ish routing | Normalized ReLU baseline implemented | pass |
| Convex sparse top-k / SOFT top-k direction | Source-backed PAV mask oracle and custom-autograd parity | partial |
| Soft-rank / NeuralSort-style direction | CAP2 pairwise soft-rank relaxation implemented | candidate |
| Capacity-aware MoE auxiliary loss | Fixed `f` and differentiable mean probability auxiliary term | pass |

CAP2-v0 is closest to the soft-rank relaxation family, with an added fixed-load
capacity pressure term and normalized gated softmax combine weights. That is a
valid candidate engineering route, but not enough evidence for novelty.

## CAP2-v0 Evidence

CAP2-v0 survived the local decision process because it:

- is differentiable under fixed load;
- responds to capacity pressure in the expected direction;
- has reference-level lower fixture loss than sparsemax, normalized ReLU, and
  normalized selected-pair variants on the shared fixture;
- has an exact manual backward for the named smooth graph;
- has RunPod Triton parity for `dZ`, `dX_router`, `dH`, and `dW`.

CAP2-v0 remains limited because it:

- does not guarantee exact two active experts;
- may be a straightforward variant of known soft-rank relaxations;
- does not differentiate through dynamic load;
- has only smoke benchmark evidence, not production tuning.

## Triton And Benchmark Evidence

RunPod validation reached:

- W6B focused Triton suite: `14 passed`;
- W6B full suite: `67 passed`;
- W6C focused Triton suite: `15 passed`;
- W6C full suite: `68 passed`;
- W7 benchmark-refresh focused Triton suite: `15 passed`;
- W7 benchmark-refresh full suite: `68 passed`.

Benchmark smoke results on NVIDIA RTX PRO 4000 Blackwell:

| Size | Fixed Mask Median ms | CAP2 Median ms |
| --- | ---: | ---: |
| small, T=128 E=8 D=64 | 0.1350 | 0.1739 |
| medium, T=512 E=16 D=128 | 0.1378 | 0.1673 |

Interpretation:

- CAP2 is slower than fixed-mask in these smoke timings, as expected, because it
  computes pairwise soft-rank relaxation work.
- Both measured paths are sub-millisecond on the recorded RunPod GPU for the
  selected smoke sizes.
- These timings are useful engineering evidence, not final production
  performance claims.

## Challenge Answer

If the challenge asks for “exact backward” while also bypassing
non-differentiable hard selection, the honest solution is to name the continuous
graph and be exact for that graph.

This work does that:

```text
Hard Top2 is not differentiated.
CAP2-v0 is the selected continuous relaxation.
The backward is exact for CAP2-v0 with fixed load.
Triton parity is validated against the reference.
```

That is a real accomplishment. It is not diminished by using fixed-mask
baselines; the fixed-mask path is the control group that proves we understand
the post-selection backward before introducing a relaxation.

## Final Status

| Area | Status |
| --- | --- |
| Research tower and glossary | pass |
| Prior-art baseline map | pass |
| Fixed-mask reference backward | pass |
| Fixed-mask Triton backward | pass-runpod |
| Fixed-mask zero-allocation checks | pass-runpod |
| Fixed-mask FP16 checks | pass-runpod |
| CAP2 candidate reference | pass |
| CAP2 exact backward reference | pass |
| CAP2 Triton backward parity | pass-runpod |
| Fixed-mask vs CAP2 benchmark | pass-runpod |
| Novelty claim | not claimed |

## Recommended Public Framing

Use:

```text
Implemented a Triton-backed exact backward path for a fixed-load continuous
Top2 routing relaxation, with PyTorch/manual VJP parity, finite-difference
checks, and RunPod CUDA validation.
```

Avoid:

```text
Proved a novel Top2 differentiable router.
```

The second sentence is not yet supported. The first one is.
