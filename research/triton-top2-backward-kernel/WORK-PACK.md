# Work Pack - Top2 Triton Challenge To Completion

Status: `complete-ready-for-review`

Owner: `research/triton-top2-backward-kernel`

## Objective

Carry the challenge from research/reference scaffold to final validated outcome:

```text
reference baselines -> math validation -> CAP2 decision -> Triton parity ->
zero-allocation/FP16 validation -> final prior-art/novelty report
```

## Current Baseline

Complete:

- V0 standard-library reference harness;
- PyTorch V0 fixed-mask reference with autograd parity against the standard-library oracle;
- PyTorch gradcheck and finite-difference parity for the fixed-mask graph;
- normalized selected-pair comparison variant for `M * P` versus renormalized weights;
- sparsemax routing baseline on the shared fixture;
- normalized ReLU routing baseline on the shared fixture;
- convex sparse top-k relaxed mask extraction for `k=2`;
- convex sparse top-k direct-mask and normalized masked-softmax router compositions;
- convex sparse top-k differentiable/JVP parity blocked report;
- convex sparse top-k PAV JVP/backward feasibility pass for a narrow PyTorch oracle;
- convex sparse top-k PAV mask-level PyTorch custom-autograd parity oracle;
- finite-difference validation for manual `dW`;
- soft-routing baseline in standard library;
- CAP2-v0 standard-library and PyTorch reference with fixed-load gradcheck;
- CAP2-v0 exact backward reference VJP and Triton parity for `dZ`,
    `dX_router`, `dH`, and `dW` under fixed load;
- final prior-art and novelty report with explicit non-claims.

## Wave Summary

| Wave | Goal | Status |
| --- | --- | --- |
| W0 | Environment/dependency gate | cuda-triton-runner-pass |
| W1 | PyTorch V0 parity and gradcheck | pass |
| W2 | Prior-art baselines | convex-router-jvp-parity-pass |
| W3 | CAP2-v0 design-or-kill | cap2-promoted-candidate |
| W4 | Formal math validation | po004-po005-pass |
| W5 | Triton fixed-mask baseline | pass-runpod |
| W6 | Triton selected relaxation | pass-runpod |
| W7 | Zero-allocation, FP16, performance | pass-runpod |
| W8 | Final comparison and novelty report | pass |

## Task Matrix

