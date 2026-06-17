# Evidence Manifest - Triton Top2 Backward Kernel Paper Package

Status: `complete`
Package: `research/triton-top2-backward-kernel/paper/`

## Evidence Classes

| ID | Class | Source | Role | Support Level |
| --- | --- | --- | --- | --- |
| EV-PAPER-001 | Paper appendix | `research/triton-top2-backward-kernel/paper/MATH-APPENDIX.md` | Reader-facing derivation bridge from routing notation to the Lean-backed router-adjoint identities. | explanatory paper evidence |
| EV-PAPER-002 | Paper manifest | `research/triton-top2-backward-kernel/paper/EVIDENCE-MANIFEST.md` | Triton-local evidence IDs, claim support rules, and public traceability boundary. | package governance evidence |
| EV-PAPER-003 | Reference ledger | `research/triton-top2-backward-kernel/paper/REFERENCE-LEDGER.md` | Source-use boundaries for paper prose, prior art, implementation, benchmark, and formal material. | package governance evidence |
| EV-TRITON-001 | Triton tower | `research/triton-top2-backward-kernel/WORK-PACK.md` | Case-study work breakdown and completion context. | source evidence |
| EV-TRITON-002 | Prior-art boundary | `research/triton-top2-backward-kernel/FINAL-PRIOR-ART-NOVELTY-REPORT.md` | Novelty/non-novelty boundary. | source evidence |
| EV-TRITON-003 | Parity report | `research/triton-top2-backward-kernel/CAP2-W6-PARITY-REPORT.md` | CAP2 fixed-load backward validation summary. | validated claim evidence |
| EV-TRITON-004 | Benchmark report | `research/triton-top2-backward-kernel/TRITON-BENCHMARK-REPORT.md` | Smoke benchmark summary and limitations. | validated claim evidence |
| EV-TRITON-005 | Formal math | `research/triton-top2-backward-kernel/FORMAL-MATH-SPEC.md` | Problem notation and proof obligations. | specification evidence |
| EV-TRITON-006 | Formal stubs | `research/triton-top2-backward-kernel/FORMAL-MATH-STUBS.md` | Open formal proof boundary. | specification evidence |
| EV-CODE-001 | Implementation | `research/triton-top2-backward-kernel/reference/router_torch.py` | PyTorch reference and validation oracle. | executable evidence |
| EV-CODE-002 | Implementation | `research/triton-top2-backward-kernel/reference/router_triton.py` | Triton implementation surface. | executable evidence |
| EV-CODE-003 | Tests | `research/triton-top2-backward-kernel/tests/test_router_torch.py` | PyTorch reference tests. | executable evidence |
| EV-CODE-004 | Tests | `research/triton-top2-backward-kernel/tests/test_router_triton.py` | Triton parity tests. | executable evidence |
| EV-CODE-005 | Benchmark script | `research/triton-top2-backward-kernel/scripts/benchmark_triton_paths.py` | Benchmark driver. | executable evidence |
| EV-RUN-001 | Run receipt | `research/triton-top2-backward-kernel/development/task-sessions/20260614T073520Z-w6-001a-cap2-reference-vjp/RESULT.md` | Reference VJP validation. | validation receipt |
| EV-RUN-002 | Run receipt | `research/triton-top2-backward-kernel/development/task-sessions/20260614T073920Z-w6-001b-cap2-row-backward/RESULT.md` | Triton row backward validation. | validation receipt |
| EV-RUN-003 | Run receipt | `research/triton-top2-backward-kernel/development/task-sessions/20260614T074112Z-w6-001c-cap2-dw-reduction/RESULT.md` | Triton CAP2 dW validation. | validation receipt |
| EV-RUN-004 | Run receipt | `research/triton-top2-backward-kernel/development/task-sessions/20260614T074226Z-w6-001d-contract-closure/RESULT.md` | Contract closure. | validation receipt |
| EV-RUN-005 | Run receipt | `research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/RESULT.md` | Benchmark task result. | validation receipt |
| EV-DATA-001 | Raw data | `research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/benchmark.json` | Raw benchmark measurements. | raw data |
| EV-DATA-002 | Data report | `research/triton-top2-backward-kernel/development/task-sessions/20260614T074500Z-w7-003-benchmark/artifacts/BENCHMARK.md` | Benchmark artifact summary. | raw data summary |
| EV-FORMAL-001 | Formal package | `research/triton-top2-backward-kernel/paper/formal/` | Repo-local Lean boundary slice. | mechanized boundary evidence |
| EV-FORMAL-002 | Mathlib hardening | `research/triton-top2-backward-kernel/paper/formal/TritonTop2/RealBackwardIdentities.lean` | Real-valued finite-sum adjoint identities for router logits. | mechanized theorem evidence |
| EV-FORMAL-003 | Fixed-mask proof | `research/triton-top2-backward-kernel/paper/formal/TritonTop2/FixedMaskBackward.lean` | Fixed-mask dW and dX-router adjoint identities over the existing real-valued router model. | mechanized theorem evidence |
| EV-FORMAL-004 | Softmax feasibility | `research/triton-top2-backward-kernel/paper/formal/SOFTMAX-PROOF-FEASIBILITY.md` | Scoped blocker and next theorem shape for finite softmax derivative formalization. | feasibility evidence |
| EV-FORMAL-005 | CAP2 feasibility | `research/triton-top2-backward-kernel/paper/formal/CAP2-PROOF-FEASIBILITY.md` | Scoped blocker and next theorem shape for CAP2 fixed-load derivative formalization. | feasibility evidence |
| EV-FORMAL-006 | Softmax foundation proof | `research/triton-top2-backward-kernel/paper/formal/TritonTop2/SoftmaxCoordinate.lean` | Finite softmax definitions, coordinate-line support lemmas, and denominator positivity. | mechanized theorem evidence |
| EV-FORMAL-007 | Softmax coordinate blocker | `research/triton-top2-backward-kernel/paper/formal/SOFTMAX-COORDINATE-BLOCKER.md` | Exact remaining Mathlib calculus chain for the coordinate derivative theorem. | blocker evidence |
| EV-FORMAL-008 | CAP2 definition proof | `research/triton-top2-backward-kernel/paper/formal/TritonTop2/CAP2Definition.lean` | Canonical CAP2-v0 row-level definitions and fixed-load boundary lemmas. | mechanized definition evidence |
| EV-FORMAL-009 | CAP2 fixed-load scalar proof | `research/triton-top2-backward-kernel/paper/formal/TritonTop2/CAP2FixedLoadScalar.lean` | First fixed-load adjusted-logit coordinate perturbation theorem slice. | mechanized theorem evidence |
| EV-FORMAL-010 | Softmax coordinate derivative proof | `research/triton-top2-backward-kernel/paper/formal/TritonTop2/SoftmaxCoordinate.lean` | Full finite softmax coordinate derivative along a coordinate perturbation line. | mechanized theorem evidence |

