# Adapter Contract Decisions

## Purpose

Lock the implementation decisions that sit between the generic durable runtime design and concrete runtime adapters.

This artifact repairs the ambiguity found by `RUNTIME-ADAPTER-INTERROGATION-REVIEW.md` and `RUNTIME-ADAPTER-DISTILL-REVIEW.md`.

It also locks the runtime package's lightweight schema discipline: adapter decisions must be expressed as stable fields, inline enums, provenance paths, and validation grades that can be checked with shell and `jq`.

## Decision Summary

| Decision | Selected | Rejected | Rationale |
| --- | --- | --- | --- |
| Adapter profile evidence | Runtime run records `adapter_profile_path` and snapshots profile evidence under `artifacts/adapter-profile.json` when available. | Only recording `adapter_id`. | Reviewers need to know which adapter properties, limits, and validation surface were in force for a run. |
| Event ownership | Runner owns `events.jsonl`; adapters return event contributions. | Adapter writes directly to `events.jsonl`. | Prevents double writes, malformed events, and split event ordering. |
| Status classification | Adapter classifies raw runtime outcome; runner validates and applies terminal status. | Runner maps raw exit codes directly. | Codex can return nonzero for pre-execution blocks, backend failures, or true execution failures. |
| Validation grade | Runtime evidence records `contract`, `adapter-safety`, or `execution`. | Treating every fixture pass as execution proof. | A blocked Codex backend can still prove isolation and blocked closeout, but not completed execution. |
| Codex auth/config rule | Missing required Codex auth/config blocks `codex-exec`; dry-run or validation-only flows may flag. | Ambiguous blocked-or-flagged behavior for selected `codex-exec`. | The selected adapter cannot execute safely without required runtime inputs. |
| Codex mutable state safety | Allow Codex-owned SQLite only when it is created inside the run-local adapter state; forbid shared, symlinked, or copied SQLite from source Codex home. | Forbidding every SQLite file under run-local Codex home. | Codex creates SQLite state during normal startup; the safety property is isolation, not absence of agent-owned state. |
| Adapter selection surface | Select runtimes through `tools/arcanum --exec --adapter <adapter-id>` and expose profiles through `--list-adapters` / `--resolve-adapter`. | Treating `codex-exec` as the built-in runtime behavior. | One command surface should make other runtimes easy to add without coupling refine or task-session to Codex. |
| Installed default adapter | Bootstrap writes non-secret `.arcanum/runtime/config.json` with `default_adapter`; `tools/arcanum` can get/set it. | Editing command files to switch runtimes. | Runtime choice should be installable and interchangeable without rewriting command contracts. |
| Schema discipline | Keep adapter contract fields and enums explicit in `RUNTIME-SCHEMAS.md` and runtime templates. | Adding a schema framework before runtime v1 proves the pattern. | The current need is repeatable validation discipline, not broad schema infrastructure. |

## Adapter Profile Evidence

Every runtime run must preserve the selected adapter profile evidence.

Required `RUN.json` field:

```json
"adapter_profile_path": "artifacts/adapter-profile.json"
```

The profile snapshot should include the v1 adapter profile fields:

```json
{
  "adapter_id": "codex-exec",
  "runtime_kind": "model-backed-cli",
  "execution_mode": "synchronous-process",
  "state_model": "normal-codex-cli-state",
  "isolation_model": "no-run-local-codex-home-by-default",
  "input_shape": "runtime-handoff-translated-prompt",
  "output_shape": "runtime-result-plus-adapter-result",
  "failure_model": "passed|flagged|blocked|failed",
  "capabilities": [],
  "limitations": [],
  "validation_surface": []
}
```

For v1, a Markdown profile may be canonical and the JSON snapshot may be generated or hand-authored by `tools/arcanum`. The durable run must still point to the profile evidence it used.

## Event Ownership

Runner core owns:

- opening `events.jsonl`,
- event ordering,
- event schema validation,
- appending normalized adapter events,
- lock, status, result, blocked, failed, and closeout events.

Adapters may return event contributions in the adapter result object:

```json
{
  "events": [
    {
      "event": "adapter-preflight",
      "message": "Codex binary found.",
      "data": {}
    }
  ]
}
```

The runner must add timestamp, run id, and current status when missing, reject malformed event names, and append the normalized event to `events.jsonl`.

Adapters must not write `events.jsonl` directly in v1.

## Status Classification

Adapter result classification is a two-step process:

```text
raw runtime outcome -> adapter classifier -> adapter result -> runner status apply
```

Adapter owns:

- runtime-specific preflight checks,
- stderr/stdout interpretation,
- exit-code classification,
- adapter blocked reason,
- adapter error summary.

