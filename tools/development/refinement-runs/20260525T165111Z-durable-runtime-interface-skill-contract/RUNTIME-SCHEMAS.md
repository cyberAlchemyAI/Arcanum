# Runtime Schemas: Durable Arcanum Runtime Interface

## Purpose

Define the exact v1 runtime artifact shapes required for envelope-backed `tools/arcanum --exec` runs.

This schema contract follows lightweight schema discipline:

- required fields are explicit in the templates,
- recommended and optional fields may be added only when they preserve compatibility,
- controlled values are listed inline where implementers read them,
- stable ids and paths are preferred over free-text cross-references,
- provenance fields point to generated evidence,
- validation uses JSON plus shell/`jq` checks before schema libraries.

## Runtime Folder

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

`RESULT.md` is not required for successful command execution. The requested `--output` path is the command response channel. A blocked compatibility path may write a blocked summary to the requested output path.

## Installed Runtime Config

Installed repositories should use:

```text
.arcanum/runtime/config.json
```

Required template:

```json
{
  "schema_version": "arcanum.runtime.config.v1",
  "command_surface": "codex|none",
  "default_adapter": "codex-exec|dry-run|future-adapter-id|null",
  "adapters": {
    "codex-exec": {
      "enabled": true,
      "profile_path": ".arcanum/runtime/adapters/codex-exec.json"
    }
  }
}
```

Rules:

- no auth tokens,
- no copied Codex config,
- no SQLite paths,
- no symlinks,
- no mutable runtime state,
- profile paths point to descriptive metadata only.

## `RUN.json`

Field tier: required for v1 unless explicitly nullable in the template.

Required template:

```json
{
  "schema_version": "arcanum.runtime.run.v1",
  "run_id": "runtime-run-id",
  "parent_run_id": null,
  "orchestrator_id": "refine|task-session|tools-arcanum|manual",
  "orchestrator_run_id": "orchestrator-run-id-or-null",
  "adapter_id": "dry-run|codex-exec|future-adapter-id",
  "adapter_profile_path": "artifacts/adapter-profile.json",
  "target_kind": "command|skill|task|swu|stage|manual",
  "target_id": "target-id",
  "loop_role": "root|stage|candidate|nested|repair|continuation",
  "loop_id": "loop-id",
  "parent_loop_id": null,
  "stage_number": null,
  "stage_name": null,
  "handoff_path": "HANDOFF.md",
  "status_path": "STATUS.json",
  "result_path": null,
  "events_path": "events.jsonl",
  "artifacts_dir": "artifacts",
  "children_dir": "children",
  "adapter_state_dir": "adapter-state"
}
```

## `STATUS.json`

Field tier: required for v1 unless explicitly nullable in the template.

Required template:

```json
{
  "schema_version": "arcanum.runtime.status.v1",
  "run_id": "runtime-run-id",
  "status": "queued",
  "adapter_status": "not-started",
  "validation_grade": null,
  "output_paths": [],
  "blocked_reason": null,
  "error_summary": null,
  "started_at": null,
  "completed_at": null
}
```

Allowed `status` values:

- `queued`
- `running`
- `passed`
- `flagged`
- `blocked`
- `failed`

Allowed `adapter_status` values:

- `not-started`
- `running`
- `passed`
- `flagged`
- `blocked`
- `failed`

Allowed v1 transitions:

```text
queued -> running -> passed
queued -> running -> flagged
queued -> running -> blocked
queued -> running -> failed
```

Rules:

- `blocked`: execution did not safely begin, or a required adapter/input was unavailable.
- `failed`: execution began and the adapter/process failed unexpectedly.
- `flagged`: output exists, but warnings or gaps remain.
- Terminal statuses: `passed`, `flagged`, `blocked`, `failed`.

Allowed `validation_grade` values:

- `contract`: required files, schemas, and runner lifecycle exist.
- `adapter-safety`: adapter isolation, preflight, blocked reporting, and closeout are correct.
- `execution`: runtime actually completed requested work and wrote clean output.
- `null`: no validation grade has been established yet.

## `events.jsonl`

Minimum event object:

```json
{
  "timestamp": "2026-05-25T00:00:00Z",
  "run_id": "runtime-run-id",
  "event": "created",
  "status": "queued",
  "message": "Runtime run created.",
  "data": {}
}
```

Allowed event names:

- `created`
- `locked`
- `status-changed`
- `adapter-started`
- `adapter-finished`
- `result-written`
- `blocked`
- `failed`
- `lock-released`

