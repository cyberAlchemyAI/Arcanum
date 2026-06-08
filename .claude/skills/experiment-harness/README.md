# Experiment Harness

Experiment Harness is an Arcana sigil for giving reusable spells and sigils a repeatable development test loop.

It creates an artifact-local `development/` harness, selects realistic prompts, runs bounded native skill/subagent examples or explicit legacy runtime examples, saves the real user-facing output, validates expected structure, checks the artifact's Quality Bar and Anti-Patterns, and records timestamped reports.

## Use When

- a new spell or sigil needs promotion evidence,
- a reusable artifact needs low, medium, and complex examples,
- a maintainer wants to run the next missing example output,
- native skill/subagent output or explicit legacy runtime output should be captured as real validation evidence,
- an external repository wants the same testing pattern as Arcanum.

## Do Not Use When

- the task is to design the artifact contract itself,
- the artifact has no reusable behavior to validate,
- the user only wants a one-off manual review,
- live model execution would be unsafe or too expensive without explicit approval.

## Scripts

```bash
arcanum/arcana/experiment-harness/scripts/init-harness.sh <artifact-path> --type spell|sigil [--profile <profile-id>]
arcanum/arcana/experiment-harness/scripts/select-prompt.sh <artifact-path> next
arcanum/arcana/experiment-harness/scripts/run-with-codex.sh <artifact-path> <example-id|next|--all> # legacy Codex CLI adapter
arcanum/arcana/experiment-harness/scripts/loop-harness.sh <artifact-path> <regime-id>
arcanum/arcana/experiment-harness/scripts/validate-harness.sh <artifact-path>
arcanum/arcana/experiment-harness/scripts/report-harness.sh <artifact-path>
arcanum/arcana/experiment-harness/scripts/observe-harness.sh <artifact-path> [report-path]
```

Codex discovers this capability as a repo skill when the folder is exposed at:

```text
.agents/skills/experiment-harness -> ../../arcana/experiment-harness
```

Invoke it explicitly by name (`experiment-harness`), or let the host runtime select it implicitly when the request matches the skill description. Legacy `.codex/commands/experiment-*` files are compatibility adapters, not the canonical skill surface.

`loop-harness.sh` is the live stability loop. It uses regime definitions, repeated attempts, observability, improvement reasoning, and rollback on regression. See [development/ARCHITECTURE.md](development/ARCHITECTURE.md).

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

1. Native skill/subagent execution is preferred for real runtime output. `run-with-codex.sh` remains a legacy Codex CLI adapter: it stores Codex's `--output-last-message` in `development/example-runs/` first, then preserves a valid artifact body written to `development/example-outputs/` instead of letting a final "Done" summary overwrite it.
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
- Empty outputs, save-summary outputs, unresolved placeholders, contradictory pass-with-blocker language, and last-message summaries that replace artifact bodies are flagged or blocked.
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
