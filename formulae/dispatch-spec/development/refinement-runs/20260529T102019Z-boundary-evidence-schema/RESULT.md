# Refine Result: Boundary Evidence Schema

Status: flag
Preset: standard
Research: no-research

## Final Synthesis

The corrected evolution of `dispatch-spec` is a general
`boundary_evidence` schema, not a Tandem/runtime bridge. It should make
composition integrity inspectable across Arcanum routes: capability handoffs,
artifact imports, human approvals, evidence returns, memory interactions, state
writes, and promotion safety.

The smallest coherent schema unit is an optional dispatch-level
`boundary_evidence` object with five parts:

1. `boundaries`: what is crossing an ownership, artifact, evidence, state, or
   approval boundary.
2. `authority`: who owns lifecycle, execution, validation, evidence, memory,
   and promotion decisions.
3. `receipts`: what evidence must come back and where it is stored.
4. `state_namespaces`: which state roots exist and who can write them.
5. `promotion_splits`: why evidence visibility is not canonical promotion.

## Architecture

Use the architecture in `stages/06-local-architecture.md` as the schema seed.
Rename the current technique family from `Runtime Bridge And Evidence
Techniques` to `Boundary And Evidence Techniques`, and migrate runtime-specific
ids to general Arcanum boundary ids.

## Plan

Use `stages/09-local-plan.md` as the non-executed implementation plan. The next
execution route should:

- rename and de-Tandem the technique family in canonical docs;
- add optional `boundary_evidence` to `dispatch.schema.json`;
- add validator cross-reference and promotion-safety rules;
- add pass/flag/block fixtures;
- run `formulae/dispatch-spec/development/run-validation-fixtures.sh`.

## Readiness

This refinement is useful but not canonical-pass because command-backed
semantic stages did not complete through `codex-exec`. Dry-run artifacts prove
command-surface availability only. Treat the architecture and plan as local
fallback artifacts ready for human review and a later `task-session`.

## Recommended Next Routes

1. `task-session`: implement `stages/09-local-plan.md`.
2. `workflow-reflect`: inspect the repeated `codex-exec-timeout` behavior if
   canonical refine execution needs to be restored.
