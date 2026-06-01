# Codex Exec Migration

## Status

`flag`: migration architecture is defined, but source mutation remains for a later Task Session because the repo has many existing uncommitted edits and `tools/arcanum` is already locally modified.

## Migration Rule

For every active repository surface:

```text
native skill execution first
dispatch-spec for multi-stage strategy
native subagents for model-backed stages
local deterministic tools for validators and scripts
observability hook when available
returned receipt when observability is unavailable
legacy codex-exec only by explicit opt-in
historical generated evidence preserved by default
```

## Current `tools/arcanum` Findings

| Area | Current behavior | Migration target |
| --- | --- | --- |
| Adapter list | `dry-run`, `codex-exec`, and `codex-bypass`. | Add `local-skill` or `native-skill`; mark model CLI adapters legacy. |
| Default adapter | Falls back to `codex-exec` when config is absent. | Default orchestration to `local-skill`; require explicit opt-in for model CLI. |
| Refine native mode | Root `tools/arcanum` can own Refine loop, but child stage adapter defaults to `codex-exec`. | Parent native Refine uses subagents or local inline execution with receipt contract. |
| Prompt guardrail | Child prompt already says not to call nested `tools/arcanum --exec` or `codex exec`. | Keep as anti-pattern text, but move enforcement to dispatch gate and receipt validation. |
| Observability | `tools/arcanum` can create observer envelopes and call `observe-invocation.sh`. | Keep for deterministic closeout; add receipt fallback for native subagents. |

## Surface Scope

The migration includes every active place that invokes, configures, documents, tests, observes, installs, or validates:

- `codex exec`
- `codex-exec`
- `codex-bypass`
- `CODEX_BIN`
- `run-with-codex`
- `observe-run-with-codex`
- `tools/arcanum --exec`

Generated historical evidence is not automatically edited. It is classified so readiness reports can distinguish active policy from preserved prior-run evidence.

## Remaining Reference Classes

Every remaining hit for `codex exec`, `codex-exec`, `codex-bypass`, or orchestration `tools/arcanum --exec` should be classified into one of these buckets:

| Class | Keep? | Rule |
| --- | --- | --- |
| `legacy-adapter-profile` | yes temporarily | Must say explicit opt-in only. |
| `migration-note` | yes | Must explain replacement path. |
| `blocked-anti-pattern` | yes | Must describe nested model runtime as blocked. |
| `deterministic-compatibility` | yes | Only for resolving commands, dry-run, validation, or output handoff. |
| `implicit-default` | no | Replace with `local-skill` or native subagent contract. |
| `required-orchestration-runtime` | no | Replace with dispatch-backed native skill/subagent execution. |
| `active-experiment-runner` | migrate | Prefer native skill/subagent execution; keep Codex CLI only as explicit legacy adapter proof. |
| `active-installer-config` | migrate | Defaults should use local/native skill runtime; legacy model CLI requires explicit opt-in. |
| `active-observability-path` | migrate | Observation must accept hooks, deterministic wrappers, or returned receipts, not only `tools/arcanum --exec`. |
| `historical-generated-evidence` | preserve | Do not rewrite by default; exclude from active readiness blockers after classification. |

## Proposed `tools/arcanum` Adapter Shape

```json
{
  "adapter_id": "local-skill",
  "runtime_kind": "native-codex-skill-surface",
  "execution_mode": "parent-orchestrated",
  "state_model": "current-thread-and-native-subagents",
  "isolation_model": "no-nested-codex-cli",
  "input_shape": "command-prompt-plus-dispatch-step",
  "output_shape": "artifact-plus-stage-receipt",
  "failure_model": "passed|flagged|blocked|interrupted|timeout",
  "capabilities": [
    "execute model-backed stages through native skill/subagent runtime",
    "return telemetry receipt when observer append is unavailable"
  ],
  "limitations": [
    "not callable as an autonomous shell-only model runtime",
    "requires parent Codex agent to own subagent spawn and join"
  ],
  "validation_surface": [
    "adapter profile evidence",
    "dispatch-spec validation",
    "stage receipt validation",
    "observer or fallback telemetry receipt"
  ]
}
```

## Migration Tasks

1. Inventory every active and historical `codex exec` surface.
2. Add `local-skill` adapter metadata without changing the default.
3. Add a dispatch profile fixture that requires `local-skill` for orchestration stages.
4. Change Refine benchmark validation to parent-owned subagent receipts.
5. Change `ARCANUM_REFINE_STAGE_ADAPTER` default from `codex-exec` to `local-skill` only after the Refine prototype passes.
6. Change installer/bootstrap default adapter from `codex-exec` to `local-skill` for Codex runtimes.
7. Migrate Experiment Harness and Invoke example runners away from required `codex exec` promotion evidence.
8. Migrate Observed Invocation Loop and framework observability docs to hook/native receipt/deterministic wrapper language.
9. Keep `codex-exec` and `codex-bypass` available as legacy explicit adapters until all benchmark smoke routes pass.
10. Remove or rewrite docs that require nested `codex exec` for ordinary orchestration.
11. Preserve generated prior-run evidence unless a cleanup task explicitly owns generated artifact migration.

## Acceptance Evidence

- `tools/arcanum --resolve-adapter local-skill` prints the adapter profile.
- `tools/arcanum --get-default-adapter` returns `local-skill` for new installs or explicit repo config.
- Refine benchmark validation produces no implicit nested model-backed CLI calls.
- Stage artifacts include receipts with `dispatch_id`, `step_id`, status, artifact paths, validation, observer status, and blockers.
- Observability append happens when `.arcanum/observability/` exists; otherwise the parent records the returned receipt as fallback telemetry.
- Grep report has no unclassified `codex-exec` or `codex exec` references in orchestration docs.
- Grep report has no unclassified active `codex exec` surfaces anywhere in the repo.
- Historical generated evidence is separated from active runtime policy.
