# Implementation Layering: Durable Arcanum Runtime Interface

## Objective

Layer the runtime implementation so Arcanum gets a durable, generic execution substrate before migrating refine and task-session away from Codex Goal.

## Source Design References

- Define artifact: `INVOKE-DEFINE.md`
- Glossary: `RUNTIME-GLOSSARY.md`
- Design artifact: `INVOKE-DESIGN.md`
- Architecture bundle: `ARCHITECTURE-BUNDLE.md`
- Glossary consistency: `GLOSSARY-CONSISTENCY.md`
- Interrogation repair input: `INTERROGATION-REVIEW.md`
- Distill repair input: `DISTILL-REVIEW.md`
- Runtime schemas: `RUNTIME-SCHEMAS.md`
- Execution pack: `EXECUTION-PACK.md`
- Runtime adapter pattern: `RUNTIME-ADAPTER-PATTERN.md`
- Codex adapter design: `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- Runtime command artifact reproduction: `RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`
- Runtime adapter surface refresh: `RUNTIME-ADAPTER-SURFACE-REFRESH.md`
- Install runtime selection refresh: `INSTALL-RUNTIME-SELECTION-REFRESH.md`
- Adapter contract decisions: `ADAPTER-CONTRACT-DECISIONS.md`
- Schema discipline integration: `SCHEMA-DISCIPLINE-INTEGRATION.md`
- Knowledge taxonomy context pack: `tools/development/context-packs/20260525-knowledge-taxonomy-types-schemas.md`
- Runtime adapter interrogation review: `RUNTIME-ADAPTER-INTERROGATION-REVIEW.md`
- Runtime adapter distill review: `RUNTIME-ADAPTER-DISTILL-REVIEW.md`

## Layer Map

| Layer | Question | Scope | Promotion Evidence |
| --- | --- | --- | --- |
| L0 | Can Arcanum create a valid durable runtime run without external execution? | Runtime docs/templates, schema-discipline field tiers/inline enums, `tools/arcanum-runtime-run`, `dry-run` adapter. | Dry-run fixture creates `RUN.json`, `STATUS.json`, `RESULT.md`, `events.jsonl`; JSON validates; docs/templates preserve required fields and controlled values. |
| L1 | Can Codex execute as an adapter without owning runtime identity or leaking state into run artifacts? | `codex-exec` adapter with normal Codex CLI state by default, adapter profile evidence, classified outcomes, optional isolated state, and validation grades. | Codex adapter records pass/flag/block/fail in runtime artifacts, preserves adapter profile evidence, creates no per-run auth/config links by default, rejects shared/symlinked source SQLite when isolation is enabled, and distinguishes adapter-safety from execution proof. |
| L2 | Can existing command dispatch use the runtime without breaking command resolution and while reproducing command-owned artifacts? | `tools/arcanum --exec` feature-flag route through runtime runner plus artifact-producing invoke fixture. | `ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec ...` writes requested output and runtime evidence; `SWU-RUNTIME-004.5` proves invoke design artifacts are created under declared target scope. |
| L3 | Can active orchestrators consume runtime evidence instead of Codex Goal handoff? | Refine and task-session active runtime docs/templates/validation. | Refine validation requires `RUNTIME-HANDOFF.md`; task-session exposes generic runtime handoff adapter. |
| L4 | Can one command surface execute through multiple runtime adapters? | `tools/arcanum --exec` owns execution and optional envelope evidence; `--adapter`, `--list-adapters`, and `--resolve-adapter` preserve runtime extensibility. | `dry-run` and `codex-exec` both execute through `tools/arcanum`; successful runs do not write runtime `RESULT.md`; envelope-backed runs record adapter profile evidence. |
| L5 | Can installation choose and later interchange runtime adapters? | Bootstrap/runtime config, default adapter get/set, installed adapter profile snapshots. | Bootstrap writes `.arcanum/runtime/config.json`; default adapter can be read and changed; explicit `--adapter` overrides config; config contains no secrets or mutable runtime state. |

## Layer Boundaries

### L0: Runtime Contract Proof

L0 owns the smallest runnable proof. It must not call Codex or mutate active refine/task-session contracts.

L0 has two SWUs. `SWU-RUNTIME-001` creates the contract artifacts; `SWU-RUNTIME-002` proves the contract with the dry-run runner. L0 is not promotable until both pass.

Required outputs:

- `framework/runtime/README.md`
- `framework/runtime/templates/RUNTIME-HANDOFF.md`
- `framework/runtime/templates/RUN.json`
- `framework/runtime/templates/STATUS.json`
- `tools/arcanum-runtime-run`
- dry-run fixture

Contract details are defined in `RUNTIME-SCHEMAS.md`.

Schema-discipline details are defined in `SCHEMA-DISCIPLINE-INTEGRATION.md`. L0 adopts those details only for the runtime artifact family.

### L1: Codex Adapter Proof

L1 proves Codex is an adapter. It must not use native `/goal`.

Required behavior:

- use normal Codex CLI state by default,
- do not create per-run auth/config links by default,
- record selected adapter profile evidence,
- classify raw Codex outcomes before runner status mutation,
- return adapter event contributions rather than writing `events.jsonl` directly,
- run `codex exec`,
- record backend/runtime failures and validation grade in `STATUS.json`,
- write requested command output directly to `--output`.
- allow Codex-created SQLite state only when explicit isolated adapter state is enabled and the state is inside the run-local adapter state.
- never share or symlink SQLite state, logs, goal databases, sockets, or transient runtime files from the source Codex home.

### L2: Command Surface Compatibility

L2 preserves the user-facing `tools/arcanum --exec` shape while moving execution lifecycle into the runtime runner.

Required behavior:

- keep `--resolve` unchanged,
- keep prompt generation semantics,
- generate runtime handoff for exec,
- call runtime runner behind `ARCANUM_RUNTIME_RUNNER=1`,
- copy/link runtime result to requested `--output`.
- if the adapter fails before producing a result, write a blocked summary to the requested `--output`.
- include target artifact write scope for artifact-producing commands,
- allow command-owned artifacts only inside declared target scope,
- prove an invoke design fixture creates expected target development files.

### L3: Orchestrator Migration

L3 updates active refine and task-session runtime surfaces.

Required behavior:

- refine uses `RUNTIME-HANDOFF.md`,
- refine stage rows reference runtime run evidence,
- task-session uses generic runtime handoff adapter,
- old `codex-goal` surfaces are marked legacy where active paths still mention them.

### L4: Single Command Surface With Adapter Selection

L4 removes the separate runner as the active execution model while preserving adapter extensibility.

Required behavior:

- `tools/arcanum --exec` is the active execution path,
- `tools/arcanum --exec --adapter <adapter-id>` selects runtimes,
- `tools/arcanum --list-adapters` lists static v1 adapters,
- `tools/arcanum --resolve-adapter <adapter-id>` shows adapter profile evidence,
- `dry-run` proves the non-Codex adapter path,
- `codex-exec` proves Codex remains selectable as an adapter,
- successful command execution writes directly to requested `--output`,
- successful command execution does not write runtime `RESULT.md`,
- envelope-backed runs record selected adapter profile evidence.

### L5: Install-Time Selection And Runtime Interchange

L5 makes the selected runtime a repository installation property without locking the repository to that runtime forever.

Required behavior:

- `tools/bootstrap_arcanum.sh` accepts `--default-adapter <adapter-id>`,
- `tools/install_arcanum.sh` forwards the option,
- `--runtime codex|none` remains the command-surface compatibility option,
- installed repositories get `.arcanum/runtime/config.json`,
- config records command surface, default adapter, enabled adapters, and profile paths,
- config stores no secrets, copied Codex config, SQLite paths, symlinks, or mutable runtime state,
- `tools/arcanum --get-default-adapter` reads the installed default,
- `tools/arcanum --set-default-adapter <adapter-id>` validates and updates the installed default,
- adapter selection precedence is explicit override, environment override, config default, then compatibility fallback.

## Deferrals

- Background scheduler.
- Remote queue.
- UI/dashboard.
- Full historical `/goal` cleanup.
- Dynamic adapter registry discovery beyond explicit adapter ids.
- Interactive installer UI for selecting adapters.
- Cross-Arcanum/CyberAlchemy schema governance; that belongs to the schema-discipline handoff thread.

## Promotion Rule

No layer promotes without evidence from the previous layer. L4 should not begin until L3 active runtime contracts pass; L5 should not begin until L4 adapter selection is stable. L5 does not promote unless install-time default selection and post-install runtime interchange both validate.
