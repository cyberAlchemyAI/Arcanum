# Architecture Plan: Loop-First Experiment Harness

## Architecture Intent

Make spell and sigil validation behave like a governed feedback loop:

```text
regime definition
  -> live Codex attempt
  -> output validation
  -> observability emission
  -> robot-talks improvement argument when needed
  -> bounded patch
  -> rerun
  -> rollback if worse
  -> stable pass after 2 consecutive passing attempts
```

The architecture keeps deterministic fixtures as controls. The main promotion evidence becomes live experiment loops that pass only after two consecutive successful attempts.

The system must support portable use across Arcanum and external repos, mandatory live Codex execution for promotion evidence, ignored generated run evidence, durable regime definitions, auto-improvement with explicit reasoning, rollback on regression, and hook telemetry without recursive observer loops.

## Source Contracts

| Contract ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SC-001 | `arcanum/arcana/experiment-harness/SKILL.md` | yes | Canonical sigil contract for harness behavior. |
| SC-002 | `arcanum/framework/observability/OBSERVED-RUNS.md` | yes | Run bundle lifecycle and checkpoint model. |
| SC-003 | `arcanum/framework/observability/SIGIL-OBSERVABILITY-HOOK.md` | yes | Telemetry envelope, hook ledger, loop guards. |
| SC-004 | `arcanum/arcana/robot-talks/SKILL.md` | yes | Auto-improvement reasoning uses robot-talks for audit and tension discovery, not silent implementation. |
| SC-005 | `arcanum/spells/invoke/templates/architecture/architecture.md` | yes | Architecture output structure and six-view design model. |
| SC-006 | Existing `invoke` development fixtures and prompts | yes | Pilot artifact for proving the harness. |

## View 1: Context View

Actors and systems:

- Maintainer starts an experiment loop for a spell or sigil.
- Experiment Harness owns live execution, validation, reports, loop state, and retry policy.
- Codex CLI runs the actual prompt against the artifact definition.
- Target spell or sigil provides the contract being validated.
- Signal Observer records capability telemetry after each attempt or loop summary.
- Reflection thresholds turn accumulated telemetry into `reflect-now` signals when usage, output, gap, or severe-gap thresholds are reached.
- Hook Ledger records background observer, extraction, and reflection actions with `observe: false`.
- Robot-Talks provides structured improvement reasoning when attempts fail.
- Git worktree is the rollback boundary for auto-improvement patches.

Ownership boundary:

- Harness owns experiment mechanics.
- Target spell or sigil owns domain behavior.
- Observer owns telemetry.
- Robot-talks owns reasoning and tension discovery.
- The loop may apply patches, but every patch must be justified and reversible.

## View 2: High-Level Structure View

Major parts:

- Regime Registry reads `development/regimes/<regime-id>.md` and exposes prompt inputs, pass criteria, expected sections, attempt limits, and artifact references.
- Loop Runner executes attempts, tracks pass streak, stops after two consecutive passes or five attempts, and decides whether to retry, reflect, patch, rollback, or fail.
- Attempt Executor calls Codex CLI and saves `prompt.md`, `output.md`, raw logs, and metadata without editing generated output to force a pass.
- Validation Engine runs output shape checks, Quality Bar checks, Anti-Pattern checks, regime-specific checks, and writes `validation.json`.
- Observer Adapter emits signal-observer telemetry, records hook operation rows, and relies on dedupe to prevent duplicate observer emissions.
- Reflection Threshold Evaluator reads observability config and reflection state, then emits `usage-threshold`, `output-threshold`, `gap-threshold`, or `severe-gap` in the observer envelope when thresholds are crossed.
- Robot-Talks Improvement Gate runs after failed, partial, or blocked attempts and produces `robot-talks.md` plus `improvement-argument.md`.
- Patch And Rollback Manager captures pre-patch state, applies bounded patches, compares the next attempt against the prior attempt, and reverts if the output gets worse.

## View 3: Low-Level Components View

Planned harness components:

- `scripts/loop-harness.sh`
  - Public entrypoint for `experiment-loop`.
  - Arguments: `<artifact-path> <regime-id>`.
  - Defaults: `MAX_ATTEMPTS=5`, `PASS_STREAK=2`, `AUTO_IMPROVE=1`.

