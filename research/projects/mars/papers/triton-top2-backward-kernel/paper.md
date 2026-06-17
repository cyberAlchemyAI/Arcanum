# A Traceable Case Study in Exact Backward Kernels for Relaxed Top2 Routing

## Abstract

This paper package documents a bounded implementation case study for a
Top2-style routing challenge. The original challenge asks for a zero-allocation
Triton kernel executing an exact backward pass around an objective involving
`Top2(softmax(X W^T))`, an FFN branch, and a load-balancing term. The central
technical obstacle is that hard Top2 selection is not differentiable: small
changes in logits can change which experts are selected.

The implemented path therefore separates the problem into evidence-backed
contracts. Fixed-mask kernels compute exact backward for a fixed selected mask.
The CAP2-v0 path computes exact backward for a smooth, fixed-load relaxation
used as the selected continuous surrogate. This paper does not claim hard Top2
differentiability, CAP2 novelty, production-optimized performance, or formal
proof of the Triton implementation. Its contribution is a traceable,
reviewable package connecting reference math, PyTorch checks, Triton parity
tests, smoke benchmarks, and a narrow Lean boundary slice.

Evidence: EV-TRITON-003, EV-TRITON-004, EV-FORMAL-001.

## Problem and Non-Differentiability Background

The routing expression starts with scores `X W^T`, applies a softmax, and then
selects the top two experts. The softmax portion is smooth, but the hard Top2
selection is a discrete operation. When the ordering of two experts changes,
the selected set can jump. That jump is why an ordinary gradient through the
hard selection is not available.

The practical bridge is to decide what backward contract is being implemented.
For a fixed mask, the mask is treated as given data and the backward pass is
exact for the smooth operations downstream of that mask. For CAP2-v0, the
selection is replaced by a smooth fixed-load relaxation, and exact backward is
claimed only for that chosen relaxation graph.

Evidence: EV-TRITON-005, EV-TRITON-006, EV-FORMAL-001. Guard: NC-001.

## Research Method and MARS Evidence Harness

The package uses MARS as a research-to-paper harness. The evidence manifest
classifies source materials, implementation surfaces, validation receipts, raw
data, and formal artifacts. The reference ledger records how each source may be
used in the paper and which guard applies.

This matters because the project contains several different kinds of truth:
mathematical intent, executable implementation, empirical validation, benchmark
data, and publication prose. The MARS layer prevents those from being blended
into stronger claims than the evidence supports.

Evidence: EV-MARS-001 through EV-MARS-005.

## Baselines and Prior Art Positioning

The case study considers fixed-mask backward kernels and a candidate continuous
relaxation path. The prior-art work in the research tower is used as a guard:
CAP2-v0 remains candidate-only and is not presented as a proven novel method.
The proper claim is narrower: given the selected relaxation contract, the
implementation and tests show a working exact-backward path for that contract.

Evidence: EV-TRITON-002, EV-TRITON-003. Guard: NC-002.

## CAP2-v0 Relaxation and Exact Fixed-Load Backward

CAP2-v0 is used as a continuous relaxation to bypass the non-differentiable
hard Top2 selection. In the W6 validation boundary, load is fixed. Within that
fixed-load graph, the backward pass produces the expected gradients for the
router logits, input contribution, hidden branch, and weight matrix.

The W6 parity report closes the selected relaxation path with this scope:
reference/manual VJP, row-local Triton components, and Triton reductions agree
on the tested contracts. The phrase "exact backward" should be read inside
this boundary only.

Evidence: EV-TRITON-003, EV-RUN-001, EV-RUN-002, EV-RUN-003. Guards: NC-001,
NC-003, NC-004.

## Formal Boundary Validation

The Lean package under `formal/` now has two layers. The first layer encodes a
small boundary slice: hard Top2 selection is a non-theorem for this package,
fixed load is an assumption, Triton memory behavior is outside the Lean proof,
and FP16 numerical analysis is deferred.

