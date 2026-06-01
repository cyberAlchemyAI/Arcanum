# Decision Gate: Evidence-Card POC Gates

## Target Scope

Inventory evidence-card POC continuation decision.

## Decision Question

Do the six data-backed POC gates support continuing with the evidence-card model, refining a narrow part of it, or stopping/redesigning?

## Gate Verdicts

| Gate | Evidence | Verdict | Decision |
| --- | --- | --- | --- |
| Source slice | `pilot-cards.json` has 11 cards from the bounded pilot slice. | pass | Continue. The slice produced more than the 10-card target without whole-repo ingest. |
| Card size | Median summary length is 20 words; max is 29 words. | pass | Continue. Cards are compact and not mini-documents. |
| Selector quality | 10 of 11 cards use line-span selectors; the remaining POC question card uses two heading selectors to local POC artifacts. | pass | Continue. Source claims are reviewable; heading selectors are acceptable for internal decision artifacts. |
| Validation strictness | `validate-evidence-card-fixtures.sh` passes real fixtures and invalid examples cover selector, enum, owner/status, relation notice, and minimal-profile misuse classes. | pass | Continue. The first validator catches the named failure classes. |
| Retrieval value | `pilot-retrieval.json` selects 6 cards, excludes 3 matches with reasons, and forms one candidate EvidenceSet; `craft-stressor-retrieval.json` selects 7 cards from a second Craft slice and forms a second candidate EvidenceSet. | pass | Continue to minimal candidate schema design. Reuse is now proven enough for design, but not enough for canonical production behavior. |
| Handoff safety | Ontology and Definitions handoff packets parse, include source refs, and include explicit non-authority notices. | pass | Continue. Candidate-only authority is visible. |

## Summary

Six gates pass for continuing the evidence-card model. The Craft stressor resolved the earlier retrieval-value flag enough to justify a minimal candidate `EvidenceSet` schema design.

This satisfies the POC decision rule from `POC-VALIDATION.md`: continue if at least five of six gates pass and the failing/flagged gate has a narrow repair.

## Blocker Decisions

No blocker remains for continuing the evidence-card model.

One blocker remains for canonical `EvidenceSet` promotion: define and validate a minimal candidate schema before production behavior changes.

## Selected Decision

Continue the evidence-card model.

Do not canonicalize `EvidenceSet` yet. Use the first retrieval and Craft stressor as inputs to a minimal candidate schema design.

## Next Route

Use `task-session` to design the minimal candidate `EvidenceSet` schema:

- required fields only;
- explicit non-goals against ledger/schema/synthesis-pack behavior;
- validation against `evidence-set.evidenceset-need` and `evidence-set.craft-recursive-ledger`;
- production promotion decision after schema validation.
