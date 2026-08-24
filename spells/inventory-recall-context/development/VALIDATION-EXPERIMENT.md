# Validation Experiment

- Artifact: spells/inventory-recall-context
- Artifact type: spell
- Runtime: Codex CLI
- Harness owner: experiment-harness

## Goal

Validate that this spell works against realistic low, medium, and complex tasks and produces user-facing outputs that satisfy its contract.

For L0, also replay the frozen `L0-SCENARIOS.json` contract: positive,
stale, missing, contradictory, unsafe, over-budget, and blocked-index. Only the
positive case may expose an injectable pack handle.

## Evidence Required

- Fixture inputs and expected outputs.
- Real example prompts.
- Real Codex CLI example outputs when runtime execution is enabled.
- Timestamped validation reports under `development/runs/`.
- Digest-bound receipts from the future L0 runtime and protected-path no-write checks.

## Promotion Gate

This artifact is not promotion-ready until validation passes, expected outputs are inspectable, and at least one real runtime output exists when a runtime adapter is available.

Scenario-contract validation alone proves fixture completeness, not runtime behavior.
