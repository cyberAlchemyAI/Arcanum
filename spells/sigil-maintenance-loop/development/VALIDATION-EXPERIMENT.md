# Validation Experiment

- Artifact: arcanum/spells/sigil-maintenance-loop
- Artifact type: spell
- Runtime: Codex CLI
- Harness owner: experiment-harness

## Goal

Validate that `sigil-maintenance-loop` is a complete Spellcraft composition and
that every maintenance run performs read-only, machine-index-first Inventory
exploration before reflection without weakening the mutation approval gate.

## Evidence Required

- Fixture inputs and artifact-specific expected outputs.
- Real example prompts covering relevant matches, no matches, fallback,
  unavailable Inventory, insufficient signal, and rejected approval.
- Real native-agent outputs when runtime execution is enabled.
- Timestamped validation reports under `development/runs/`.

## Promotion Gate

This artifact is not promotion-ready until structural validation passes,
expected outputs are inspectable, and at least one real runtime output proves
the automatic Inventory boundary when a native runtime is available.
