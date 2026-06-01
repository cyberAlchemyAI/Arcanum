# Durable Arcanum Runtime Interface: Skill-Contract Refined Handoff

## Summary

This run re-executes the refinement loop from the current Codex session while preserving the output contracts of the Arcanum skills:

- Context Builder produced a `Context Pack Summary`.
- Invoke stages produced `Invoke Result` artifacts.
- Interrogation stages produced `Structured Interview Result` artifacts.
- Distill stages produced `Distill Result` artifacts.
- The schema-discipline refresh incorporated `knowledge-taxonomy` as a precedent for lightweight field tiers, inline enums, stable ids/paths, provenance, validation grades, and shell/`jq` checks.
- The command artifact reproduction refresh separates runtime transport proof from UI/IDE-like command artifact proof.
- The single-command refresh collapses execution into `tools/arcanum` while preserving runtime adapters as the extension boundary.
- The install-selection refresh makes default runtime adapter selection an Arcanum installation concern and adds a post-install interchange surface.

The refined design is to add a generic durable runtime layer shared by refine, task-session, and future Arcanum orchestrators:

```text
orchestrator -> async task handoff -> tools/arcanum -> selected adapter
```

Codex is not the runtime model. Codex is one adapter, `codex-exec`.

The runtime package now also acts as the first proving ground for schema discipline across Arcanum and CyberAlchemy. This means runtime artifacts should be mechanically checkable without adding a broad schema framework.

## Proposed Runtime Architecture

### Orchestrator

Owns workflow meaning and final synthesis.

Examples:

- `refine`: loop topology, seed proposal, stage manifest, evidence index, final synthesis.
- `task-session`: selected task/SWU, safety gates, context pack, write scope, done criteria, validation, work-pack synchronization.

### Async Task Handoff

Immutable request artifact. Recommended name:

```text
RUNTIME-HANDOFF.md
```

It records:

- objective,
- inputs,
- allowed write scope,
- expected outputs,
- validation,
- blocked conditions,
- adapter preference,
- nesting policy.

### Runtime Translator

Converts generic handoff into adapter-specific execution input.

Examples:

- build a Codex prompt for `codex-exec`,
- build a no-op validation request for `dry-run`,
- future shell/local-agent adapters.

### Runtime Executor

`tools/arcanum` owns durable run lifecycle when runtime envelope mode is enabled:

- create run folder,
- write `RUN.json`,
- write `STATUS.json`,
- append `events.jsonl`,
- call translator,
- invoke adapter,
- write the requested command output path,
- record blocked/failure evidence.

The former `tools/arcanum-runtime-run` should no longer be the conceptual runtime model. It may remain only as a short-lived compatibility shim.

### Installed Runtime Selection

Installation separates command surface from runtime adapter:

- command surface: `--runtime codex|none`,
- default adapter: `--default-adapter <adapter-id>`.

Installed repositories should record non-secret runtime defaults in:

```text
.arcanum/runtime/config.json
```

Adapter selection precedence:

1. explicit `--adapter <adapter-id>`,
2. `ARCANUM_RUNTIME_ADAPTER`,
3. installed config `default_adapter`,
4. compatibility fallback, normally `codex-exec` for Codex installs.

## Durable Run Folder Contract

Runtime-owned folder:

```text
.arcanum/runtime/runs/<runtime-run-id>/
  RUN.json
  HANDOFF.md
  STATUS.json
  events.jsonl
  artifacts/
  children/
  adapter-state/
```

Successful command execution does not require a runtime `RESULT.md`. The requested `--output` path is the command response channel. Runtime envelope files are evidence about the invocation, not a duplicate result channel.

Required `RUN.json` concepts:

- `run_id`
- `parent_run_id`
- `orchestrator_id`
- `orchestrator_run_id`
- `adapter_id`
- `adapter_profile_path`
- `target_kind`
- `target_id`
- `loop_role`
- `loop_id`
- `parent_loop_id`
- `stage_number`
- `stage_name`
- `handoff_path`
- `result_path` when a compatibility or blocked path materializes one; otherwise null

Schema discipline:

- required fields are explicit in templates,
- controlled values are documented inline,
- stable ids and paths are preferred over free text,
- adapter profile evidence records provenance,
- validation grade states proof strength.

Required `STATUS.json` concepts:

