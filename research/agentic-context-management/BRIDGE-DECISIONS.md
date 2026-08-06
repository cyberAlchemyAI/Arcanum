# Bridge Decisions

| Concept | Decision | Rationale | Follow-up |
| --- | --- | --- | --- |
| Context as a lifecycle | `borrow-carefully` | Corrects store/retrieve tunnel vision and exposes coupled decisions. | Use as a local review lens only. |
| Five primitives | `borrow-carefully` | Strong checklist; no exhaustive or necessary/sufficient proof. | Compare against future architectures without promotion. |
| Context architecture artifact | `borrow-carefully` | Makes retention, extraction, scope, and compaction policies inspectable. | A future design may define its own owner and schema. |
| Paper's user/customer/client hierarchy | `analogy-only` | Useful narrow-to-broad intuition; vocabulary and authority semantics are source-specific. | Map explicitly before any reuse. |
| Anticipatory retrieval | `future-work` | Potential latency benefit, but predictor, miss cost, and safety evidence are absent. | Requires an evidence harness and threat model. |
| Validated compaction contract | `borrow-carefully` | Acceptance/retry/refusal is a sound shape for lossy transformations. | Define invariants and fixtures before implementation. |
| “Lossless” compaction | `block` | Public mechanism and traces do not establish semantic losslessness. | Require measurable preservation obligations. |
| Reasoning-sufficiency distinction | `borrow-carefully` | Prevents relevant-hit metrics from standing in for complete evidence. | Design multi-premise fixtures if promoted to an experiment. |
| Reported benchmark superiority | `block` | Scores are configuration-sensitive, self-reported, and not causally controlled. | Reproduce under a pinned protocol. |
| Decision-level context | `future-work` | Rationale capture, causal attribution, supersession, and security remain unresolved. | Separate research tower or evidence harness. |
| Canonical Arcanum vocabulary change | `block` | Research is not promotion authority. | Requires a separate governed definitions decision. |

## Promotion Result

No promotion candidates are listed. The tower changes no canonical definition,
Inventory entry, ontology, sigil, spell, runtime contract, or behavior.
