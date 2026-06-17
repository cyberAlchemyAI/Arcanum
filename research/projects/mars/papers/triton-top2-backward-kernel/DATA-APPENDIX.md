# Data Appendix

Status: `complete`

## Scope Box

This appendix proves or supports:

- the recorded benchmark environment and raw smoke timing table;
- the validation receipt summaries used by the paper;
- the interpretation boundary for FP16 and allocation evidence.

This appendix does not prove:

- production-optimized performance;
- universal hardware scaling;
- formal FP16 numerical equivalence;
- Lean-level correctness of Triton/CUDA memory behavior;
- full CAP2 zero-allocation acceptance beyond the recorded validation boundary.

## Benchmark Environment

Source: EV-DATA-001 and EV-TRITON-004.

| Field | Value |
| --- | --- |
| Timestamp UTC | 2026-06-14T07:44:35Z |
| Device | NVIDIA RTX PRO 4000 Blackwell |
| CUDA | 12.8 |
| PyTorch | 2.8.0+cu128 |
| Warmup / iterations | 10 / 50 |

## Raw Timing Table

| Size | Path | Tokens | Experts | Dim | Min ms | Median ms | Mean ms | Max ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| small | fixed_mask | 128 | 8 | 64 | 0.130624 | 0.134976 | 0.139435 | 0.268800 |
| small | cap2_fixed_load | 128 | 8 | 64 | 0.165632 | 0.173936 | 0.180474 | 0.299008 |
| medium | fixed_mask | 512 | 16 | 128 | 0.130912 | 0.137840 | 0.141242 | 0.172384 |
| medium | cap2_fixed_load | 512 | 16 | 128 | 0.164608 | 0.167280 | 0.170669 | 0.211008 |

## Validation Receipts

| Receipt | Summary |
| --- | --- |
| RUN-W6A | Local reference VJP suite: 54 passed, 11 skipped. |
| RUN-W6B | RunPod focused Triton suite: 14 passed; full suite: 67 passed. |
| RUN-W6C | RunPod focused Triton suite: 15 passed; full suite: 68 passed. |
| RUN-W7 | Benchmark task produced EV-DATA-001 and EV-DATA-002. |

## Interpretation Guard

These timings are useful for a case-study smoke comparison. They are not an
exhaustive scaling study, not a production tuning result, and not a universal
hardware claim.

## FP16 And Allocation Boundary

The current evidence should be read as empirical validation, not formal numeric
analysis. Fixed-mask FP16 behavior is covered by tolerance-based tests in the
implemented validation surface, but the package does not contain a formal FP16
rounding-error theorem and does not use fixed-mask FP16 checks as proof of CAP2
FP16 equivalence.

The zero-allocation claim is also boundary-sensitive. The fixed-mask path has
the strongest allocation evidence in the current package. CAP2 fixed-load has
recorded Triton parity and smoke benchmark evidence, but a full CAP2
zero-allocation acceptance claim remains reserved for the systems-hardening
work-pack. Until that work closes, the safe paper wording is that the tested
CAP2 fixed-load path runs on the recorded CUDA runner and benchmark surface, not
that every CAP2 path satisfies the original zero-allocation challenge.
