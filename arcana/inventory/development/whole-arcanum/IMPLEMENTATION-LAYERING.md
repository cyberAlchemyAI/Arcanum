---
module: inventory-whole-arcanum
version: 0.1.0
status: planned
updatedAt: 2026-05-29
docType: implementation-layering
---

# Implementation Layering: Whole Arcanum Inventory

## Layer Thesis

The smallest useful proof is not "cards for everything." It is a trustworthy
source boundary plus one real retrieval path that helps an agent answer a
cross-capability question faster than raw repository search.

## Layers

| Layer | Question | Scope | Promotion Evidence |
| --- | --- | --- | --- |
| L0 Source Boundary | Can we decide what belongs in the inventory before card creation? | source manifest, exclusion policy, source-family classification | manifest validates against Artifact Constitution and excludes generated/local runtime state |
| L1 Proof Slice | Can cards and EvidenceSets answer real implementation questions? | Inventory package plus governance/schema/lifecycle pilot | validated cards, candidate EvidenceSets, retrieval examples, missing-context report |
| L2 Capability Expansion | Can the same model scale across Arcanum families? | arcana, spells, transmutations, formulae, framework, registry, tools | family indexes, coverage report, selector-quality checks, duplicate/drift notes |
| L3 Operational Readiness | Can agents refresh and query inventory repeatedly? | refresh commands, lint checks, readiness docs, handoff examples | repeatable validation command, query examples, task-session result, readiness report |

## Layer Gates

### L0 Gate

Pass when:

- source families are explicitly classified,
- generated and local runtime paths are excluded by default,
- durable evidence inclusion requires a named reason,
- first manifest validation can run with shell tooling.

### L1 Gate

Pass when:

- the Inventory self-slice has evidence cards for behavior, schema, validator,
  and handoff boundaries,
- the governance/lifecycle pilot contains enough cards to test a real query,
- card references resolve,
- EvidenceSet candidates record why selected cards were included or excluded.

### L2 Gate

Pass when:

- each capability family has a bounded slice plan,
- source selectors do not require full-file ingestion for common queries,
- duplicate concepts and conflicting ownership claims are reported instead of
  silently merged.

### L3 Gate

Pass when:

- agents can run one command to validate cards and candidate sets,
- inventory updates produce reviewable diffs,
- stale or missing coverage is visible,
- no human UI is required for the agent-fast path.

## Deferrals

| Deferral | Reason | Revisit Trigger |
| --- | --- | --- |
| Human UI | Current value is agent-speed retrieval. | Query/report output becomes hard for humans to inspect. |
| Canonical EvidenceSet promotion | Candidate sets need reuse evidence across multiple slices. | At least three distinct task-session runs consume EvidenceSets successfully. |
| Automated full ingest | Boundary quality matters more than raw volume. | L1 and L2 selectors prove low false-positive retrieval. |