The second layer uses Mathlib to prove real-valued finite-sum adjoint identities
for the router linear map `logits(X, W) = X W^T`. The theorem
`dWReal_adjoint` shows that the dW contraction has the correct inner-product
action for the W argument. The theorem `dXRouterReal_adjoint` does the same for
the router-side X argument.

The third layer composes those identities with fixed mask/upstream routing
weights. The theorem `fixedMaskDW_adjoint` proves the fixed-mask dW adjoint
identity, and `fixedMaskDXRouter_adjoint` proves the matching fixed-mask
dX-router identity. This is still a fixed-mask theorem: it does not differentiate
the act of selecting the mask.

The fourth layer adds a finite softmax derivative slice and a CAP2 definition
slice. `softmaxDen_pos` proves the softmax denominator is positive for a
nonempty expert index set. `softmaxCoord_coordLine_hasDerivAt` proves the
finite softmax coordinate derivative along a coordinate perturbation line:
`softmaxCoord z i * (basis k i - softmaxCoord z k)`. `CAP2Definition.lean`
freezes the CAP2-v0 row-level formula, and
`cap2AdjustedLogit_coordLine_self` proves a first fixed-load adjusted-logit
coordinate perturbation theorem. A packaged full softmax Jacobian theorem and
full CAP2 calculus remain deferred.

This is a stronger formal standing than a boundary scaffold alone. It still
does not prove hard Top2 differentiability, a packaged full softmax Jacobian,
full CAP2 calculus, Triton/CUDA memory behavior, or FP16 numerical equivalence.

Evidence: EV-FORMAL-001 through EV-FORMAL-010. Guards: NC-006 through NC-011.

## Math Appendix

`MATH-APPENDIX.md` gives the reader-facing derivation bridge for the routing
backward contract. It defines `Z = X W^T`, `P = sigma(Z)`, the fixed or relaxed
routing weights, and the upstream logit gradient `dZ`. It also connects the
Lean-backed identities `dWReal_adjoint` and `dXRouterReal_adjoint` to the
standard contractions `dW = dZ^T X` and `dX_router = dZ W`.

The appendix is explanatory evidence for the paper's claim boundary. It does
not add a new claim that hard Top2 is differentiable or that Lean proves the
Triton implementation.

Evidence: EV-PAPER-001, EV-FORMAL-002. Guards: NC-001, NC-006.

## Triton Implementation

The implementation evidence is split between reference code, Triton code, test
surfaces, and benchmark scripts. The fixed-mask path includes Triton reductions
for `dW`, `dX_router`, and `dH`. The CAP2 fixed-load path includes row-local
Triton computation for `dZ` and `dH`, plus the shared reduction kernels for
`dX_router` and `dW`.

The implementation is validated empirically against PyTorch/manual references
on local and RunPod CUDA surfaces. No formal proof of Triton kernel memory
behavior is claimed.

The allocation and FP16 evidence is intentionally narrower than the original
challenge wording. Fixed-mask FP16 checks are empirical tolerance checks, not a
formal rounding-error theorem. Fixed-mask allocation evidence is stronger than
the current CAP2 allocation evidence; CAP2 fixed-load parity and benchmark
receipts should not be read as a closed full-CAP2 zero-allocation proof.

Evidence: EV-CODE-001 through EV-CODE-005, EV-RUN-001 through EV-RUN-004.

## Validation and Benchmark Results

The validation receipts report:

| Receipt | Result |
| --- | --- |
| RUN-W6A | Local reference VJP suite: 54 passed, 11 skipped. |
| RUN-W6B | RunPod focused Triton suite: 14 passed; full suite: 67 passed. |
| RUN-W6C | RunPod focused Triton suite: 15 passed; full suite: 68 passed. |
| RUN-W7 | Benchmark artifacts produced from the RunPod GPU run. |

The benchmark environment was an NVIDIA RTX PRO 4000 Blackwell with CUDA 12.8
and PyTorch 2.8.0+cu128. Median timings from EV-DATA-001 were:

