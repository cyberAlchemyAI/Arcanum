# Arcanum Sigil: experiment harness

<!-- arcanum:capability-id experiment-harness -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command arcanum-sigil-experiment-harness -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-experiment-harness-<UTC timestamp>`.
- `capability.id`: `experiment-harness`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `experiment-harness` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `experiment-harness`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/experiment-harness/README.md

````markdown
# Experiment Harness

Experiment Harness is an Arcana sigil for giving reusable spells and sigils a repeatable development test loop.

It creates an artifact-local `development/` harness, selects realistic prompts, runs bounded native skill/subagent examples or explicit legacy CLI adapter examples, saves the real user-facing output, validates expected structure, checks the artifact's Quality Bar and Anti-Patterns, and records timestamped reports.

## Use When

- a new spell or sigil needs promotion evidence,
- a reusable artifact needs low, medium, and complex examples,
- a maintainer wants to run the next missing example output,
- native skill/subagent or explicit legacy adapter output should be captured as real validation evidence,
- an external repository wants the same testing pattern as Arcanum.

## Do Not Use When

- the task is to design the artifact contract itself,
- the artifact has no reusable behavior to validate,
- the user only wants a one-off manual review,
- live model execution would be unsafe or too expensive without explicit approval.

## Commands

```bash
arcanum/arcana/experiment-harness/scripts/init-harness.sh <artifact-path> --type spell|sigil [--profile <profile-id>]
arcanum/arcana/experiment-harness/scripts/select-prompt.sh <artifact-path> next
arcanum/arcana/experiment-harness/scripts/run-with-codex.sh <artifact-path> <example-id|next|--all>
arcanum/arcana/experiment-harness/scripts/loop-harness.sh <artifact-path> <regime-id>
arcanum/arcana/experiment-harness/scripts/validate-harness.sh <artifact-path>
arcanum/arcana/experiment-harness/scripts/report-harness.sh <artifact-path>
arcanum/arcana/experiment-harness/scripts/observe-harness.sh <artifact-path> [report-path]
```

Codex command adapters expose the same workflow through:

- `arcanum-sigil-experiment-harness`
- `experiment-next`
- `experiment-run`
- `experiment-validate`
- `experiment-observe`

`experiment-loop` is the live Codex stability loop. It uses regime definitions, repeated attempts, observability, robot-talks improvement reasoning, and rollback on regression. See [development/ARCHITECTURE.md](development/ARCHITECTURE.md).

## Experiment Profiles

Every new harness is profile-aware. `--type spell` infers `generic-spell`, and `--type sigil` infers `generic-sigil`. Lifecycle-specific profiles are available with `--profile spellcraft` and `--profile sigil-development`.

Initialization writes `development/EXPERIMENT-PROFILE.md`, profile-specific prompts, regimes, and fixtures. It blocks when the target artifact has no readable `SKILL.md` or `README.md`, because profile validation needs a contract boundary.

Validation treats missing profile metadata as a blocker and emits:

```text
PROFILE_ID=<profile-id>
LIFECYCLE_OWNER=<owner>
ARTIFACT_TYPE=<spell|sigil>
CONTRACT_PATH=<path>
PROMPT_SET=<ids>
REGIME_SET=<ids>
PROFILE_VALIDATION=pass|flag|block
```

## Closed Loop

The harness closes the development cycle with observability:

1. `run-with-codex.sh` captures real runtime output.
2. `validate-harness.sh` checks fixtures, output shape, and `SKILL.md` `<quality-bar>` / `<anti-patterns>` evidence.
3. `report-harness.sh` writes a timestamped report.
4. `observe-harness.sh` appends one signal-observer-compatible event to `.arcanum/observability/signals/sigil-invocations.jsonl` when the repository observability package exists.
5. Observer hook activity is recorded in `.arcanum/observability/hooks/hook-operations.jsonl`.
6. Reflection counters are updated for later `sigil-development` or `workflow-reflect` review.
7. Reflection thresholds from `.arcanum/observability/config.json` are evaluated during observation; threshold hits emit `usage-threshold`, `output-threshold`, `gap-threshold`, or `severe-gap` with recommendation `reflect-now`.

Set `EXPERIMENT_OBSERVE=0` when a report should not emit telemetry.

## Quality And Anti-Pattern Checks

The reusable check step reads the target artifact's `SKILL.md` when present:

- `<quality-bar>` criteria are treated as acceptance evidence and map to `pass`, `partial`, `fail`, or `not_checked`.
- `<anti-patterns>` criteria are treated as rejection evidence and surface as `anti_pattern_hits`.
- Empty outputs, save-summary outputs, unresolved placeholders, and contradictory pass-with-blocker language are flagged or blocked.
- Findings are written as machine-readable report lines so `observe-harness.sh` can emit `quality_bar_status`, `anti_pattern_hits`, and `workflow_gaps`.

## Artifact Layout

```text
<artifact-folder>/
  development/
    VALIDATION-EXPERIMENT.md
    EXPERIMENT-PROFILE.md
    VALIDATION.md
    TASK-MATRIX.md
    regimes/
    fixtures/
    example-prompts/
    example-outputs/
    example-runs/
    experiment-loops/
    runs/
    .gitignore
    run-validation-fixtures.sh
    run-example-with-codex.sh
    select-example-prompt.sh
    write-experiment-report.sh
    observe-experiment-report.sh
