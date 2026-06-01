# Refine Seed Proposal: Validate Craft

## Target

`development/craft/`

## Operator Intent

Use Refine so Craft can be validated through a concrete next local sequence instead of promoting from architecture evidence alone.

## Refinement Objective

Turn the current vague next move, "validate Craft", into a governed validation route that:

1. selects the smallest coherent next validation unit,
2. uses `CRAFT-VALIDATION.md` as the review surface,
3. preserves route and owner boundaries,
4. keeps promotion, runtime integration, scoring, generated indexes, and role delegation automation deferred,
5. produces an executable next work-pack only after route-shape validation is safe.

## Source Context

| Source | Use |
| --- | --- |
| `development/craft/README.md` | Current verdict and next move. |
| `development/craft/SESSION-LEDGER.md` | Candidate seeds, current gaps, and durable state. |
| `development/craft/CRAFT-VALIDATION.md` | Current Craft validation and recomposition guide. |
| `development/craft/CRAFT-VALIDATION-EXAMPLES.yml` | Structured validation example suite. |
| `development/craft/CRAFT-PROMOTION-READINESS.md` | Promotion readiness recommendation: `defer`. |
| `development/craft/task-sessions/20260529T163804Z-NEXT-TASK-BLOCK/RESULT.md` | Evidence that Task Session cannot proceed without a concrete next work-pack task. |

## Write Scope

Allowed for this refine run:

- `development/craft/refinement-runs/20260529T164919Z-validate-craft/`

Deferred unless a later explicit work-pack authorizes mutation:

- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`
- runtime adapters,
- command routes,
- registries,
- sigils,
- spells,
- generated indexes,
- role delegation automation.

## Done Criteria

- The run folder contains the required Refine artifacts.
- `REFINE-DISPATCH.json` represents the canonical ten-stage Refine loop.
- Dispatch validation is attempted against `formulae/dispatch-spec/dispatch.schema.yml`.
- Command-route blockers are recorded exactly.
- The final result recommends a safe next route for validating Craft.

## Validation Surface

- `python3 formulae/dispatch-spec/scripts/validate-dispatch.py <REFINE-DISPATCH.json>`
- `tools/arcanum --resolve <command>` for command-backed stages.
- Manual owner-boundary review against `CRAFT-VALIDATION.md`.

## Preset

`standard`

## Research Mode

`no-research`

Rationale: validation is local-first and the current blocker is route shape/executable task selection, not external factual context.

## Planned Stage Configuration

The canonical ten-stage Refine loop is preserved:

1. Context Builder evidence baseline.
2. Invoke Define.
3. Interrogation using `refine-review`.
4. Research decision.
5. Distill.
6. Invoke Redefine / Design.
7. Interrogation using `refine-design-review`.
8. Distill Repair.
9. Invoke Plan.
10. Final Interrogation and Refine-owned synthesis.

## Expected Gate

This run is expected to block before command-backed execution because `dispatch-spec` and `runtime-handoff` do not currently resolve through `tools/arcanum`.