Runner owns:

- allowed status validation,
- `STATUS.json` mutation,
- terminal status transition,
- event emission,
- compatibility output handling.

## Codex Classification Rules

For `codex-exec`:

| Condition | Adapter Status | Runtime Status | Notes |
| --- | --- | --- | --- |
| Codex binary missing | `blocked` | `blocked` | Required executable unavailable. |
| Required auth/config missing | `blocked` | `blocked` | Selected adapter cannot safely execute. |
| Backend/network unavailable before sampling | `blocked` | `blocked` | Preserve exact backend error. |
| Process starts and exits nonzero after work begins | `failed` | `failed` | Preserve exit code and output if any. |
| Codex creates run-local SQLite state | `flagged` or `passed` | `flagged` or `passed` | Allowed when contained inside the runtime run and not shared from source Codex home. |
| Codex state includes symlinked/copied source SQLite | `blocked` | `blocked` | Shared mutable state violates isolation. |
| Output exists with warnings or incomplete evidence | `flagged` | `flagged` | Result usable but not clean. |
| Output exists cleanly | `passed` | `passed` | Execution proof. |

V1 pseudocode:

```bash
run_adapter_codex_exec() {
  prepare_codex_adapter_state || return_adapter_blocked "codex-state-prep-failed"
  build_codex_prompt_from_handoff || return_adapter_blocked "codex-prompt-translation-failed"
  codex_preflight || return_adapter_blocked "$codex_preflight_reason"

  CODEX_HOME="$adapter_codex_home" "$codex_bin" exec \
    -C "$repo_root" \
    --sandbox workspace-write \
    --output-last-message "$runtime_result" \
    "$prompt"
  codex_exit="$?"

  classify_codex_outcome "$codex_exit" "$runtime_result" "$adapter_log"
}
```

`classify_codex_outcome` must distinguish a pre-execution block from execution failure before returning the adapter result object.

## Validation Grades

Runtime-backed validation must state which grade it proves:

| Grade | Meaning | Example |
| --- | --- | --- |
| `contract` | Required files, schemas, and runner lifecycle exist. | `dry-run` creates `RUN.json`, `STATUS.json`, `RESULT.md`, and `events.jsonl`. |
| `adapter-safety` | Adapter isolation, preflight, blocked reporting, and closeout are correct. | `codex-exec` blocks on backend but creates isolated Codex home and exact blocked reason. |
| `execution` | Runtime actually completes requested work and writes clean output. | `codex-exec` runs a smoke request and returns `passed`. |

`STATUS.json` must record the strongest validation grade proven by the run.

L1 `codex-exec` promotion requires:

- `adapter-safety` proof at minimum,
- `execution` proof before claiming the adapter can complete model-backed work,
- no shared, symlinked, or copied SQLite state from source Codex home.

## Codex State Safety Check

Validation must allow Codex-owned SQLite files created inside:

```text
<runtime-run-dir>/adapter-state/codex-home/
```

Validation must fail only when SQLite state is shared from outside the runtime run folder.

Forbidden cases:

- any SQLite file under `adapter-state/codex-home/` is a symlink,
- any SQLite file under `adapter-state/codex-home/` resolves outside `<runtime-run-dir>`,
- any SQLite file from source Codex home is copied into the run instead of created by the run,
- Codex is configured to use shared mutable state outside the run folder.

Watched SQLite patterns:

```text
*.sqlite
*.sqlite-wal
*.sqlite-shm
state_*.sqlite*
logs_*.sqlite*
goals_*.sqlite*
```

Reviewable shell check:

```bash
run_dir=/tmp/arcanum-runtime-codex-exec
find "$run_dir/adapter-state/codex-home" \
  \( -name '*.sqlite' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name 'state_*.sqlite*' -o -name 'logs_*.sqlite*' -o -name 'goals_*.sqlite*' \) \
  -type l -print -quit | grep -q . && exit 1 || true
```

Optional stronger review should resolve every watched SQLite path and confirm it remains under `$run_dir`.

## Work-Pack Impact

`SWU-RUNTIME-003` must cite this artifact as a source contract.

`SWU-RUNTIME-003` is unblocked when:

- `RUN.json` records adapter profile evidence,
- `STATUS.json` records validation grade evidence,
- `codex-exec` implements classifier-based status mapping,
- event contributions flow through runner-owned `events.jsonl`,
- Codex state safety checks allow run-local SQLite while forbidding shared/symlinked source SQLite.
- status, adapter status, validation grade, target kind, and loop role remain inside the documented enums.

## Next Route

Continue `SWU-RUNTIME-003` with the corrected Codex state isolation policy.
