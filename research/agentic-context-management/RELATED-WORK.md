# Related Framework Crosswalk

Target: `arXiv:2607.21503v1`

Related work is included only to close a named residue or prevent a misleading
equivalence.

| Framework or paper | Why included | Source kind | Closes residue | Boundary |
| --- | --- | --- | --- | --- |
| [MemGPT v2](https://arxiv.org/abs/2310.08560v2) | Shows prior virtual context management via memory tiers and paging | `related-source` | R1: lifecycle novelty | `borrow-carefully`: context placement is active; not the same five-part taxonomy |
| [ACE v3](https://arxiv.org/abs/2510.04618v3) | Names context collapse and preserves detail through incremental updates | `related-source` | R3: compaction alternatives | `analogy-only`: it avoids destructive rewriting rather than proving validated compaction |
| [LongMemEval v2](https://arxiv.org/abs/2410.10813v2) | Defines the 500-question long-term conversational-memory abilities | `related-source` | R5: benchmark proof ceiling | `borrow-carefully`: useful recall/reasoning benchmark, not production-context coverage |
| [LoCoMo v1](https://arxiv.org/abs/2402.17753v1) | Defines long-form dialogue tasks over roughly 300 turns | `related-source` | R5: benchmark proof ceiling | `borrow-carefully`: conversational memory, not organization-scale isolation or latency |
| [Maximem harness](https://github.com/maximem-ai/memory_and_context_eval_harness) | Exposes the public evaluation pipeline and present documentation mismatch | `primary-source` companion artifact | R6: reproducibility | `future-work`: run artifacts and exact published configuration remain unresolved |

## Synthesis

The paper's strongest contribution in this bounded corpus is the coupling of
architecture, ingestion, scope, anticipation, and validated reduction into one
operational category. MemGPT and ACE show that active context movement and
context evolution are established adjacent ideas. LongMemEval and LoCoMo support
evaluation of conversational-memory behavior, but do not establish the paper's
production claims about latency, token efficiency, isolation, or context-rot
resistance.

## Excluded Expansion

Commercial-system feature matrices, investment claims about context graphs, and
an exhaustive novelty survey are intentionally out of scope because they do not
close the tower's current conceptual or proof-boundary residue.
