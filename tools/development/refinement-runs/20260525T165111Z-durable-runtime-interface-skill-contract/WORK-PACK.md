# Work Pack: Durable Arcanum Runtime Interface

## Objective

Implement the durable runtime foundation that lets refine, task-session, and future Arcanum orchestrators hand off work through generic runtime runs instead of Codex Goal.

## Source Design References

- Define artifact: `INVOKE-DEFINE.md`
- Glossary artifact: `RUNTIME-GLOSSARY.md`
- Define transport: `DEFINE-TRANSPORT.md`
- Design artifact: `INVOKE-DESIGN.md`
- Architecture bundle: `ARCHITECTURE-BUNDLE.md`
- Glossary consistency report: `GLOSSARY-CONSISTENCY.md`
- Design transport: `DESIGN-TRANSPORT.md`
- Plan artifact: `INVOKE-PLAN.md`
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Runtime schemas: `RUNTIME-SCHEMAS.md`
- Execution pack: `EXECUTION-PACK.md`
- Runtime adapter pattern: `RUNTIME-ADAPTER-PATTERN.md`
- Codex adapter design: `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- Runtime command artifact reproduction: `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`
- Single command surface refresh: `SINGLE-COMMAND-SURFACE-REFRESH.md`
- Runtime adapter surface refresh: `RUNTIME-ADAPTER-SURFACE-REFRESH.md`
- Install runtime selection refresh: `INSTALL-RUNTIME-SELECTION-REFRESH.md`
- Codex exec environment repair: `CODEX-EXEC-ENVIRONMENT-REPAIR.md`
- Adapter contract decisions: `ADAPTER-CONTRACT-DECISIONS.md`
- Schema discipline integration: `SCHEMA-DISCIPLINE-INTEGRATION.md`
- Knowledge taxonomy context pack: `tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md`
- Interrogation review: `INTERROGATION-REVIEW.md`
- Distill review: `DISTILL-REVIEW.md`
- Runtime adapter interrogation review: `RUNTIME-ADAPTER-INTERROGATION-REVIEW.md`
- Runtime adapter distill review: `RUNTIME-ADAPTER-DISTILL-REVIEW.md`

## Current State

- Refine has a canonical ten-stage loop and now uses `RUNTIME-HANDOFF.md` plus runtime evidence for active validation.
- Task-session now has a generic `runtime-handoff` adapter; the old native goal adapter remains only as legacy compatibility.
- `tools/arcanum --exec` currently invokes Codex CLI directly through shared repo-local runtime state.
- A command-backed refine experiment failed at nested Codex execution before producing a stage artifact.
- A local skill-contract refinement produced this plan-ready design package.
- Adapter review flagged that `codex-exec` needs explicit adapter profile evidence, outcome classification, validation grades, runner-owned event logging, and state isolation checks before implementation.
- A security review found that per-run Codex homes expose auth/config links and replicate Codex SQLite state into runtime artifacts. Default `codex-exec` now runs the normal Codex CLI environment directly; run-local `CODEX_HOME` isolation is opt-in only with `ARCANUM_RUNTIME_ISOLATE_CODEX_HOME=1`.
- A context-builder pass over `cyberAlchemyAI/knowledge-taxonomy` confirmed that runtime v1 should copy schema discipline patterns, not dependencies: field tiers, inline enums, stable ids/paths, provenance, validation grades, and small shell/`jq` validators.
- A schema-discipline handoff now exists for broader Arcanum/CyberAlchemy generalization. This work-pack only applies the pattern to the runtime artifact family.
- `SWU-RUNTIME-004` proved runtime transport and requested-output compatibility, but not reproduction of command-owned artifacts such as invoke design outputs. `SWU-RUNTIME-004.5` is now required before L3.
- `SWU-RUNTIME-007` was added after L3 because Task Session had moved to `--via runtime` while Context Builder still advertised only `--handoff codex-goal`.
- `SINGLE-COMMAND-SURFACE-REFRESH.md` supersedes the two-tool runtime model. `tools/arcanum` should become the only active command execution surface; `tools/arcanum-runtime-run` should be removed or demoted to a temporary compatibility shim.
- `RUNTIME-ADAPTER-SURFACE-REFRESH.md` clarifies that one command surface must still make non-Codex runtimes easy to select. `tools/arcanum` is the front door; adapters such as `dry-run`, `codex-exec`, and future runtimes remain the extension model.
- `INSTALL-RUNTIME-SELECTION-REFRESH.md` moves default adapter selection into Arcanum installation and adds a post-install interchange surface. `--runtime codex|none` remains command-surface compatibility; `--default-adapter <adapter-id>` selects execution.
- `CODEX-EXEC-ENVIRONMENT-REPAIR.md` separates nested Codex environment failures from backend/auth failures and adds a follow-up preflight/private-state slice.
- `SWU-RUNTIME-009` implemented install-time default adapter selection and post-install adapter interchange without requiring command file edits.

## Delivery Slices

| Slice | Layer | Goal | Status |
| --- | --- | --- | --- |
| RUNTIME-L0 | L0 | Add runtime contract, templates, runner, and dry-run adapter. | ready; promotion requires SWU-RUNTIME-001 and SWU-RUNTIME-002 |
| RUNTIME-L1 | L1 | Add `codex-exec` adapter with adapter contract evidence and safe default CLI state handling. | passed in task session `tools/development/task-sessions/20260525T2040Z-swu-runtime-003.md`; amended by security fix to remove per-run Codex home as default |
| RUNTIME-L2 | L2 | Route `tools/arcanum --exec` through runtime runner behind feature flag and prove command-owned artifact reproduction. | passed in task sessions `tools/development/task-sessions/20260525T2055Z-swu-runtime-004.md` and `tools/development/task-sessions/20260525T2210Z-swu-runtime-004-5.md` |
| RUNTIME-L3 | L3 | Migrate active refine/task-session/context-builder runtime contracts. | passed in task sessions `tools/development/task-sessions/20260525T2221Z-swu-runtime-005-006.md` and `tools/development/task-sessions/20260525T2230Z-swu-runtime-007.md` |
| RUNTIME-L4 | L4 | Collapse runtime execution into one `tools/arcanum` command surface while preserving runtime adapter selection. | passed in task session `tools/development/task-sessions/20260526T1301Z-swu-runtime-008.md` |
| RUNTIME-L5 | L5 | Add install-time default adapter selection and runtime interchange. | passed in task session `tools/development/task-sessions/20260526T1452Z-swu-runtime-009.md` |
| RUNTIME-L6 | L6 | Add Codex exec environment preflight and private state policy. | ready; continue `SWU-RUNTIME-010` |

## Task Board

| Task | Layer | SWUs | Status | Validation |
| --- | --- | --- | --- | --- |
| TASK-RUNTIME-001 Add Runtime Contract And Dry-Run Runner | L0 | SWU-RUNTIME-001, SWU-RUNTIME-002 | ready | dry-run fixture and JSON checks |
| TASK-RUNTIME-002 Add Codex Exec Adapter | L1 | SWU-RUNTIME-003 | passed | codex adapter fixture with adapter profile, validation grade, execution evidence, and SQLite safety checks |
| TASK-RUNTIME-003 Migrate Arcanum Exec Compatibility Path | L2 | SWU-RUNTIME-004, SWU-RUNTIME-004.5 | passed | feature-flag exec smoke plus artifact-producing invoke fixture |
| TASK-RUNTIME-004 Migrate Refine Active Runtime Contract | L3 | SWU-RUNTIME-005 | passed | refine fixture validation |
| TASK-RUNTIME-005 Add Task-Session Runtime Handoff Adapter | L3 | SWU-RUNTIME-006 | passed | adapter doc/readiness review |
| TASK-RUNTIME-006 Add Context Builder Runtime Handoff Mode | L3 | SWU-RUNTIME-007 | passed | active context-builder stale-language and JSON checks |
| TASK-RUNTIME-007 Collapse Runtime Runner Into tools/arcanum | L4 | SWU-RUNTIME-008 | passed | one-tool command execution validation plus adapter selection validation |
| TASK-RUNTIME-008 Add Install-Time Runtime Selection And Interchange | L5 | SWU-RUNTIME-009 | passed | bootstrap config and adapter switching validation |
| TASK-RUNTIME-009 Add Codex Exec Environment Preflight And Private State | L6 | SWU-RUNTIME-010 | ready | preflight, classifier, and private-state validation |

## SWU Manifest

| SWU | Parent Task | Dependencies | Write Scope | Done Criteria | Verification | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-RUNTIME-001 | TASK-RUNTIME-001 | none | `framework/runtime/` | Runtime contract docs/templates exist, match `RUNTIME-SCHEMAS.md`, and preserve schema-discipline field tiers/inline enums. | `test -f framework/runtime/README.md && test -f framework/runtime/templates/RUNTIME-HANDOFF.md && test -f framework/runtime/templates/RUN.json && test -f framework/runtime/templates/STATUS.json` | local-fallback |
| SWU-RUNTIME-002 | TASK-RUNTIME-001 | SWU-RUNTIME-001 | `tools/arcanum-runtime-run`, `framework/runtime/development/fixtures/` | Dry-run adapter creates complete runtime folder. | `tools/arcanum-runtime-run --adapter dry-run --handoff framework/runtime/development/fixtures/dry-run/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-dry-run && jq empty /tmp/arcanum-runtime-dry-run/RUN.json && jq empty /tmp/arcanum-runtime-dry-run/STATUS.json` | local-fallback |
| SWU-RUNTIME-003 | TASK-RUNTIME-002 | SWU-RUNTIME-002 plus `ADAPTER-CONTRACT-DECISIONS.md` | `tools/arcanum-runtime-run`, `framework/runtime/adapters/`, `framework/runtime/development/fixtures/codex-exec/` | `codex-exec` adapter records adapter profile evidence, classifies raw Codex outcomes, records validation grade, returns runner-owned event contributions, and does not create per-run auth/config links by default. | `tools/arcanum-runtime-run --adapter codex-exec --handoff framework/runtime/development/fixtures/codex-exec/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-codex-exec && jq empty /tmp/arcanum-runtime-codex-exec/RUN.json && jq empty /tmp/arcanum-runtime-codex-exec/STATUS.json && jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' /tmp/arcanum-runtime-codex-exec/RUN.json && jq -e '.validation_grade == "adapter-safety" or .validation_grade == "execution"' /tmp/arcanum-runtime-codex-exec/STATUS.json` | local-fallback |
| SWU-RUNTIME-004 | TASK-RUNTIME-003 | SWU-RUNTIME-003 | `tools/arcanum` | Feature-flag `--exec` delegates to runtime runner and preserves output path. | `ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output <tmp> invoke "define runtime smoke"`. | local-fallback |
| SWU-RUNTIME-004.5 | TASK-RUNTIME-003 | SWU-RUNTIME-004 | `tools/arcanum`, `tools/arcanum-runtime-run`, `framework/runtime/development/fixtures/invoke-design-artifacts/` | Feature-flag `--exec` reproduces command-owned invoke design artifacts in the declared target development directory while preserving runtime-owned artifact boundaries. | `ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output /tmp/arcanum-runtime-invoke-design-output.md invoke "<artifact-producing invoke design fixture request>" && test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/INVOKE-DESIGN.md && test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/ARCHITECTURE-BUNDLE.md && test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/GLOSSARY-CONSISTENCY.md && test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/DESIGN-TRANSPORT.md` | local-fallback |
| SWU-RUNTIME-005 | TASK-RUNTIME-004 | SWU-RUNTIME-004.5 | `arcana/refine/`, `.codex/commands/refine.md`, installed refine skill if requested | Active refine contract uses `RUNTIME-HANDOFF.md` and runtime evidence. | `arcana/refine/development/run-validation-fixtures.sh`. | local-fallback |
| SWU-RUNTIME-006 | TASK-RUNTIME-005 | SWU-RUNTIME-004.5 | `arcana/task-session/runtime-adapters/`, `.codex/commands/task-session.md` | Task-session has generic runtime handoff adapter and no canonical dependency on native `/goal`. | Review adapter doc and command surface stale-language check with historical exceptions. | local-fallback |
| SWU-RUNTIME-007 | TASK-RUNTIME-006 | SWU-RUNTIME-006 | `transmutations/context-builder/`, `.codex/commands/context-builder.md` | Context Builder active contract supports `--handoff runtime` and generic runtime handoff templates. | `jq empty transmutations/context-builder/templates/runtime-handoff-index.json` plus active stale-language check. | local-fallback |
| SWU-RUNTIME-008 | TASK-RUNTIME-007 | SWU-RUNTIME-007 plus `SINGLE-COMMAND-SURFACE-REFRESH.md` and `RUNTIME-ADAPTER-SURFACE-REFRESH.md` | `tools/arcanum`, `tools/arcanum-runtime-run`, `framework/runtime/`, runtime package docs | `tools/arcanum --exec` is the single active execution path; `--adapter <adapter-id>` selects runtimes; `--list-adapters` and `--resolve-adapter <adapter-id>` expose profiles; command output writes directly to requested `--output`; runtime envelope is evidence only; no successful command run writes runtime `RESULT.md`; `tools/arcanum-runtime-run` is removed or a deprecated shim. | `bash -n tools/arcanum`; `tools/arcanum --resolve invoke`; `tools/arcanum --list-adapters`; `tools/arcanum --resolve-adapter dry-run`; `tools/arcanum --resolve-adapter codex-exec`; one-tool exec output checks for `dry-run` and `codex-exec`; no new runtime `RESULT.md`; no Codex auth/config links in runtime runs. | local-fallback |
| SWU-RUNTIME-009 | TASK-RUNTIME-008 | SWU-RUNTIME-008 plus `INSTALL-RUNTIME-SELECTION-REFRESH.md` | `tools/bootstrap_arcanum.sh`, `tools/install_arcanum.sh`, `tools/arcanum`, `framework/runtime/`, bootstrap docs, runtime package docs | Installer accepts `--default-adapter <adapter-id>`; installed `.arcanum/runtime/config.json` records default adapter and profile paths without secrets; `tools/arcanum --get-default-adapter` and `--set-default-adapter <adapter-id>` work; explicit `--adapter` overrides config; no runtime interchange requires command file edits. | bootstrap dry-run/install fixture; `jq empty .arcanum/runtime/config.json`; adapter default get/set checks; explicit override check; secret/state grep over runtime config. | local-fallback |
| SWU-RUNTIME-010 | TASK-RUNTIME-009 | SWU-RUNTIME-009 plus `CODEX-EXEC-ENVIRONMENT-REPAIR.md` | `tools/arcanum`, `.gitignore`, `framework/runtime/`, runtime package docs | `tools/arcanum --preflight-adapter codex-exec` reports precise environment status; private Codex state policy is documented and gitignored; `codex-exec` distinguishes state, sandbox, backend/auth, and output-reported block reasons; runtime run folders contain no auth/config/SQLite state. | preflight command; `.gitignore` check; envelope-backed codex-exec blocked/passed classifier check; run-folder secret/state scan. | local-fallback |

