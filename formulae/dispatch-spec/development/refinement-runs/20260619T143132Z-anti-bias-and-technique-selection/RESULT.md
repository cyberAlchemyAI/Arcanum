# Refine Result: dispatch-spec anti-bias + technique-selection advisor

Status: flag (refined proposal + non-executed plan; no dispatch-spec files mutated — refine
authored a design/plan, the dispatch-spec dev cycle owns the mutation).

## Final Synthesis
dispatch-spec becomes **validator + advisor** (operator decision). Two additive capabilities,
the validator core untouched:

1. **Anti-bias as an enforced tension contract** — a new `anti_bias_composition` technique +
   schema `anti_bias` block + rules R26–R29, all REFERENCING `anti-bias-vector-composition`
   (no redefinition). Closes the gap that `subagent_strategy` sibling roles were never forced to
   be tensioned. (Promotes this session's C7 from deferred.)
2. **Technique-selection advisor** — a `route_shape` input → `technique_recommendation` output,
   backed by a rule table in `TECHNIQUE-SELECTION.md`, plus consistency rules R30–R31 that flag
   routes whose cited techniques contradict their problem-shape or lack rationale. (Promotes C8.)

Engine form chosen: **rule table (L0)**; decision-tree deferred to L1; scored-heuristic rejected.

## Why this shape
- Keeps dispatch-spec's "standards catalog" discipline (the rule table is the same shape as the
  POLE technique family already in the package).
- Honors C7's "borrow discipline, not form": enforce + reference, don't fork the anti-bias rule.
- Guards dispatch-spec's own anti-pattern (techniques cited but unused) via R31 rationale-present.

## Claim <= proof
Every rule references an existing owner/section; the anti_bias axis vocabulary is reused verbatim
from anti-bias-vector-composition; the advisor never overrides the operator (status: advisory).

## Recommended Next Route
`task-session` on PLAN.md, starting **T-AB1→T-AB3 (L0 anti-bias contract)** — additive, lowest
risk, and the dependency floor for the advisor. Then L1 (T-SEL1–T-SEL4). Ownership-boundary review
before L1 closes (dispatch-spec technique-advice vs subagents-strategy type-routing).

## Deferred
Decision-tree engine (option B) and scored-heuristic (option C); see PLAN L2.