```

## Why This Is Arcana

The sigil coordinates lifecycle evidence across artifacts and runtimes. It does not decide what a spell or sigil should mean; it makes the development feedback loop executable and portable.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/experiment-harness/SKILL.md

````markdown
---
name: experiment-harness
description: "Use when initializing, running, looping, validating, reporting, or observing repeatable profile-aware development experiments for Arcanum spells and sigils."
argument-hint: "<init|next|run|loop|validate|report|observe> <artifact-path> [regime-id|example-id|report-path|--type spell|sigil|--profile <id>|--all]"
tier: arcana
domain: spell-sigil-validation
version: 0.1.0
origin: created to make every spell and sigil development harness executable and portable across repositories
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Sigil: Experiment Harness

<objective>
Create and operate a repeatable experiment harness for reusable spells and sigils so development evidence comes from realistic prompts, real runtime outputs, validation checks, and timestamped reports.
</objective>

<logic-type>
Arcana: lifecycle evidence orchestration for spell and sigil development.
</logic-type>

<applicability>
Use this sigil for:

- initializing a development harness for a spell or sigil,
- selecting the next missing example prompt,
- running one bounded native skill/subagent example or explicit legacy adapter example,
- running a live stability loop for one regime,
- validating fixtures, expected outputs, live outputs, and reports,
- writing a run report,
- emitting signal-observer-compatible telemetry from a run report,
- making the same harness pattern usable in external repositories.
</applicability>

<inputs>
Expected inputs:

- mode: `init`, `next`, `run`, `loop`, `validate`, `report`, or `observe`,
- artifact path,
- artifact type for init: `spell` or `sigil`,
- optional profile for init: `generic-spell`, `spellcraft`, `generic-sigil`, or `sigil-development`,
- optional example ID or `--all`,
- optional `RERUN=1` when overwriting existing example outputs is intentional,
- optional legacy runtime binary such as `CODEX_BIN` when explicitly testing a CLI adapter.
</inputs>

<process>
1. Resolve the artifact path and confirm the artifact exists and has a readable `SKILL.md` or `README.md` contract.
2. For `init`, infer a generic profile from `--type` unless `--profile` is explicit, then create `development/` directories, `EXPERIMENT-PROFILE.md`, profile prompts, regimes, fixtures, and starter validation files without overwriting existing files.
3. For `next`, select the first prompt in `development/example-prompts/` without a matching `development/example-outputs/<task-id>.output.md`.
4. For `run`, execute exactly one selected prompt through the active native skill/subagent surface unless `--all` is explicitly provided; use CLI runners only for explicit legacy adapter tests.
5. For `loop`, execute the selected regime until it reaches the required pass streak or max attempts.
6. Save the final user-facing message to generated evidence paths and raw logs to the attempt bundle.
7. Reject empty outputs and self-referential save summaries such as `Saved the output to ...`.
8. For `validate`, check profile metadata, profile prompt/regime drift, required harness files, fixture pairs, example outputs, Quality Bar evidence, Anti-Pattern hits, and latest report shape.
9. For `report`, write a timestamped report under `development/runs/`.
10. For `observe`, or after `report` when observability exists, append one JSONL signal under `.arcanum/observability/`, update reflection counters, and emit threshold-backed reflection triggers when configured thresholds are reached.
11. Return the selected artifact, command mode, files touched, validation state, telemetry state, and next missing example.
</process>

<validation-loop>
When validating saved outputs, extract the target artifact's `SKILL.md` sections:

- `<quality-bar>` defines the acceptance criteria that classify the output as `pass`, `partial`, `fail`, or `not_checked`.
- `<anti-patterns>` defines known false-success boundaries that become `anti_pattern_hits`.
- The first implementation uses structured section and keyword checks; semantic judging can be layered into the observer later.
- Report machine fields must include `QUALITY_BAR_STATUS`, `ANTI_PATTERN_HITS_JSON`, and `WORKFLOW_GAPS_JSON` when findings exist.
- Profile-aware validation must emit `PROFILE_ID`, `LIFECYCLE_OWNER`, `ARTIFACT_TYPE`, `CONTRACT_PATH`, `PROMPT_SET`, `REGIME_SET`, and `PROFILE_VALIDATION`.
</validation-loop>

<observability-loop>
The experiment harness closes the lifecycle loop by integrating with `signal-observer` and the framework observability package:

- reports become safe invocation envelopes,
- envelopes are appended to `.arcanum/observability/signals/sigil-invocations.jsonl`,
- observer hook activity is recorded under `.arcanum/observability/hooks/`,
- per-sigil and per-capability lookup indexes are rebuilt from the central ledger,
- reflection counters are updated in `.arcanum/observability/reflection-state.json`,
- configured reflection thresholds are evaluated during observation and emitted as `usage-threshold`, `output-threshold`, `gap-threshold`, or `severe-gap` with recommendation `reflect-now`,
- dedupe prevents repeated observer emissions for the same report and observer version,
- telemetry write failures never block the primary validation result.
</observability-loop>

<loop-first-architecture>
The planned promotion path is loop-first:

- live Codex regimes are primary promotion evidence,
- deterministic fixtures remain controls,
- a loop passes after two consecutive successful attempts,
- failed attempts require robot-talks improvement reasoning before auto-improvement,
- improvements must be reversible and rolled back when the next attempt is worse.

See `development/ARCHITECTURE.md` and `development/IMPLEMENTATION-LAYERING.md`.
</loop-first-architecture>

<artifact-boundary>
This sigil owns testing mechanics only. Artifact-specific meaning stays with the target spell or sigil. If the output contract is wrong, route that change through `spellcraft` or `sigil-development`.
</artifact-boundary>

<runtime-runner-contract>
Native example execution uses the active skill/subagent surface first. Legacy Codex CLI example execution is explicit adapter evidence only and uses this command shape:

```bash
codex exec \
  -C <repository-root> \
  --sandbox workspace-write \
  --output-last-message <artifact-folder>/development/example-outputs/<task-id>.output.md \
  "$(cat <artifact-folder>/development/example-prompts/<task-id>.md)"
