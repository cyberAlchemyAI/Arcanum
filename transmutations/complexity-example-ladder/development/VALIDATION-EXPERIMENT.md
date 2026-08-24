# Validation Experiment

- Artifact: arcanum/transmutations/complexity-example-ladder
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

## Promotion Gate

This artifact is not promotion-ready until validation passes, expected outputs are inspectable, and at least one real runtime output exists when a runtime adapter is available.