## Completion Evidence

| SWU | Status | Evidence |
| --- | --- | --- |
| SWU-RUNTIME-001 | passed | `tools/development/task-sessions/20260525T1920Z-runtime-runner-until-blocker.md` |
| SWU-RUNTIME-002 | passed | `tools/development/task-sessions/20260525T1920Z-runtime-runner-until-blocker.md` |
| SWU-RUNTIME-003 | passed | `tools/development/task-sessions/20260525T2040Z-swu-runtime-003.md` |
| SWU-RUNTIME-004 | passed | `tools/development/task-sessions/20260525T2055Z-swu-runtime-004.md` |
| SWU-RUNTIME-004.5 | passed | `tools/development/task-sessions/20260525T2210Z-swu-runtime-004-5.md` |
| SWU-RUNTIME-005 | passed | `tools/development/task-sessions/20260525T2221Z-swu-runtime-005-006.md` |
| SWU-RUNTIME-006 | passed | `tools/development/task-sessions/20260525T2221Z-swu-runtime-005-006.md` |
| SWU-RUNTIME-007 | passed | `tools/development/task-sessions/20260525T2230Z-swu-runtime-007.md` |
| SWU-RUNTIME-008 | passed | `tools/development/task-sessions/20260526T1301Z-swu-runtime-008.md` |
| SWU-RUNTIME-009 | passed | `tools/development/task-sessions/20260526T1452Z-swu-runtime-009.md` |
| SWU-RUNTIME-010 | ready | `CODEX-EXEC-ENVIRONMENT-REPAIR.md` |