## Adapter Result Contract

Adapters return or materialize this shape for the runner to fold into `STATUS.json`:

```json
{
  "adapter_id": "dry-run|codex-exec",
  "adapter_status": "not-started|running|passed|flagged|blocked|failed",
  "validation_grade": "contract|adapter-safety|execution|null",
  "exit_code": 0,
  "output_paths": ["requested-output.md"],
  "result_path": null,
  "blocked_reason": null,
  "error_summary": null,
  "state_path": "adapter-state/<adapter-id>",
  "events": []
}
```

Adapters return event contributions only. The runner owns `events.jsonl`, validates adapter event contributions, appends normalized events, and rejects malformed event objects.

## Adapter Profile Evidence

Every runtime run records selected adapter profile evidence.

Required profile path:

```text
artifacts/adapter-profile.json
```

The profile snapshot must preserve the selected adapter's properties, limitations, failure model, and validation surface. `RUN.json.adapter_profile_path` points to this snapshot.

The selected adapter may be resolved from a static v1 table. Dynamic runtime plugin discovery is deferred.

Minimum adapter profile fields:

- `adapter_id`
- `runtime_kind`
- `execution_mode`
- `state_model`
- `isolation_model`
- `input_shape`
- `output_shape`
- `failure_model`
- `capabilities`
- `limitations`
- `validation_surface`

The profile is provenance evidence. It must describe the selected adapter used by this run, not a generic future adapter.

## Lock And Existing-Run Policy

V1 runner behavior:

- create `<run-dir>/.lock` before adapter execution,
- append a `locked` event after lock acquisition,
- remove the lock and append `lock-released` on normal closeout,
- if `.lock` exists and `STATUS.json` is `running`, return `blocked` with `blocked_reason: run-already-active`,
- if status is terminal, do not overwrite unless a future `--force` option is added,
- if a run needs retry after `blocked` or `failed`, create a new continuation child run instead of mutating the original terminal run.

## `RUNTIME-HANDOFF.md`

Required sections:

- Objective
- Orchestrator
- Target
- Inputs
- Allowed Write Scope
- Expected Outputs
- Validation
- Blocked Conditions
- Adapter Preference
- Nesting Policy

The handoff is Markdown because it is the human-authored request surface. Runtime status, schema_version, and machine state remain in JSON artifacts.

## Schema Discipline Boundaries

Runtime v1 must not introduce:

- `knowledge-taxonomy` as a package dependency,
- graph database state,
- YAML/frontmatter parsing,
- repository-wide Zod or JSON Schema adoption,
- a universal ontology for runtime facts.

The runtime schema owns durable execution facts only: identity, handoff, status, adapter profile, event log, result paths, and parent/child topology.

## `codex-exec` Adapter State Safety

Default `codex-exec` behavior uses the normal Codex CLI environment directly. It must not copy or symlink Codex auth/config into runtime run folders by default.

Optional isolated Codex home, only when explicitly enabled:

```text
<runtime-run-dir>/adapter-state/codex-home/
```

Allowed source-home references when explicitly isolated mode is enabled:

- `auth.json`
- `config.toml`
- `installation_id`
- `models_cache.json`

These references must be treated as sensitive adapter configuration and should not be created by default.

Allowed run-local mutable state:

- Codex-created SQLite state/log/goal databases under the run-local Codex home,
- per-run logs under the runtime run folder,
- transient runtime state under the runtime run folder.

Disallowed sharing:

- symlinked SQLite state/log/goal databases from source Codex home,
- copied SQLite state/log/goal databases from source Codex home,
- mutable logs, sockets, or runtime state outside the runtime run folder,
- any `.sqlite`, `.sqlite-wal`, or `.sqlite-shm` file that resolves outside the runtime run folder.

Validation must watch SQLite patterns, not only known filenames:

```text
*.sqlite
*.sqlite-wal
*.sqlite-shm
state_*.sqlite*
logs_*.sqlite*
goals_*.sqlite*
```

Presence of these files is allowed when they are created inside the run-local Codex home and are not symlinks to shared state.

## `tools/arcanum --exec --output` Compatibility

When runtime envelope mode is enabled:

- `tools/arcanum --exec --output <path>` writes the command response directly to `<path>`,
- successful command execution does not create runtime `RESULT.md`,
- if the selected adapter blocks before producing output, `<path>` receives a blocked summary instead of being absent,
- `STATUS.json.output_paths` records the requested output path,
- envelope evidence records selected adapter profile and status/events, not a duplicate result channel.
