## Invoke Result

- Mode: refresh
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/design.md` and `spells/invoke/plan.md`
- Outputs: `ADAPTER-CONTRACT-DECISIONS.md`, `SCHEMA-DISCIPLINE-INTEGRATION.md`, `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`, `SINGLE-COMMAND-SURFACE-REFRESH.md`, `RUNTIME-ADAPTER-SURFACE-REFRESH.md`, `INSTALL-RUNTIME-SELECTION-REFRESH.md`, `CODEX-EXEC-ENVIRONMENT-REPAIR.md`, context-builder runtime handoff refresh, refreshed design artifacts, refreshed plan artifacts
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: existing runtime architecture and medium-complexity plan package
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Work-pack: `WORK-PACK.md`
- Decisions: adapter contract repair is now a required design/plan input before `codex-exec`; runtime evidence records adapter profile and validation grade; `tools/arcanum` is the single active command surface; the single surface must still support selectable runtime adapters such as `dry-run` and `codex-exec`; installation must select a default runtime adapter separately from command surface; runtime interchange must be possible through config, explicit `--adapter`, and adapter discovery; nested Codex environment failures must distinguish state, sandbox, backend/auth, and output-reported blocks; `tools/arcanum-runtime-run` is no longer the conceptual runtime model and should become a temporary shim or be removed; schema discipline is adopted as a lightweight runtime contract pattern, not a new dependency; command transport proof is separate from command-owned artifact reproduction proof.
- Unresolved gaps: none blocking for L0; L1 still blocked until L0 passes and adapter contract behavior is implemented.
- Next route: `SWU-RUNTIME-008` to collapse runtime execution into `tools/arcanum`

## Refresh Inputs

- `RUNTIME-ADAPTER-INTERROGATION-REVIEW.md`
- `RUNTIME-ADAPTER-DISTILL-REVIEW.md`
- `RUNTIME-ADAPTER-PATTERN.md`
- `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `RUNTIME-SCHEMAS.md`
- `WORK-PACK.md`
- `EXECUTION-PACK.md`
- `tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md`
- `tools/development/handoffs/20260525-schema-discipline-arcanum-cyberalchemy-handoff.md`

## Refreshed Artifacts

- `ADAPTER-CONTRACT-DECISIONS.md`
- `SCHEMA-DISCIPLINE-INTEGRATION.md`
- `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`
- `RUNTIME-ADAPTER-SURFACE-REFRESH.md`
- `INSTALL-RUNTIME-SELECTION-REFRESH.md`
- `CODEX-EXEC-ENVIRONMENT-REPAIR.md`
- `INVOKE-DESIGN.md`
- `ARCHITECTURE-BUNDLE.md`
- `DESIGN-TRANSPORT.md`
- `RUNTIME-ADAPTER-PATTERN.md`
- `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `RUNTIME-ADAPTER-DESIGN-TRANSPORT.md`
- `RUNTIME-SCHEMAS.md`
- `INVOKE-PLAN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `EXECUTION-PACK.md`
- `PLAN-TRANSPORT.md`
- `RESULT.md`
- `evidence-index.json`

## Refresh Summary

The adapter review found a real implementation ambiguity: the architecture correctly treats Codex as an adapter, but the plan did not yet force the first execution adapter to preserve profile evidence, validation grade evidence, event ownership, or blocked-vs-failed classification.

This refresh promotes that critique into a design decision artifact and makes the plan consume it.

## State Policy Refresh

The task-session implementation pass found that Codex creates SQLite files during normal startup. The selected repair is:

- allow Codex-created SQLite when it is contained inside the run-local adapter state,
- forbid shared, copied, or symlinked SQLite from source Codex home,
- block only when watched SQLite files are symlinks or resolve outside the runtime run folder.

This keeps the real safety property: no shared mutable Codex database across runtime runs.

## Schema Discipline Refresh

The `knowledge-taxonomy` context pack contributes reusable schema practice, not runtime infrastructure. This refresh adopts the low-overhead pieces into the runtime package:

- field tiers for runtime docs/templates,
- inline enum lists for implementer-facing contracts,
- stable ids and paths for cross-artifact references,
- provenance for adapter profile evidence,
- validation grades as proof levels,
- shell/`jq` validation before schema libraries.

Cross-Arcanum and CyberAlchemy schema discipline remains a separate follow-up design thread through `tools/development/handoffs/20260525-schema-discipline-arcanum-cyberalchemy-handoff.md`.

## Command Artifact Reproduction Refresh

`SWU-RUNTIME-004` proved transport only. The runtime path can produce `RESULT.md`, copy it to `--output`, and record runtime evidence, but that does not yet prove a normal UI/IDE-like command run that writes invoke-owned target artifacts.

This refresh adds `SWU-RUNTIME-004.5` before L3. It requires a real artifact-producing invoke design fixture that writes target development files while the runner keeps ownership of runtime state.

## Runtime Handoff Refresh