- `scripts/validate-loop-attempt.sh`
  - Validates one attempt output.
  - Uses existing `check-contract-output.sh`.
  - Adds regime-specific checks from the regime definition.

- `scripts/reflect-loop-attempt.sh`
  - Produces robot-talks discussion and improvement argument.
  - Must not apply edits directly.

- `scripts/apply-loop-improvement.sh`
  - Applies the bounded patch from the improvement argument.
  - Records changed files and rollback data.

- `scripts/rollback-loop-improvement.sh`
  - Reverts the last improvement when the next run regresses.

Artifact-local generated layout:

```text
development/experiment-loops/<regime-id>/<loop-id>/
  loop-report.md
  loop-state.json
  attempt-001/
    prompt.md
    output.md
    raw.log
    validation.json
    observer-event.json
    robot-talks.md
    improvement-argument.md
    patch.diff
    rollback.patch
    attempt-report.md
```

Artifact-local durable layout:

```text
development/regimes/
  LIVE-DEFINE-001.md
  LIVE-DESIGN-001.md
  LIVE-DEFINE-DESIGN-001.md
  LIVE-OBSERVABILITY-001.md
```

## View 4: Workflow Process View

Normal passing flow:

```text
load regime
run Codex attempt 1
validate output
observe attempt
if pass: streak = 1
run Codex attempt 2
validate output
observe attempt
if pass: streak = 2
write loop-report pass
observe loop summary
```

Failing then improving flow:

```text
run attempt
validate partial/fail/block
observe attempt
run robot-talks improvement gate
write improvement argument
capture rollback patch
apply improvement
run next attempt
compare result
if better: continue
if worse: rollback and mark regression
```

A next attempt is worse when any of these happen:

- `pass` becomes `partial`, `fail`, or `block`,
- `partial` becomes `fail` or `block`,
- `fail` becomes `block`,
- anti-pattern severity increases,
- output becomes empty or save-summary,
- required observability disappears,
- required regime sections disappear.

Stop conditions:

- `pass`: two consecutive passing attempts.
- `partial`: at least one pass, but no two-pass streak after five attempts.
- `fail`: no passing attempt after five attempts.
- `block`: fatal anti-pattern remains, Codex unavailable, telemetry cannot be recorded, or rollback fails.

## View 5: Decision Flow View

| Decision | Rule |
| --- | --- |
| Should the loop retry? | Retry while attempts are below five and pass streak is below two. |
| Should the loop auto-improve? | Yes when validation is partial, fail, or block and robot-talks can produce a bounded improvement argument. |
| Can the loop patch the target artifact? | Yes, full artifact scope is allowed, but only with an improvement argument and rollback patch. |
| Can generated outputs be patched? | No. Generated outputs are evidence, not implementation surface. |
| Can robot-talks directly implement? | No. It produces reasoning and patch rationale; patch application is separate. |
| Should the patch stay? | Only if the next attempt is not worse. |
| Should observer hook work be observed? | No. Hook operations use ledger rows with `observe: false`. |

## View 6: Dependency Interface View

Codex execution:

- Existing `run-with-codex.sh` remains the primitive.
- Loop runner may call it or use the same command shape directly.

Validation:

- Existing `check-contract-output.sh` remains the shared contract checker.
- Regime checks add expected headings and keywords per live regime.

Observability:

- Use existing `observe-harness.sh` for reports.
- For attempt-level telemetry, write a report-like machine summary or observed-run bundle that observer can consume.

Robot-talks:

- Use `robot-talks` as a required reasoning template.
- Minimum output sections: findings, tensions, improvement proposal, reasoning argument, regression criteria, rollback plan.

Rollback:

- Use non-interactive git diff/apply style.
- Capture `patch.diff` and `rollback.patch`.
- Never run destructive git commands.

## Constraints