| Size | Path | Median ms |
| --- | --- | ---: |
| small | fixed_mask | 0.134976 |
| small | cap2_fixed_load | 0.173936 |
| medium | fixed_mask | 0.137840 |
| medium | cap2_fixed_load | 0.167280 |

These values are smoke benchmark data. They support "the tested paths run in
sub-millisecond median time on this recorded environment"; they do not support
a production performance claim.

Evidence: EV-TRITON-004, EV-DATA-001, EV-DATA-002. Guard: NC-005.

## Limitations and Non-Claims

This paper package does not claim:

- differentiability of hard Top2 selection;
- novelty of CAP2-v0;
- exact 2-sparsity for CAP2-v0;
- gradients through dynamic load-balancing decisions;
- production-optimized performance;
- Lean proof of Triton/CUDA implementation correctness;
- formal FP16 numerical equivalence;
- full CAP2 zero-allocation acceptance beyond the recorded validation boundary.

These are not cosmetic caveats. They are the boundary that makes the remaining
claims defensible.

Evidence: CLAIM-GUARDS.md.

## Conclusion

The case study shows a disciplined route from a difficult routing challenge to
a bounded implementation result. The key move is not pretending that hard Top2
became differentiable. The key move is selecting a valid backward contract:
fixed-mask exact backward for fixed discrete choices, and exact backward for a
smooth fixed-load relaxation when continuous routing is desired.

The next strongest steps are a fuller formal treatment of the relaxation
calculus following the softmax and CAP2 feasibility reports, a broader
benchmark suite, prior-art hardening for any novelty argument, and a more
explicit FP16 numerical error story.

## Reproducibility Appendix

Primary sources are listed in `EVIDENCE-MANIFEST.md` and `REFERENCE-LEDGER.md`.
The raw benchmark table is in `DATA-APPENDIX.md`. The math bridge from routing
notation to the current Lean-backed router-adjoint identities is in
`MATH-APPENDIX.md`.

The reproducibility surface has four layers: CPU/reference tests, CUDA/Triton
runner tests, benchmark artifact checks, and Lean formal validation. The command
table below names what each layer supports and what it does not support.

| Layer | Environment | Command | Interpretation |
| --- | --- | --- | --- |
| CPU reference tests | Local Python environment with project test dependencies | `cd <repo>/research/triton-top2-backward-kernel && .venv/bin/python -m pytest tests/test_router_reference.py tests/test_router_torch.py -q` | Supports reference/autograd behavior, not Triton parity. |
| Full local test suite | Local Python environment; CUDA tests may skip without GPU | `cd <repo>/research/triton-top2-backward-kernel && .venv/bin/python -m pytest tests -q` | Local CPU success does not prove GPU behavior. |
| RunPod CUDA iteration | NVIDIA CUDA/Triton runner with SSH access | `cd <repo>/research/triton-top2-backward-kernel && <cuda-runner-iteration-command>` | Supports CUDA/Triton parity on the recorded runner. |
| Focused Triton tests | Inside CUDA runner after upload/bootstrap | `/usr/local/bin/python -m pytest tests/test_router_triton.py -q` | Supports Triton parity for implemented kernels. |
| Benchmark generation | Inside CUDA runner | `/usr/local/bin/python scripts/benchmark_triton_paths.py --json-out development/task-sessions/<run>/artifacts/benchmark.json --markdown-out development/task-sessions/<run>/artifacts/BENCHMARK.md` | Supports smoke timing only unless the benchmark sweep is expanded. |
| Benchmark JSON syntax | Local or CUDA runner | `cd <repo> && jq empty research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/benchmark.json` | Checks data file parseability, not benchmark correctness. |
| Formal build | Lean/Lake environment | `cd <repo>/research/projects/mars/papers/triton-top2-backward-kernel/formal && lake build` | Supports theorem-specific real-valued formal claims only. |

Minimal formal validation:

```bash
cd <repo>/research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Benchmark JSON validation:

```bash
cd <repo>
jq empty research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/benchmark.json
```
