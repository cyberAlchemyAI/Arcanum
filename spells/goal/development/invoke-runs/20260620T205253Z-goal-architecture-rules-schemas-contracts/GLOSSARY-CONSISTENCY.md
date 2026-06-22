# Goal Glossary Consistency

Status: pass

## Sources Checked

| Source | Role |
| --- | --- |
| `../20260620T202601Z-goal-spec-definitions/DEFINITIONS.md` | Local goal spell glossary. |
| `arcanum/definitions/DEFINITIONS.md` | Arcanum-wide canonical definitions. |
| `arcanum/definitions/DEFINITIONS-INDEX.md` | Definition lookup and alias surface. |
| `arcanum/spells/goal/README.md` | Source spell contract. |
| `SPEC.md` | Goal define-stage spec. |

## Consistency Matrix

| Term | Status | Canonical Or Local Authority | Notes |
| --- | --- | --- | --- |
| goal spell | linked | `DEF-ARC-GOAL-SPELL` | README and spec use the term compatibly as a router spell. |
| staged delta | linked | `DEF-ARC-STAGED-DELTA` | Rules, contracts, and schema use proposal-before-apply semantics. |
| approval token | linked | `DEF-ARC-APPROVAL-TOKEN` | Approval remains batch-specific, not ambient authority. |
| Craft frontier | local | `GOAL-DEF-FRONTIER` | Local to goal package; no global promotion needed. |
| risk tier | local | `GOAL-DEF-RISK-TIER` | Local enum for goal routing. |
| dispatch route | local | `GOAL-DEF-DISPATCH-ROUTE` | Uses Dispatch Spec authority without redefining it. |
| execution receipt | local | `GOAL-DEF-EXECUTION-RECEIPT` | Local receipt shape for goal handoff; Task Session still owns execution evidence. |
| decision profile | local | `GOAL-DEF-DECISION-PROFILE` | Public schema only; filled profiles stay outside public package. |
| gap discovery | local | `GOAL-DEF-GAP-DISCOVERY` | Local optional module. |
| proportionality guard | local | `GOAL-DEF-PROPORTIONALITY-GUARD` | Local budget and down-route module. |

## Drift Findings

| Finding | Severity | Route |
| --- | --- | --- |
| No conflicting canonical terms found. | none | n/a |
| Goal-specific local terms may later become reusable. | expected | Promote through definitions-governance only after repeated use outside `spells/goal`. |
| README does not yet link definition IDs inline. | low | Spellcraft validation may add links if desired. |

## Result

Glossary consistency passes for this design bundle. Local terms remain local;
canonical promoted terms are available in the Arcanum definitions source and
index.