| Constraint | Source | Impact |
| --- | --- | --- |
| Live Codex is mandatory | User decision | Missing Codex blocks loop promotion. |
| Stability requires two consecutive passes | User decision | One lucky pass is not enough. |
| Max attempts is five | User decision | Prevents runaway cost. |
| Auto-improvement can edit full artifact | User decision | Requires strong reasoning and rollback. |
| Robot-talks does not implement directly | `robot-talks` contract | Separate reasoning from patch application. |
| Hook telemetry must not self-trigger | Observability docs | Prevent infinite loops. |
| Generated evidence ignored | Harness standard | Keeps repo clean. |

## Dependency And Interface Rules

| Rule ID | Rule | Applies To | Enforcement |
| --- | --- | --- | --- |
| R-001 | Every live loop attempt must call Codex. | Loop runner | Block if Codex unavailable. |
| R-002 | Every attempt must produce real artifact output. | Attempt executor | Block empty/save-summary output. |
| R-003 | Every failed improvement must include robot-talks reasoning. | Improvement gate | Block patch application without argument. |
| R-004 | Every patch must be reversible. | Patch manager | Require rollback patch before applying. |
| R-005 | Worse next output reverts the patch. | Patch manager | Compare validation severity and anti-patterns. |
| R-006 | Observer hook operations are not capability telemetry. | Observer adapter | Always write hook rows with `observe: false`. |
| R-007 | Reflection thresholds must be emitted as observer signals. | Observer adapter | Emit threshold trigger and `reflect-now` recommendation before counter update. |
| R-008 | Generated evidence must not be committed. | Artifact layout | `.gitignore` covers loop outputs, logs, and reports. |

## Decision Log

| Decision ID | Decision | Options Considered | Reason |
| --- | --- | --- | --- |
| D-001 | Make live loops primary evidence. | Fixture-first, live-only, loop-first | Loop-first proves actual runtime behavior and stability. |
| D-002 | Keep fixtures as controls. | Delete fixtures, keep as primary, keep as controls | Controls isolate contract regressions from runtime drift. |
| D-003 | Use two consecutive passes. | One pass, two-of-three, two consecutive | Consecutive passes prove short-term stability better than one lucky run. |
| D-004 | Allow full-artifact auto-improvement. | Prompts only, validators only, full artifact | User wants the loop to improve the real artifact when needed. |
| D-005 | Require robot-talks argument before patching. | Direct patch, simple reflection, robot-talks gate | Prevents silent self-justifying edits. |
| D-006 | Roll back worse improvements. | Keep all patches, manual review, auto rollback | Protects against false progress and degraded outputs. |

## Risks

| Risk ID | Risk | Mitigation | Owner |
| --- | --- | --- | --- |
| RK-001 | Harness rewrites the artifact to satisfy weak tests. | Require regime-specific checks, robot-talks argument, and rollback comparison. | experiment-harness |
| RK-002 | Live Codex nondeterminism causes flaky promotion. | Require two consecutive passes and preserve all attempt evidence. | loop runner |
| RK-003 | Auto-improvement creates unrelated repo churn. | Patch plan must list files; generated evidence ignored; dirty worktree reported. | patch manager |
| RK-004 | Observer loop observes itself recursively. | Hook operation rows always `observe: false`; no observer on hook reflections. | observer adapter |
| RK-005 | Rollback loses user changes. | Only revert changes captured in the loop patch; detect pre-existing dirty files before patching. | patch manager |
| RK-006 | Robot-talks becomes expensive for every minor miss. | Run only after non-pass attempts, cap attempts at five. | loop runner |

## Downstream Planning Notes

- Implementation should proceed through `IMPLEMENTATION-LAYERING.md`, not a single large patch.
- `invoke` remains the pilot artifact.
- Registry release remains blocked until `plan`, `full`, and `validate` modes have their own loop evidence.

## Design Transport Notes

Carry this architecture into:

- `arcanum/arcana/experiment-harness/development/IMPLEMENTATION-LAYERING.md`,
- invoke live regime files under `arcanum/spells/invoke/development/regimes/`,
- future `spellcraft` and `sigil-development` initialization behavior.

## Gate Result

- Status: pass
- Reason: The architecture identifies source contracts, six views, component boundaries, workflow, decision rules, rollback and observability constraints, and a phased implementation plan for the loop-first experiment harness.
