# Local Glossary

Every entry is local research vocabulary. None is promoted into canonical
Arcanum definitions.

## Agentic Context Management (ACM)

- Source kind: `primary-source`
- Local meaning: The full lifecycle of deciding what an agent holds in context, when, for how long, at what scope, and at what cost.
- Arcanum reading: A reminder to make selection, scope, budget, provenance, and retirement explicit in a capability's evidence path.
- Promotion status: `local-only`
- Misuse warning: Do not reduce ACM to a vector store, or claim the five primitives are an exhaustive theorem.
- Evidence: paper §2

## Architecting

- Source kind: `primary-source`
- Local meaning: Designing memory categories, extraction, stores, retention, retrieval, and compaction before ingestion.
- Arcanum reading: Declare the evidence shape and lifecycle policy before running the route.
- Promotion status: `analogy-only`
- Misuse warning: The paper's per-agent generated architecture is a product design, not a required Arcanum runtime behavior.
- Evidence: paper §2, §4–§5

## Ingesting

- Source kind: `primary-source`
- Local meaning: Turning raw conversations, documents, and tool events into structured, provenance-bearing memory.
- Arcanum reading: Evidence quality is bounded by what capture preserves.
- Promotion status: `analogy-only`
- Misuse warning: Storage of raw bytes alone is not the structured ingestion described by the paper.
- Evidence: paper §2, §4

## Scoping

- Source kind: `primary-source`
- Local meaning: Selecting permissible context at ingestion and retrieval across isolated organizational levels.
- Arcanum reading: Scope is enforced policy, not a ranking hint.
- Promotion status: `analogy-only`
- Misuse warning: The paper's `user/customer/client` names are paper-specific and must not be imported as canonical owner kinds.
- Evidence: paper §2, §5

## Anticipating

- Source kind: `primary-source`
- Local meaning: Predicting and preparing context likely to be needed next, before an explicit query.
- Arcanum reading: A speculative prefetch lane whose misses and cost need receipts.
- Promotion status: `analogy-only`
- Misuse warning: Do not call ordinary caching or background indexing anticipation.
- Evidence: paper §2, §4

## Compacting & Consolidation

- Source kind: `primary-source`
- Local meaning: Reducing over-budget context while preserving needed information and maintaining a validated durable form.
- Arcanum reading: Reduction should be checked against explicit preservation obligations.
- Promotion status: `analogy-only`
- Misuse warning: Smaller output is not evidence of preserved meaning.
- Evidence: paper §2, §4–§5

## Validated Compaction

- Source kind: `primary-source`
- Local meaning: A compaction operation accompanied by an information-preservation check and fallback/retry policy.
- Arcanum reading: A lossy transformation must emit a receipt tied to declared invariants.
- Promotion status: `local-only`
- Misuse warning: The paper does not publicly establish a universally lossless validator.
- Evidence: paper §3.2, §4–§5

## Reasoning Sufficiency

- Source kind: `primary-source`
- Local meaning: Whether the assembled context contains all evidence needed to complete the reasoning chain, not merely one relevant hit.
- Arcanum reading: A result needs enough connected evidence to discharge the claim.
- Promotion status: `local-only`
- Misuse warning: Relevance, recall@k, and sufficiency are not interchangeable.
- Evidence: paper §3.3

## Scope Hierarchy

- Source kind: `primary-source`
- Local meaning: The paper's narrow-to-broad user, customer, and client levels plus a separate global knowledge layer.
- Arcanum reading: Resolve the narrowest authorized context first and preserve isolation.
- Promotion status: `analogy-only`
- Misuse warning: Broader scope is not automatically authorized scope.
- Evidence: paper §2

## Context Rot

- Source kind: `primary-source`
- Local meaning: Degradation in usefulness or robustness as context becomes long or crowded.
- Arcanum reading: More evidence can lower signal quality when selection is weak.
- Promotion status: `local-only`
- Misuse warning: The paper names context-rot resistance as a missing benchmark dimension; it does not report a measurement.
- Evidence: paper §6.3

## Decision-Level Context

- Source kind: `primary-source`
- Local meaning: Future context that captures why an organizational decision was made, not just what happened.
- Arcanum reading: Rationale needs provenance, temporal supersession, and outcome linkage.
- Promotion status: `blocked`
- Misuse warning: The paper explicitly treats the hard causal and security problems as unresolved.
- Evidence: paper §8

## Proof Ceiling

- Source kind: `operator-reading`
- Local meaning: The strongest claim that the available source and artifacts can support.
- Arcanum reading: Stop claims at the evidence boundary and route residue separately.
- Promotion status: `local-only`
- Misuse warning: A polished architecture description is not runtime or production proof.
- Evidence: paper §4, §6.3 and companion-artifact inspection
