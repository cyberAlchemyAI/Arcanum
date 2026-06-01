# Refine Result: EvidenceSet Candidate

## Status

`flag`

## Compact Synthesis

The first POC gives positive signal for `EvidenceSet`, but not enough to promote it as canonical.

Evidence in favor:

- Retrieval naturally produced a grouped candidate with 4 included cards and 2 excluded cards.
- The group has a clear task purpose: decide whether an intermediate artifact belongs between cards and handoff packets.
- Handoff examples reused related boundary and term groups, which suggests grouping may reduce repeated packet assembly.
- The validator now proves the current card/retrieval/handoff fixtures are structurally safe.

Evidence against immediate promotion:

- Reuse is only shown inside one pilot slice.
- The current candidate may still be a retrieval result with stable IDs, not a stored artifact family.
- `POC-VALIDATION.md` says to continue with EvidenceSet only if the grouped result naturally becomes reusable.
- Craft was explicitly selected as the best second-pass stressor for nested contexts, artifacts, gates, blockers, enablers, and recomposition.

## Smallest Coherent Unit

The smallest next unit is not "implement EvidenceSet".

It is:

> Run one Craft stressor pass that tries to compose `evidence-set.craft-recursive-ledger` from selected Craft evidence-cards, then compare whether the set adds value beyond retrieval output.

## Rejected Alternatives

| Alternative | Reason Rejected For Now |
| --- | --- |
| Promote EvidenceSet now | Too early; current evidence comes from one pilot slice. |
| Drop EvidenceSet | Too early; first retrieval and handoff examples show real grouping pressure. |
| Build human UI for EvidenceSet review | Premature; agent/runtime validator and data gates are enough for this decision. |

## Recommended Decision-Gate Option

Select: keep `EvidenceSet` as a candidate and run the Craft stressor before canonical promotion.