| Task ID | Wave | Objective | Dependencies | Status | Validation |
| --- | --- | --- | --- | --- | --- |
| TASK-W0-001 | W0 | Establish PyTorch-capable environment or record exact blocker. | none | pass-via-W0-005 | Tower-local `.venv` has PyTorch CPU 2.12.0+cpu. |
| TASK-W0-002 | W0 | Establish pytest or keep unittest adapter. | none | pass-via-W0-005 | Tower-local `.venv` has pytest 8.4.2; stdlib unittest still works. |
| TASK-W0-003 | W0 | Detect Triton/GPU availability for later waves. | none | blocked | Blocker recorded: Triton is not installed and `nvidia-smi` is unavailable. |
| TASK-W0-004 | W0 | Add isolated dependency manifests and environment check tests. | none | pass | requirement files and environment test exist; 12 stdlib tests pass with 1 expected GPU skip. |
| TASK-W0-005 | W0 | Provision CPU reference environment. | TASK-W0-004 | pass | PyTorch CPU 2.12.0+cpu imports; pytest suite passes with expected GPU skip. |
| TASK-W0-006 | W0 | Provision GPU/Triton runner. | TASK-W0-004 | blocked | Blocker recorded: CPU-only PyTorch, no Triton, no `nvidia-smi`, no `nvcc`. |
| TASK-W0-007 | W0 | Select and prepare a CUDA runner path. | TASK-W0-006 | pass-free-runner-kit | Local GPU is AMD/WSL2, not CUDA; selected free hosted notebook path and added validation kit. |
| TASK-W0-008 | W0 | Validate CUDA/Triton runner readiness. | TASK-W0-007 | pass-runpod | RunPod external probe passed: `49 passed in 3.47s` and `PASS: CUDA/Triton runner is ready`; evidence in `development/task-sessions/20260614T063208Z-runpod-cuda-probe/RUNPOD-CUDA-PROBE-PASS.md`. |
| TASK-W0-009 | W0 | Provision paid on-demand CUDA runner if free runners fail twice. | TASK-W0-008 | fallback-ready | Use `PAID-CUDA-RUNNER-FALLBACK.md`; record provider, GPU, spending cap, validation, and teardown. |
| TASK-W1-001 | W1 | Port V0 reference to PyTorch tensors and autograd. | TASK-W0-005 | pass | PyTorch forward, `dW`, and `dH` match standard-library oracle; mask remains fixed data. |
| TASK-W1-002 | W1 | Add gradcheck/finite-difference parity for V0. | TASK-W1-001 | pass | PyTorch gradcheck passes for fixed-mask `W` and `H`; autograd `dW` matches finite-difference oracle. |
| TASK-W1-003 | W1 | Add normalized pair-weight comparison variant. | TASK-W1-001 | pass | Tests compare raw `M*P` against selected-pair renormalized weights in stdlib and PyTorch. |
| TASK-W2-001 | W2 | Add sparsemax/entmax baseline. | TASK-W0-005 | pass-sparsemax | Sparsemax baseline runs on shared fixtures; entmax remains a named family gap until exact formula/source is pinned for implementation. |
| TASK-W2-002 | W2 | Add ReLU routing baseline. | TASK-W0-005 | pass | Normalized ReLU routing baseline runs on shared fixtures in stdlib and PyTorch. |
| TASK-W2-003 | W2 | Add convex sparse top-k baseline or explicit blocked report. | TASK-W0-005 | blocked-report | `CONVEX-SPARSE-TOPK-BLOCKED.md` records missing operator/backward details. |
| TASK-W2-003A | W2 | Extract implementation-ready convex sparse top-k operator. | TASK-W2-003 | pass | `convex_sparse_topk_mask_rows` extracts official PAV p=4/3 mask path for `k=2`; tests pin support and official README behavior. |
| TASK-W2-003B | W2 | Decide and implement convex sparse top-k router composition. | TASK-W2-003A | pass | Implemented selected options 1 and 3: direct relaxed mask and normalized relaxed-mask softmax. |
| TASK-W2-003C | W2 | Add differentiable/JVP-backed convex sparse top-k parity or blocked report. | TASK-W2-003B | blocked-report | `CONVEX-SPARSE-TOPK-JVP-BLOCKED.md` records missing source-backed PyTorch/custom-JVP backward parity. |
| TASK-W2-003D-RG | W2 | Run a bounded feasibility research gate for convex sparse top-k PAV JVP/backward extraction. | TASK-W2-003C | pass | `CONVEX-SPARSE-TOPK-JVP-FEASIBILITY.md` records a feasible narrow PyTorch custom-autograd route. |
| TASK-W2-003D-DG | W2 | Decide whether to implement PAV JVP parity now or defer to CAP2-v0. | TASK-W2-003D-RG | pass | User selected option 1: implement narrow PAV JVP parity now. |
| TASK-W2-003D | W2 | Extract source-backed PyTorch/custom-JVP parity for convex sparse top-k PAV. | TASK-W2-003D-DG | pass | Mask-level custom autograd and direct-mask router parity pass against finite differences and standard-library oracle. |
| TASK-W3-001 | W3 | Implement CAP2-v0 reference. | TASK-W1-001 | pass | Standard-library/PyTorch CAP2-v0 forward parity and fixed-load gradcheck pass. |
| TASK-W3-002 | W3 | Compare CAP2-v0 against prior-art baselines. | TASK-W2-001,TASK-W2-002,TASK-W2-003D,TASK-W3-001 | pass | `CAP2-PRIOR-ART-COMPARISON.md` compares fixture behavior, capacity response, support, and backward status. |
| TASK-W3-003 | W3 | Kill/promote/defer CAP2. | TASK-W3-002 | pass-promoted-candidate | User selected option 1: promote CAP2-v0 as candidate only, with no novelty claim. |
| TASK-W4-001 | W4 | Convert proof stubs into Lean theorem stubs or proof notes. | none | pass | `W4-PROOF-NOTES.md` exists and `FORMAL-MATH-STUBS.md` links Lean-shaped stubs/proof notes for PO-001..PO-006. |
| TASK-W4-002 | W4 | Prove or manually validate PO-004/PO-005. | TASK-W4-001 | pass | `W4-PO004-PO005-VALIDATION.md` validates PO-004/PO-005 with proof notes and finite-difference tests; `tests/test_router_reference.py` passes. |
| TASK-W5-001 | W5 | Implement Triton fixed-mask `dW` kernel. | TASK-W1-002,TASK-W0-008 | pass-runpod | Triton `dW` matches reference on RunPod: focused `tests/test_router_triton.py` passed `5 passed in 2.92s`; full suite passed `55 passed in 3.73s`. |
| TASK-W5-002 | W5 | Add Triton `dX_router` and optional `dH`. | TASK-W5-001 | pass-runpod | Triton `dX_router` and `dH` match reference on RunPod: focused `tests/test_router_triton.py` passed `9 passed in 3.05s`; full suite passed `59 passed in 3.74s`. |
| TASK-W6-001 | W6 | Implement selected relaxation kernel if CAP2/promoted relaxation survives. | TASK-W3-003,TASK-W5-001 | pass-runpod | CAP2 fixed-load exact-backward reference and Triton parity pass; see `CAP2-W6-PARITY-REPORT.md`. |
| TASK-W7-001 | W7 | Add zero-allocation checks. | TASK-W5-001 | pass-runpod | Fixed-mask W5 kernels reuse preallocated outputs with no measured CUDA allocation increase after warm-up; focused Triton tests passed `11 passed in 3.05s`; full suite passed `61 passed in 3.96s`. |
| TASK-W7-002 | W7 | Add FP16 tolerance checks. | TASK-W5-001 | pass-runpod | Fixed-mask W5 kernels accept FP16 inputs and emit FP32 outputs within `rtol=2e-3, atol=2e-3`; focused Triton tests passed `12 passed in 3.07s`; full suite passed `62 passed in 3.76s`. |
| TASK-W7-003 | W7 | Benchmark fixed-mask and selected relaxation. | TASK-W7-001,TASK-W7-002,TASK-W6-001 | pass-runpod | `TRITON-BENCHMARK-REPORT.md` records fixed-mask vs CAP2 timing on RunPod. |
| TASK-W8-001 | W8 | Write final prior-art/novelty report. | TASK-W3-003,TASK-W7-003 | pass | `FINAL-PRIOR-ART-NOVELTY-REPORT.md` separates supported claims from non-claims. |

