# EX: Overhead Feasibility Envelope

**Status:** draft
**Tier:** foundation
**Paper Claim:** MOGT-C4
**Paper Section:** operational feasibility and adoption guidance
**Priority:** P0

---

## Objective

Determine whether multi-objective and negotiation-aware decision policies remain operationally viable once token, latency, and review overhead are measured explicitly.

## Methodology Profile

- Method profile path: `experiments/E4-overhead-feasibility-envelope/methodology.md`
- Method contract: `protocols/MOGT-PROTOCOL-CHECKLIST.md`
- Tier: foundation
- Primary framework: observational performance study over matched benchmark runs
- Validity plan: fixed scenario set, explicit threshold policy, quality and overhead measured jointly

## Protocol

1. Select a matched benchmark scenario set.
2. Run the scenario set under progressively more complex policy regimes.
3. Record token cost, latency, turn count, and reviewer burden alongside quality.
4. Evaluate which configurations stay inside the accepted overhead envelope.
5. Identify any breakpoint where added complexity stops paying off.

## Claim Mapping

| Claim ID | Research Question                                                    | Expected Signal                                                |
| -------- | -------------------------------------------------------------------- | -------------------------------------------------------------- |
| MOGT-C4  | is there a viable operating region for the approach?                 | measurable overhead envelope with acceptable quality retention |
| MOGT-C2  | do higher-quality policies remain worthwhile under cost constraints? | quality benefit survives within the envelope                   |

## Definition Anchors

- Definitions index path: `definitions/DEFINITIONS-INDEX.md`
- Referenced definition IDs: MOGT-D8, MOGT-D9, MOGT-M1, MOGT-M4

## Reference Anchors

- Reference ledger path: `sources/REFERENCE-LEDGER.md`
- Authoritative references used by this protocol: REF-WOHLIN-2012, REF-JAIN-1991, REF-HART-STAVELAND-1988, REF-WALKER-1997, REF-MARLER-2010

## Context Bundle

- Context bundle path: `experiments/E4-overhead-feasibility-envelope/context.md`
- Template: `implementation/mars/templates/context-bundle-template.md`

## Data Schema

- Schema file: `implementation/mars/templates/schema-foundation-template.json`
- Row target: 40-80 run configurations across scenarios and policy regimes
- Sampling plan: matched scenario replays with systematically varied objective count and negotiation depth

## Source Requirements

| Source ID                 | Type          | Why needed                                                       | Version Pin                       |
| ------------------------- | ------------- | ---------------------------------------------------------------- | --------------------------------- |
| PAPER-WOHLIN-2012         | methodology   | performance-study baseline                                       | book:springer-2012                |
| BOOK-JAIN-1991            | overhead      | latency, throughput, and breakpoint measurement discipline       | book:jain-1991                    |
| PAPER-HART-STAVELAND-1988 | human-factors | reviewer workload and burden instrumentation                     | doi:10.1016/S0166-4115(08)62386-9 |
| PAPER-WALKER-1997         | evaluation    | dialogue and decision-episode quality-versus-cost framing        | doi:10.3115/976909.979652         |
| PAPER-MARLER-2010         | theory        | weighted-sum comparison context for practical baseline selection | doi:10.1007/s00158-009-0460-7     |

## Inventory Requirements

| Entry Type             | Required? | Notes                                                      |
| ---------------------- | --------- | ---------------------------------------------------------- |
| paper-abstract         | yes       | methodology and comparison context                         |
| framework-architecture | yes       | policy complexity ladder                                   |
| role-definition        | yes       | reviewer-burden accounting                                 |
| domain-model           | no        | benchmark scenarios can be treated as standalone artifacts |
| tool-evaluation        | no        | only needed if infrastructure differences become material  |

## Success Criteria

| ID   | Metric                       | Threshold                                                   | Pass Rule                                                        |
| ---- | ---------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------- |
| SC-1 | overhead_acceptability_ratio | at least 0.7 within the preferred operating region          | majority of tested runs remain within configured overhead limits |
| SC-2 | quality_retention            | at least baseline quality in the preferred operating region | retained quality does not fall below the agreed baseline floor   |

## Analysis Path

Foundation tier minimum analysis:

- data integrity
- descriptive statistics
- success-criteria evaluation
- claim adjudication recommendation

Optional in foundation:

- breakpoint analysis across objective counts and negotiation depth

## Hard Gate Checklist

| Gate | Condition                                                                                  | Evidence                                       | Decision |
| ---- | ------------------------------------------------------------------------------------------ | ---------------------------------------------- | -------- |
| G1   | methodology-linked protocol measurable with definition/context anchors and schema complete | methodology + protocol + context + definitions | pending  |
| G2   | sources validated and pinned                                                               | E4 sources bundle                              | pending  |
| G3   | inventory readiness confirmed                                                              | threshold and telemetry inventory artifacts    | pending  |
| G4   | data integrity pass                                                                        | integrity report after first run               | pending  |

## Artifact Paths

- Experiment bundle root: `experiments/E4-overhead-feasibility-envelope/`
- Methodology profile: `experiments/E4-overhead-feasibility-envelope/methodology.md`
- Protocol: `experiments/E4-overhead-feasibility-envelope/protocol.md`
- Source selection: `experiments/E4-overhead-feasibility-envelope/sources.md`
- Context bundle: `experiments/E4-overhead-feasibility-envelope/context.md`
- Raw data: `experiments/E4-overhead-feasibility-envelope/data/run-YYYY-MM-DD[-suffix].jsonl`
- Results: `experiments/E4-overhead-feasibility-envelope/results/<run-id>-results.md`

## Notes

This experiment should be paired with E2 because feasibility is only meaningful when quality gains are measured in the same evaluation family.
