# Experiment Harness Standard

Use this standard to make validation experiments repeatable for every Arcanum spell and sigil.

The goal is to turn each capability into a small, inspectable test harness: realistic tasks go in, user-facing outputs come out, and promotion decisions are based on evidence rather than contract prose alone.

## Required Layout

Every reusable spell or sigil that is being promoted should use this development layout:

```text
<artifact-folder>/
  development/
    VALIDATION-EXPERIMENT.md
    VALIDATION.md
    TASK-MATRIX.md                  optional until multiple templates/modes exist
    fixtures/
      <fixture-id>.md
      <fixture-id>.expected.md
      <fixture-id>.<artifact>.md     optional real output artifact
    example-prompts/
      <task-id>.md                  generated or hand-authored prompts
    example-outputs/
      <task-id>.output.md           live or dry-run user-facing outputs
    example-runs/
      <timestamp>-<task-id>.log      live command logs
    runs/
      <timestamp>.md                validation runner reports
    .gitignore                      ignores generated outputs, logs, and reports
    run-validation-fixtures.sh
    write-experiment-report.sh
    observe-experiment-report.sh
```

For small artifacts, `TASK-MATRIX.md`, `example-prompts/`, and `example-outputs/` may be omitted until the artifact has more than one mode, template family, or task class. `VALIDATION-EXPERIMENT.md`, `VALIDATION.md`, fixtures, and a runner are still required for promotion.

Generated runtime evidence under `example-outputs/`, `example-runs/`, and `runs/` should be ignored by default. Promote durable examples into `fixtures/` or another explicitly versioned evidence folder when they become part of the artifact contract.

When `.arcanum/observability/` exists in the repository, reports should emit one signal-observer-compatible event to `.arcanum/observability/signals/sigil-invocations.jsonl`. This closes the loop from experiment evidence to reflection counters without committing generated logs or model outputs.

Validation should use the target artifact's own `SKILL.md` contract when available. `<quality-bar>` defines acceptance evidence. `<anti-patterns>` defines known false-success boundaries. The harness records those findings as `QUALITY_BAR_STATUS`, `ANTI_PATTERN_HITS_JSON`, and `WORKFLOW_GAPS_JSON` so telemetry can distinguish a real pass from a polished-looking violation.

## Required Evidence Types

| Evidence | Purpose | Required For Promotion |
| --- | --- | --- |
| Task matrix | Lists realistic low, medium, and complex tasks by mode, template, or capability class. | Required when the artifact has multiple modes/templates or a reusable template surface. |
| Fixture input | Captures one realistic request and input state. | Yes. |
| Expected output | Shows the user-facing result shape before live execution exists. | Yes. |
| Real artifact output | Contains the actual spec, design, research brief, handoff, telemetry, or other deliverable the user would inspect. | Required when the artifact claims to produce a document or structured handoff. |
| Live example output | Captures a real run through Codex, Claude, GitHub Copilot, or another runtime. | Required before registry release when a runtime adapter exists. |
| Runner report | Records pass, flag, or block with checked fixtures and artifacts. | Yes. |

## Runner Requirements

Each artifact-local runner should:

1. Validate contract files exist.
2. Validate fixture files exist.
3. Validate expected outputs contain the artifact's real output contract.
4. Reject save-summary outputs such as `Saved the output to ...` when a real result body is required.
5. Check the artifact's Quality Bar criteria and record `pass`, `partial`, `fail`, or `not_checked`.
6. Check the artifact's Anti-Patterns and record any hits as validation flags or blocks.
7. Validate mode-specific gates and known negative cases.
8. Validate integration handoffs when one stage consumes another stage's output.
9. Write a timestamped report under `development/runs/`.
10. Exit non-zero on any failed check.

The runner should not silently run expensive live AI calls. Live runtime execution must be explicit through a separate script or flag.

## Prompt Runner Requirements

When a runtime adapter exists, provide a bounded example runner that:

- selects exactly one prompt by task ID, template plus complexity, or `next`,
- supports explicit batch mode only through `--all`,
- writes the final runtime response to `development/example-outputs/<task-id>.output.md`,
- writes raw logs to `development/example-runs/`,
- skips existing outputs unless `RERUN=1` or an equivalent explicit override is set,
- validates that saved output is the actual artifact body, not a summary of having saved it.