## Task Details

### TASK-RUNTIME-001 Add Runtime Contract And Dry-Run Runner

Purpose: establish durable runtime structure without external execution.

Source anchors:

- `ARCHITECTURE-BUNDLE.md#low-level-components-view`
- `IMPLEMENTATION-LAYERING.md#l0-runtime-contract-proof`
- `INVOKE-DEFINE.md#acceptance-criteria`
- `RUNTIME-SCHEMAS.md`
- `SCHEMA-DISCIPLINE-INTEGRATION.md`
- `EXECUTION-PACK.md#w0-runtime-contract-proof`

Implementation detail:

1. Create runtime docs and templates under `framework/runtime/`.
2. Document schema discipline for the runtime family: required fields, controlled enum values, stable ids/paths, provenance, and validation grades.
3. Create `tools/arcanum-runtime-run`.
4. Parse `--handoff`, `--run-dir`, and `--adapter`.
5. For `dry-run`, create the run directory and write:
   - `RUN.json`
   - `HANDOFF.md`
   - `STATUS.json`
   - `RESULT.md`
   - `events.jsonl`
   - `artifacts/`
   - `children/`
6. Return nonzero only for invalid inputs or failed artifact writes.

Runtime lifecycle requirements:

- create a run-local `.lock` before adapter execution,
- block with `blocked_reason: run-already-active` when a running lock exists,
- do not overwrite terminal runs by default,
- write status transitions exactly as defined in `RUNTIME-SCHEMAS.md`,
- append event objects matching `RUNTIME-SCHEMAS.md#eventsjsonl`.

