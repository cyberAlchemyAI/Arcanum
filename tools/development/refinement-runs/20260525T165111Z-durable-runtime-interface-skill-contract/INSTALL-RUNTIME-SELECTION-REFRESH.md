# Install Runtime Selection Refresh

## Decision

Arcanum installation must select the default runtime adapter, and Arcanum must expose a simple way to interchange runtimes after install.

Separate two concepts that are currently blurred:

- command surface: where Arcanum commands are installed, such as Codex slash-style command files or none,
- runtime adapter: how `tools/arcanum --exec` executes a command, such as `codex-exec`, `dry-run`, or a future adapter.

Current `--runtime codex` should remain as compatibility for "install Codex command surface." New design should add an explicit adapter selection field instead of overloading `--runtime`.

## Installer Surface

Recommended bootstrap options:

```bash
tools/bootstrap_arcanum.sh \
  --target <repo> \
  --runtime codex \
  --default-adapter codex-exec
```

Compatibility behavior:

- `--runtime codex` with no `--default-adapter` selects `codex-exec`.
- `--runtime none` with no `--default-adapter` selects no execution adapter, or `dry-run` only when validation fixtures explicitly request it.
- Existing installs that omit `--default-adapter` keep current behavior.

Future-friendly aliases may be added later:

```bash
tools/bootstrap_arcanum.sh --command-surface codex --default-adapter codex-exec
```

Do not require that future adapters install Codex command files. A non-Codex adapter may still use `tools/arcanum` directly.

## Installed Runtime Config

Installation should write a small, non-secret configuration file:

```text
.arcanum/runtime/config.json
```

Shape:

```json
{
  "schema_version": "arcanum.runtime.config.v1",
  "command_surface": "codex",
  "default_adapter": "codex-exec",
  "adapters": {
    "codex-exec": {
      "enabled": true,
      "profile_path": ".arcanum/runtime/adapters/codex-exec.json"
    },
    "dry-run": {
      "enabled": true,
      "profile_path": ".arcanum/runtime/adapters/dry-run.json"
    }
  }
}
```

Rules:

- The config must not contain auth tokens, Codex config copies, SQLite paths, or local model secrets.
- It may record adapter ids, profile paths, command surface, and default selection.
- Adapter profile snapshots are safe descriptive metadata.

## Runtime Interchange Surface

Minimum interchange commands:

```bash
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter <adapter-id>
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter <adapter-id>
tools/arcanum --exec --adapter <adapter-id> --output <path> <command> <request>
```

Selection precedence:

1. Explicit `tools/arcanum --exec --adapter <adapter-id>`.
2. Environment override, if provided:

```bash
ARCANUM_RUNTIME_ADAPTER=<adapter-id>
```

3. Installed `.arcanum/runtime/config.json` `default_adapter`.
4. Compatibility fallback from command surface, normally `codex-exec` for Codex installs.

## Adapter Registration

V1 can use a static adapter table. Installation should still materialize readable profile snapshots:

```text
.arcanum/runtime/adapters/dry-run.json
.arcanum/runtime/adapters/codex-exec.json
```

Future adapters should be addable by:

1. adding an adapter profile,
2. adding an adapter dispatch branch,
3. enabling it in `.arcanum/runtime/config.json`,
4. validating it through `tools/arcanum --resolve-adapter` and a fixture.

Refine, task-session, invoke, interrogation, and distill should not need command-contract changes when a new runtime adapter is enabled.

## Implemented Surface

Implementation should land in the existing one-tool path, not in a second runner:

- `tools/arcanum --get-default-adapter`
- `tools/arcanum --set-default-adapter <adapter-id>`
- `tools/arcanum --exec --adapter <adapter-id> ...`
- `tools/bootstrap_arcanum.sh --default-adapter <adapter-id>`
- `tools/install_arcanum.sh` forwarding `--default-adapter`

The bootstrap package must write only non-secret runtime selection metadata. It must not copy Codex auth, `config.toml`, SQLite state, model caches, or private runtime directories into `.arcanum/runtime/`.

## SWU Impact

Add a follow-up implementation slice:

```text
SWU-RUNTIME-009 Install-Time Runtime Selection And Interchange
```

Dependencies:

- `SWU-RUNTIME-008` single command surface with adapter selection.

Done criteria:

- bootstrap accepts `--default-adapter <adapter-id>`,
- install writes `.arcanum/runtime/config.json`,
- installed config has no secrets or copied runtime state,
- `tools/arcanum --get-default-adapter` reads config,
- `tools/arcanum --set-default-adapter <adapter-id>` updates config after resolving the adapter,
- `tools/arcanum --exec` uses selection precedence,
- validation proves explicit adapter override and config default selection.

Validation:

```bash
tools/bootstrap_arcanum.sh --target /tmp/arcanum-install-runtime-selection --runtime codex --default-adapter codex-exec --dry-run
tools/bootstrap_arcanum.sh --target /tmp/arcanum-install-runtime-selection --runtime codex --default-adapter codex-exec --force
jq empty /tmp/arcanum-install-runtime-selection/.arcanum/runtime/config.json
jq -e '.default_adapter == "codex-exec"' /tmp/arcanum-install-runtime-selection/.arcanum/runtime/config.json
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter dry-run
tools/arcanum --exec --output /tmp/arcanum-default-adapter-output.md invoke "define runtime smoke"
tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-explicit-adapter-output.md invoke "define runtime smoke"
```

Security checks:

```bash
rg -n "auth|token|sqlite|config.toml|installation_id|models_cache" /tmp/arcanum-install-runtime-selection/.arcanum/runtime/config.json && exit 1 || true
find /tmp/arcanum-install-runtime-selection/.arcanum/runtime -type l -print -quit | grep -q . && exit 1 || true
```

## Reflection Trigger

Trigger another refresh if:

- installer still only asks for `--runtime codex|none` and cannot select the default adapter,
- changing runtime requires editing command files,
- adapter config stores secrets or mutable runtime state,
- `tools/arcanum --exec` ignores explicit adapter override,
- a new adapter requires changing refine/task-session/invoke contracts.
