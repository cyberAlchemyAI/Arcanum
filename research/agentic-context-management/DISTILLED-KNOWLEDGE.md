# Distilled Knowledge

## One Sentence

Useful agent context is an evidence lifecycle whose selection, scope, budget,
provenance, anticipation, compression, validation, and retirement decisions must
be designed together.

## Compositional Spine

```text
purpose
  -> architecture: decide what kinds of evidence matter
  -> ingestion: preserve structure, identity, time, provenance
  -> scoping: admit only authorized and relevant evidence
  -> anticipation: optionally prepare likely next evidence
  -> compaction/consolidation: fit the budget and validate preservation
  -> model turn
  -> new signals, outcomes, staleness, and retirement
  -> repeat
```

This is a lifecycle, not a promise that each arrow is a separate service or that
the order is strictly serial.

## What To Borrow Carefully

- Treat context architecture as a first-class artifact with explicit downstream
  consequences.
- Make tenant/principal scope enforceable at storage and query boundaries.
- Separate recent verbatim working context from asynchronous durable ingestion.
- Make compaction emit a preservation receipt and permit retry or refusal.
- Measure evidence sufficiency, not only retrieval relevance.
- Keep benchmark configuration attached to every score.

## What To Keep Analogy-Only

- The paper's five primitives as an Arcanum route checklist.
- `primitives x scopes` as a coverage matrix.
- The user/customer/client hierarchy as a generic authority lattice.
- Product-specific generated memory architectures as general admission plans.

## What To Block

- “Vector retrieval plus summarization equals context management.”
- “Bounded context preserves fidelity.” Budget and fidelity are separate claims.
- “Validated means lossless.” The public validation contract is underspecified.
- “92% proves all five primitives.” The benchmark does not ablate the lifecycle.
- “A smaller answer model proves causal improvement.” Cross-vendor rows are not a
  controlled experiment.
- “Decision-level context is solved.” The paper names it as a frontier.

## The Sharpest Operator Test

For any proposed context subsystem, ask:

1. What preservation obligations are declared before ingestion?
2. Which principal and scope authorize each item?
3. What evidence is needed now, and what is only predicted for later?
4. What is removed to meet budget, and how is loss checked?
5. Which source and revision can reproduce the assembled context?
6. What becomes stale, superseded, or retired?

If any answer is implicit, the lifecycle has an unaudited gap.
