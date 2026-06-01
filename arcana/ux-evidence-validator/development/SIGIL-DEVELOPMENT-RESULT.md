# Sigil Development Result: UX Evidence Validator

Verdict: seed package created.

## Summary

The UX Playwright evidence research was moved out of the dispatch-spec development lane and into a dedicated Arcana sigil seed at `arcana/ux-evidence-validator`.

The sigil remains in development. It owns the evidence model, claim classes, validator contract, fixture route, telemetry shape, and promotion guardrails. It does not yet include executable Playwright validator code or calibrated fixture output.

## Files Added Or Moved

| Path | Purpose |
| --- | --- |
| `arcana/ux-evidence-validator/README.md` | Human-facing sigil overview. |
| `arcana/ux-evidence-validator/SKILL.md` | Seed execution contract. |
| `arcana/ux-evidence-validator/development/WORK-PACK.md` | Development route and SWUs. |
| `arcana/ux-evidence-validator/development/EXPERIMENT-PROFILE.md` | Experiment Harness profile. |
| `arcana/ux-evidence-validator/development/example-prompts/` | Starter promotion examples. |
| `arcana/ux-evidence-validator/templates/usage-telemetry.md` | Usage telemetry shape. |
| `arcana/ux-evidence-validator/development/UX-*.md` | Research outputs from the task-session run. |
| `arcana/ux-evidence-validator/development/UX-EVIDENCE-REFERENCE-CARDS.yml` | Evidence cards from the research run. |
| `arcana/ux-evidence-validator/development/ux-playwright-evidence-research.dispatch.json` | Dispatch route from the research run. |
| `arcana/ux-evidence-validator/development/task-sessions/20260601T141642Z-ux-playwright-evidence-research/` | Research task-session receipt. |

## Observer Pass

Observer pass: local fallback.

Findings:

- The sigil should be Arcana, because it governs cross-source evidence, browser validation, calibration, residues, and promotion boundaries.
- The sigil must remain seed status until fixture and Playwright execution evidence exist.
- The next valuable work is fixture corpus implementation, not validator code first.

## Validation

Checks run:

- evidence-card YAML parsed with 25 cards,
- dispatch JSON parsed,
- dispatch route validated with `formulae/dispatch-spec/scripts/validate-dispatch.py`,
- stale old-path references checked,
- diff whitespace checked.
- artifact constitution validation passed with existing generated-artifact warnings only.

## Next Lifecycle Step

Run `UEV-SWU-002`: implement the fixture corpus from `development/UX-PLAYWRIGHT-FIXTURE-PLAN.md`.
