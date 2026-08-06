# L1 — Residue Map

| Residue | Question | Resolution in this tower | Status |
| --- | --- | --- | --- |
| R1 | Is context management more than storage and retrieval? | The five primitives and their coupling provide a coherent lifecycle model; prior MemGPT work shows context movement predates this taxonomy. | closed-for-conceptual-use |
| R2 | Does the quadratic cost claim hold? | Yes under the paper's full-append assumptions; it is an arithmetic model, not a measured universal law. | closed-with-guard |
| R3 | Does “validated compaction” establish lossless preservation? | No. It is a quality contract and target; the validator is proprietary and no public per-run fidelity traces were found. | closed-as-block |
| R4 | Do retrieval hits prove reasoning sufficiency? | No. LongMemEval/LoCoMo evaluate conversational memory, while multi-document sufficiency requires evidence beyond a relevant-hit metric. | closed-as-distinction |
| R5 | Do 92.0% and 93.2% prove the complete lifecycle? | No. They are reported conversational-memory results under stated configurations, not an ablation of all five primitives or production evidence. | closed-as-proof-ceiling |
| R6 | Are the published scores reproducible from current public artifacts? | Not yet demonstrated: per-run traces are request-only and the harness/results documentation disagrees on 50 versus 500 LongMemEval questions. | future-work |
| R7 | Is the five-primitive taxonomy exhaustive or uniquely novel? | Not established by the bounded corpus; it is useful as a decomposition, not a completeness theorem. | future-work |
| R8 | Should any paper term enter Arcanum canon or runtime? | No decision is authorized by research alone. | closed-as-promotion-block |
