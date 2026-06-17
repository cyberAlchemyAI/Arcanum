# Paper Review

Status: `pass-with-boundaries`

## Section Verdicts

| Section | Verdict | Notes |
| --- | --- | --- |
| Abstract | pass | Exact-backward wording is scoped to fixed-mask/relaxed paths. |
| Problem/background | pass | Hard Top2 is described as non-differentiable. |
| Evidence method | pass | Uses manifest and ledger paths. |
| Prior art | pass | Candidate-only posture retained. |
| CAP2 relaxation | pass | Fixed-load assumption is explicit. |
| Formal boundary | pass | Mathlib-backed router adjoint identities, fixed-mask adjoint identities, finite softmax coordinate derivative, CAP2 definitions, and a first CAP2 fixed-load adjusted-logit slice are proved; full Jacobian/CAP2 calculus remains scoped and Lean is not overclaimed as Triton/CAP2 implementation proof. |
| Math appendix | pass | Appendix explains `Z = X W^T`, `P = sigma(Z)`, `dZ`, `dW = dZ^T X`, `dX_router = dZ W`, and the hard-selection boundary. |
| Triton implementation | pass | Implementation claims point to code/tests/reports. |
| Validation/results | pass | Benchmark table matches EV-DATA-001. |
| Limitations | pass | Non-claims are explicit. |
| Conclusion | pass | Future work is framed as future work. |
| Reproducibility appendix | pass | Commands and source paths are present. |

## Test Spec Review

| Test ID | Verdict |
| --- | --- |
| TST-001 | pass |
| TST-002 | pass |
| TST-003 | pass |
| TST-004 | pass after `lake build` validation |
| TST-005 | pass |
| TST-006 | pass |
| TST-007 | pass |
| TST-008 | pass |

## Residual Risks

- Broader prior-art review is still needed before making novelty claims.
- Full formal softmax Jacobian packaging and CAP2 calculus proofs are deferred with scoped evidence.
- GPU implementation correctness remains empirical/test-backed, not formally proved.
- Benchmark coverage is intentionally small.

## Review Pass 2026-06-14

High-severity overclaim check: pass.

Findings:

- No positive hard `Top2` differentiability claim was found.
- Fixed-mask theorem language is scoped to fixed mask/upstream routing weights as data.
- Softmax coordinate derivative is named as a completed finite-softmax theorem.
- CAP2 formal work remains definition/fixed-load-slice evidence, not completed full calculus proof.
- Lean proof claims are separated from Triton/CUDA implementation correctness.
- CAP2 remains candidate/scoped and is not presented as novel.

## Review Pass 2026-06-15

Manifest path check: pass.

Findings:

- Every backtick source path in `EVIDENCE-MANIFEST.md` resolves in the current
  checkout.
- No manifest path mutation was required.
- The 2026-06-15 hardening pass added explicit FP16, CAP2 zero-allocation, and
  appendix scope boundaries; those boundaries do not change the evidence ID
  inventory.