Edge cases:

- missing handoff path,
- existing run dir,
- invalid adapter id,
- inability to write JSON.
- stale lock with non-running status.

### TASK-RUNTIME-002 Add Codex Exec Adapter

Purpose: make Codex an adapter, not the runtime identity.

Source anchors:

- `ARCHITECTURE-BUNDLE.md#dependency-interface-view`
- `RUNTIME-GLOSSARY.md#terms`
- `IMPLEMENTATION-LAYERING.md#l1-codex-adapter-proof`
- `RUNTIME-SCHEMAS.md#codex-exec-adapter-state-safety`
- `RUNTIME-ADAPTER-PATTERN.md`
- `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `ADAPTER-CONTRACT-DECISIONS.md`

Implementation detail:

1. Add `codex-exec` adapter dispatch.
2. Use normal Codex CLI state by default; do not create per-run Codex auth/config links.
3. Keep isolated per-run Codex home support opt-in only for explicit adapter-state experiments.
4. Materialize selected adapter profile evidence at `artifacts/adapter-profile.json` and point `RUN.json.adapter_profile_path` to it.
5. Run Codex preflight before runtime invocation.
6. Run `codex exec` with output capture to the requested `--output` path when preflight passes.
7. Classify raw Codex outcome into `passed`, `flagged`, `blocked`, or `failed` before runner status mutation.
8. Record exit code, adapter status, runtime status, validation grade, and blocked/failure reason in `STATUS.json`.
9. Return adapter event contributions for the runner to append; do not write `events.jsonl` directly.
10. Allow Codex-created `.sqlite`, `.sqlite-wal`, and `.sqlite-shm` files only inside opt-in run-local adapter state.
11. Never share or symlink `.sqlite`, `.sqlite-wal`, `.sqlite-shm`, log, socket, or transient runtime files from the source Codex home.
12. Preserve the adapter result object defined in `RUNTIME-ADAPTER-PATTERN.md`.
13. Preserve the Codex-specific status mapping defined in `CODEX-RUNTIME-ADAPTER-DESIGN.md` and `ADAPTER-CONTRACT-DECISIONS.md`.

Edge cases:

- Codex binary missing,
- network/backend unavailable,
- output file not produced,
- adapter home cannot be prepared.
- source Codex home has no auth/config files.
- adapter profile snapshot cannot be written.
- backend/network unavailable before sampling, which should classify as `blocked` and `adapter-safety`, not `failed` or `execution`.
- any SQLite file under run-local Codex home is a symlink or resolves outside the runtime run folder.

### TASK-RUNTIME-003 Migrate Arcanum Exec Compatibility Path

Purpose: preserve command UX while moving execution lifecycle into runtime, including artifact-producing command behavior.

Source anchors:

- `ARCHITECTURE-BUNDLE.md#workflow-process-view`
- `ARCHITECTURE-BUNDLE.md#decision-flow-view`
- `IMPLEMENTATION-LAYERING.md#l2-command-surface-compatibility`
- `RUNTIME-SCHEMAS.md#toolsarcanum---exec---output-compatibility`
- `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`

