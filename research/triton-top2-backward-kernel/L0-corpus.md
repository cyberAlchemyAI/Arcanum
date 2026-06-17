# L0 Corpus - Source Records

Checked: 2026-06-12

## Primary Sources

| Source | Use |
| --- | --- |
| Triton matrix multiplication tutorial, https://triton-lang.org/main/getting-started/tutorials/03-matrix-multiplication.html | Block-level matmul pattern, FP16 kernel context, pointer arithmetic, tiling, accumulation. |
| Triton fused softmax tutorial, https://triton-lang.org/main/getting-started/tutorials/02-fused-softmax.html | Numerically stable row softmax, row-level reductions, bandwidth/fusion motivation. |
| Triton `tl.dot` API, https://triton-lang.org/main/python-api/generated/triton.language.dot.html | Block matrix multiplication semantics and dtype/accumulator constraints. |
| PyTorch extending autograd note, https://docs.pytorch.org/docs/stable/notes/extending.html | Custom backward integration requirements for PyTorch. |
| PyTorch custom operators landing page, https://docs.pytorch.org/tutorials/advanced/custom_ops_landing_page.html | Custom op integration with PyTorch subsystems. |
| PyTorch user-defined Triton kernels with `torch.compile`, https://docs.pytorch.org/tutorials/recipes/torch_compile_user_defined_triton_kernel_tutorial.html | How user-defined Triton kernels fit into compiled PyTorch flows. |
| GShard paper, https://arxiv.org/pdf/2006.16668 | Top-2 MoE routing, capacity, auxiliary loss, nondifferentiable top-2 count approximated through mean gates. |
| Switch Transformer paper, https://arxiv.org/pdf/2101.03961 | Auxiliary load-balancing loss `alpha * N * sum_i f_i P_i`; `f` is nondifferentiable, `P` is differentiable. |
| Sparsely-Gated MoE paper, https://arxiv.org/abs/1701.06538 | Historical MoE gating and conditional computation context. |

## Context Extract

- Triton is relevant because the requested operation wants fused GPU kernels, FP16-friendly block operations, and no intermediate allocations.
- The objective is MoE-router-shaped: `X W^T` produces router logits, `sigma` likely means softmax, `Top2` selects two experts, and `FFN(X)` likely denotes per-expert feed-forward outputs.
- The load-balancing term matches the Switch/GShard family: a hard routing fraction `f_j` multiplied by a differentiable probability average `P_j`.
- The capacity constraint `max(f_j) <= 2.1 / E` is a load ceiling, roughly "no expert receives more than 2.1x uniform traffic."

## Warning

The problem statement is not implementation-complete. It lacks shapes, exact `Top2`
semantics, whether `W` before the norm is a scalar/operator/typo, whether `FFN(X)`
is precomputed or inside the kernel, and what "exact" means after continuous
relaxation.
