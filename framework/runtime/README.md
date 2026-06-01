# Durable Runtime

The durable runtime is Arcanum's generic execution substrate.

It lets orchestrators such as refine and task-session hand off work without depending on Codex Goal or any other runtime-specific state model.

## Model

```text
orchestrator -> RUNTIME-HANDOFF.md -> native skill/subagent surface or tools/arcanum --exec --adapter <adapter-id> -> runtime evidence
```

The orchestrator owns workflow meaning. `tools/arcanum` owns command resolution, adapter selection, requested output capture, and optional durable envelope evidence. The adapter owns runtime-specific translation, preparation, and outcome classification.

`tools/arcanum-runtime-run` is a deprecated compatibility wrapper. New execution should use `tools/arcanum --exec`.

## Run Folder

Every runtime run writes:

```text
<run-dir>/
  RUN.json
  HANDOFF.md
  STATUS.json
  events.jsonl
  artifacts/
    adapter-profile.json
  children/
  adapter-state/
```

Successful command execution writes to the requested `--output` path. Runtime `RESULT.md` is not a required output for the active one-tool path.

## Status Model

Runtime status is stored in `STATUS.json`, not in the handoff.

Allowed terminal statuses:

- `passed`
- `flagged`
- `blocked`
- `failed`

Allowed validation grades:

- `contract`
- `adapter-safety`
- `execution`

## Schema Discipline

Runtime v1 keeps schema discipline lightweight:

- JSON artifacts include `schema_version`.
- Controlled values are documented inline near the fields they constrain.
- Durable references use stable ids and paths.
- Adapter profile evidence is recorded at `artifacts/adapter-profile.json`.
- Validation starts with shell and `jq` checks before adding schema libraries.

The runtime does not depend on `knowledge-taxonomy`; that repository is used only as a schema-design precedent.

## Adapters

V1 adapters:

- `local-skill`: represents native skill/subagent execution without spawning a nested model-backed CLI. It emits a handoff and receipt contract for the parent agent surface.
- `dry-run`: validates the runtime folder contract without external execution.
- `codex-exec`: legacy explicit adapter that runs Codex CLI using the normal Codex CLI environment by default. Per-run `CODEX_HOME` isolation is opt-in only with `ARCANUM_RUNTIME_ISOLATE_CODEX_HOME=1`.
- `codex-bypass`: legacy explicit adapter for trusted automation environments that bypasses Codex CLI sandbox and approval prompts.

Codex is not the runtime model. Claude and Copilot are not runtime models either. Arcanum installs thin agent surfaces for each host and keeps canonical behavior in sigil and spell files.

## Runtime Config

Installed repositories record runtime adapter selection in:

```text
.arcanum/runtime/config.json
.arcanum/runtime/adapters/<adapter-id>.json
```

The config is non-secret. It records the command surface, default adapter id, and adapter profile paths. It must not contain copied Codex auth, `config.toml`, SQLite state, tokens, or symlinks into private runtime state.

Runtime adapter selection order:

1. `tools/arcanum --exec --adapter <adapter-id> ...`
2. `ARCANUM_RUNTIME_ADAPTER=<adapter-id>`
3. `.arcanum/runtime/config.json`
4. implicit `local-skill` fallback when a Codex command surface exists

Runtime interchange commands:

```bash
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter local-skill
tools/arcanum --exec --adapter local-skill --output /tmp/arcanum-local-skill-output.md invoke "define runtime smoke"
tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-codex-output.md invoke "define runtime smoke"
```

## Event Ownership

`tools/arcanum` owns `events.jsonl` when runtime envelope evidence is enabled. Adapters may return event contributions, but they must not write the event log directly in v1.

## Command

```bash
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter local-skill
tools/arcanum --resolve-adapter dry-run
tools/arcanum --exec --adapter local-skill --output /tmp/arcanum-local-skill-output.md invoke "define runtime smoke"
tools/arcanum --exec --adapter dry-run --output /tmp/arcanum-dry-run-output.md invoke "define runtime smoke"
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-codex-output.md invoke "define runtime smoke"
```