- `status`: `queued`, `running`, `passed`, `flagged`, `blocked`, or `failed`
- `adapter_status`
- `validation_grade`: `contract`, `adapter-safety`, `execution`, or null
- `output_paths`
- `blocked_reason`
- `started_at`
- `completed_at`

Important rule: `HANDOFF.md` is immutable intent. Runtime status belongs in `STATUS.json` and `events.jsonl`.

Every run also preserves selected adapter profile evidence, normally:

```text
artifacts/adapter-profile.json
```

Command-owned artifacts remain outside the runtime folder. For example, an `invoke design` command should write target development artifacts such as `INVOKE-DESIGN.md`, `ARCHITECTURE-BUNDLE.md`, `GLOSSARY-CONSISTENCY.md`, and `DESIGN-TRANSPORT.md` under a declared target write scope. Runtime transport is not complete until that behavior is proven.

## Refine Integration

Replace active refine required artifact:

```text
GOAL-HANDOFF.md
```

with:

```text
RUNTIME-HANDOFF.md
```

Refine target-local folder:

```text
<target>/development/refinement-runs/<run-id>/
  RUN-MANIFEST.md
  evidence-index.json
  REFINE-SEED-PROPOSAL.md
  RUNTIME-HANDOFF.md
  RESULT.md
  stages/
```

Each command-backed stage should reference:

- runtime run id,
- adapter id,
- command or skill target,
- resolved command file when applicable,
- output artifact,
- status,
- verdict,
- blocked reason when applicable.

Refine should never require native `/goal` or Codex Goal state to prove execution.

## Task-Session Integration

Replace the canonical task-session runtime path:

```text
task-session -> codex-goal adapter -> native /goal
```

with:

```text
task-session -> RUNTIME-HANDOFF.md -> tools/arcanum --exec --adapter <adapter-id>
```

Task-session still owns task/SWU selection and safety. The runtime owns execution status and adapter evidence.

Add:

```text
arcana/task-session/runtime-adapters/runtime-handoff.md
```

Then mark the current `codex-goal.md` adapter as legacy/historical.

## Multiple-Loop Model

Each runtime run should expose loop topology:

- `loop_role`: `root`, `stage`, `candidate`, `nested`, `repair`, or `continuation`
- `loop_id`
- `parent_loop_id`
- `stage_number`
- `stage_name`

Usage:

- candidate loops are sibling runtime runs,
- nested loops are child runtime runs,
- repair loops are bounded child runs tied to a failed verdict,
- continuation loops resume from existing runtime status.

This keeps multiple refinement loops inspectable without compressing them into one prose artifact.

## Adapter Model

V1 adapters:

- `dry-run`
- `codex-exec`

`dry-run` validates the handoff and creates complete runtime artifacts without external execution.

`codex-exec` runs Codex CLI through `codex exec`.

Runtime selection is exposed through:

```bash
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter <adapter-id>
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter <adapter-id>
tools/arcanum --exec --adapter <adapter-id> --output <path> <command> <request>
```

When `--adapter` is omitted, `codex-exec` may remain the compatibility default for the Codex UI, but that default is not the architecture.

Codex adapter rules:

- do not use native `/goal`,
- run through the normal Codex CLI environment by default,
- do not create per-run Codex auth/config links by default,
- do not replicate Codex SQLite state into runtime artifacts,
- allow Codex-created SQLite state only when explicitly isolated adapter state is enabled and the state is contained inside the run-local adapter state,
- forbid shared or symlinked SQLite state from source Codex home,
- record adapter profile evidence,
- classify raw Codex outcomes before runner status mutation,
- return event contributions for `tools/arcanum`-owned `events.jsonl`,
- distinguish `adapter-safety` from `execution` validation,
- record backend/network/runtime failures in `STATUS.json`,
- write final output directly to the requested `--output`,
- never mutate orchestrator manifests directly.
- allow command-owned artifacts only inside target write scope declared in the runtime handoff.

## Validation Plan

Required checks:

- active refine run folders require `RUNTIME-HANDOFF.md`, not `GOAL-HANDOFF.md`,
- every non-blocked runtime-backed stage has runtime run evidence,
- every blocked stage has an exact blocked reason,
- runtime `RUN.json` and `STATUS.json` are valid JSON,
- `tools/arcanum` can list and resolve adapters,
- `tools/arcanum --exec --adapter dry-run ...` proves the non-Codex adapter path,
- `codex-exec` creates no per-run auth/config links by default,
- runtime `RUN.json` records adapter profile evidence,
- runtime `STATUS.json` records validation grade evidence,
- contained run-local Codex SQLite is allowed,
- shared or symlinked source Codex SQLite is blocked,
- blocked Codex backend runs count only as `adapter-safety`, not `execution`,
- nested runs preserve parent/child ids,
- candidate loops are separate sibling runs,
- active refine paths do not require `/goal`, `Codex Goal`, or `codex-goal`.
- runtime templates preserve `schema_version`, inline enums, adapter profile paths, and validation grade semantics.
- artifact-producing command fixtures create expected command-owned artifacts under declared target scope.
- successful command execution does not create a runtime `RESULT.md`.
- bootstrap writes `.arcanum/runtime/config.json` when a default adapter is selected.
- installed runtime config contains no secrets, auth/config copies, SQLite paths, or symlinks.
- changing default adapter does not require editing command files.

Validation commands:

```bash
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter dry-run
tools/arcanum --resolve-adapter codex-exec
tools/arcanum --exec --adapter dry-run --output /tmp/arcanum-dry-run-output.md invoke "define runtime smoke"
jq empty <tmp-run>/RUN.json
jq empty <tmp-run>/STATUS.json
jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' <tmp-run>/RUN.json
jq -e '.schema_version == "arcanum.runtime.run.v1"' <tmp-run>/RUN.json
jq -e '.schema_version == "arcanum.runtime.status.v1"' <tmp-run>/STATUS.json
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --adapter codex-exec --output <tmp-output> invoke "define runtime smoke"
tools/arcanum --exec --output /tmp/arcanum-runtime-invoke-design-output.md invoke "<artifact-producing invoke design fixture request>"
tools/bootstrap_arcanum.sh --target /tmp/arcanum-install-runtime-selection --runtime codex --default-adapter codex-exec --force
jq empty /tmp/arcanum-install-runtime-selection/.arcanum/runtime/config.json
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter dry-run
arcana/refine/development/run-validation-fixtures.sh
rg -n "GOAL-HANDOFF|Codex Goal|codex-goal|/goal" arcana/refine .codex/commands/refine.md
```

Historical paths may need explicit exceptions.

## First Implementation Slice

1. Create `framework/runtime/README.md`.
2. Create runtime templates for `RUNTIME-HANDOFF.md`, `RUN.json`, and `STATUS.json`.
3. Implement runtime envelope support inside `tools/arcanum`.
4. Add adapter discovery: `--list-adapters` and `--resolve-adapter <adapter-id>`.
5. Implement `tools/arcanum --exec --adapter dry-run`.
6. Add dry-run fixture validation.
7. Apply `ADAPTER-CONTRACT-DECISIONS.md` before `codex-exec`.
8. Implement `codex-exec` as a selected adapter with normal Codex CLI state by default, classifier-based status, adapter profile evidence, and validation grades.
9. Prove artifact-producing command reproduction with `SWU-RUNTIME-004.5`.
10. Update active refine docs/templates/fixtures/validation to use `RUNTIME-HANDOFF.md`.
11. Add task-session generic runtime handoff adapter doc.
12. Remove or shim `tools/arcanum-runtime-run`; `tools/arcanum --exec` is the active path.
13. Add install-time `--default-adapter <adapter-id>` and `.arcanum/runtime/config.json`.
14. Add default adapter get/set and selection precedence.

## Open Decisions

No blocking decisions remain.

Recommended names:

- command surface: `tools/arcanum`
- refine handoff: `RUNTIME-HANDOFF.md`
- runtime root: `.arcanum/runtime/runs/<runtime-run-id>/`
- installed runtime config: `.arcanum/runtime/config.json`
- first adapter: `dry-run`
- first execution adapter: `codex-exec`

## Stage Artifacts

- `stages/01-context-builder.md`
- `stages/02-invoke-define.md`
- `stages/03-interrogation-refine-review.md`
- `stages/04-research-decision.md`
- `stages/05-distill.md`
- `stages/06-invoke-design.md`
- `stages/07-interrogation-design-review.md`
- `stages/08-distill-repair.md`
- `stages/09-invoke-plan.md`
- `stages/10-final-interrogation.md`
