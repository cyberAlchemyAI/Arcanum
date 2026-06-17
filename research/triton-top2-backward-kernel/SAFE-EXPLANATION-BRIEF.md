# Safe Explanation Brief

Use this when explaining the challenge without overclaiming.

## Short Version

This challenge is about building a fast Triton backward kernel for a sparse
router. The dangerous part is that `Top2` is a hard choice, and hard choices do
not have ordinary gradients. So the rigorous path is to first define the
differentiable graph we are actually training, then test/prove that graph, and
only after that write the Triton kernel.

## What I Can Safely Say

- Hard `Top2` is nondifferentiable through the selected indices.
- "Exact backward" only makes sense after choosing a differentiable graph or
  treating the top-2 mask as fixed.
- The load-balancing term resembles MoE router losses from Switch/GShard-style
  routing.
- A PyTorch reference is the first anti-hallucination tool.
- Lean can help prove the clean gradient identities over real numbers.
- Triton tests must compare against the reference and separately check
  allocation/FP16 behavior.

## What I Should Not Say Yet

- "We have the exact gradient through Top2."
- "The capacity constraint is differentiable."
- "Lean proves the Triton kernel is correct."
- "FP16 behavior follows from the real-number proof."
- "The objective is fully specified."

## Honest Explanation@

The problem statement mixes a hard routing operation with a desire for exact
backpropagation. That is only rigorous if we choose a bridge:

```text
hard Top2 forward + fixed mask backward
```

or:

```text
RelaxedTop2 / soft routing / other smooth surrogate
```

Once that bridge is chosen, we can:

1. write a PyTorch reference;
2. test its gradients;
3. prove the core equations in Lean if we want formal assurance;
4. make Triton match the reference;
5. measure zero allocation and FP16 error.

## Good Phrase For The Challenge

The challenge is not "differentiate Top2." The challenge is to define a
trainable routing surrogate whose backward pass is exact for that surrogate, then
fuse that backward pass into a zero-allocation Triton kernel.