Implementation detail:

1. Keep `tools/arcanum --resolve` unchanged.
2. In `--exec`, when runtime envelope mode is enabled, generate a runtime handoff from command name, command file, request, and output path.
3. Select `codex-exec` by default unless `--adapter` chooses another runtime.
4. Write the command response directly to the requested `--output`.
5. Preserve existing summary output fields.
6. If adapter blocks before producing output, write a blocked summary to requested `--output`.
7. For artifact-producing commands, include target artifact write scope in the generated runtime handoff.
8. Allow the adapter to write command-owned artifacts only inside the declared target scope.
9. Record or reference command-owned artifact paths in runtime result/status evidence.
10. Validate a real invoke design fixture that creates expected target development artifacts.

Edge cases:

- generated handoff path collision,
- runtime runner unavailable,
- adapter blocked,
- output copy fails.
- adapter fails before result exists.
- command-owned target artifact scope missing.
- nested Codex attempts to write runtime-owned artifacts.
- command returns a response but expected target artifacts are absent.

### TASK-RUNTIME-004 Migrate Refine Active Runtime Contract

Purpose: make refine consume runtime evidence instead of Codex Goal handoff.

Source anchors:

- `INVOKE-DESIGN.md#design-decisions`
- `ARCHITECTURE-BUNDLE.md#context-view`
- `IMPLEMENTATION-LAYERING.md#l3-orchestrator-migration`

