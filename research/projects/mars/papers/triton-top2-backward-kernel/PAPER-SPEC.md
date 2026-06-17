# Paper Spec - Triton Top2 Backward Kernel

Status: `complete`

## Paper Contract

The paper presents a traceable case study: starting from a non-differentiable
Top2 routing challenge, it narrows the claim to exact backward computation for
fixed masks and a smooth fixed-load CAP2 relaxation, then reports reference,
Triton, benchmark, and formal-boundary evidence.

## Section Registry

| Section | Purpose | Required Inputs | Claim Guard |
| --- | --- | --- | --- |
| Abstract | Summarize challenge, approach, and bounded result. | CL-001, CL-002, CL-004 | No novelty/performance overclaim. |
| Problem and Non-Differentiability Background | Explain why hard routing is not differentiable. | REF-002, REF-004 | NC-001. |
| Research Method and MARS Evidence Harness | Explain how evidence is governed. | EV-MARS-001..005 | No internal/private leakage beyond paths. |
| Baselines and Prior Art Positioning | Position fixed-mask and relaxation routes. | EV-TRITON-002, REF-010 | NC-002. |
| CAP2-v0 Relaxation and Exact Fixed-Load Backward | State selected relaxation contract. | EV-TRITON-003, REF-006, REF-007 | NC-001, NC-003, NC-004. |
| Formal Boundary Validation | Report Lean and Mathlib scope. | EV-FORMAL-001, EV-FORMAL-002 | NC-006. |
| Triton Implementation | Describe implementation surfaces. | EV-CODE-001..005 | Empirical correctness only. |
| Validation and Benchmark Results | Present validation receipts and timing table. | EV-RUN-001..005, EV-DATA-001 | NC-005. |
| Limitations and Non-Claims | Make boundaries explicit. | CLAIM-GUARDS.md | Must include all non-claims. |
| Conclusion | State what was learned and what remains. | Manifest and review. | Candidate-only. |
| Reproducibility Appendix | List commands, source paths, and data. | REFERENCE-LEDGER.md, DATA-APPENDIX.md | Do not imply universal reproducibility without GPU/runtime. |

## Acceptance

- Each section has a source path or claim ID.
- Each risky sentence has a non-claim guard.
- Any future public derivative must run a private/public boundary review before distribution.
