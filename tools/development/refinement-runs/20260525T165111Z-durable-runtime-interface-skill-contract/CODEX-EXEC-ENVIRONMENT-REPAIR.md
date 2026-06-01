# Codex Exec Environment Repair

## Decision

`codex-exec` needs an explicit environment preflight and repair path separate from adapter selection.

Recent local runs exposed two different nested Codex blockers:

- `codex-state-unavailable`: Codex could not initialize its local SQLite state because the active sandbox made `~/.codex/state_*.sqlite` read-only.
- `codex-sandbox-unavailable`: nested Codex shell execution can fail when `bubblewrap`/`bwrap` is unavailable to the nested Codex process.

These are not generic backend/auth failures. They are local runtime environment failures and must be classified separately.

## Runtime State Policy

Do not store Codex auth, config, or SQLite inside runtime run evidence folders.

Accepted locations:

- Runtime evidence: `.arcanum/runtime/runs/<run-id>/`
- Installed runtime config: `.arcanum/runtime/config.json`
- Adapter profile snapshots: `.arcanum/runtime/adapters/*.json`
- Private local adapter state: `.arcanum/runtime/private/`

`.arcanum/runtime/private/` must be gitignored and must not be copied into task evidence, package fixtures, or runtime run folders.

## Codex Private State Strategy

For nested `codex exec`, Arcanum should support a stable private Codex state home:

```text
.arcanum/runtime/private/codex-home/
```

Rules:

- It is not per-run.
- It is not copied into `.arcanum/runtime/runs/`.
- It is not listed as evidence.
- It must be gitignored.
- It may contain mutable Codex state produced by Codex.
- Auth/config handling remains explicit and should not be silently copied into evidence.

The default should remain normal Codex CLI state when available. When normal Codex state is not writable, the adapter can block with `codex-state-unavailable` and recommend configuring private state.

## Preflight Surface

Add a lightweight preflight command:

```bash
tools/arcanum --preflight-adapter codex-exec
```

Minimum checks:

- Codex binary resolves.
- `codex exec --help` works.
- writable state strategy is available:
  - normal Codex state is writable, or
  - configured private state path is writable.
- sandbox support is likely available:
  - `bwrap` is on PATH, or
  - Codex can run a no-tool smoke without tripping sandbox startup.

The preflight should report precise blockers:

- `codex-binary-missing`
- `codex-state-unavailable`
- `codex-sandbox-unavailable`
- `codex-backend-or-auth-unavailable`

## SWU Impact

Add a follow-up slice after install-time selection:

```text
SWU-RUNTIME-010 Codex Exec Environment Preflight And Private State
```

Dependencies:

- `SWU-RUNTIME-009`

Done criteria:

- `.gitignore` excludes `.arcanum/runtime/private/`.
- `tools/arcanum --preflight-adapter codex-exec` reports precise environment status.
- `codex-exec` distinguishes state, sandbox, backend/auth, and output-reported block reasons.
- installed runtime config may reference a private state policy without storing secrets.
- runtime run folders still contain no auth/config/SQLite state.

Validation:

```bash
tools/arcanum --preflight-adapter codex-exec || true
rg -n "^\\.arcanum/runtime/private/" .gitignore
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-codex-preflight-output.md invoke "define runtime smoke" || true
latest="$(find .arcanum/runtime/runs -maxdepth 1 -type d -name 'arcanum-command-invoke-*' | sort | tail -n 1)"
jq -e '.blocked_reason == "codex-state-unavailable" or .blocked_reason == "codex-sandbox-unavailable" or .blocked_reason == "codex-backend-or-auth-unavailable" or .status == "passed"' "$latest/STATUS.json"
find "$latest" \( -name 'auth.json' -o -name 'config.toml' -o -name '*.sqlite*' \) -print -quit | grep -q . && exit 1 || true
```

## Reflection Trigger

Trigger another refresh if:

- `codex-exec` reports environment failures as backend/auth,
- fixing Codex state requires copying auth/config into run evidence,
- private mutable state is not gitignored,
- runtime runs contain Codex auth/config/SQLite files.
