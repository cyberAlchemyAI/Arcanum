# Implementation Notes

## Recommended Scope Split

Do not start with a monolithic "entire FFN plus router plus objective" kernel.
Use three layers:

1. **Reference layer:** PyTorch reference for the chosen relaxation.
2. **Router backward layer:** Triton kernel for `dW` and optional `dX_router`, treating `H = FFN(X)` as an input.
3. **Fusion layer:** only after correctness, consider fusing `H` computation or expert FFN backward.

## Zero-Allocation Contract

The Python wrapper should allocate outputs before launch:

```text
dX: [T, D]
dW: [E, D]
dH: [T, E, D] or omitted if FFN owns it elsewhere
```

The kernel should not materialize:

```text
Z [T, E]
P [T, E]
M [T, E]
dP [T, E]
dZ [T, E]
```

Acceptable state:

- scalar/tile values in registers,
- SRAM tile accumulators,
- preexisting forward top-2 indices/gates,
- preallocated reduction outputs or scratch explicitly passed by caller.

## Triton Strategy

For `dW = dZ^T X`:

- Tile over experts and feature dimension.
- Reduce over token blocks.
- Accumulate in FP32.
- Use atomics or a two-pass reduction when multiple programs cover the same `(expert, feature)` tile.

For `dX_router = dZ W`:

- Tile over tokens and feature dimension.
- Reduce over experts.
- Accumulate in FP32.

For row softmax backward:

- Recompute row max and denominator for `P` when not saved.
- Use stable softmax.
- Keep row reductions inside the token/expert tile when `E` fits the block.
- If `E` is larger than one block, use a multi-pass design or require saved row statistics.

## FP16 Guidance

- Load `X`, `W`, and `H` as FP16 where appropriate.
- Accumulate dot products and gradient reductions in FP32.
- Decide output dtype explicitly: FP32 gradients for training stability, or FP16 only if the training stack expects it.
- Disable or specify TF32 behavior when comparing with exact FP32 references.

## Validation Plan

1. Define a PyTorch reference for fixed-mask top-2 and, separately, any requested relaxation.
2. Run `torch.autograd.gradcheck` in FP64/FP32 for the reference relaxation where possible.
3. Compare Triton backward to PyTorch reference in FP32 first.
4. Compare FP16 inputs with FP32 accumulation using tolerances that separate numerical precision from semantic errors.
5. Include tie cases, equal logits, capacity overflow, `E` not power-of-two, `D` not multiple of block size, small `T`, and large `E`.
6. Measure allocations with PyTorch CUDA memory stats around the backward wrapper.

## Likely Failure Modes

- Treating hard top-2 as differentiable without naming a surrogate.
- Computing `f_j` from hard counts but expecting gradients through it.
- Normalized vs unnormalized top-2 gates silently changing gradients.
- Allocating hidden intermediates in the wrapper while the Triton kernel itself is allocation-free.
- Atomics causing nondeterministic small differences in `dW`.
- Capacity constraint interpreted as a loss in one reference and as a forward routing rule in the kernel.
