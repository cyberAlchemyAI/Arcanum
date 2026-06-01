# Codex Runtime Adapter Design

## Purpose

Explain how Codex is used as an Arcanum runtime adapter.

Codex is not the Arcanum runtime model. Codex is a selected runtime behind the generic durable runtime runner.

```text
RUNTIME-HANDOFF.md -> tools/arcanum-runtime-run --adapter codex-exec -> codex exec
```

## Runtime Profile

| Field | Value |
| --- | --- |
| `adapter_id` | `codex-exec` |
| `runtime_kind` | model-backed CLI runtime |
| `execution_mode` | synchronous process execution with durable local capture |
| `state_model` | run-local adapter state plus read-only symlinked auth/config |
| `isolation_model` | per-run `CODEX_HOME`, workspace sandbox from Codex CLI |
| `input_shape` | generic runtime handoff translated into a Codex prompt |
| `output_shape` | final Codex response captured as runtime `RESULT.md` and adapter result object |
| `failure_model` | blocked for unavailable CLI/config/backend before safe execution; failed for process/runtime failure after execution starts; flagged for usable output with warnings |
| `capabilities` | read/edit within sandbox, execute commands according to Codex CLI policy, produce final message artifacts |
| `limitations` | no native `/goal`; no shared SQLite state; run-local Codex SQLite is allowed; no implicit orchestration ownership |
| `validation_surface` | codex-exec fixture, isolated state checks, result/status JSON checks |

## Why Codex Is An Adapter

Codex has strong model execution properties:

- can read repository context,
- can run commands through controlled tooling,
- can edit files when asked,
- can produce structured final output,
- can be constrained by workspace sandbox.

But Codex should not own Arcanum runtime semantics:

- Codex should not decide refine's stage list.
- Codex should not decide task-session's SWU safety gates.
- Codex should not own durable runtime status.
- Codex should not use native `/goal` for this runtime model.
- Codex should not share mutable databases across nested Arcanum runs.

## Execution Layers For Codex

| Layer | Responsibility | Codex Behavior |
| --- | --- | --- |
| L0 Handoff | Orchestrator creates `RUNTIME-HANDOFF.md`. | Codex is not invoked yet. |
| L1 Runtime Run | Runner creates run folder and lock. | Codex is not invoked yet. |
| L2 Translation | Runner/adapter builds prompt from handoff. | Prompt instructs Codex to use Arcanum command/skill contract and output path. |
| L3 Preparation | Adapter prepares Codex state. | Create `<run-dir>/adapter-state/codex-home`; symlink safe auth/config only. |
| L4 Execution | Adapter invokes Codex CLI. | Run `codex exec -C <repo> --sandbox workspace-write --output-last-message <runtime-result> <prompt>`. |
| L5 Capture | Runner normalizes result. | Copy runtime result to requested output when compatibility caller provided one; write `STATUS.json` and events. |

## Runner Script Architecture For Codex

V1 shell function shape:

```bash
run_adapter_codex_exec() {
  prepare_codex_adapter_state || return_adapter_blocked "codex-state-prep-failed"
  build_codex_prompt_from_handoff || return_adapter_blocked "codex-prompt-translation-failed"
  codex_preflight || return_adapter_blocked "$codex_preflight_reason"
  append_event adapter-started
  CODEX_HOME="$adapter_codex_home" "$codex_bin" exec \
    -C "$repo_root" \
    --sandbox workspace-write \
    --output-last-message "$runtime_result" \
    "$prompt"
  codex_exit="$?"
  classify_codex_outcome "$codex_exit" "$runtime_result" "$adapter_log"
}
```

Runner core should call this function only after:

- `RUN.json` exists,
- `STATUS.json` is `running`,
- lock is acquired,
- adapter state dir exists,
- handoff is readable.

`classify_codex_outcome` must return the adapter result object and must distinguish pre-execution blocked conditions from true execution failures.

## Codex Adapter State

Per-run state root:

```text
<runtime-run-dir>/adapter-state/codex-home/
```

Allowed symlinks from source Codex home:

