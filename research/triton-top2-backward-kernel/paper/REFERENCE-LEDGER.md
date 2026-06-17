# Reference Ledger - Triton Top2 Backward Kernel

Status: `complete`

## Core References

| Ref | Source | Paper Use | Guard |
| --- | --- | --- | --- |
| REF-001 | `research/triton-top2-backward-kernel/README.md` | Case-study orientation. | Do not treat as validation receipt. |
| REF-002 | `research/triton-top2-backward-kernel/glossary.md` | Plain-language terminology. | Recheck technical claims against reports/tests. |
| REF-003 | `research/triton-top2-backward-kernel/derivation.md` | Derivation narrative. | Superseded by formal spec where they differ. |
| REF-004 | `research/triton-top2-backward-kernel/FORMAL-MATH-SPEC.md` | Formal problem and obligation naming. | Not a completed proof artifact. |
| REF-005 | `research/triton-top2-backward-kernel/FORMAL-MATH-STUBS.md` | Proof status and deferred obligations. | Cite as boundary, not as proof completion. |
| REF-006 | `research/triton-top2-backward-kernel/CAP2-CANDIDATE-SPEC.md` | CAP2 relaxation definition. | Candidate-only. |
| REF-007 | `research/triton-top2-backward-kernel/CAP2-REFERENCE.md` | CAP2 implementation reference. | Validate through tests/reports. |
| REF-008 | `research/triton-top2-backward-kernel/CAP2-W6-PARITY-REPORT.md` | CAP2 fixed-load backward parity. | Scope excludes hard Top2 and dynamic load gradients. |
| REF-009 | `research/triton-top2-backward-kernel/TRITON-BENCHMARK-REPORT.md` | Timing table and environment. | Smoke benchmark, not production tuning. |
| REF-010 | `research/triton-top2-backward-kernel/FINAL-PRIOR-ART-NOVELTY-REPORT.md` | Prior-art and novelty posture. | No novelty claim unless explicitly supported. |
| REF-011 | `research/triton-top2-backward-kernel/reference/router_torch.py` | Reference implementation. | Code evidence, not prose authority alone. |
| REF-012 | `research/triton-top2-backward-kernel/reference/router_triton.py` | Triton implementation. | Implementation correctness is validated empirically. |
| REF-013 | `research/triton-top2-backward-kernel/tests/test_router_triton.py` | Triton parity checks. | Coverage is limited to tested shapes/contracts. |
| REF-014 | `research/triton-top2-backward-kernel/scripts/benchmark_triton_paths.py` | Benchmark reproduction path. | Depends on CUDA/Triton runtime. |

## Result Receipts

| Ref | Receipt | Key Fact |
| --- | --- | --- |
| RUN-W6A | `development/task-sessions/20260614T073520Z-w6-001a-cap2-reference-vjp/RESULT.md` | Reference VJP validated against autograd/finite differences. |
| RUN-W6B | `development/task-sessions/20260614T073920Z-w6-001b-cap2-row-backward/RESULT.md` | RunPod Triton row backward suite passed. |
| RUN-W6C | `development/task-sessions/20260614T074112Z-w6-001c-cap2-dw-reduction/RESULT.md` | RunPod Triton CAP2 dW reduction suite passed. |
| RUN-W6D | `development/task-sessions/20260614T074226Z-w6-001d-contract-closure/RESULT.md` | Contract closure recorded. |
| RUN-W7 | `development/task-sessions/20260614T074500Z-w7-003-benchmark/RESULT.md` | Benchmark task completed. |
