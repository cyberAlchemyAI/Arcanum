# Context Pack: SWU-RUNTIME-009

## Context Pack Summary

- Task session: `SWU-RUNTIME-009`
- Work-pack: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- Selected task: `TASK-RUNTIME-008 Add Install-Time Runtime Selection And Interchange`
- Mode: local execution
- Strict coverage: pass
- Runtime delegation: none

## Controlling Sources

- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/INSTALL-RUNTIME-SELECTION-REFRESH.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/EXECUTION-PACK.md`
- `tools/arcanum`
- `tools/bootstrap_arcanum.sh`
- `tools/install_arcanum.sh`
- `framework/runtime/README.md`
- `spells/arcanum-bootstrap/README.md`

## Task Contract

`tools/arcanum --exec` must select the execution adapter from an explicit override, environment override, installed runtime config, or compatibility fallback. Arcanum install must create the non-secret runtime config needed to make that default adapter interchangeable.

Required behavior:

- `tools/bootstrap_arcanum.sh --default-adapter <adapter-id>` is accepted.
- `tools/install_arcanum.sh` forwards `--default-adapter`.
- Installed `.arcanum/runtime/config.json` records `command_surface`, `default_adapter`, and adapter profile paths.
- Installed adapter profiles are descriptive metadata only.
- `tools/arcanum --get-default-adapter` and `--set-default-adapter <adapter-id>` work.
- `tools/arcanum --exec --adapter <adapter-id>` overrides config.
- Runtime switching does not require editing command files.

## Write Scope

- `tools/arcanum`
- `tools/bootstrap_arcanum.sh`
- `tools/install_arcanum.sh`
- `framework/runtime/README.md`
- `spells/arcanum-bootstrap/README.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/INSTALL-RUNTIME-SELECTION-REFRESH.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/EXECUTION-PACK.md`
- `tools/development/context-packs/20260526-swu-runtime-009-task-session.md`
- `tools/development/task-sessions/20260526T1452Z-swu-runtime-009.md`

## Gate Check

- Dependencies: pass; `SWU-RUNTIME-008` is recorded passed.
- Source context: pass; install-selection refresh is present.
- Write scope: pass.
- Validation surface: pass.
- User approval: task-session invocation implies execute next ready SWU.

## Validation Surface

```bash
bash -n tools/arcanum
bash -n tools/bootstrap_arcanum.sh
bash -n tools/install_arcanum.sh
tools/bootstrap_arcanum.sh --target /tmp/arcanum-install-runtime-selection-swu009 --runtime codex --default-adapter codex-exec --dry-run
tools/bootstrap_arcanum.sh --target /tmp/arcanum-install-runtime-selection-swu009-clean --runtime codex --default-adapter codex-exec --force
jq empty /tmp/arcanum-install-runtime-selection-swu009-clean/.arcanum/runtime/config.json
jq -e '.command_surface == "codex" and .default_adapter == "codex-exec"' /tmp/arcanum-install-runtime-selection-swu009-clean/.arcanum/runtime/config.json
jq empty /tmp/arcanum-install-runtime-selection-swu009-clean/.arcanum/runtime/adapters/dry-run.json
jq empty /tmp/arcanum-install-runtime-selection-swu009-clean/.arcanum/runtime/adapters/codex-exec.json
tools/arcanum --set-default-adapter dry-run
tools/arcanum --get-default-adapter
tools/arcanum --exec --output /tmp/arcanum-default-adapter-output.md invoke "define runtime smoke"
tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-explicit-adapter-output.md invoke "define runtime smoke"
tools/arcanum --set-default-adapter codex-exec
rg -n "auth|token|sqlite|config\.toml|installation_id|models_cache" /tmp/arcanum-install-runtime-selection-swu009-clean/.arcanum/runtime/config.json /tmp/arcanum-install-runtime-selection-swu009-clean/.arcanum/runtime/adapters .arcanum/runtime/config.json .arcanum/runtime/adapters
find /tmp/arcanum-install-runtime-selection-swu009-clean/.arcanum/runtime -type l -print
git diff --check -- tools/arcanum tools/bootstrap_arcanum.sh tools/install_arcanum.sh framework/runtime/README.md spells/arcanum-bootstrap/README.md tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/INSTALL-RUNTIME-SELECTION-REFRESH.md
```
