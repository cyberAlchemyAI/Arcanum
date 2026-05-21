# Loop-First Experiment Harness Phase TODO

This TODO tracks implementation and validation work for each phase. Lessons from one phase should update later phase tasks before implementation continues.

## Phase 0: Stabilize Current Work

- [x] Keep deterministic invoke controls runnable while loop architecture lands.
- [x] Add architecture and implementation layering records.
- [x] Add Quality Bar and Anti-Pattern telemetry checks.
- [x] Add invoke experiment regimes index.
- [ ] Resolve the known placeholder finding in `architecture-complex.output.md`.

## Phase 1: Regime Model

- [x] Add `development/regimes/` layout.
- [x] Add `validate-regime.sh`.
- [x] Add invoke pilot regime files.
- [x] Validate regime prompt mappings.
- [ ] Extend `init-harness.sh` with starter regime files for new artifacts.

## Phase 2: Single-Attempt Loop

- [x] Add `loop-harness.sh`.
- [x] Add attempt bundle creation.
- [x] Add Codex execution path.
- [x] Add mock execution path for deterministic phase gates.
- [x] Add attempt validation JSON.
- [x] Add attempt report and observer-event JSON.

## Phase 3: Stability Loop

- [x] Add `loop-state.json`.
- [x] Track attempts and pass streak.
- [x] Stop on two consecutive passing attempts.
- [x] Stop at five attempts by default.
- [x] Write loop report.
- [ ] Add richer status scoring for semantic quality once observer judging exists.

## Phase 4: Robot-Talks Improvement Gate

- [x] Add `reflect-loop-attempt.sh`.
- [x] Produce `robot-talks.md`.
- [x] Produce `improvement-argument.md`.
- [x] Include failure summary, tensions, proposed patch, rationale, files, regression criteria, and rollback plan.
- [ ] Replace deterministic reflection with Codex/robot-talks subagent support when runtime delegation is available.

## Phase 5: Patch And Rollback Manager

- [x] Add `apply-loop-improvement.sh`.
- [x] Add `rollback-loop-improvement.sh`.
- [x] Support no-op improvements safely.
- [x] Roll back applied patch when the next attempt regresses.
- [ ] Add dirty-file ownership guard before applying patches to real artifacts.

## Phase 6: Invoke Pilot End-To-End

- [x] Add invoke live regime definitions.
- [x] Run invoke loops with mock outputs for phase-gate validation.
- [ ] Run real Codex loops for `LIVE-DEFINE-001`.
- [ ] Run real Codex loops for `LIVE-DESIGN-001`.
- [ ] Run real Codex loops for `LIVE-DEFINE-DESIGN-001`.
- [ ] Run real observability loop using a completed live loop report.

## Phase 7: Generalize To All Spells And Sigils

- [x] Design the shared lifecycle experiment profile boundary.
- [x] Plan Spellcraft and Sigil Development integration layers.
- [x] Define Sigil Development as the first generalized harness test case.
- [x] Interrogate the generalization plan and close resolvable blockers.
- [x] Fill design gaps with a generalized profile contract.
- [x] Refresh implementation plan around the profile contract.
- [x] S1: update `init-harness.sh` to support `--profile` while preserving `--type spell|sigil`.
- [x] S1: block invalid profile/type combinations.
- [x] S2: generate `development/EXPERIMENT-PROFILE.md` during initialization.
- [x] S2: generate profile starter prompts, fixtures, and regimes for `generic-sigil` and `sigil-development`.
- [x] S2: generate profile starter prompts, fixtures, and regimes for `generic-spell` and `spellcraft`.
- [x] S3: add profile drift validation against target lifecycle contracts.
- [x] S3: validate generated prompt and regime ids against the selected profile.
- [x] S3: emit `PROFILE_VALIDATION` and profile report fields.
- [x] S4: update runtime command adapters to expose `experiment-loop`.
- [x] S4: update `spellcraft` and `sigil-development` lifecycle plans.
- [x] S5: run the Sigil Development test case against a sandbox copy of a target sigil.
- [x] S6: select a toy spell target for the Spellcraft proof.
- [x] S6: validate a toy spell loop.
- [x] S6: validate a toy sigil loop.
