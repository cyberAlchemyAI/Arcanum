# Execution Pack: Durable Arcanum Runtime Interface

## Purpose

Provide medium-complexity execution choreography for the runtime implementation package.

## Execution Principle

Work proceeds one SWU at a time. Later layers remain blocked until required promotion evidence exists.

## Waves

| Wave | Layer | SWUs | Goal | Gate |
| --- | --- | --- | --- | --- |
| W0 Runtime Contract Proof | L0 | SWU-RUNTIME-001, SWU-RUNTIME-002 | Prove durable folder contract and dry-run execution. | Both SWUs pass; runtime folder JSON validates. |
| W1 Codex Adapter Proof | L1 | SWU-RUNTIME-003 | Prove Codex is an isolated adapter. | Passed in `tools/development/task-sessions/20260525T2040Z-swu-runtime-003.md`: adapter profile evidence, classified status, execution validation, contained run-local SQLite allowed, symlinked shared SQLite blocked. |
| W2 Command Compatibility | L2 | SWU-RUNTIME-004, SWU-RUNTIME-004.5 | Prove `tools/arcanum --exec` can delegate through runtime runner and reproduce command-owned artifacts. | Passed in `tools/development/task-sessions/20260525T2055Z-swu-runtime-004.md` and `tools/development/task-sessions/20260525T2210Z-swu-runtime-004-5.md`. |
| W3 Orchestrator Migration | L3 | SWU-RUNTIME-005, SWU-RUNTIME-006, SWU-RUNTIME-007 | Migrate active refine/task-session/context-builder runtime contracts. | Passed in `tools/development/task-sessions/20260525T2221Z-swu-runtime-005-006.md` and `tools/development/task-sessions/20260525T2230Z-swu-runtime-007.md`. |
| W4 Single Command Surface | L4 | SWU-RUNTIME-008 | Collapse active execution into `tools/arcanum` while preserving adapter selection. | Passed in `tools/development/task-sessions/20260526T1301Z-swu-runtime-008.md`. |
| W5 Install Selection And Interchange | L5 | SWU-RUNTIME-009 | Select default runtime adapter during install and allow safe switching after install. | Passed in `tools/development/task-sessions/20260526T1452Z-swu-runtime-009.md`. |
| W6 Codex Environment Repair | L6 | SWU-RUNTIME-010 | Add precise `codex-exec` environment preflight and private state policy. | Ready; preflight distinguishes state, sandbox, backend/auth, and output-reported blocks. |

## Dependency Order

```text
SWU-RUNTIME-001
  -> SWU-RUNTIME-002
    -> SWU-RUNTIME-003
      -> SWU-RUNTIME-004
        -> SWU-RUNTIME-004.5
          -> SWU-RUNTIME-005
          -> SWU-RUNTIME-006
          -> SWU-RUNTIME-007
            -> SWU-RUNTIME-008
              -> SWU-RUNTIME-009
                -> SWU-RUNTIME-010
```

## Parallelization

- No parallel work before W0 completes.
- `SWU-RUNTIME-005` and `SWU-RUNTIME-006` may run in parallel only after `SWU-RUNTIME-004.5` passes.

## Promotion Evidence

### W0

Required:

```bash
test -f framework/runtime/README.md
test -f framework/runtime/templates/RUNTIME-HANDOFF.md
test -f framework/runtime/templates/RUN.json
test -f framework/runtime/templates/STATUS.json
test -x tools/arcanum-runtime-run
tools/arcanum-runtime-run --adapter dry-run --handoff framework/runtime/development/fixtures/dry-run/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-dry-run
jq empty /tmp/arcanum-runtime-dry-run/RUN.json
jq empty /tmp/arcanum-runtime-dry-run/STATUS.json
jq -e '.schema_version == "arcanum.runtime.run.v1"' /tmp/arcanum-runtime-dry-run/RUN.json
jq -e '.schema_version == "arcanum.runtime.status.v1"' /tmp/arcanum-runtime-dry-run/STATUS.json
test -f /tmp/arcanum-runtime-dry-run/RESULT.md
test -f /tmp/arcanum-runtime-dry-run/events.jsonl
```

### W1

Required:

```bash
tools/arcanum-runtime-run --adapter codex-exec --handoff framework/runtime/development/fixtures/codex-exec/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-codex-exec
jq empty /tmp/arcanum-runtime-codex-exec/RUN.json
jq empty /tmp/arcanum-runtime-codex-exec/STATUS.json
jq -e '.adapter_profile_path == "artifacts/adapter-profile.json"' /tmp/arcanum-runtime-codex-exec/RUN.json
jq -e '.validation_grade == "adapter-safety" or .validation_grade == "execution"' /tmp/arcanum-runtime-codex-exec/STATUS.json
jq -e '.status == "passed" or .status == "flagged" or .status == "blocked" or .status == "failed"' /tmp/arcanum-runtime-codex-exec/STATUS.json
find /tmp/arcanum-runtime-codex-exec/adapter-state/codex-home \( -name '*.sqlite' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name 'state_*.sqlite*' -o -name 'logs_*.sqlite*' -o -name 'goals_*.sqlite*' \) -type l -print -quit | grep -q . && exit 1 || true
```

If network/backend access blocks Codex execution, W1 may pass only as `adapter-safety` validation when `STATUS.json.status=blocked`, the blocked reason is exact, and isolated adapter state checks pass. Run-local SQLite files do not block W1 unless they are shared, symlinked, or resolve outside the runtime run folder. A blocked run does not count as `execution` validation.

### W2

