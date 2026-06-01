# Runtime Adapter: codex-exec

## Purpose

`codex-exec` runs Codex CLI as one adapter behind Arcanum's `tools/arcanum` execution surface.

Codex does not own Arcanum runtime semantics. `tools/arcanum` owns command resolution, requested output capture, optional durable state, status, and events. The adapter owns Codex-specific translation, execution, and raw outcome classification.

## Profile

| Field | Value |
| --- | --- |
| `adapter_id` | `codex-exec` |
| `runtime_kind` | `model-backed-cli` |
| `execution_mode` | `synchronous-process` |
| `state_model` | `normal-codex-cli-state` |
| `isolation_model` | `no-run-local-codex-home-by-default` |
| `input_shape` | `runtime-handoff-translated-prompt` |
| `output_shape` | `runtime-result-plus-adapter-result` |
| `failure_model` | `passed|flagged|blocked|failed` |

## State Policy

Default behavior:

- run `codex exec` as a normal CLI command,
- do not create a per-run `CODEX_HOME`,
- do not symlink auth/config files into runtime run folders,
- do not replicate Codex SQLite state into runtime run folders.

Opt-in behavior:

- `ARCANUM_RUNTIME_ISOLATE_CODEX_HOME=1` enables the older run-local `adapter-state/codex-home/` mode for explicit experiments.
- When opt-in isolation is enabled, SQLite-like files must be contained under the runtime run directory and must not be symlinks to shared state.

## Status Mapping

| Condition | Runtime Status | Validation Grade |
| --- | --- | --- |
| Codex binary missing | `blocked` | `adapter-safety` |
| Required Codex auth/config unavailable to CLI | `blocked` | `adapter-safety` |
| Backend/auth unavailable before clean result | `blocked` | `adapter-safety` |
| Shared or symlinked SQLite detected in opt-in isolated mode | `blocked` | `adapter-safety` |
| Codex exits nonzero after invocation without pre-execution signal | `failed` | `adapter-safety` |
| Codex writes clean result | `passed` | `execution` |

## Validation Surface

Minimum checks:

```bash
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-runtime-codex-exec.md invoke "define runtime smoke" || true
latest="$(find .arcanum/runtime/runs -maxdepth 1 -type d -name 'arcanum-command-invoke-*' | sort | tail -n 1)"
jq empty "$latest/RUN.json"
jq empty "$latest/STATUS.json"
jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' "$latest/RUN.json"
jq -e '.validation_grade == "adapter-safety" or .validation_grade == "execution"' "$latest/STATUS.json"
find "$latest" -path '*/adapter-state/codex-home/auth.json' -print -quit | grep -q . && exit 1 || true
```

Run-local Codex auth/config links and SQLite files are not expected unless `ARCANUM_RUNTIME_ISOLATE_CODEX_HOME=1` was explicitly used.