- `auth.json`
- `config.toml`
- `installation_id`
- `models_cache.json`

Allowed run-local state:

- `state_*.sqlite`
- `logs_*.sqlite`
- `goals_*.sqlite`
- `*.sqlite-wal`
- `*.sqlite-shm`

These files are allowed only when Codex creates them inside the run-local Codex home.

Never share or symlink from source Codex home:

- `state_*.sqlite`
- `logs_*.sqlite`
- `goals_*.sqlite`
- `*.sqlite-wal`
- `*.sqlite-shm`
- runtime logs,
- sockets,
- transient process state.

This is the main safety property for nested Arcanum runs: every Codex execution sees stable credentials/config but gets fresh runtime databases.

## Prompt Translation

The Codex translator consumes `RUNTIME-HANDOFF.md` and produces a single execution prompt.

Prompt sections:

- runtime objective,
- source artifacts,
- selected Arcanum command/skill contract,
- output path expectations,
- blocked report shape,
- validation command or reviewable evidence,
- instruction not to use native `/goal`.

For `tools/arcanum --exec` compatibility, the prompt should preserve current command prompt shape:

```text
Use the Arcanum command surface for command `<selected>`.

1. Read `<command-file>`.
2. Follow that command's process and embedded canonical contract.
3. Treat the user request below as the command arguments.
4. Preserve output contract and observability closeout.

User request:
<request>
```

## Status Mapping

| Codex Condition | Runtime Status | Adapter Status | Notes |
| --- | --- | --- | --- |
| Codex binary missing | `blocked` | `blocked` | Execution cannot safely begin. |
| Required source auth/config unavailable | `blocked` | `blocked` | Selected `codex-exec` adapter cannot safely execute. |
| Backend/network unavailable before sampling | `blocked` | `blocked` | Preserve exact backend error summary. |
| Codex process exits nonzero after execution starts | `failed` | `failed` | Preserve exit code and output if any. |
| Codex writes output with warnings | `flagged` | `flagged` | Output exists but needs review. |
| Codex writes final output cleanly | `passed` | `passed` | Copy to requested output if needed. |

## Output Compatibility

Runtime canonical result:

```text
<runtime-run-dir>/RESULT.md
```

Compatibility output:

```bash
tools/arcanum --exec --output <path> ...
```

Behavior:

- always prefer canonical runtime `RESULT.md`,
- copy `RESULT.md` to `<path>` when `--output` is provided,
- if Codex fails before `RESULT.md`, write a blocked summary to `<path>`,
- record both paths in `STATUS.json.output_paths`.

## Validation

Required checks:

```bash
tools/arcanum-runtime-run --adapter codex-exec --handoff framework/runtime/development/fixtures/codex-exec/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-codex-exec
jq empty /tmp/arcanum-runtime-codex-exec/RUN.json
jq empty /tmp/arcanum-runtime-codex-exec/STATUS.json
find /tmp/arcanum-runtime-codex-exec/adapter-state/codex-home \( -name '*.sqlite' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name 'state_*.sqlite*' -o -name 'logs_*.sqlite*' -o -name 'goals_*.sqlite*' \) -type l -print -quit | grep -q . && exit 1 || true
```

If backend/network blocks execution, validation may still pass as `adapter-safety` validation when:

- `STATUS.json.status` is `blocked`,
- `STATUS.json.validation_grade` is `adapter-safety`,
- blocked reason is exact,
- no shared or symlinked SQLite state exists,
- `events.jsonl` records adapter start/block closeout,
- requested output receives a blocked summary if compatibility mode was used.

It must not be reported as `execution` validation unless Codex completes the requested work and writes a clean runtime result.

## Design Risks

- Treating Codex adapter success as runtime system success.
- Accidentally sharing SQLite state from source Codex home.
- Letting Codex prompt translation invent orchestration semantics.
- Losing requested `--output` compatibility.
- Collapsing `blocked` and `failed` into one ambiguous status.

## Design Decision

Codex is the reference execution adapter, not the reference runtime. The reference runtime is the durable Arcanum runner contract. Codex proves that a powerful model-backed CLI can live behind that contract without owning it.
