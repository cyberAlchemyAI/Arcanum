# Final Question Resolution For Work-Pack

Status: `resolved-for-execution`

This file turns remaining questions into working decisions for the full work
pack. These are not truth claims about the original prompt; they are controlled
execution assumptions.

## Resolved Decisions

| Question | Work-Pack Decision |
| --- | --- |
| What does leading `W` mean? | Use `lambda_rec` scalar. Keep original ambiguity noted. |
| What is `FFN(X)`? | Treat as precomputed expert outputs `H` until full FFN backward is explicitly scoped. |
| What is baseline top-2 combine? | Fixed-mask baseline uses `A = M * P`. Add normalized variant only as comparison. |
| What continuous relaxation do we choose? | CAP2-v0 from `CAP2-CANDIDATE-SPEC.md`, compared against entmax/sparsemax and convex sparse top-k. |
| Is CAP2 exact 2-sparse? | No. CAP2-v0 is sparse-ish/top-2-shaped. Exact 2-sparsity is a measured target, not a claim. |
| How does capacity enter? | V0 baseline checks/flags capacity. CAP2-v0 adjusts logits with fixed smooth overload pressure. |
| Do we differentiate through load? | Not initially. Dynamic load gradients are a later extension. |
| Do we need PyTorch? | Yes for full autograd/gradcheck. Current standard-library harness remains the minimal oracle until PyTorch is available. |
| Do we need GPU/Triton now? | No for Waves 0-4. Yes for Triton implementation/performance waves. |
| What is "end"? | End means reference baselines, CAP2 decision, math validation, Triton parity, zero-allocation checks, FP16 tolerance, and final comparison report. |

## Hard Blockers Moved To Gates

| Blocker | Gate |
| --- | --- |
| PyTorch missing | Blocks PyTorch autograd/gradcheck wave, not pure reference work. |
| Triton/GPU missing | Blocks Triton implementation/performance waves only. |
| CAP2 novelty unknown | Blocks novelty claim, not CAP2 candidate testing. |
| Exact 2-sparsity unknown | Becomes metric/acceptance criterion. |

## Completion Definition

The full effort is complete when:

1. V0 fixed-mask baseline passes reference and gradient tests.
2. At least three prior-art baselines run on the same fixtures.
3. CAP2-v0 is either killed or promoted to candidate with evidence.
4. Formal math proof notes/stubs cover V0 and CAP2 scope boundaries.
5. Triton kernel matches selected reference within tolerance.
6. Zero-allocation checks pass.
7. FP16 tolerance checks pass.
8. Final report states what is novel, what is prior art, and what remains unproven.
