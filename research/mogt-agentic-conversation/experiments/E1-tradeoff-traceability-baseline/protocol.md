# EX: Tradeoff Traceability Baseline

**Status:** draft
**Tier:** foundation
**Paper Claim:** MOGT-C1
**Paper Section:** traceability and explainability baseline
**Priority:** P0

---

## Objective

Validate whether explicit objective vectors improve the inspectability of conversation decisions without degrading reviewer-rated acceptance quality.

## Methodology Profile

- Method profile path: `experiments/E1-tradeoff-traceability-baseline/methodology.md`
- Method contract: `protocols/MOGT-PROTOCOL-CHECKLIST.md`
- Tier: foundation
- Primary framework: comparative experiment with blinded review
- Validity plan: fixed scenario set, blinded reviewers, separate traceability and acceptance metrics

## Protocol

1. Select a benchmark set of conversation decision episodes.
2. Run each episode under a heuristic baseline and an explicit-objective policy regime.
3. Capture traces with the same metadata envelope for both regimes.
4. Have blinded reviewers score traceability coverage and acceptance quality.
5. Compare regime-level outcomes against the success criteria.

## Claim Mapping

| Claim ID | Research Question                            | Expected Signal                                 |
| -------- | -------------------------------------------- | ----------------------------------------------- |
| MOGT-C1  | do explicit objectives improve traceability? | higher traceability coverage                    |
| MOGT-C4  | do gains hold without unacceptable overhead? | non-inferior acceptance with bounded added cost |

## Definition Anchors

- Definitions index path: `definitions/DEFINITIONS-INDEX.md`
- Referenced definition IDs: MOGT-D1, MOGT-D3, MOGT-M2

## Reference Anchors

- Reference ledger path: `sources/REFERENCE-LEDGER.md`
- Authoritative references used by this protocol: REF-WOHLIN-2012, REF-KEENEY-RAIFFA-1976, REF-DOSHI-VELEZ-KIM-2017, REF-WALKER-1997

## Context Bundle

- Context bundle path: `experiments/E1-tradeoff-traceability-baseline/context.md`
- Template: `implementation/mars/templates/context-bundle-template.md`

## Data Schema

- Schema file: `implementation/mars/templates/schema-foundation-template.json`
- Row target: 30-60 scored decision episodes
- Sampling plan: paired policy runs over the same scenario set with reviewer scoring per episode

## Source Requirements

| Source ID                   | Type        | Why needed                                                      | Version Pin                   |
| --------------------------- | ----------- | --------------------------------------------------------------- | ----------------------------- |
| PAPER-WOHLIN-2012           | methodology | comparative-experiment baseline                                 | book:springer-2012            |
| BOOK-KEENEY-RAIFFA-1976     | theory      | explicit objective and value-tradeoff framing                   | book:wiley-1976-keeney-raiffa |
| REPORT-DOSHI-VELEZ-KIM-2017 | evaluation  | rigorous explainability and interpretability evaluation framing | arxiv:1702.08608v2            |
| PAPER-WALKER-1997           | evaluation  | dialogue and decision-episode evaluation baseline               | doi:10.3115/976909.979652     |

## Inventory Requirements

| Entry Type             | Required? | Notes                                           |
| ---------------------- | --------- | ----------------------------------------------- |
| paper-abstract         | yes       | methodology and theory baseline                 |
| framework-architecture | yes       | policy regime definitions                       |
| role-definition        | yes       | reviewer and policy-role contract               |
| domain-model           | no        | not required for first traceability wave        |
| tool-evaluation        | no        | only needed if tool differences become material |

## Success Criteria

| ID   | Metric                | Threshold                                       | Pass Rule                                               |
| ---- | --------------------- | ----------------------------------------------- | ------------------------------------------------------- |
| SC-1 | traceability_coverage | +20 percentage points vs heuristic baseline     | explicit-objective regime exceeds baseline by threshold |
| SC-2 | acceptance_score      | no worse than -10 percentage points vs baseline | intervention remains non-inferior on acceptance         |

## Analysis Path

Foundation tier minimum analysis:

- data integrity
- descriptive statistics
- success-criteria evaluation
- claim adjudication recommendation

Optional in foundation:

- subgroup analysis by scenario family

## Hard Gate Checklist

| Gate | Condition                                                                                  | Evidence                                       | Decision |
| ---- | ------------------------------------------------------------------------------------------ | ---------------------------------------------- | -------- |
| G1   | methodology-linked protocol measurable with definition/context anchors and schema complete | methodology + protocol + context + definitions | pending  |
| G2   | sources validated and pinned                                                               | E1 sources bundle                              | pending  |
| G3   | inventory readiness confirmed                                                              | inventory artifacts and rubric notes           | pending  |
| G4   | data integrity pass                                                                        | integrity report after first run               | pending  |

## Artifact Paths

- Experiment bundle root: `experiments/E1-tradeoff-traceability-baseline/`
- Methodology profile: `experiments/E1-tradeoff-traceability-baseline/methodology.md`
- Protocol: `experiments/E1-tradeoff-traceability-baseline/protocol.md`
- Source selection: `experiments/E1-tradeoff-traceability-baseline/sources.md`
- Context bundle: `experiments/E1-tradeoff-traceability-baseline/context.md`
- Raw data: `experiments/E1-tradeoff-traceability-baseline/data/run-YYYY-MM-DD[-suffix].jsonl`
- Results: `experiments/E1-tradeoff-traceability-baseline/results/<run-id>-results.md`

## Notes

This experiment should run before negotiation-heavy scenarios because it establishes whether objective-vector framing is useful at all.