## Native Runner Standard

When the active agent surface supports native skills or subagents, the bounded runner should use that surface first and return a receipt with artifacts, validation, observer status, blockers, and handoff notes.

## Legacy Codex CLI Runner Standard

When Codex CLI is explicitly selected as a legacy adapter test, the bounded runner may use `codex exec`.

Recommended command shape:

```bash
codex exec \
  -C <repository-root> \
  --sandbox workspace-write \
  --output-last-message <artifact-folder>/development/example-outputs/<task-id>.output.md \
  "$(cat <artifact-folder>/development/example-prompts/<task-id>.md)"
```

Runner rules:

- Use `CODEX_BIN` when provided.
- Fall back to `command -v codex`.
- Optionally check known local install paths, such as VS Code extension paths.
- Do not assume every installed `codex exec` supports top-level CLI flags. Check `codex exec --help` before adding flags.
- Do not pass unsupported approval flags to `codex exec`; keep approval/sandbox behavior explicit and version-compatible.
- Write stdout/stderr logs under `development/example-runs/`.
- Validate the saved output after Codex returns.
- Fail if the output is missing, empty, self-referential, or lacks the artifact's required result shape.
- Skip existing outputs unless `RERUN=1` or an equivalent explicit override is set.

Example wrapper behavior:

```text
run-example-with-codex.sh sigil-medium
run-example-with-codex.sh sigil medium
run-example-with-codex.sh next
RERUN=1 run-example-with-codex.sh sigil-medium
run-example-with-codex.sh --all
```

Batch mode must always be explicit because it starts one Codex run per prompt.

## Artifact-Specific Validators

Every artifact type should define checks for what "real output" means.

Examples:

| Artifact Type | Minimum Real Output Checks |
| --- | --- |
| Spell | `Invoke Result` or spell result, phases, gates, handoff artifacts, next route. |
| Sigil | result contract, inputs, outputs, quality bar, anti-patterns, observability/reflection route when reusable. |
| Research | claims, evidence, conflicts, gaps, verdict/gate result. |
| Architecture | source contracts, six views, dependency/interface rules, decision log, risks, downstream notes, gate result. |
| Implementation plan | source design refs, tasks or waves, gates, blockers, validation plan. |
| Work-pack | objective, complexity, tasks/waves, traceability links, blockers, closure strategy. |
| Observability | signal definitions, emission points, storage path, reflection trigger, privacy/safety notes. |

## Quality Bar And Anti-Patterns

The generic harness check is intentionally conservative. It does not prove deep semantic correctness by itself; it catches common contract violations that should never pass quietly:

- missing or empty artifact output,
- self-referential save summaries instead of the artifact body,
- unresolved placeholders or TODO markers,
- `pass` status paired with missing-required or blocker language,
- missing Quality Bar or Anti-Pattern sections in reusable artifact contracts.

Artifact-specific runners should add deeper checks for phase rules. For example, `invoke define` checks goal, scope, missing input, glossary, and transport evidence; `invoke design` checks source contracts, views, risks, dependency/interface notes, and handoff boundaries; the combined define-to-design experiment checks that design consumes define outputs without inventing upstream authority.

## Generalization Workflow

Use this sequence for any new or revised spell/sigil:

1. Create or update the artifact contract.
2. Add `development/VALIDATION-EXPERIMENT.md`.
3. Add realistic fixtures and expected outputs.
4. Add a runner that checks contract gates and output shape.
5. Add a task matrix when the artifact has multiple modes/templates or task classes.
6. Add generated prompts when runtime execution should be sampled.
7. Add a bounded runtime runner when a runtime adapter exists. For Codex, use the Codex CLI runner standard above.
8. Run the harness and save the timestamped report.
9. Update `development/VALIDATION.md` with the latest report and verdict.
10. Only then promote the artifact or update registry entries.

## Promotion Rule

An artifact is not registry-ready when it only has passing markdown links or a well-written contract.

It is registry-ready when:

- contract validation passes,
- realistic fixtures pass,
- real output artifacts are inspectable,
- integration handoffs pass when applicable,
- live runtime examples pass when a runtime adapter exists,
- observability or reflection expectations are documented,
- the latest validation report is linked from `development/VALIDATION.md`.
