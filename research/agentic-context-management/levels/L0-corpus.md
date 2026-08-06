# L0 — Bounded Corpus

## Inclusion Rule

Include a source only when it supports the primary taxonomy, tests a proof
boundary, or closes a named residue. Unbounded market comparison is excluded.

| ID | Source | Source kind | Included for | Excluded use |
| --- | --- | --- | --- | --- |
| S0 | [ACM paper v1](https://arxiv.org/html/2607.21503v1) | `primary-source` | Taxonomy, equations, architecture description, reported evaluation, limitations | Independent product verification |
| S1 | [ACM PDF v1](https://arxiv.org/pdf/2607.21503v1) | `primary-source` | Stable source identity and hash | Local redistribution |
| S2 | [Maximem evaluation harness](https://github.com/maximem-ai/memory_and_context_eval_harness) | `primary-source` companion artifact | Public evaluation mechanics and current documentation state | Proof that reported runs are reproducible as published |
| S3 | [Maximem results repository](https://github.com/maximem-ai/eval_benchmark_runs_output) | `primary-source` companion artifact | Reported counts, scope, and configuration summary | Controlled competitor comparison |
| R1 | [MemGPT v2](https://arxiv.org/abs/2310.08560v2) | `related-source` | Prior virtual-context framing | Full five-primitive equivalence |
| R2 | [ACE v3](https://arxiv.org/abs/2510.04618v3) | `related-source` | Context collapse and incremental evolution | Evidence for loss-validated compaction |
| R3 | [LongMemEval v2](https://arxiv.org/abs/2410.10813v2) | `related-source` | Benchmark task scope | Production latency, cost, privacy, or isolation evidence |
| R4 | [LoCoMo v1](https://arxiv.org/abs/2402.17753v1) | `related-source` | Long-form conversational-memory scope | Organization-scale context evidence |

## Corpus Cutoff

Checked through 2026-07-31. Later paper revisions, repository commits, requested
per-run artifacts, and forthcoming production-context benchmarks are outside
this tower's evidence window.