## Claim Support Rules

| Rule | Requirement |
| --- | --- |
| C1 | Every paper claim must reference at least one manifest ID. |
| C2 | Novelty language must reference EV-TRITON-002 and remain candidate-only unless the source explicitly supports a stronger claim. |
| C3 | Any statement about exact backward must specify the smooth fixed-load CAP2 relaxation or fixed-mask path, not hard Top2 selection. |
| C4 | Any performance statement must identify the recorded RunPod environment and smoke benchmark scope. |
| C5 | Lean validation may be cited for formal boundary/algebra checks and Mathlib-backed real-valued router adjoint identities only, not Triton implementation correctness. |
| C6 | EV-PAPER-001 through EV-PAPER-003 may explain notation, source use, and proof boundaries, but they are not independent proof of a new mathematical or implementation claim. |
| C7 | EV-FORMAL-004 and EV-FORMAL-005 may be cited as scoped feasibility/deferred-proof evidence only, not as completed calculus proofs. |
| C8 | EV-FORMAL-006 and EV-FORMAL-010 may be cited for finite softmax foundation and coordinate derivative evidence; they do not prove hard Top2 differentiability or a packaged full softmax Jacobian theorem. |
| C9 | EV-FORMAL-008 and EV-FORMAL-009 may be cited for CAP2 definition and first CAP2 fixed-load scalar theorem only; they do not prove full CAP2 calculus. |