The L3 migration exposed one more integration split: Task Session now delegates with `--via runtime`, but Context Builder still advertised only `--handoff codex-goal`.

This refresh adds `SWU-RUNTIME-007` and aligns the active Context Builder contract with the generic runtime model:

- `transmutations/context-builder/SKILL.md` uses `--handoff runtime`,
- `transmutations/context-builder/README.md` describes generic runtime handoff packs,
- `.codex/commands/context-builder.md` mirrors the active contract,
- `transmutations/context-builder/templates/runtime-handoff-pack.md` and `runtime-handoff-index.json` provide generic template shapes.

Legacy native-goal templates remain as compatibility artifacts, but new active runtime handoffs should use the generic runtime templates.

## Single Command Surface Refresh

The latest correction removes the reason for two active tools. `tools/arcanum-runtime-run` was useful while the runtime model owned Codex state and runtime `RESULT.md`, but both are now rejected:

- Codex must run through the normal CLI environment by default.
- The command's requested `--output` is the final response path.
- Runtime envelope files are invocation evidence, not a second result channel.

This refresh adds `SINGLE-COMMAND-SURFACE-REFRESH.md` and `SWU-RUNTIME-008`. The implementation target is one active command surface:

```text
tools/arcanum --exec --output <path> <command> <request>
```

`tools/arcanum-runtime-run` may remain only as a deprecated compatibility shim during migration.

## Runtime Adapter Surface Refresh

The single command surface still needs to make other runtimes easy to use. This refresh adds `RUNTIME-ADAPTER-SURFACE-REFRESH.md` and tightens `SWU-RUNTIME-008`:

- `tools/arcanum` is the front door, not the only runtime.
- `tools/arcanum --exec --adapter <adapter-id> ...` selects a runtime.
- `tools/arcanum --list-adapters` and `tools/arcanum --resolve-adapter <adapter-id>` expose runtime profiles.
- `dry-run` remains the generic non-Codex proof adapter.
- `codex-exec` remains the Codex adapter, not the architecture.
- Envelope-backed runs record selected adapter profile evidence.

## Install Runtime Selection Refresh

Runtime adapter selection belongs in installation, not only at execution time. This refresh adds `INSTALL-RUNTIME-SELECTION-REFRESH.md` and a follow-up implementation slice:

```text
SWU-RUNTIME-009 Install-Time Runtime Selection And Interchange
```

The installer should separate:

- command surface: `--runtime codex|none` for compatibility,
- default runtime adapter: `--default-adapter <adapter-id>`.

Installed repositories should get `.arcanum/runtime/config.json` with the selected default adapter and profile paths. The config must not store secrets, Codex auth/config copies, or mutable runtime state.

Interchange should be exposed through:

```bash
tools/arcanum --get-default-adapter
tools/arcanum --set-default-adapter <adapter-id>
tools/arcanum --exec --adapter <adapter-id> --output <path> <command> <request>
```

## Codex Exec Environment Repair

The latest nested Codex checks showed environment-specific blockers, not a generic backend/auth issue:

- `codex-state-unavailable`: Codex cannot write/open its local state DB from the nested environment.
- `codex-sandbox-unavailable`: nested shell tool execution cannot find usable `bubblewrap`.

This refresh adds `CODEX-EXEC-ENVIRONMENT-REPAIR.md` and a follow-up slice:

```text
SWU-RUNTIME-010 Codex Exec Environment Preflight And Private State
```

The selected direction is:

- keep runtime run folders evidence-only,
- keep Codex auth/config/SQLite out of run folders,
- optionally support a stable gitignored `.arcanum/runtime/private/codex-home/`,
- add `tools/arcanum --preflight-adapter codex-exec`,
- classify state, sandbox, backend/auth, and output-reported blocks separately.

## Validation

Validated:

```bash
jq empty tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/evidence-index.json
git diff --check -- tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract
```

Both checks passed.

## Observability Closeout

OBSERVATION:

- Local command resolution confirmed `/invoke` resolves to `.codex/commands/invoke.md`.
- This refresh was executed as local skill-contract authoring because the durable runtime runner is still an implementation target.

LEDGER:

- Inputs: adapter interrogation review, adapter distill review, knowledge-taxonomy context pack, schema-discipline handoff, existing runtime design and plan artifacts.
- Outputs: adapter contract decisions, schema-discipline integration, refreshed design and plan artifacts.
- Verdict: pass.

REFLECTION_TRIGGER:

- Trigger if a successful `tools/arcanum --exec` run creates a runtime `RESULT.md`, creates Codex auth/config links under `.arcanum/runtime/runs`, cannot select a non-Codex adapter, or if runtime schemas drift from the lightweight schema-discipline contract.

RECOMMENDATION:

- Continue implementation at `SWU-RUNTIME-009` so install-time adapter selection and runtime interchange are first-class. Then continue `SWU-RUNTIME-010` for Codex environment preflight and private state.

DEDUPE_KEY:

- `invoke-refresh:durable-runtime:single-command-surface:20260526`
