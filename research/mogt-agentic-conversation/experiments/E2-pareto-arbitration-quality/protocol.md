# EX: Pareto Arbitration Quality

**Status:** draft
**Tier:** foundation
**Paper Claim:** MOGT-C2
**Paper Section:** arbitration quality and frontier reasoning
**Priority:** P0

---

## Objective

Validate whether Pareto-aware arbitration selects better multi-objective actions than heuristic and weighted-sum baselines.

## Methodology Profile

- Method profile path: `experiments/E2-pareto-arbitration-quality/methodology.md`
- Method contract: `protocols/MOGT-PROTOCOL-CHECKLIST.md`
- Tier: foundation
- Primary framework: controlled comparison over matched benchmark scenarios
- Validity plan: fixed scenarios, auditable objective annotations, blinded review of outcomes

## Protocol

1. Define a benchmark scenario set with explicit candidate actions and objective annotations.
2. Execute heuristic, weighted-sum, and Pareto-guided policy regimes on each scenario.
3. Record chosen actions, objective vectors, and policy metadata.
4. Classify selected actions as frontier or dominated.
5. Compare quality, regret, and dominated-selection rate across regimes.

## Claim Mapping

| Claim ID | Research Question                                                | Expected Signal                                 |
| -------- | ---------------------------------------------------------------- | ----------------------------------------------- |
| MOGT-C2  | does Pareto-aware arbitration improve multi-objective decisions? | lower dominated-selection rate and lower regret |
| MOGT-C4  | do gains survive cost constraints?                               | quality gains remain under acceptable overhead  |

## Definition Anchors

- Definitions index path: `definitions/DEFINITIONS-INDEX.md`
- Referenced definition IDs: MOGT-D3, MOGT-D5, MOGT-D9, MOGT-M1, MOGT-M4

## Reference Anchors

- Reference ledger path: `sources/REFERENCE-LEDGER.md`
- Authoritative references used by this protocol: REF-WOHLIN-2012, REF-DEB-2001, REF-KEENEY-RAIFFA-1976, REF-MARLER-2010

## Context Bundle

- Context bundle path: `experiments/E2-pareto-arbitration-quality/context.md`
- Template: `implementation/mars/templates/context-bundle-template.md`

## Data Schema

- Schema file: `implementation/mars/templates/schema-foundation-template.json`
- Row target: 30-60 matched scenario evaluations per regime
- Sampling plan: same scenario set run across three policy regimes with reviewer scoring afterward

## Source Requirements

| Source ID               | Type        | Why needed                                                 | Version Pin                   |
| ----------------------- | ----------- | ---------------------------------------------------------- | ----------------------------- |
| PAPER-WOHLIN-2012       | methodology | comparative baseline                                       | book:springer-2012            |
| PAPER-DEB-2001          | theory      | Pareto-front and multi-objective baseline                  | book:deb-2001                 |
| BOOK-KEENEY-RAIFFA-1976 | theory      | objective articulation and value-tradeoff framing          | book:wiley-1976-keeney-raiffa |
| PAPER-MARLER-2010       | theory      | weighted-sum comparison context for the practical baseline | doi:10.1007/s00158-009-0460-7 |

## Inventory Requirements

| Entry Type             | Required? | Notes                                              |
| ---------------------- | --------- | -------------------------------------------------- |
| paper-abstract         | yes       | methodology and theory baseline                    |
| framework-architecture | yes       | policy regime specification                        |
| role-definition        | yes       | reviewer and arbitration role definition           |
| domain-model           | no        | benchmark scenarios can be artifact-defined        |
| tool-evaluation        | no        | only add if tooling affects the outcome materially |

## Success Criteria

| ID   | Metric                   | Threshold                                         | Pass Rule                                                                   |
| ---- | ------------------------ | ------------------------------------------------- | --------------------------------------------------------------------------- |
| SC-1 | dominated_selection_rate | at least 30 percent lower than heuristic baseline | Pareto-guided regime beats heuristic by threshold                           |
| SC-2 | decision_quality_score   | non-inferior to best baseline                     | Pareto-guided regime is not meaningfully worse than the best comparison arm |

## Analysis Path

Foundation tier minimum analysis:

- data integrity
- descriptive statistics
- success-criteria evaluation
- claim adjudication recommendation

Optional in foundation:

- sensitivity by number of active objectives

## Hard Gate Checklist

| Gate | Condition                                                                                  | Evidence                                       | Decision |
| ---- | ------------------------------------------------------------------------------------------ | ---------------------------------------------- | -------- |
| G1   | methodology-linked protocol measurable with definition/context anchors and schema complete | methodology + protocol + context + definitions | pending  |
| G2   | sources validated and pinned                                                               | E2 sources bundle                              | pending  |
| G3   | inventory readiness confirmed                                                              | benchmark and theory inventory artifacts       | pending  |
| G4   | data integrity pass                                                                        | integrity report after first run               | pending  |

## Artifact Paths

- Experiment bundle root: `experiments/E2-pareto-arbitration-quality/`
- Methodology profile: `experiments/E2-pareto-arbitration-quality/methodology.md`
- Protocol: `experiments/E2-pareto-arbitration-quality/protocol.md`
- Source selection: `experiments/E2-pareto-arbitration-quality/sources.md`
- Context bundle: `experiments/E2-pareto-arbitration-quality/context.md`
- Raw data: `experiments/E2-pareto-arbitration-quality/data/run-YYYY-MM-DD[-suffix].jsonl`
- Results: `experiments/E2-pareto-arbitration-quality/results/<run-id>-results.md`

## Notes

This experiment is the main test of whether multi-objective reasoning improves selection quality rather than just explanation quality.