Implementation detail:

1. Replace active `GOAL-HANDOFF.md` requirements with `RUNTIME-HANDOFF.md`.
2. Replace `codex-goal` handoff language with generic runtime handoff language.
3. Require runtime run evidence for non-blocked command-backed stages.
4. Update examples, templates, fixtures, validation docs, and installed skill if needed.

Edge cases:

- historical `/goal` references should not break active validation,
- blocked stage evidence must remain valid,
- target-local refine folders must stay index/manifest owners, not runtime state owners.

### TASK-RUNTIME-005 Add Task-Session Runtime Handoff Adapter

Purpose: let task-session reuse the runtime without duplicating refine logic.

Source anchors:

- `INVOKE-DEFINE.md#target-behavior`
- `INVOKE-DESIGN.md#design-summary`
- `IMPLEMENTATION-LAYERING.md#l3-orchestrator-migration`

Implementation detail:

1. Add `arcana/task-session/runtime-adapters/runtime-handoff.md`.
2. Define task-session inputs to generic runtime handoff.
3. Mark `codex-goal.md` as legacy/deprecated where active docs allow.
4. Update command docs enough that task-session points to generic runtime adapter for new handoffs.

Edge cases:

- work-pack/SWU safety gates still belong to task-session,
- runtime must not update work-pack status directly,
- native `/goal` history may remain in old development evidence.

### TASK-RUNTIME-007 Collapse Runtime Runner Into tools/arcanum

Purpose: remove the two-tool execution model and make `tools/arcanum` the only active command execution surface while keeping runtime adapters easy to add and select.

Source anchors:

- `SINGLE-COMMAND-SURFACE-REFRESH.md`
- `RUNTIME-ADAPTER-SURFACE-REFRESH.md`
- `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`
- `framework/runtime/adapters/codex-exec.md`

Implementation detail:

