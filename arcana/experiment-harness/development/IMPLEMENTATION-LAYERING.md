# Loop-First Experiment Harness Implementation Layering

## Summary

Implement the loop-first experiment harness in layers. Each layer should leave the repository in a coherent state, preserve deterministic controls, and avoid introducing live-loop blocking gates before the loop runner exists.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Outcome | Promotion Decision |
| --- | --- | --- | --- | --- |
| L0 | Can the current harness baseline stay coherent while loop architecture lands? | Stabilized controls, architecture docs, quality/anti-pattern telemetry checks. | Existing validation remains useful. | Continue if deterministic invoke controls pass. |
| L1 | Can live regimes be described durably without executing loops yet? | Regime model and invoke pilot regime files. | Live loop intent is explicit and portable. | Continue if regime files validate. |
| L2 | Can one live Codex attempt produce a complete attempt bundle? | Single-attempt loop runner. | Live evidence has a stable storage shape. | Continue if attempt bundle validates and is ignored by git. |
| L3 | Can repeated live attempts prove stability? | Pass-streak loop state and loop report. | Harness can distinguish lucky passes from stable passes. | Continue if mocked pass/fail/pass/pass behavior works. |
| L4 | Can failed attempts produce safe improvement reasoning? | Robot-talks improvement gate. | Auto-improvement has explicit argumentation. | Continue if incomplete reasoning blocks patching. |
| L5 | Can improvements be applied and reverted safely? | Patch and rollback manager. | Regressions are automatically reverted. | Continue if worse output rolls back only loop-owned edits. |
| L6 | Can `invoke` prove the full cycle? | Invoke live loops for define, design, integration, and observability. | Pilot validates loop-first harness. | Generalize if all live regimes reach two consecutive passes. |
| L7 | Can every new spell/sigil start loop-ready? | Initialization and runtime adapter updates. | Loop-first harness becomes reusable across projects. | Package when toy spell and toy sigil pass loops. |

## Phase 0: Stabilize Current Work

Goal: finish and clean the already-started Quality Bar, Anti-Pattern, and invoke live-regime groundwork.

Implementation tasks:

- Keep `run-validation-fixtures.sh` focused on deterministic controls until `loop-harness.sh` exists.
- Ensure `check-contract-output.sh`, `validate-harness.sh`, and `observe-harness.sh` are syntactically valid and tested.
- Update invoke docs to distinguish `CTRL-*` controls from `LIVE-*` loop regimes.
- Add this architecture and layering record.

Exit criteria:

- Deterministic invoke controls pass.
- Generic harness validation runs.
- Observer emits quality/anti-pattern telemetry from a temp observability directory.
- Git status contains only intentional tracked changes.

## Phase 1: Add Regime Model

Goal: define durable live regime inputs without implementing retry loops yet.

Implementation tasks:

- Add `development/regimes/<regime-id>.md` format.
- Add invoke pilot regimes:
  - `LIVE-DEFINE-001`
  - `LIVE-DESIGN-001`
  - `LIVE-DEFINE-DESIGN-001`
  - `LIVE-OBSERVABILITY-001`
- Add a parser/checker that validates required regime sections.
- Keep `EXPERIMENT-REGIMES.md` as the human-readable index.

Exit criteria:

- Regime files validate.
- Existing prompts map cleanly to regime IDs.
- No live loop behavior is required yet.

## Phase 2: Implement Single-Attempt Loop

Goal: create the attempt bundle shape and run exactly one live attempt.

Implementation tasks:

- Add `loop-harness.sh`.
- Add attempt directory creation.
- Run Codex once.
- Save prompt, output, raw log, validation JSON, and attempt report.
- Emit attempt telemetry through an observed-run or report-compatible observer path.

Exit criteria:

- One invoke live regime can run once.
- Attempt bundle is complete.
- Generated loop evidence is ignored by git.
- Validation catches empty, save-summary, and missing-section outputs.

## Phase 3: Add Stability Loop

Goal: support repeated attempts and pass streak.

Implementation tasks:

- Add `loop-state.json`.
- Track attempts, current status, pass streak, and final status.
- Stop at two consecutive passes or five attempts.
- Write `loop-report.md`.

Exit criteria:

- Mocked pass/pass succeeds.
- Mocked pass/fail/pass/pass succeeds after streak reset.
- Mocked five failures ends as fail.
- Loop report is human-readable and machine-readable.

## Phase 4: Add Robot-Talks Improvement Gate