## SWU Manifest

| SWU ID | Task | Smallest Working Unit | Status |
| --- | --- | --- | --- |
| SWU-W0-001 | TASK-W0-001 | PyTorch environment check/setup decision. | pass-via-SWU-W0-005 |
| SWU-W0-004 | TASK-W0-004 | Add dependency manifests and environment tests. | pass |
| SWU-W0-005 | TASK-W0-005 | Attempt CPU PyTorch/pytest environment. | pass |
| SWU-W0-006 | TASK-W0-006 | Attempt GPU/Triton runner validation. | blocked |
| SWU-W0-007 | TASK-W0-007 | Select and prepare CUDA runner path. | pass-free-runner-kit |
| SWU-W0-008 | TASK-W0-008 | Validate selected CUDA/Triton runner. | pass-runpod |
| SWU-W0-009 | TASK-W0-009 | Provision paid fallback CUDA runner. | fallback-ready |
| SWU-W1-001 | TASK-W1-001 | PyTorch V0 reference parity. | pass |
| SWU-W1-002 | TASK-W1-002 | PyTorch gradcheck and finite-difference parity. | pass |
| SWU-W1-003 | TASK-W1-003 | Normalized pair-weight comparison variant. | pass |
| SWU-W2-001 | TASK-W2-001 | Sparsemax/entmax baseline. | pass-sparsemax |
| SWU-W2-002 | TASK-W2-002 | ReLU routing baseline. | pass |
| SWU-W2-003 | TASK-W2-003 | Convex sparse top-k baseline or blocked report. | blocked-report |
| SWU-W2-003A | TASK-W2-003A | Convex sparse top-k formula extraction. | pass |
| SWU-W2-003B | TASK-W2-003B | Convex sparse top-k router composition. | pass |
| SWU-W2-003C | TASK-W2-003C | Convex sparse top-k differentiable parity or blocked report. | blocked-report |
| SWU-W2-003D-RG | TASK-W2-003D-RG | Feasibility research gate for source-backed PAV JVP/backward extraction. | pass |
| SWU-W2-003D-DG | TASK-W2-003D-DG | Decide implement-now versus defer-to-CAP2 for PAV JVP parity. | pass |
| SWU-W2-003D | TASK-W2-003D | Source-backed PyTorch/custom-JVP extraction for PAV top-k. | pass |
| SWU-W3-001 | TASK-W3-001 | CAP2-v0 reference. | pass |
| SWU-W3-002 | TASK-W3-002 | CAP2-v0 prior-art comparison. | pass |
| SWU-W3-003 | TASK-W3-003 | CAP2-v0 kill/promote/defer decision. | pass-promoted-candidate |
| SWU-W4-001 | TASK-W4-001 | Formal theorem stubs/proof notes. | pass |
| SWU-W4-002 | TASK-W4-002 | Validate PO-004/PO-005 proof obligations. | pass |
| SWU-W5-001 | TASK-W5-001 | Triton fixed-mask `dW`. | pass-runpod |
| SWU-W5-002 | TASK-W5-002 | Triton fixed-mask `dX_router` and `dH`. | pass-runpod |
| SWU-W7-001 | TASK-W7-001 | Fixed-mask zero-allocation checks. | pass-runpod |
| SWU-W7-002 | TASK-W7-002 | Fixed-mask FP16 tolerance checks. | pass-runpod |
| SWU-W6-001 | TASK-W6-001 | Selected-relaxation Triton scope decision and implementation. | pass-runpod |
| SWU-W7-003 | TASK-W7-003 | Benchmark fixed-mask and selected relaxation. | pass-runpod |
| SWU-W8-001 | TASK-W8-001 | Final report. | pass |