1. Move any still-needed runtime envelope/status logic into `tools/arcanum`.
2. Add adapter selection to `tools/arcanum --exec` through `--adapter <adapter-id>`, defaulting to `codex-exec` only for compatibility.
3. Add static adapter discovery through `tools/arcanum --list-adapters` and `tools/arcanum --resolve-adapter <adapter-id>`.
4. Run the selected adapter from `tools/arcanum --exec`.
5. Write final command response directly to the requested `--output`.
6. Keep runtime envelope files as invocation evidence only.
7. Record selected adapter profile evidence in envelope-backed runs.
8. Remove runtime-owned `RESULT.md` from successful command runs.
9. Remove default per-run Codex home/state behavior.
10. Delete `tools/arcanum-runtime-run` or convert it into a deprecated shim that delegates to `tools/arcanum --exec`.
11. Update active docs and fixtures so they no longer present `tools/arcanum-runtime-run` as the runtime model.

Edge cases:

- Codex backend/auth unavailable should still write a blocked command output and status evidence.
- Existing historical runtime runs may still contain old files; validation should use a pre-run marker for new files.
- Dry-run fixture behavior should move to `tools/arcanum --exec --adapter dry-run`.
- Adding a future runtime should require an adapter profile and dispatch branch, not command-specific changes in refine or task-session.

### TASK-RUNTIME-008 Add Install-Time Runtime Selection And Interchange

Purpose: make runtime adapter choice part of Arcanum installation while preserving easy post-install switching.

Source anchors:

- `INSTALL-RUNTIME-SELECTION-REFRESH.md`
- `RUNTIME-ADAPTER-SURFACE-REFRESH.md`
- `tools/bootstrap_arcanum.sh`
- `tools/install_arcanum.sh`
- `spells/arcanum-bootstrap/README.md`

Implementation detail:

1. Keep `--runtime codex|none` as command-surface compatibility.
2. Add `--default-adapter <adapter-id>` to `tools/bootstrap_arcanum.sh`.
3. Forward `--default-adapter` through `tools/install_arcanum.sh`.
4. Validate the selected adapter with `tools/arcanum --resolve-adapter <adapter-id>` or the same static adapter table.
5. Write `.arcanum/runtime/config.json` in installed repositories.
6. Materialize safe adapter profile snapshots under `.arcanum/runtime/adapters/`.
7. Add `tools/arcanum --get-default-adapter`.
8. Add `tools/arcanum --set-default-adapter <adapter-id>`.
9. Apply adapter selection precedence: explicit `--adapter`, `ARCANUM_RUNTIME_ADAPTER`, installed config default, compatibility fallback.
10. Update bootstrap docs and output contracts to report command surface and default adapter separately.

Edge cases:

- `--runtime codex` without `--default-adapter` should select `codex-exec`.
- `--runtime none` should not imply Codex execution.
- missing or invalid `.arcanum/runtime/config.json` should fall back safely and report a flag.
- config must not store secrets, auth paths, copied Codex config, SQLite files, or symlinks.

### TASK-RUNTIME-009 Add Codex Exec Environment Preflight And Private State

Purpose: make nested Codex execution failures diagnosable and provide a non-evidence private state policy.

Source anchors:

- `CODEX-EXEC-ENVIRONMENT-REPAIR.md`
- `tools/arcanum`
- `framework/runtime/adapters/codex-exec.md`
- `.gitignore`

Implementation detail:

1. Add `tools/arcanum --preflight-adapter codex-exec`.
2. Check Codex binary, Codex help, writable state strategy, and sandbox availability.
3. Distinguish `codex-state-unavailable`, `codex-sandbox-unavailable`, `codex-backend-or-auth-unavailable`, and output-reported blocks.
4. Gitignore `.arcanum/runtime/private/`.
5. Document optional `.arcanum/runtime/private/codex-home/` as stable private mutable adapter state, not evidence.
6. Keep runtime run folders free of Codex auth/config/SQLite files.

Edge cases:

- missing `bwrap`,
- read-only `~/.codex/state_*.sqlite`,
- output file exists but says command blocked,
- private state path configured but not writable,
- backend/auth unavailable after local preflight passes.

