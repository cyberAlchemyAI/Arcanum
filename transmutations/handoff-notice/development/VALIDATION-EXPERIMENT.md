# Validation Experiment

- Artifact: arcanum/transmutations/handoff-notice
- Artifact type: sigil
- Runtime: Codex CLI
- Harness owner: experiment-harness

## Goal

Validate that Handoff Notice can synthesize a useful product-neutral message, persist and resolve it deterministically, and preserve authority, repository, lifecycle, and delivery boundaries under realistic low, medium, and complex cases.

## Evidence Required

- Fixture inputs and expected outputs.
- Deterministic runtime tests for publish, resolve, inspect, collision handling, supersession, Git state, and failure cases.
- Real example prompts for lifecycle-owner review.
- A real user-facing result body when runtime execution is enabled.
- Timestamped validation reports under `development/runs/`.

## Promotion Gate

This artifact is not promotion-ready until deterministic validation passes, expected lifecycle outputs are inspectable, one real runtime output exists when a runtime adapter is available, and `sigil-development` reviews the final evidence.
