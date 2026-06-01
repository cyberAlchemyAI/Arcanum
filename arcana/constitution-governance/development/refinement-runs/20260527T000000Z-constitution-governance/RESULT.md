# Refine Result: Constitution Governance

## Final Synthesis

The design concern is valid: a single bloated constitution can lose force because agents will either load too much context or fail to notice the rules that matter. Constitutions should stay modular and behave as pattern enforcers for artifact structure and form.

Context Builder should select relevant constitution material before a task. It should not own composition or enforcement. Constitution Governance owns the missing middle: selection interpretation, composition packs, precedence/conflict handling, validator mapping, split/debloat decisions, and promotion readiness.

## Status

Pass with validation gaps.

## Recommended Next Routes

1. `experiment-harness`: add passing/failing fixtures for validation adapter behavior.
2. `decision-gate`: decide whether rendering rules remain in Artifact Constitution or split into a Visual Artifact Constitution.
3. `sigil-runtime-installer`: install a command surface once fixtures pass.
