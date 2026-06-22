# Refine Seed Proposal: Anti-Bias + Technique-Selection Advisor in dispatch-spec

Status: seed accepted for refinement (operator confirmed 2026-06-19; identity = validator + advisor).

## Target
`arcanum/formulae/dispatch-spec/` (SKILL.md, TECHNIQUE-CATALOG.md, dispatch.schema.yml, validator).

## Starting intent
Add anti-bias to dispatch-spec, and expand its usage by giving it heuristics/rules for
selecting techniques and methods from its catalog.

## Source context
- `dispatch-spec/SKILL.md` (current identity: validator only — "does not decide which sigils"; rules 1–25; `subagent_strategy`).
- `dispatch-spec/TECHNIQUE-CATALOG.md` (Arcanum + POLE + boundary/evidence families; no anti-bias technique; no selection guidance).
- `.claude/skills/anti-bias-vector-composition/SKILL.md` and `check-tension/SKILL.md` (the anti-bias OWNERS — four-test rule).
- `.claude/skills/domainspec-subagents-strategy` constitution (anti-bias Principle 5; routes by dispatch_type).
- Prior run `20260528T231321Z-expand-dispatch-techniques` (added the boundary/evidence VOCABULARY — this run adds SELECTION + TENSION, not more vocabulary).
- This session's research `arcanum/arcana/refine/development/refine-improvement/findings.md` (C7 anti-bias-at-spawn-gate; C8 dispatch-algebra — both promoted here from deferred).

## Write scope
dispatch-spec package only. Anti-bias is REFERENCED from anti-bias-vector-composition, not redefined.

## Done criteria
A non-executed plan that (a) adds an `anti_bias_composition` technique + enforcement rules, and
(b) adds a technique-selection advisor (problem-shape → technique), with the validator core intact.

## Preset / research
standard / research-if-gap-appears (anti-bias already owned internally — no external research gap expected).

## Decisions already taken (operator)
- Identity = **validator + advisor** (dispatch-spec may now RECOMMEND techniques, not only validate shape).