Goal: require reasoning before auto-improvement.

Implementation tasks:

- Add `reflect-loop-attempt.sh`.
- Produce `robot-talks.md`.
- Produce `improvement-argument.md`.
- Validate the argument has failure summary, tensions found, proposed patch, why the patch should improve output, files to change, regression criteria, and rollback plan.
- Block patching if the argument is incomplete.

Exit criteria:

- Failed attempt creates robot-talks artifacts.
- Missing reasoning blocks auto-improvement.
- Robot-talks artifact is not counted as validation success without rerun.

## Phase 5: Add Patch And Rollback Manager

Goal: apply bounded improvements and revert regressions.

Implementation tasks:

- Capture patch state before edits.
- Apply auto-improvement patch.
- Run next attempt.
- Compare previous and next validation.
- Revert if worse.
- Record rollback in loop report and telemetry.

Exit criteria:

- Worse output triggers rollback.
- Better output keeps patch.
- Rollback does not touch unrelated dirty files.
- Generated outputs are never patched to force pass.

## Phase 6: Invoke Pilot End-To-End

Goal: prove the whole architecture on `invoke`.

Implementation tasks:

- Run `LIVE-DEFINE-001`.
- Run `LIVE-DESIGN-001`.
- Run `LIVE-DEFINE-DESIGN-001`.
- Run `LIVE-OBSERVABILITY-001`.
- Keep deterministic controls as baseline checks.

Exit criteria:

- Each live regime reaches two consecutive passes within five attempts.
- Observer telemetry contains required fields.
- Hook ledger records background work with `observe: false`.
- Invoke remains blocked for registry release until unimplemented `plan`, `full`, and `validate` modes exist.

## Phase 7: Generalize To All Spells And Sigils

Goal: make loop-first harness the default development path.

Design references:

- [GENERALIZATION-DESIGN.md](GENERALIZATION-DESIGN.md)
- [GENERALIZATION-IMPLEMENTATION-PLAN.md](GENERALIZATION-IMPLEMENTATION-PLAN.md)
- [GENERALIZATION-PROFILE-CONTRACT.md](GENERALIZATION-PROFILE-CONTRACT.md)
- [SIGIL-DEVELOPMENT-TEST-CASE.md](SIGIL-DEVELOPMENT-TEST-CASE.md)
- [GENERALIZATION-INTERROGATION-REVIEW.md](GENERALIZATION-INTERROGATION-REVIEW.md)

Implementation tasks:

- S1: update `init-harness.sh` to support lifecycle experiment profiles while preserving the existing `--type spell|sigil` interface.
- S1: infer `generic-spell` or `generic-sigil` from `--type`, while allowing explicit `--profile spellcraft|sigil-development` override.
- S2: generate `development/EXPERIMENT-PROFILE.md` as the durable profile boundary record.
- S2: add Spellcraft and Sigil Development starter profiles that generate lifecycle-appropriate prompts, regimes, fixtures, and validation expectations.
- S3: add profile drift validation against the target lifecycle contract's `SKILL.md` Quality Bar, Anti-Patterns, and output contract.
- S3: validate generated prompt and regime ids against the selected profile.
- S4: update runtime command adapters to expose `experiment-loop`.
- S4: update `spellcraft` and `sigil-development` planning so new artifacts initialize profile-aware loop regimes.
- S5: run the Sigil Development test case against a sandbox copy before treating the generalized profile path as reusable.
- S5: use `arcana/concept-layer-optimizer` as the first real sigil target after sandbox proof or explicit write-scope approval.
- S6: run a Spellcraft proof against a toy spell target.
- S6: document external repo installation.

Exit criteria:

- New spell/sigil harness includes profile-aware loop-ready layout.
- `development/EXPERIMENT-PROFILE.md` exists and matches generated prompts/regimes.
- Generated profiles keep Experiment Harness as mechanics owner while Spellcraft or Sigil Development remains lifecycle owner.
- External repo install exposes Codex command bridge.
- The Sigil Development test case produces a reviewable pass/flag/block report.
- At least one toy spell and one toy sigil pass live loop validation.

## Non-Regression Guardrails

- Deterministic controls remain useful and are not promoted as the main live evidence.
- Live loops must not patch generated outputs to force a pass.
- Every auto-improvement patch must have a robot-talks argument and rollback plan.
- Worse next output must revert the improvement patch.
- Hook telemetry must not trigger observation of itself.
- Generated loop evidence remains ignored by git.
