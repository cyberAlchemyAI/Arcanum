# CAP2-v0 Prior-Art Comparison

Status: comparison-ready-for-decision
Date: 2026-06-12

## Task

`TASK-W3-002`: Compare CAP2-v0 against prior-art baselines.

## Scope

This comparison uses the shared local fixture from `reference/router_reference.py`.
It is a reference-level comparison only. It is not a benchmark, not a novelty
claim, and not a Triton-readiness result.

## Compared Variants

| Variant | Role |
| --- | --- |
| Fixed-mask Top2 | Exact fixed-mask backward baseline for the post-selection graph. |
| Normalized selected pair | Same selected pair as fixed mask, but row-normalized weights. |
| Sparsemax | Sparse differentiable probability baseline. |
| Normalized ReLU | Simple sparse-ish differentiable routing baseline. |
| Convex sparse top-k direct mask | Source-backed sparse top-k prior-art mask used directly. |
| Convex sparse top-k normalized masked-softmax | Source-backed sparse top-k prior-art mask composed with normalized softmax weights. |
| CAP2-v0 | Capacity-aware pairwise soft-rank relaxation. |

## Fixture Results

| Variant | Loss | Rec Loss | Aux Loss | Active Counts | Row Sums | Top-2 Weights |
| --- | ---: | ---: | ---: | --- | --- | --- |
| Fixed-mask Top2 | 1.227485800 | 0.827485800 | 0.400000000 | [2, 2, 2] | [0.727324366, 0.744532046, 0.776250294] | [[0.431938, 0.295386], [0.392720, 0.351812], [0.403642, 0.372608]] |
| Normalized selected pair | 1.307308587 | 0.907308587 | 0.400000000 | [2, 2, 2] | [1.000000000, 1.000000000, 1.000000000] | [[0.593873, 0.406127], [0.527472, 0.472528], [0.519989, 0.480011]] |
| Sparsemax | 1.380417900 | 0.980417900 | 0.400000000 | [3, 3, 2] | [1.000000000, 1.000000000, 1.000000000] | [[0.613333, 0.233333], [0.513333, 0.403333], [0.540000, 0.460000]] |
| Normalized ReLU | 1.434352706 | 1.034352706 | 0.400000000 | [1, 2, 2] | [1.000000000, 1.000000000, 1.000000000] | [[1.000000, 0.000000], [0.579710, 0.420290], [0.574074, 0.425926]] |
| Convex top-k direct mask | 2.347000000 | 1.547000000 | 0.800000000 | [2, 2, 2] | [2.000000000, 2.000000000, 2.000000000] | [[1.000000, 1.000000], [1.000000, 1.000000], [1.000000, 1.000000]] |
| Convex top-k normalized masked-softmax | 1.307308587 | 0.907308587 | 0.400000000 | [2, 2, 2] | [1.000000000, 1.000000000, 1.000000000] | [[0.593873, 0.406127], [0.527472, 0.472528], [0.519989, 0.480011]] |
| CAP2-v0 | 1.243467186 | 0.843467186 | 0.400000000 | [3, 3, 3] | [1.000000000, 1.000000000, 1.000000000] | [[0.501831, 0.269005], [0.436156, 0.366288], [0.450566, 0.399573]] |

## Capacity Response Probe

Probe row:

```text
z = [2.0, 1.9, 0.0, -1.0]
```

With no capacity pressure:

```text
A = [0.520408, 0.458864, 0.018974, 0.001754]
```

With expert 0 overloaded and `mu = 2.0`:

```text
A = [0.128701, 0.823155, 0.045001, 0.003144]
```

Expert 0 changed by:

```text
-0.391706840
```

This confirms CAP2-v0 capacity pressure moves routing away from the overloaded
expert in the intended direction on the probe.

## Backward Availability

| Variant | Backward Status |
| --- | --- |
| Fixed-mask Top2 | Manual/PyTorch parity pass for post-selection graph. |
| Normalized selected pair | PyTorch parity pass. |
| Sparsemax | PyTorch baseline pass. |
| Normalized ReLU | PyTorch baseline pass. |
| Convex top-k direct mask | Mask-level custom-autograd parity pass; direct-mask router forward parity pass. |
| Convex top-k normalized masked-softmax | Forward parity pass; full composed backward not yet claimed. |
| CAP2-v0 | PyTorch fixed-load smooth graph gradcheck pass. |

## Interpretation

CAP2-v0 survives as a candidate for further comparison because:

- it is differentiable under fixed load;
- it responds to capacity pressure directly;
- it has lower fixture loss than sparsemax, normalized ReLU, and normalized
  selected-pair comparisons on this fixture;
- it is not identical in support behavior to sparsemax/ReLU/convex top-k.

CAP2-v0 should not be promoted as novel yet because:

- it uses all 3 experts on the shared fixture, so exact top-2 sparsity is not
  satisfied;
- it may still be a minor variant of known soft-rank / NeuralSort-style
  relaxations plus a capacity penalty;
- it has no Triton or zero-allocation implementation;
- it has no dynamic-load gradient.

## Decision Needed

Proceed to `TASK-W3-003`: kill, promote, or defer CAP2-v0.

Recommended decision framing:

1. **Promote as a candidate only**: keep CAP2-v0 for later Triton feasibility
   and broader comparison, with no novelty claim.
2. **Defer CAP2**: preserve the reference but move to formal math or Triton
   fixed-mask work.
3. **Kill CAP2-v0**: record it as too close to soft-rank prior art or too weak
   on exact top-2 sparsity.
