# Claim Ledger

## Source-Backed Claims

| ID | Claim | Source Kind | Evidence |
| --- | --- | --- | --- |
| C001 | Triton supports customized block-level matrix multiplication patterns and FP16 matmul kernels. | primary-source | Triton matmul tutorial: https://triton-lang.org/main/getting-started/tutorials/03-matrix-multiplication.html |
| C002 | Triton softmax kernels use row-wise max subtraction and reductions to avoid overflow and reduce memory traffic. | primary-source | Triton fused softmax tutorial: https://triton-lang.org/main/getting-started/tutorials/02-fused-softmax.html |
| C003 | `tl.dot` multiplies 2D or 3D blocks with compatible inner dimensions and supports FP16/BF16/FP32-like tensor types. | primary-source | Triton `tl.dot` API: https://triton-lang.org/main/python-api/generated/triton.language.dot.html |
| C004 | Switch Transformer auxiliary loss has the form `alpha * N * sum_i f_i P_i`, with `f` nondifferentiable and `P` differentiable. | primary-source | Switch Transformer paper, section 2.2: https://arxiv.org/pdf/2101.03961 |
| C005 | GShard uses group-level top-2 gating, capacity, and an auxiliary loss where nondifferentiable counts are paired with differentiable mean gates. | primary-source | GShard paper, algorithm 1 and section 2.2: https://arxiv.org/pdf/2006.16668 |
| C006 | PyTorch custom backward integration is normally exposed through `torch.autograd.Function` or custom operator registration. | primary-source | PyTorch extending docs: https://docs.pytorch.org/docs/stable/notes/extending.html |

## Local Inferences

| ID | Claim | Source Kind | Rationale |
| --- | --- | --- | --- |
| I001 | The requested objective is MoE/router-like rather than ordinary dense FFN training. | local-inference | It combines router weights, top-2 selection, expert FFNs, load fractions, and an expert capacity constraint. |
| I002 | "Exact backward" and "bypassing non-differentiable selection" are compatible only after defining the relaxed graph. | local-inference | Hard top-k indices are piecewise constant with discontinuities; exact gradients require a differentiable surrogate or a fixed-mask interpretation. |
| I003 | A single monolithic kernel can compute `dW` for moderate `E` but may need staged reductions for large `T, D, E`. | local-inference | `dW = dZ^T X` is a reduction over tokens; atomics or split reductions may be required. |
| I004 | If `FFN(X)` is not precomputed, a zero-allocation backward kernel for the entire expression must also include expert FFN backward, making scope much larger. | local-inference | Expert FFN gradients require layer weights, activations, nonlinear derivatives, and their own reductions. |

## Operator Readings

| ID | Reading | Status |
| --- | --- | --- |
| O001 | Treat `FFN(X)` as an input tensor to the router backward research pass unless implementation scope explicitly includes expert FFN internals. | recommended |
| O002 | Store top-2 indices/gates from forward if the backward must match the actual forward routing exactly. | recommended |
| O003 | For FP16 optimization, accumulate reductions in FP32 and cast outputs according to wrapper expectations. | recommended |
| O004 | Validate against a PyTorch reference implementation before performance tuning. | required |

## Blockers

| ID | Blocker | Impact |
| --- | --- | --- |
| B001 | The leading `W` before the norm is ambiguous. | Cannot know whether it is a scalar weight, typo, or operator. |
| B002 | `Top2(sigma(...)) * FFN(X)` lacks shape and combine semantics. | Cannot derive final `dX`, `dW`, `dFFN` contract exactly. |
| B003 | The continuous relaxation is not specified. | Cannot honestly implement "exact" relaxation gradients. |
| B004 | Capacity handling is unspecified: hard constraint, projection, penalty, barrier, or forward-only gate. | Cannot include correct gradient contribution for violations. |
