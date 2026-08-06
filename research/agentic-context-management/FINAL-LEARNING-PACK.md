# Final Learning Pack

Profile: `standard-source-first`

Status: `pass-for-source-backed-learning`

Promotion scope: `local-research-only`

## One Sentence

An agent's context should be managed as a coupled, scope-safe, budgeted, and
validated lifecycle; storage and retrieval are necessary components, but they do
not decide what deserves to exist, what may be seen, what will be needed next,
or what can be removed safely.

## Source-First Spine

| Layer | Source meaning | Closure artifact |
| --- | --- | --- |
| Category | ACM spans acquisition through retirement | [definition card](definition-cards/agentic-context-management.md) |
| Decomposition | Architecting, ingesting, scoping, anticipating, compacting & consolidation | [DEFINITIONS.md](DEFINITIONS.md) |
| Economics | Full append is quadratic under fixed-growth assumptions; bounded context is linear | [cost example](worked-examples/cost-envelope.md) |
| Information | Extraction, retrieval, and reasoning sufficiency form a bottleneck chain | [sufficiency card](definition-cards/reasoning-sufficiency.md) |
| Reference design | Synap is described as a multi-tenant implementation with proprietary mechanisms | [claim ledger](tracks/paper-claim-ledger.md) |
| Evidence | Conversational-memory scores are reported under stated configurations | [source record](sources/source-record.md) |
| Frontier | Production latency/cost/context-rot and decision-level context remain open | [open residue](residue/open-residue.md) |

## Notation Entry Point

Read [NOTATION.md](NOTATION.md) before using the cost equations. The decisive
guard is that `O(n^2)` versus `O(n)` follows from the model's assumptions; it is
not a universal measurement of every agent stack.

## Operator Model

```text
policy before capture
  + structure before retrieval
  + authorization before relevance
  + sufficient evidence before answer
  + preservation proof before compaction acceptance
  + provenance through retirement
= auditable context lifecycle
```

## Durable Lessons

1. Context selection is an architecture decision, not just a search query.
2. Ingestion can irreversibly cap later answer quality.
3. Relevance and authorization are independent gates.
4. Predictive retrieval is useful only with miss-cost and safety accounting.
5. A bounded window solves growth, not fidelity.
6. Compression needs declared preservation obligations and a receipt.
7. Retrieval metrics must not stand in for complete reasoning evidence.
8. Benchmark numbers remain attached to dataset, scope, answer model, judge,
   prompts, revision, and raw run artifacts.

## What To Borrow Carefully

- The five primitives as a design-review checklist.
- The principle that architecture configures downstream context behavior.
- Narrowest-authorized-scope-first assembly with provenance.
- Validation/retry/refusal around lossy compaction.
- Reasoning sufficiency as a distinct evaluation target.

## What To Keep Analogy-Only

- Mapping the five primitives onto Arcanum capability stages.
- Treating the paper's organizational hierarchy as an authority model.
- Treating `primitives x scopes` as a coverage matrix for another system.

## What To Block

- Promotion of paper terms into canonical vocabulary from research alone.
- Claims that proprietary compaction is proved lossless.
- Claims that the reported benchmarks establish production latency, cost,
  isolation, context-rot resistance, or all-five-primitive causality.
- Claims that a cross-vendor table with different models is a controlled
  comparison.
- Claims that decision-level organizational context is delivered rather than a
  research frontier.

## Closed Residue Summary

| Residue | Closure |
| --- | --- |
| Store versus lifecycle | Closed by the five coupled decisions and prior-work boundary |
| Quadratic versus linear cost | Closed as conditional arithmetic in [cost-envelope.md](worked-examples/cost-envelope.md) |
| Relevance versus sufficiency | Closed as a conceptual and fixture-level distinction |
| Benchmark proof scope | Closed at conversational-memory behavior, not production ACM |
| Promotion effect | Closed at zero; all artifacts remain local research |

## Remaining Honest Cutoff

The tower is not closed for:

- independent score reproduction;
- public validation of compaction fidelity or anticipation hit rate;
- measured latency, token efficiency, privacy isolation, or context-rot
  resistance under production load;
- exhaustive novelty of the ACM taxonomy;
- canonical or runtime adoption.

The next evidence-producing route is [explicitly recorded](residue/open-residue.md).

## Sources

- [Primary and companion source record](sources/source-record.md)
- [Bounded related-work crosswalk](RELATED-WORK.md)
