# Claim Guards

Status: `complete`

## Supported Claims

| Claim ID | Paper Claim | Evidence |
| --- | --- | --- |
| CL-001 | The case study implements backward kernels for fixed-mask Top2-style routing and CAP2 fixed-load relaxation paths. | EV-CODE-001, EV-CODE-002, EV-RUN-001, EV-RUN-002, EV-RUN-003 |
| CL-002 | The exact-backward claim applies to the selected smooth/fixed-load relaxation boundary, not the non-differentiable hard Top2 selection. | EV-TRITON-003, EV-TRITON-005, EV-TRITON-006, EV-FORMAL-001 |
| CL-003 | CAP2 fixed-load Triton backward matched the manual/reference contract on the recorded RunPod validation tasks. | EV-TRITON-003, EV-RUN-001, EV-RUN-002, EV-RUN-003 |
| CL-004 | The measured smoke benchmark medians were sub-millisecond on the recorded RTX PRO 4000 Blackwell environment. | EV-TRITON-004, EV-DATA-001, EV-DATA-002 |
| CL-005 | Lean is used here to validate a narrow algebra and boundary slice, plus Mathlib-backed real-valued adjoint identities for the router linear map, not to prove CUDA/Triton memory behavior. | EV-FORMAL-001, EV-FORMAL-002, EV-TRITON-006 |
| CL-006 | The Triton paper package records a local manifest and reference ledger for public traceability. | EV-PAPER-002, EV-PAPER-003 |
| CL-007 | The fixed-mask Lean theorem slice proves fixed-mask dW and dX-router adjoint identities only after mask/upstream routing weights are treated as fixed data. | EV-FORMAL-003, EV-FORMAL-001 |
| CL-008 | Lean now proves finite softmax definitions, coordinate-line support lemmas, denominator positivity, and the finite softmax coordinate derivative along a coordinate perturbation line. | EV-FORMAL-006, EV-FORMAL-010 |
| CL-009 | Lean now encodes CAP2-v0 row-level definitions and proves a first fixed-load adjusted-logit coordinate perturbation slice. | EV-FORMAL-008, EV-FORMAL-009 |

## Non-Claims

| Guard ID | Non-Claim | Reason |
| --- | --- | --- |
| NC-001 | This package does not claim differentiability of hard Top2 selection. | Hard selection changes discretely; the backward contract bypasses it through fixed masks or continuous relaxation. |
| NC-002 | This package does not claim CAP2 is novel. | Prior-art report supports candidate positioning only. |
| NC-003 | This package does not claim exact 2-sparsity for CAP2. | CAP2 is a smooth relaxation, not hard Top2. |
| NC-004 | This package does not claim gradients through dynamic load-balancing decisions. | W6 scope is fixed-load. |
| NC-005 | This package does not claim production-optimized performance. | W7 benchmark is a smoke benchmark over two sizes. |
| NC-006 | This package does not claim Lean proves the Triton implementation. | Lean slice covers boundary/algebra and router adjoint identities only. |
| NC-007 | The fixed-mask Lean slice does not prove gradients through mask selection. | The mask/upstream routing weights are explicit data in the theorem statement. |
| NC-008 | This package does not claim a packaged full softmax Jacobian or full softmax VJP theorem. | Lean proves the finite softmax coordinate derivative along a coordinate perturbation line, but the packaged full Jacobian/VJP theorem remains deferred. |
| NC-009 | This package does not claim a completed full CAP2 derivative proof. | Lean now encodes CAP2-v0 definitions and a first fixed-load adjusted-logit coordinate perturbation slice, but normalized gate, soft-rank, and full CAP2 calculus remain deferred. |
| NC-010 | The completed finite softmax coordinate derivative theorem does not prove hard Top2 differentiability or a packaged full softmax Jacobian theorem. | The theorem is a smooth finite-softmax coordinate-line result, not a hard-selection theorem. |
| NC-011 | The CAP2 definition and adjusted-logit slice do not prove normalized gate, soft-rank, or full CAP2 derivatives. | The theorem slice is limited to fixed-load adjusted logits under coordinate perturbation. |
| NC-012 | Fixed-mask FP16 tolerance checks do not establish a formal FP16 error bound or CAP2 FP16 numerical equivalence. | FP16 behavior is validated empirically inside selected tests; Lean explicitly defers FP16 numeric analysis. |
| NC-013 | CAP2 benchmark and wrapper evidence does not by itself close a full CAP2 zero-allocation claim. | The package records tested CAP2 fixed-load behavior, but CAP2 zero-allocation hardening remains a separate systems obligation. |