## Validation Strategy

Run after each layer:

```bash
test -f framework/runtime/README.md
test -f framework/runtime/templates/RUNTIME-HANDOFF.md
test -f framework/runtime/templates/RUN.json
test -f framework/runtime/templates/STATUS.json
jq empty <runtime-run>/RUN.json
jq empty <runtime-run>/STATUS.json
tools/arcanum-runtime-run --adapter dry-run --handoff framework/runtime/development/fixtures/dry-run/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-dry-run
jq empty /tmp/arcanum-runtime-dry-run/RUN.json
jq empty /tmp/arcanum-runtime-dry-run/STATUS.json
jq -e '.schema_version == "arcanum.runtime.run.v1"' /tmp/arcanum-runtime-dry-run/RUN.json
jq -e '.schema_version == "arcanum.runtime.status.v1"' /tmp/arcanum-runtime-dry-run/STATUS.json
jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' /tmp/arcanum-runtime-dry-run/RUN.json
test -f /tmp/arcanum-runtime-dry-run/RESULT.md
test -f /tmp/arcanum-runtime-dry-run/events.jsonl
```

Run before L2:

```bash
tools/arcanum-runtime-run --adapter codex-exec --handoff framework/runtime/development/fixtures/codex-exec/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-codex-exec
jq empty /tmp/arcanum-runtime-codex-exec/RUN.json
jq empty /tmp/arcanum-runtime-codex-exec/STATUS.json
jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' /tmp/arcanum-runtime-codex-exec/RUN.json
jq -e '.validation_grade == "adapter-safety" or .validation_grade == "execution"' /tmp/arcanum-runtime-codex-exec/STATUS.json
find /tmp/arcanum-runtime-codex-exec/adapter-state/codex-home \( -name '*.sqlite' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name 'state_*.sqlite*' -o -name 'logs_*.sqlite*' -o -name 'goals_*.sqlite*' \) -type l -print -quit | grep -q . && exit 1 || true
```

Run before L3 completion:

```bash
tools/arcanum --resolve refine
tools/arcanum --resolve invoke
tools/arcanum --resolve context-builder
tools/arcanum --resolve interrogation
tools/arcanum --resolve distill
arcana/refine/development/run-validation-fixtures.sh
```

Run stale-language check scoped to active runtime paths:

```bash
rg -n "GOAL-HANDOFF|Codex Goal|codex-goal|/goal" arcana/refine/SKILL.md arcana/refine/README.md arcana/refine/REFINEMENT-LOOP.md arcana/refine/templates arcana/refine/examples .codex/commands/refine.md
rg -n "Codex Goal|codex-goal|/goal|runtime-goal|goal-like|goal handoff|Goal handoff" arcana/task-session/SKILL.md arcana/task-session/README.md .codex/commands/task-session.md
rg -n -- "--handoff codex-goal|Codex Goal|codex-goal|/goal|goal-profile" transmutations/context-builder/SKILL.md transmutations/context-builder/README.md .codex/commands/context-builder.md transmutations/context-builder/templates/runtime-handoff-pack.md transmutations/context-builder/templates/runtime-handoff-index.json
```

## Blockers

- None for L0.
- L0 promotion passed in task session `tools/development/task-sessions/20260525T1920Z-runtime-runner-until-blocker.md`.
- L1 previous blocker resolved by changing the policy from no SQLite to no shared/symlinked source SQLite.
- Runtime schema-discipline refresh completed for this package; broad Arcanum/CyberAlchemy schema governance remains a separate handoff.
- L2 passed behind `ARCANUM_RUNTIME_RUNNER=1`, including command-owned artifact reproduction.
- L3 passed for active refine, task-session, and context-builder contracts. Installed global refine/task-session skills were synchronized for Codex UI.
- L4 passed in task session `tools/development/task-sessions/20260526T1301Z-swu-runtime-008.md`.
- L5 passed in task session `tools/development/task-sessions/20260526T1452Z-swu-runtime-009.md`.
- L6 is ready because installed runtime config and adapter selection now exist.

## Recommended Next Route

Continue `SWU-RUNTIME-010` for Codex exec environment preflight and private state.
