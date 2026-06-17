# Implementation Layering - W6 CAP2 Exact Backward

## L0 - Math/Reference Validity

Question: is the CAP2 backward formula correct for fixed load?

Evidence:

- manual VJP matches PyTorch autograd for `W` and `H`;
- finite differences match `dW`;
- intermediate `dZ` is exposed for Triton parity.

Promotion gate:

- all reference parity tests pass locally.

## L1 - Triton Numerical Parity

Question: can Triton reproduce the validated CAP2 backward outputs?

Evidence:

- `dZ`, `dW`, `dX_router`, and `dH` match reference on RunPod;
- small-shape and fixture tests pass.

Promotion gate:

- focused Triton tests and full suite pass on RunPod.

## L2 - Systems Contract

Question: does the CAP2 kernel have an honest memory and dtype contract?

Evidence:

- explicit output buffers;
- explicit scratch policy;
- FP16 tolerance checks;
- no hidden claim of full zero-allocation unless measured.

Promotion gate:

- allocation/FP16 tests pass or blocker is recorded.

## L3 - Benchmark and Report

Question: what can be claimed in the final challenge report?

Evidence:

- benchmark report includes fixed-mask and CAP2-v0 if W6 passes;
- final report separates correctness, allocation, FP16, performance, and novelty.

Promotion gate:

- W7-003 and W8 reports written with non-claims intact.
