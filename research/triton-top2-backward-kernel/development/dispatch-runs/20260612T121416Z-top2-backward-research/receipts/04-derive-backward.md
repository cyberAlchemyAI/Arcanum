# Receipt 04 - Derive Backward

Step id: `derive-backward`

Status: `pass`

Capability: `math-context-builder`

## Evidence

- `research/triton-top2-backward-kernel/derivation.md`
- `research/triton-top2-backward-kernel/FORMAL-MATH-SPEC.md`

## Result

The derivation covers:

- reconstruction gradient;
- fixed-mask gradient into router probabilities;
- auxiliary loss gradient when `f_j` is fixed;
- softmax backward;
- router gradients `dW = dZ^T X` and `dX_router = dZ W`;
- non-theorems that must not be claimed.

## Verdict

`pass`: the fixed-mask backward surface is derived as a research baseline and
formal proof targets are named.
