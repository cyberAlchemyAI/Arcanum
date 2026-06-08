# Validation Experiment

- Artifact: `<artifact-path>`
- Artifact type: `<spell|sigil>`
- Runtime: Codex CLI
- Harness owner: `experiment-harness`

## Goal

Validate the artifact against realistic low, medium, and complex tasks using fixtures, expected outputs, real runtime outputs, and timestamped reports.

## Evidence Required

- Fixture inputs and expected outputs.
- Example prompts.
- Real Codex CLI outputs when a runtime adapter exists.
- Validation reports under `development/runs/`.

## Promotion Gate

The artifact is promotion-ready only when validation passes and the latest report links to inspectable evidence.