Transport proof:

```bash
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output /tmp/arcanum-runtime-invoke-output.md invoke "define runtime smoke"
test -f /tmp/arcanum-runtime-invoke-output.md
```

Artifact reproduction proof:

```bash
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output /tmp/arcanum-runtime-invoke-design-output.md invoke "<artifact-producing invoke design fixture request>"
test -f /tmp/arcanum-runtime-invoke-design-output.md
jq empty <runtime-run>/RUN.json <runtime-run>/STATUS.json
jq -e '.status == "passed" or .status == "flagged"' <runtime-run>/STATUS.json
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/INVOKE-DESIGN.md
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/ARCHITECTURE-BUNDLE.md
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/GLOSSARY-CONSISTENCY.md
test -f framework/runtime/development/fixtures/invoke-design-artifacts/target/development/DESIGN-TRANSPORT.md
```

W2 does not promote until both transport and artifact reproduction pass.

### W3

Required:

```bash
arcana/refine/development/run-validation-fixtures.sh
rg -n "GOAL-HANDOFF|Codex Goal|codex-goal|/goal" arcana/refine/SKILL.md arcana/refine/README.md arcana/refine/REFINEMENT-LOOP.md arcana/refine/templates arcana/refine/examples .codex/commands/refine.md
rg -n "Codex Goal|codex-goal|/goal|runtime-goal|goal-like|goal handoff|Goal handoff" arcana/task-session/SKILL.md arcana/task-session/README.md .codex/commands/task-session.md
```

The stale-language check may return only explicit legacy/migration notes.

### W4

Required:

```bash
bash -n tools/arcanum
tools/arcanum --resolve invoke
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter dry-run
tools/arcanum --resolve-adapter codex-exec
tools/arcanum --print-prompt invoke "define runtime smoke"
marker="$(mktemp)"
tools/arcanum --exec --adapter dry-run --output /tmp/arcanum-dry-run-output.md invoke "define runtime smoke"
test -f /tmp/arcanum-dry-run-output.md
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --output /tmp/arcanum-one-tool-output.md invoke "define runtime smoke" || true
test -f /tmp/arcanum-one-tool-output.md
find .arcanum/runtime/runs -name RESULT.md -newer "$marker" -print -quit | grep -q . && exit 1 || true
find .arcanum/runtime/runs -path '*/adapter-state/codex-home/auth.json' -newer "$marker" -print -quit | grep -q . && exit 1 || true
```

If Codex backend/auth is unavailable, W4 may pass as adapter-safety only when the requested output contains the blocked command result and the envelope records the blocked reason without creating runtime `RESULT.md` or Codex auth/config links. The non-Codex `dry-run` adapter must still pass through the same `tools/arcanum --exec --adapter` path.

### W5

Required:

```bash
tmp_target=/tmp/arcanum-install-runtime-selection
tools/bootstrap_arcanum.sh --target "$tmp_target" --runtime codex --default-adapter codex-exec --dry-run
tools/bootstrap_arcanum.sh --target "$tmp_target" --runtime codex --default-adapter codex-exec --force
jq empty "$tmp_target/.arcanum/runtime/config.json"
jq -e '.command_surface == "codex"' "$tmp_target/.arcanum/runtime/config.json"
jq -e '.default_adapter == "codex-exec"' "$tmp_target/.arcanum/runtime/config.json"
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter dry-run
tools/arcanum --exec --output /tmp/arcanum-default-adapter-output.md invoke "define runtime smoke"
tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-explicit-adapter-output.md invoke "define runtime smoke" || true
rg -n "auth|token|sqlite|config.toml|installation_id|models_cache" "$tmp_target/.arcanum/runtime/config.json" && exit 1 || true
find "$tmp_target/.arcanum/runtime" -type l -print -quit | grep -q . && exit 1 || true
```

### W6

Required:

```bash
tools/arcanum --preflight-adapter codex-exec || true
rg -n "^\\.arcanum/runtime/private/" .gitignore
ARCANUM_RUNTIME_ENVELOPE=1 tools/arcanum --exec --adapter codex-exec --output /tmp/arcanum-codex-preflight-output.md invoke "define runtime smoke" || true
latest="$(find .arcanum/runtime/runs -maxdepth 1 -type d -name 'arcanum-command-invoke-*' | sort | tail -n 1)"
jq -e '.blocked_reason == "codex-state-unavailable" or .blocked_reason == "codex-sandbox-unavailable" or .blocked_reason == "codex-backend-or-auth-unavailable" or .blocked_reason == "codex-output-reported-block" or .status == "passed"' "$latest/STATUS.json"
find "$latest" \( -name 'auth.json' -o -name 'config.toml' -o -name '*.sqlite*' \) -print -quit | grep -q . && exit 1 || true
```

## Blockers

- W1 blocks if isolated adapter state cannot be prepared.
- W2 passed; requested output compatibility and command-owned artifact reproduction were preserved behind the feature flag.
- W3 blocks if active refine validation still requires `GOAL-HANDOFF.md` or active task-session docs still require native goal handoff.
- W4 passed; active execution is owned by `tools/arcanum`, adapter selection includes non-Codex `dry-run`, envelope-backed runs record adapter profile evidence, and successful command execution no longer writes runtime `RESULT.md`.
- W5 passed; install can select a default adapter, runtime switching does not require command file edits, and installed runtime config stores only non-secret adapter metadata.
- W6 blocks if local Codex environment failures are classified as generic backend/auth, if private state is not gitignored, or if run evidence contains auth/config/SQLite state.
