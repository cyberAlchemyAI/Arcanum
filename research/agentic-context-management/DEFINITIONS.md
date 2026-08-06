# Governed Local Definitions

Status: `local-research-only`

These definitions are owned by this tower only. They do not alter
`arcanum/definitions/DEFINITIONS.md`.

## D1 — Agentic Context Management

**Source meaning.** The discipline of deciding what an agent should hold in
context, when, for how long, and at what cost, from acquisition to retirement.

**Structural shape.**

```text
ACM = coupled(
  architecting,
  ingesting,
  scoping,
  anticipating,
  compacting_and_consolidation
) across authorized scopes
```

**Intuition.** The store is one component inside a policy and evidence loop.

**Anti-misuse.** This decomposition is not proved necessary and sufficient for
all agents.

## D2 — Context Architecture

**Source meaning.** A per-agent design for memory categories, extraction,
storage, retention, retrieval, and compaction.

**Structural shape.**

```text
agent purpose + reference material
  -> context policy/configuration
  -> constraints on downstream primitives
```

**Intuition.** Decide the shape of remembered evidence before collecting it.

**Anti-misuse.** A generated configuration is not automatically correct,
authorized, or safe; the paper says scope policy remains client-governed.

## D3 — Scope-Safe Context Assembly

**Source meaning.** Retrieval and assembly constrained by the paper's
user/customer/client hierarchy, tenant isolation, provenance, ranking, and token
budget.

**Structural shape.**

```text
authorized principal + query + budget
  -> narrowest-first scoped retrieval
  -> provenance-tagged context
```

**Intuition.** Relevance never overrides isolation.

**Anti-misuse.** A broad organizational pool is not an authorization model by
itself.

## D4 — Anticipatory Retrieval

**Source meaning.** Predictive preparation of context likely to be needed on a
future turn, distinct from responding to a current query or replaying a cache.

**Structural shape.**

```text
observed behavior -> predicted need -> speculative fetch -> hit | miss
```

**Intuition.** Move likely retrieval off the critical path.

**Anti-misuse.** The paper reports a product hit-rate claim without publishing
the predictor or a benchmark; treat benefit and waste as unverified.

## D5 — Validated Compaction

**Source meaning.** A bounded-context reduction checked for recoverability of
key information, with a less-aggressive retry when a threshold is missed.

**Structural shape.**

```text
original context + preservation obligations + budget
  -> compact
  -> validate
  -> accept(receipt) | retry | refuse
```

**Intuition.** Compression is a claim that needs evidence.

**Anti-misuse.** `validation score` is undefined publicly in the paper; do not
equate it with semantic losslessness.

## D6 — Reasoning Sufficiency

**Source meaning.** The assembled evidence is sufficient to complete the
reasoning chain needed for the answer.

**Structural shape.**

```text
answer_quality <= min(extraction_quality,
                      retrieval_quality,
                      reasoning_sufficiency)
```

**Intuition.** One relevant document can still omit the bridge premise.

**Anti-misuse.** The inequality is a conceptual bottleneck, not a calibrated
scoring function.

## D7 — Managed Context Cost Envelope

**Source meaning.** With fixed per-turn budget `W`, periodic compaction every
`p` turns, and check cost `c` times bounded context, cumulative token use is
modeled as `N*W*(1+c/p)`.

**Intuition.** Validation adds a constant factor while retaining linear growth
under fixed assumptions.

**Anti-misuse.** The model excludes variable turns, cache discounts, retrieval,
outputs, and quality effects.

## D8 — Decision-Level Context

**Source meaning.** Context that preserves why decisions were made and how they
relate to outcomes and superseding decisions.

**Structural shape.**

```text
decision + rationale provenance + time + outcome linkage + supersession state
```

**Intuition.** Institutional judgment is more than a fact log.

**Anti-misuse.** This is a future direction in the paper, not a demonstrated
system contract.
