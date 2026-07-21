# Validation Experiment

- Artifact: arcana/continuation-router
- Artifact type: sigil
- Runtime: Codex CLI
- Harness owner: experiment-harness

## Goal

Validate that this sigil works against realistic low, medium, and complex tasks and produces user-facing outputs that satisfy its contract.

## Evidence Required

- Fixture inputs and expected outputs.
- Real example prompts.
- Real Codex CLI example outputs when runtime execution is enabled.
- Timestamped validation reports under `development/runs/`.
- Schema-valid route receipts for unauthorized, exactly authorized, ambiguous, repeated-fingerprint, unknown-owner, and legacy-adaptation cases.
- Semantic checks that a completed dispatch has one selected route, exact authorization when required, a joined helper, and a separate owner receipt.
- Public-boundary scanning for consuming-project vocabulary.

## Promotion Gate

This artifact is not promotion-ready until validation passes, expected outputs are inspectable, and at least one real runtime output exists when a runtime adapter is available.

The initial maintenance run may establish contract and fixture readiness without claiming live promotion. A live one-hop owner dispatch is recorded separately as operational evidence.
