# Non-executed Plan: dispatch-spec anti-bias + selection advisor

Owner: dispatch-spec maintainer. Anti-bias rule owner stays `anti-bias-vector-composition`.
Layered by trust+dependency. NOT executed by refine — handed off to task-session.

## L0 — Anti-bias tension contract (additive, lowest risk)
- **T-AB1** Add `anti_bias_composition` to `TECHNIQUE-CATALOG.md` (Arcanum family).
  Verify: catalog lists it with the validation expectation; cites anti-bias-vector-composition.
- **T-AB2** Extend `dispatch.schema.yml` with the `anti_bias` block on steps + `subagent_strategy`.
  Verify: schema accepts the block; rejects an axis outside the closed vocabulary.
- **T-AB3** Add rules R26–R29 to `SKILL.md` + `validate-dispatch.py`; add 2 fixtures
  (tensioned-pass, untensioned-flag). Verify: `run-validation-fixtures.sh` → pass vs flag/block.

## L1 — Selection advisor (depends on L0 vocabulary)
- **T-SEL1** Author `TECHNIQUE-SELECTION.md` with the rule table (problem-shape → techniques).
  Verify: every catalog technique is either in a rule or marked non-selectable (no orphans).
- **T-SEL2** Add `route_shape` input + `technique_recommendation` output to `SKILL.md` contract
  and schema. Verify: a declared `route_shape` produces a recommendation block.
- **T-SEL3** Add R30 (consistency) + R31 (rationale-present) to validator + fixtures.
  Verify: a many-solutions route with no comparison technique → `flag` naming the gap.
- **T-SEL4** Update `SKILL.md` identity line: "validates route shape AND advises technique
  selection"; update Purpose + "does not decide which sigils" caveat (sigil choice still not owned;
  TECHNIQUE choice now advised). Verify: identity text is internally consistent.

## L2 — Decision-tree form (only if the flat table proves insufficient)
- **T-SEL5 (deferred)** Promote rule table → decision tree (route-menu option B). Gate: evidence
  that flat signals mis-fire on dependent cases.

## Validation strategy
Each task ships a fixture or reviewable check (above). Promotion L0→L1→L2 requires the prior
layer's fixtures green.

## Residue (named owners)
- Anti-bias DEFINITION stays in `anti-bias-vector-composition`; dispatch-spec only enforces +
  references. If the four-test rule changes there, R26–R29 inherit it. — Owner: anti-bias-vector-composition.
- Selection rule table can drift from the catalog; T-SEL1's orphan check is the guard. — Owner: dispatch-spec maintainer.
- Overlap with the subagents-strategy ROUTER (routes by dispatch_type) vs dispatch-spec
  (advises TECHNIQUE within a route): keep distinct levels — type-routing ≠ technique-selection. — Owner: ownership-boundary review.
- Scored-heuristic engine (option C) deferred; revisit only if both table and tree are insufficient. — Owner: dispatch-spec maintainer.
