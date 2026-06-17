# Presentation Package

Status: `ready-with-boundaries`

## One-Slide Thesis

Hard Top2 routing is not differentiable, so the rigorous implementation path is
to choose a defensible backward contract: exact backward for fixed masks, and
exact backward for a smooth fixed-load relaxation when mixed routing is needed.

## Talk Outline

| Slide | Title | Message |
| --- | --- | --- |
| 1 | The Challenge | Top2 routing is attractive, but hard selection blocks ordinary gradients. |
| 2 | The Boundary | Exact backward is scoped to fixed-mask or smooth fixed-load relaxation paths. |
| 3 | The Method | The evidence harness keeps claims tied to source evidence, tests, and non-claims. |
| 4 | CAP2-v0 | CAP2 is a candidate continuous relaxation, not claimed novel here. |
| 5 | Implementation | PyTorch reference plus Triton kernels for the selected backward contracts. |
| 6 | Validation | RunPod parity and benchmark receipts support the bounded implementation claim. |
| 7 | Formal Slice | Lean plus Mathlib proves router/fixed-mask identities, the finite softmax coordinate derivative, CAP2 definitions, and one fixed-load CAP2 scalar slice; full Jacobian/CAP2 calculus is scoped. |
| 8 | Results | Smoke benchmark medians are sub-millisecond on the recorded GPU. |
| 9 | Limitations | No hard Top2 differentiability, no novelty claim, no production benchmark claim. |
| 10 | Next Work | Softmax/CAP2 formalization, broader scaling, novelty hardening, FP16 analysis. |

## Public-Safety Checklist

| Check | Status |
| --- | --- |
| No private unrelated repository material included. | pass |
| No hard Top2 differentiability claim. | pass |
| No CAP2 novelty claim. | pass |
| No production performance claim. | pass |
| Lean scope is explicitly narrow and Mathlib claims are theorem-specific. | pass |
| Softmax coordinate derivative is theorem evidence; CAP2 reports remain feasibility/deferred-proof evidence. | pass |
| New softmax/CAP2 theorem slices are not described as hard Top2, full Jacobian, or full CAP2 calculus proofs. | pass |
| Benchmark environment is named. | pass |
