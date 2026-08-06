# Source Record

## Primary Source

| Field | Value |
| --- | --- |
| Title | *Agentic Context Management: Solving Agent Memory and Cost by Treating Them as Lifecycle and Architecture Problems* |
| Author | Gaurav Dadhich |
| Identifier | `arXiv:2607.21503v1` |
| Submitted | 2026-07-23 |
| Checked | 2026-07-31 |
| Abstract | https://arxiv.org/abs/2607.21503v1 |
| HTML | https://arxiv.org/html/2607.21503v1 |
| PDF | https://arxiv.org/pdf/2607.21503v1 |
| PDF SHA-256 | `107f18872b8f58c6992c3ff8ac1beb0b08131bcdb4622cc2fdcd4701f40f77e0` |
| Declared extent | 23 pages, 6 figures, 4 tables |
| License | CC BY 4.0, as linked by arXiv |

The PDF hash was computed from a fresh download on the checked date. The PDF is
not copied into this repository; the versioned URL and hash form the source
identity receipt.

## Companion Evidence Checked

| Artifact | Observed revision | Source kind | What it can support |
| --- | --- | --- | --- |
| https://github.com/maximem-ai/memory_and_context_eval_harness | `1dbbcfe025d64c84146ff4c316ed492c5fb760de` (`HEAD`, checked 2026-07-31) | `primary-source` companion artifact | Public harness shape and current README claims |
| https://github.com/maximem-ai/eval_benchmark_runs_output | `6d9754245eec3e8c29e053cb15d04ea57fd41ef5` (`HEAD`, checked 2026-07-31) | `primary-source` companion artifact | Reported category counts and methodology summary |

## Related Primary Sources

| Source | Version checked | Why included |
| --- | --- | --- |
| [MemGPT](https://arxiv.org/abs/2310.08560v2) | v2 | Distinguishes virtual context/memory tiers from the paper's broader lifecycle taxonomy |
| [Agentic Context Engineering](https://arxiv.org/abs/2510.04618v3) | v3 | Grounds context-collapse and incremental-update alternatives to summarization |
| [LongMemEval](https://arxiv.org/abs/2410.10813v2) | v2 | Defines the 500-question conversational-memory benchmark and its ability categories |
| [LoCoMo](https://arxiv.org/abs/2402.17753v1) | v1 | Defines the long-form conversational-memory dataset and evaluation scope |

## Source Boundary

- Product internals described as proprietary are accepted only as author claims.
- Reported scores are not independent replications.
- Vendor-to-vendor rows are not controlled comparisons.
- Current companion artifacts contain a material mismatch: the results repository
  says LongMemEval used all 500 questions, while the harness README labels its
  headline result `LongMemEval (50q)` and marks methodology documentation `TBD`.
- Per-run answers, retrieved contexts, and judge verdicts are not public in the
  checked companion repositories; the paper says they are available on request.
- No claim in this tower crosses into canonical Arcanum definitions or behavior.