## Gates

### G0 - Dependency Gate

PyTorch must be available for W1-W3. Triton/GPU must be available for W5-W7.

### G1 - Semantic Gate

No implementation may claim hard Top2 differentiability.

### G2 - Novelty Gate

CAP2 cannot be called novel unless compared against:

- fixed-mask Top2;
- entmax/sparsemax;
- convex sparse top-k;
- ReLU routing/ReMoE.

### G3 - Triton Gate

No Triton implementation before reference parity.

### G4 - Completion Gate

The project is complete only when W8 final report is written.

## Next Ready Task

No ready tasks.

```text
W5 fixed-mask Triton parity is complete on RunPod. W6 CAP2 fixed-load
exact-backward Triton parity is complete on RunPod. W7 fixed-mask
zero-allocation, FP16 checks, and fixed-mask-vs-CAP2 benchmark also pass. The
final prior-art and novelty report is complete. The tower is ready for review.
```

GPU/Triton validation passed externally with `TASK-W0-008` on RunPod. The
recorded evidence is
`development/task-sessions/20260614T063208Z-runpod-cuda-probe/RUNPOD-CUDA-PROBE-PASS.md`.

Local substitute CUDA probing for `TASK-W0-008` is recorded in
`development/task-sessions/20260614T000000Z-w0-008-cuda-runner-readiness/RUNNER-READINESS-BLOCKED.md`.
It still confirms this local machine is not an NVIDIA CUDA/Triton runner, but
the external RunPod runner unblocks Triton implementation work.

CAP2-v0 is promoted as a candidate only. It remains non-novelty-claimed and not
exact 2-sparse. It now has fixed-load exact-backward reference and Triton parity
for `dZ`, `dX_router`, `dH`, and `dW`; performance and zero-allocation behavior
for CAP2 remain limited to the smoke benchmark and preallocated-output wrapper
coverage recorded in W7.

Convex sparse top-k backward parity now has a narrow CPU/PyTorch oracle for
mask-level non-boundary score gradients. It is not a Triton, zero-allocation, or
normalized masked-softmax backward claim.
