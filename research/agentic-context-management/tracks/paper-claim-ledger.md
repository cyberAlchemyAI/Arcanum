# Source Claim Ledger

Target: `Agentic Context Management`, arXiv:2607.21503v1

## Direct Paper Claims

| ID | Claim | Source kind | Evidence | Local reading | Status |
| --- | --- | --- | --- | --- | --- |
| C1 | Agentic Context Management decides what an agent holds in context, when, for how long, and at what cost across acquisition through retirement. | `primary-source` | [§2](https://arxiv.org/html/2607.21503v1#S2) | Context is governed across a lifecycle, not just at read/write boundaries. | accepted |
| C2 | The lifecycle is decomposed into architecting, ingesting, scoping, anticipating, and compacting & consolidation. | `primary-source` | [§2](https://arxiv.org/html/2607.21503v1#S2) | A useful completeness checklist, not a proof of exhaustive taxonomy. | accepted |
| C3 | Each primitive operates across a user/customer/client hierarchy under isolation, with a separate global-knowledge layer. | `primary-source` | [§2](https://arxiv.org/html/2607.21503v1#S2) | Treat scope and isolation as first-class policy dimensions. | accepted |
| C4 | Full-append cumulative input tokens grow as `t*n(n+1)/2 = O(n^2)` under constant per-turn growth. | `primary-source` | [§3.1](https://arxiv.org/html/2607.21503v1#S3.SS1), Appendix A | Arithmetic consequence of the stated model, not a universal observed curve. | accepted |
| C5 | Holding context to `W` tokens per turn produces `nW = O(n)` cumulative input tokens. | `primary-source` | [§3.1](https://arxiv.org/html/2607.21503v1#S3.SS1) | Budgeting changes the cost order but says nothing by itself about fidelity. | accepted |
| C6 | Crude summarization can trade linear cost for an accuracy cliff; validated compaction targets linear cost with preserved fidelity. | `primary-source` | [§3.2](https://arxiv.org/html/2607.21503v1#S3.SS2) | Validation must be an explicit contract, but the target is not proof of losslessness. | accepted |
| C7 | Answer quality is capped by extraction, retrieval, and reasoning sufficiency. | `primary-source` | [§3.3](https://arxiv.org/html/2607.21503v1#S3.SS3) | Evaluate the whole evidence chain, not retrieval hits alone. | accepted |
| C8 | The motivating retrieval study reports lexical/vector regime differences and a 60–100x indexing-time asymmetry for its configuration. | `primary-source` | [Appendix B](https://arxiv.org/html/2607.21503v1#A2) | Configuration-specific motivation; no hybrid system was tested. | accepted |
| C9 | Maximem Synap is described as a multi-tenant reference implementation of all five primitives. | `primary-source` | [§4](https://arxiv.org/html/2607.21503v1#S4) | Architecture description, not independent mechanism verification. | accepted |
| C10 | The reference system reports 92.0% (460/500) on LongMemEval and 93.2% on LoCoMo categories 1–4. | `primary-source` | [§6](https://arxiv.org/html/2607.21503v1#S6), [results repo](https://github.com/maximem-ai/eval_benchmark_runs_output) | Preserve as self-reported under the stated configuration. | accepted |
| C11 | Those benchmarks do not measure production latency, token efficiency, or context-rot resistance. | `primary-source` | [§6.3](https://arxiv.org/html/2607.21503v1#S6.SS3) | Benchmark success cannot establish the production category. | accepted |
| C12 | Decision-level and organization-scale context are future directions with unresolved causal, temporal, canonicalization, and security problems. | `primary-source` | [§8](https://arxiv.org/html/2607.21503v1#S8) | Keep decision rationales as future work, not a delivered capability. | accepted |

## Related-Source Claims

| ID | Claim | Source kind | Evidence | Closure role | Status |
| --- | --- | --- | --- | --- | --- |
| RC1 | MemGPT proposes virtual context management across memory tiers for long-context tasks. | `related-source` | [MemGPT v2 abstract](https://arxiv.org/abs/2310.08560v2) | Shows that active context movement predates this five-part taxonomy. | accepted |
| RC2 | ACE identifies brevity bias and context collapse and uses structured incremental updates. | `related-source` | [ACE v3 abstract](https://arxiv.org/abs/2510.04618v3) | Supplies an alternative to lossy rewriting; it is not validated compaction. | accepted |
| RC3 | LongMemEval covers 500 questions and long-term abilities including extraction, multi-session reasoning, temporal reasoning, updates, and abstention. | `related-source` | [LongMemEval v2 abstract](https://arxiv.org/abs/2410.10813v2) | Bounds what the 92.0% result can measure. | accepted |
| RC4 | LoCoMo uses roughly 300-turn, 9K-token conversations and evaluates QA, summarization, and multimodal dialogue. | `related-source` | [LoCoMo v1 abstract](https://arxiv.org/abs/2402.17753v1) | Bounds what the 93.2% result can measure. | accepted |

## Local Inferences And Operator Readings

| ID | Claim | Source kind | Evidence basis | Status |
| --- | --- | --- | --- | --- |
| LI1 | The five primitives are best used as coupled contract questions, not assumed to map one-to-one onto services. | `local-inference` | Paper §2 and §4 explicitly separate primitives from runtime components. | accepted |
| LI2 | A context lifecycle needs receipts for selection, isolation, budget, provenance, and validation if operators are to audit it. | `operator-reading` | Paper's isolation, provenance, budget, and validation requirements. | accepted |
| LI3 | The reported benchmark numbers cannot causally isolate the value of the context layer from the answer model without a controlled ablation. | `local-inference` | Paper Table 3 is explicitly non-comparable and the run is a system/configuration combination. | accepted |
| A1 | An Arcanum capability route can be read as lifecycle-shaped when it makes admission, scope, evidence, compaction, and retirement explicit. | `analogy` | Structural similarity only. | accepted |

## Tensions And Open Claim Residue

| ID | Question or tension | Source kind | Evidence | Status | Next route |
| --- | --- | --- | --- | --- | --- |
| R1 | The paper says the results repository tags run date/revision, but the checked public surface exposes no pinned run tag in the paper's table. | `open-residue` | Paper §6.1 and checked results repository | open | `research-evidence-harness` |
| R2 | The results repository and paper say LongMemEval used 500 questions; the current harness README labels the headline result `50q`. | `open-residue` | Checked companion repositories at recorded HEADs | open | `research-evidence-harness` |
| R3 | Per-run answers, retrieved context, and judge verdicts are request-only, so the scores were not independently reproduced here. | `open-residue` | Paper §6.3 and results repository | open | `research-evidence-harness` |
| R4 | The proprietary validation mechanism does not expose a public definition or trace proving “lossless” compaction. | `open-residue` | Paper §4–§5 | open | mechanism disclosure or independent experiment |
| B1 | “A smaller answer model proves the gain comes from the context layer.” | `local-inference` | Paper §6.2 | blocked | Requires controlled ablation, not cross-vendor comparison |
| B2 | “All five primitives are necessary and sufficient for every agent.” | `local-inference` | No completeness proof in the bounded corpus | blocked | Broader taxonomy review |
