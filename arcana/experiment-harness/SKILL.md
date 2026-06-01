---
name: experiment-harness
description: "Use when initializing, running, looping, validating, reporting, or observing repeatable profile-aware development experiments for Arcanum spells and sigils through native skill/subagent execution or explicit legacy runtime adapters."
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
- running one bounded native skill/subagent or explicit legacy runtime example,
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
4. For `run`, execute exactly one selected prompt through the native skill/subagent surface unless `--all` is explicitly provided. Use CLI adapters only when explicitly selected as legacy runtime tests.
5. For `loop`, execute the selected regime until it reaches the required pass streak or max attempts.
6. Save the runtime's final user-facing artifact body to generated evidence paths and raw logs to the attempt bundle.
7. Capture `--output-last-message` to a sidecar file first. If the nested agent writes the artifact body directly to the expected output path, preserve that file; if it does not, promote the sidecar only when it is a valid artifact body.
8. Reject empty outputs and self-referential save summaries such as `Saved the output to ...`.
9. For `validate`, check profile metadata, profile prompt/regime drift, required harness files, fixture pairs, example outputs, Quality Bar evidence, Anti-Pattern hits, and latest report shape.
10. For `report`, write a timestamped report under `development/runs/`.
11. For `observe`, or after `report` when observability exists, append one JSONL signal under `.arcanum/observability/`, update reflection counters, and emit threshold-backed reflection triggers when configured thresholds are reached.
12. Return the selected artifact, command mode, files touched, validation state, telemetry state, and next missing example.
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
Native example execution uses the active agent skill/subagent surface first. The runner must return an artifact body plus a receipt with artifacts, validation, observer status, blockers, and handoff notes.

Legacy Codex CLI example execution is explicit adapter evidence only and uses this command shape:

```bash
codex exec \
  -C <repository-root> \
  --sandbox workspace-write \
  --output-last-message <artifact-folder>/development/example-runs/<run-id>.last-message.md \
  "$(cat <artifact-folder>/development/example-prompts/<task-id>.md)"
```

The runner then chooses the evidence body:

1. Prefer `<artifact-folder>/development/example-outputs/<task-id>.output.md` when the nested agent wrote a valid artifact result body there.
2. Otherwise copy the sidecar last-message file into the output path only when the sidecar is itself a valid artifact result body.
3. Block when both paths are empty, save-summaries, or lack a recognizable result heading.

Use `CODEX_BIN` when provided. Otherwise discover `codex` from `PATH` or known local extension paths.
</runtime-runner-contract>

<quality-bar>
A successful execution must:

- create the standard harness layout for new reusable spells and sigils,
- create and validate `development/EXPERIMENT-PROFILE.md` for every initialized harness,
- preserve existing harness files unless overwrite is explicit,
- select exactly one prompt for normal runs,
- require explicit `--all` for batch model calls,
- save the real artifact response rather than a save-summary,
- preserve artifact-file output when the nested agent writes it before returning a final summary,
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
