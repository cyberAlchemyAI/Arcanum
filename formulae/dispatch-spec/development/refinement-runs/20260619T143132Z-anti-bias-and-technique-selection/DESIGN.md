# Design: Anti-Bias + Technique-Selection Advisor for dispatch-spec

Identity after this change: **dispatch-spec validates route shape AND advises technique
selection.** The validator core is unchanged; an advisory layer is added on top.

## Part A — Anti-bias as an enforced tension contract

dispatch-spec does NOT redefine anti-bias. It **references** `anti-bias-vector-composition`
(definition owner) and `check-tension` (the four-test rule), and adds a citable technique +
enforcement so tension is checked at *route-design time* (the gap: today nothing forces
sibling roles to be opposed — `subagent_strategy.explanation` is free text).

### New catalog technique (Arcanum family)
| Technique ID | Use In Dispatch | Validation Expectation |
| --- | --- | --- |
| `anti_bias_composition` | Any n≥2 sibling/role set (`fanout`/`dialectic`/`tournament` step, or `subagent_strategy.roles`) that must be structurally OPPOSED, not merely non-overlapping. | Declares `anti_bias.axis` from {methodology, source-corpus, attack-vector, temporal-prior} or a declared composite; each sibling carries a per-role `angle`; every unordered pair carries a predicted-disagreement note. Defers the four-test rule to `anti-bias-vector-composition`. |

### New schema block (`dispatch.schema.yml`)
On a step (n≥2) and on `subagent_strategy`:
```
anti_bias:
  axis: <methodology|source-corpus|attack-vector|temporal-prior|composite:...>
  angles: [ {ref: <role/sibling id>, angle: <position on the axis>} , ... ]   # ≥2
  predicted_disagreements: [ "<a_i runs X, a_j runs Y on the [axis] axis; bias in a_i exposed by a_j>" , ... ]
  owner_ref: "anti-bias-vector-composition"
```

### New validation rules (extend the current 25)
- **R26** — a `fanout`/`dialectic`/`tournament` step, or a `subagent_strategy` with ≥2 roles,
  MUST cite `anti_bias_composition` with an `anti_bias` block. Missing → `flag`; if the route
  also claims tensioned synthesis/dissent downstream → `block` (false tension).
- **R27** — `anti_bias.axis` must be in the closed vocabulary or a `composite:` declaration
  (format-conformity check).
- **R28** — no two `angles[].angle` share a core noun phrase (clone check) → `flag`.
- **R29** — every unordered angle pair has a `predicted_disagreements` entry (evidence check) → `flag`.
- Boundary preserved: dispatch-spec ENFORCES these but cites `anti-bias-vector-composition` as
  the rule owner; it never re-states the four tests' internals (no fork).

## Part B — Technique-selection advisor (problem-shape → technique)

New input `route_shape` (declared signals) → advisor returns a `technique_recommendation`.
Companion doc `TECHNIQUE-SELECTION.md` holds the rules; the validator checks consistency.

### Problem-shape signals (the `route_shape` input)
- `solution_count`: one | few | many
- `problem_settled`: settled | contested
- `prior_artifact`: greenfield | brownfield
- `dominant_risk`: hidden-structure | survival-under-stress | anchoring | cost-tradeoff | ownership-crossing | none
- `subtask_independence`: independent | dependent
- `sibling_agents`: 0 | 1 | many

### Heuristic rule table (initial — every rule names the technique set it fires)
| When (signals) | Recommend techniques | Why |
| --- | --- | --- |
| `solution_count=many` + selection risk | `tournament` + `pareto_gate` + `recomposition_proof` | compare candidates, prove the winner recomposes |
| `problem_settled=contested` / `dominant_risk=anchoring` | `dialectic` + `anti_bias_composition` + `residue_ledger` | hold competing framings; force opposed lanes; bank residue |
| `dominant_risk=hidden-structure` | `x_ray` | surface structure before deciding |
| chosen abstraction needs cheap falsification | `toy_game` + `validation_loop` | controlled failure test before promotion |
| `sibling_agents=many` | `anti_bias_composition` (MANDATORY per R26) | n≥2 siblings must be tensioned |
| `dominant_risk=survival-under-stress` | `residuality_spec`-style stressor lens + `toy_game` | probe degradation |
| `dominant_risk=ownership-crossing` | `authority_split_gate` + boundary/evidence family | resolve who owns lifecycle/promotion |
| repeated sequence detected | `spell_candidate` | mark for Spellcraft |
| `solution_count=one` + `problem_settled=settled` | `sequence` only | no tension machinery needed (avoid decoration) |

### Advisor output (`technique_recommendation` block)
```
technique_recommendation:
  fired_rules: [ <rule ids> ]
  recommend: [ <technique ids> ]
  rationale: "<why, per fired rule>"
  status: advisory   # never overrides the operator
```

### Validator side (consistency, keeps dispatch-spec honest)
- **R30** — if a route declares `route_shape`, the cited techniques should be consistent with the
  fired rules; a contradiction (e.g. `solution_count=many` selection problem but no comparison
  technique) → `flag` with the missing technique named.
- **R31** — a route that cites tension/selection techniques MUST carry a `route_shape` rationale
  (the "rationale present" check) → else `flag`. Guards the "decorating with unused technique
  names" anti-pattern, which dispatch-spec already polices (current rule 11).

### Form of the engine — route menu (operator decision recorded)
- **A. Rule table (CHOSEN, L0):** signals → technique set. Legible, machine-checkable, matches the
  POLE "standards catalog" discipline already in the package. Lowest maintenance.
- **B. Decision tree (L1, later):** ordered questions; handles dependent signals more precisely.
  Promote only if the flat table proves insufficient.
- **C. Scored heuristic (deferred):** score every technique against signals, pick top-k. Most
  flexible, least legible/deterministic — rejected at L0 (determinism + validation cost).

## Glossary consistency note
`anti_bias_composition` reuses {methodology, source-corpus, attack-vector, temporal-prior} verbatim
from `anti-bias-vector-composition` (no drift). `route_shape` signals are new dispatch-spec terms.
