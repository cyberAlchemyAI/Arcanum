# Single Command Surface Refresh

## Decision

Collapse the runtime command model around one user-facing tool:

```text
tools/arcanum
```

`tools/arcanum` owns command resolution, prompt construction, optional runtime envelope creation, Codex CLI execution, requested output capture, and observability closeout.

`tools/arcanum-runtime-run` should no longer be the conceptual runtime model. It may remain temporarily as a deprecated compatibility shim while existing fixtures and scripts are migrated, but new design and validation should target `tools/arcanum --exec`.

Single command surface does not mean single runtime. `tools/arcanum` is the front door; runtime adapters remain the extension boundary. Codex stays one selectable adapter, normally `codex-exec`.

## Why

The two-tool model added complexity without enough value after two corrections:

- Codex state must not be copied or symlinked into run folders.
- Command output should be written as the command output, not duplicated through runtime-owned `RESULT.md`.

Once those are true, the runtime runner is mostly an envelope/status wrapper around a normal CLI command. Keeping it as a separate tool makes the architecture harder to reason about and risks reintroducing split ownership.

## New Execution Shape

```text
tools/arcanum --exec --output <output> <command> <request>
  -> resolve .codex/commands/<command>.md
  -> build the normal Arcanum command prompt
  -> optionally create .arcanum/runtime/runs/<run-id>/ envelope
  -> select adapter, defaulting to codex-exec when omitted
  -> run selected adapter with <output> as the command response path
  -> record status/events/profile when envelope is enabled
  -> emit observed invocation closeout
```

Adapter-specific form:

```text
tools/arcanum --exec --adapter <adapter-id> --output <output> <command> <request>
```

The command owns its normal artifacts. The requested `--output` is the command's final response. Runtime envelope files are evidence about the invocation, not a replacement result channel.

## Ownership Rules

`tools/arcanum` owns:

- command resolution,
- runtime/envelope id,
- adapter selection,
- adapter profile resolution,
- handoff prompt,
- requested output path,
- observability closeout,
- optional status/event evidence.

The selected adapter owns:

- runtime-specific translation,
- runtime-specific execution,
- runtime-specific state preparation,
- raw outcome classification.

The invoked command owns:

- its output contract,
- target development artifacts,
- target-owned paths under the declared write scope.

Runtime envelope owns only:

- `HANDOFF.md`,
- `RUN.json` or successor invocation metadata,
- `STATUS.json` or successor status metadata,
- `events.jsonl`,
- adapter profile/log evidence when useful.

Runtime envelope must not own:

- duplicate `RESULT.md` for successful command execution,
- Codex auth/config links,
- copied Codex SQLite state,
- command-owned target artifacts.

## Compatibility Policy

Keep `tools/arcanum-runtime-run` only if needed as a short-lived shim:

```text
tools/arcanum-runtime-run ... -> tools/arcanum --exec ...
```

The shim must not be the source of truth for new runtime semantics.

## Adapter Surface

Minimum adapter-facing surface:

```bash
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter <adapter-id>
tools/arcanum --exec --adapter <adapter-id> --output <path> <command> <request>
```

V1 adapters:

- `dry-run`
- `codex-exec`

`dry-run` must remain useful after the two-tool collapse because it proves the generic adapter path without invoking Codex. `codex-exec` must remain a profile-backed adapter, not hardcoded generic runtime behavior.

## Required Follow-Up SWU

Add a new implementation slice:

```text
SWU-RUNTIME-008 Collapse Runtime Runner Into tools/arcanum
```

Done criteria:

- `tools/arcanum --exec --output <path> <command> <request>` is the only active command execution path.
- `tools/arcanum --exec --adapter <adapter-id> ...` can select at least `dry-run` and `codex-exec`.
- `tools/arcanum --list-adapters` and `tools/arcanum --resolve-adapter <adapter-id>` expose the available runtime profiles.
- Successful command execution writes directly to `<path>`.
- No successful command run writes runtime `RESULT.md`.
- Runtime envelope, when enabled, records status/events without owning command output.
- Envelope-backed runs record selected adapter profile evidence.
- `tools/arcanum-runtime-run` is deleted or converted into a compatibility shim with deprecation text.
- Active docs no longer describe the two-tool model as canonical.

Validation:

```bash
bash -n tools/arcanum
tools/arcanum --resolve invoke
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter dry-run
tools/arcanum --resolve-adapter codex-exec
tools/arcanum --print-prompt invoke "define runtime smoke"
tools/arcanum --exec --adapter dry-run --output /tmp/arcanum-dry-run-output.md invoke "define runtime smoke"
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --output /tmp/arcanum-one-tool-output.md invoke "define runtime smoke"
test -f /tmp/arcanum-one-tool-output.md
find .arcanum/runtime/runs -path '*/RESULT.md' -newer <pre-run-marker> -print -quit | grep -q . && exit 1 || true
find .arcanum/runtime/runs -path '*/adapter-state/codex-home/auth.json' -print -quit | grep -q . && exit 1 || true
```

If Codex backend/auth is unavailable, the fallback validation is:

- command output path contains the blocked command result,
- envelope status records `blocked`,
- no `RESULT.md` or Codex auth/config links are created.
