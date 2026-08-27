# Validation Experiment

- Artifact: arcana/subagent-strategy
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

## Target-Specific Regimes

- `strategy-inline-low`: no trigger, no dispatch, no ledger mutation.
- `strategy-proposal-medium`: degraded preflight, genuine tension, explicit
  confirmation stop.
- `strategy-form-version-drift-medium`: stale profile warning, non-mutating
  current-form admission, and exactly one confirmation request.
- `strategy-single-confirmation-readiness-medium`: unpooled approver and
  companion-only disagreement evidence block before the human gate; the
  repaired digest-owned sheet reaches exactly one confirmation request.
- `strategy-carried-confirmation-medium`: changed serialization bytes rerun
  readiness and both tension checks and invalidate the prior exact-sheet
  confirmation.
- `strategy-handoff-gap-complex`: an existing upstream artifact fails the
  type-owner handoff gate, so the consumer stays blocked and a declared
  feedback edge is used without spending final-approval revision capacity.
- `strategy-close-complex`: dependency graph, partial failure, final approval,
  complete closeout, and exactly two lifecycle YAML rows.

These fixtures are deterministic controls. They are not substitutes for real
runtime output bodies or registrar integration evidence.
