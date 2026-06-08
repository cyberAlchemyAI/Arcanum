# EX: Negotiation Stability Under Conflict

**Status:** draft
**Tier:** foundation
**Paper Claim:** MOGT-C3
**Paper Section:** disagreement handling and convergence
**Priority:** P1

---

## Objective

Validate whether a negotiation-aware policy reduces unresolved disagreement and turn cycling in contested agent conversations.

## Methodology Profile

- Method profile path: `experiments/E3-negotiation-stability-under-conflict/methodology.md`
- Method contract: `protocols/MOGT-PROTOCOL-CHECKLIST.md`
- Tier: foundation
- Primary framework: intervention comparison with turn-level telemetry
- Validity plan: fixed conflict scenarios, bounded-turn threshold, separate quality scoring for final decisions

## Protocol

1. Create a contested scenario suite with role-specific preferences.
2. Run each scenario with a baseline disagreement policy and a negotiation-enabled policy.
3. Capture turn-level telemetry, escalation events, and final outcomes.
4. Score final resolution quality under blinded review.
5. Compare convergence, cycling, and quality across regimes.

## Claim Mapping

| Claim ID | Research Question                                | Expected Signal                               |
| -------- | ------------------------------------------------ | --------------------------------------------- |
| MOGT-C3  | does negotiation reduce unresolved disagreement? | higher convergence rate and lower cycle count |
| MOGT-C4  | does it remain practical?                        | bounded added turns and acceptable overhead   |

## Definition Anchors

- Definitions index path: `definitions/DEFINITIONS-INDEX.md`
- Referenced definition IDs: MOGT-D6, MOGT-D7, MOGT-D9, MOGT-M3, MOGT-M4

## Reference Anchors

- Reference ledger path: `sources/REFERENCE-LEDGER.md`
- Authoritative references used by this protocol: REF-WOHLIN-2012, REF-WOOLDRIDGE-2009, REF-NASH-1950

## Context Bundle

- Context bundle path: `experiments/E3-negotiation-stability-under-conflict/context.md`
- Template: `implementation/mars/templates/context-bundle-template.md`

## Data Schema

- Schema file: `implementation/mars/templates/schema-foundation-template.json`
- Row target: 20-40 contested scenario runs per regime
- Sampling plan: paired baseline and negotiation-enabled runs over the same contested scenario suite

## Source Requirements

| Source ID             | Type        | Why needed                        | Version Pin          |
| --------------------- | ----------- | --------------------------------- | -------------------- |
| PAPER-WOHLIN-2012     | methodology | comparative-intervention baseline | book:springer-2012   |
| PAPER-WOOLDRIDGE-2009 | theory      | multi-agent coordination framing  | book:wooldridge-2009 |
| PAPER-NASH-1950       | theory      | negotiation stability framing     | paper:nash-1950      |

## Inventory Requirements

| Entry Type             | Required? | Notes                                             |
| ---------------------- | --------- | ------------------------------------------------- |
| paper-abstract         | yes       | methodology and theory baseline                   |
| framework-architecture | yes       | negotiation policy definition                     |
| role-definition        | yes       | role preference and escalation contract           |
| domain-model           | no        | contested scenarios are sufficient for first wave |
| tool-evaluation        | no        | not needed in the initial intervention wave       |

## Success Criteria

| ID   | Metric           | Threshold                               | Pass Rule                                                  |
| ---- | ---------------- | --------------------------------------- | ---------------------------------------------------------- |
| SC-1 | convergence_rate | +20 percentage points vs baseline       | negotiation-enabled regime exceeds baseline by threshold   |
| SC-2 | cycle_count      | at least 25 percent lower than baseline | negotiation-enabled regime reduces repeated conflict loops |

## Analysis Path

Foundation tier minimum analysis:

- data integrity
- descriptive statistics
- success-criteria evaluation
- claim adjudication recommendation

Optional in foundation:

- subgroup analysis by conflict severity or role asymmetry

## Hard Gate Checklist

| Gate | Condition                                                                                  | Evidence                                       | Decision |
| ---- | ------------------------------------------------------------------------------------------ | ---------------------------------------------- | -------- |
| G1   | methodology-linked protocol measurable with definition/context anchors and schema complete | methodology + protocol + context + definitions | pending  |
| G2   | sources validated and pinned                                                               | E3 sources bundle                              | pending  |
| G3   | inventory readiness confirmed                                                              | role and scenario inventory artifacts          | pending  |
| G4   | data integrity pass                                                                        | integrity report after first run               | pending  |

## Artifact Paths

- Experiment bundle root: `experiments/E3-negotiation-stability-under-conflict/`
- Methodology profile: `experiments/E3-negotiation-stability-under-conflict/methodology.md`
- Protocol: `experiments/E3-negotiation-stability-under-conflict/protocol.md`
- Source selection: `experiments/E3-negotiation-stability-under-conflict/sources.md`
- Context bundle: `experiments/E3-negotiation-stability-under-conflict/context.md`
- Raw data: `experiments/E3-negotiation-stability-under-conflict/data/run-YYYY-MM-DD[-suffix].jsonl`
- Results: `experiments/E3-negotiation-stability-under-conflict/results/<run-id>-results.md`

## Notes

This experiment should stay second-wave unless E1 and E2 show that explicit objective framing is already useful.