```

Use `CODEX_BIN` when provided for a legacy adapter run. Otherwise discover `codex` from `PATH` or known local extension paths.
</runtime-runner-contract>

<quality-bar>
A successful execution must:

- create the standard harness layout for new reusable spells and sigils,
- create and validate `development/EXPERIMENT-PROFILE.md` for every initialized harness,
- preserve existing harness files unless overwrite is explicit,
- select exactly one prompt for normal runs,
- require explicit `--all` for batch model calls,
- save the real artifact response rather than a save-summary,
- write raw run logs and timestamped reports,
- emit one observer-compatible telemetry event when repository observability is available,
- report `pass`, `flag`, or `block` honestly,
- remain usable from external repositories through runtime command adapters.
</quality-bar>

<anti-patterns>
Avoid:

- treating a well-written contract as validation evidence without examples,
- silently running every prompt,
- overwriting outputs without `RERUN=1`,
- making artifact-local wrappers authoritative over the canonical sigil,
- validating only markdown presence while ignoring output shape,
- accepting a legacy harness without profile metadata as valid,
- embedding invoke-specific assumptions in the generic harness.
</anti-patterns>

<output-contract>
Return:

```markdown
## Experiment Harness Result

- Mode: init | next | run | loop | validate | report | observe
- Artifact: <path>
- Artifact type: spell | sigil | unknown
- Profile: <profile-id | unknown>
- Selection: <regime-id | task-id | none | not applicable>
- Output: <path | none | not applicable>
- Report: <path | none | not applicable>
- Validation: pass | flag | block | not run
- Profile validation: pass | flag | block | not run
- Observation: recorded | skipped | failed
- Next unrun: <task-id | none | unknown>
```
</output-contract>

````
