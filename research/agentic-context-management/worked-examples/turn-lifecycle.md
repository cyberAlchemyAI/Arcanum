# Worked Example: One Support Turn Across The Lifecycle

Source kind: `operator-reading` based on the paper's support-agent example.

Input:

```text
“Sarah said I should ask you. We upgraded to Pro last week,
but the dashboard still shows Starter.”
```

| Primitive | Local action | Required guard or receipt |
| --- | --- | --- |
| Architecting | The support-agent policy declares billing facts, temporal events, customer entities, and conservative compaction as important. | Approved architecture revision and retention policy |
| Ingesting | Preserve `Starter -> Pro`, the relative time, dashboard mismatch, and the mention of Sarah as separate structured evidence. | Source pointer, extraction confidence, temporal normalization |
| Scoping | Resolve Sarah and plan history only inside the authorized customer scope. | Principal identity, scope predicate, provenance per item |
| Anticipating | Optionally prefetch known plan-propagation guidance for a likely next question. | Prediction basis, hit/miss, speculative cost, no scope expansion |
| Compacting & consolidation | When the conversation grows, preserve the plan transition and unresolved dashboard state. | Explicit preservation obligations and validation receipt |

## Failure Counterexamples

- Store only “user mentioned pricing”: ingestion destroyed decisive detail.
- Resolve every “Sarah” globally: scope and identity may leak.
- Return a relevant billing article without the account transition: retrieval hit,
  reasoning insufficiency.
- Summarize “plan issue resolved” before confirmation: compaction fabricated state.
