# Orchestration Runtime Implementation Plan

## Invoke Plan Result

- Mode: `plan`
- Spell: `invoke`
- Target artifact: orchestration runtime, Claude/Copilot install surfaces, and repository-wide `codex exec` surface migration for Arcanum sigils and spells
- Phase status: `pass`
- Mode contract: `spells/invoke/plan.md`
- Source design: `formulae/dispatch-spec/development/ORCHESTRATION-RUNTIME-ARCHITECTURE.md`
- Implementation layering: included inline below
- Work-pack output mode: split-ready planning artifact
- Next route: `task-session`

## Objective

Migrate orchestration sigils and spells to use `dispatch-spec` for stage strategy and native skill/subagent execution for model-backed work across Codex, Claude, and Copilot surfaces, while keeping `tools/arcanum` as a deterministic resolver, validator, compatibility layer, and local runtime metadata surface.

The migration also covers every active repository surface that invokes, configures, documents, tests, installs, observes, or preserves `codex exec`, `codex-exec`, `codex-bypass`, `CODEX_BIN`, or `tools/arcanum --exec`. Historical generated run evidence is inventoried but not rewritten by default.

## Implementation Layering

| Layer | Question | Work | Promotion evidence |
| --- | --- | --- | --- |
| L0 contract proof | Can the new orchestration contract be represented without runtime mutation? | Add dispatch profile, receipt schema, and validation fixture. | Dispatch validator returns pass or accepted flag; docs name blocker behavior. |
| L1 parent orchestration | Can one orchestration sigil use dispatch plus native subagent receipts? | Update Refine development contract and benchmark validation route to parent-owned subagents. | Refine benchmark run manifest records dispatch id, subagent receipts, and no nested `codex exec`. |
| L2 runtime surface migration | Can `tools/arcanum` stop defaulting to nested model CLI for orchestration? | Add local-skill adapter metadata, deprecate `codex-exec` defaults, add Claude/Copilot install surfaces, update installer/bootstrap docs. | `tools/arcanum --list-adapters` and config tests show native/local default, Claude/Copilot files, and legacy opt-in. |
| L3 active-surface rollout | Can every active Codex-exec surface follow the same rule? | Migrate command prompts, installers, bootstrap, framework runtime docs, observed-run helpers, experiment harnesses, Task Session adapters, and Invoke example runners. | Repo grep shows every active hit classified as migrated, deterministic compatibility, or legacy explicit opt-in. |
| L4 historical evidence quarantine | Can generated and prior-run evidence stop confusing migration readiness? | Add generated/historical reference policy and optional cleanup handoff. | Grep report separates active policy from historical evidence and generated run folders. |

## Work-Pack

### TASK-ORCH-001: Lock Dispatch Runtime Contract

- Owner route: `task-session`
- Layer: L0
- Write scope:
  - `formulae/dispatch-spec/development/orchestration-runtime.dispatch.json`
  - `formulae/dispatch-spec/development/ORCHESTRATION-RUNTIME-ARCHITECTURE.md`
  - `formulae/dispatch-spec/development/ORCHESTRATION-RUNTIME-PLAN.md`
- Goal: Make the architecture inspectable and schema-validated before runtime mutation.
- Steps:
  1. Validate the dispatch profile with `formulae/dispatch-spec/scripts/validate-dispatch.py`.
  2. Confirm the profile names native skill execution, subagent fanout, receipt telemetry, and `tools/arcanum` compatibility.
  3. Record validation status in the plan closeout.
- Verification:
  - `formulae/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/orchestration-runtime.dispatch.json`

### TASK-ORCH-002: Add Runtime Receipt Fixture

- Owner route: `task-session`
- Layer: L0
- Write scope:
  - `formulae/dispatch-spec/development/fixtures/pass-orchestration-runtime.json`
  - optional validator rule updates if the fixture exposes a missing rule
- Goal: Prove dispatch-spec can validate the orchestration route shape with subagent receipt outputs.
- Implementation detail:
  - Create a fixture that includes `runtime.preferred_surface=native-skill`.
  - Require each model-backed step to output a `trace_event` or `artifact` handle.
  - Include a validation gate that blocks missing receipts.
- Verification:
  - `formulae/dispatch-spec/development/run-validation-fixtures.sh`

### TASK-ORCH-003: Refine Parent-Owned Subagent Prototype

- Owner route: `task-session`
- Layer: L1
- Write scope:
  - `arcana/refine/SKILL.md`
  - `arcana/refine/REFINEMENT-LOOP.md`
  - `arcana/refine/templates/refine-dispatch.json`
  - benchmark refinement run artifacts only under `benchmark/development/`
- Goal: Make Refine use dispatch-spec for the ten-stage loop and native subagents for model-backed stages.
- Implementation detail:
  - Parent Refine writes a dispatch document for the canonical loop.
  - Parent Refine validates it before stage execution.
  - Parent Refine spawns subagents for model-backed stage roles when available.
  - Parent Refine runs local inline fallback for deterministic or unavailable subagent cases.
  - Each stage returns the receipt schema from the architecture artifact.
  - Parent Refine blocks any child attempt to run `tools/arcanum --exec` or `codex exec`.
- Verification:
  - Benchmark smoke target produces a manifest with dispatch id and receipt paths.
  - Grep the new run folder for nested `codex exec` use and confirm it appears only as a blocked anti-pattern or migration note.

### TASK-ORCH-004: Add Local-Skill Runtime Adapter Metadata

- Owner route: `task-session`
- Layer: L2
- Write scope:
  - `tools/arcanum`
  - `tools/bootstrap_arcanum.sh`
  - `tools/install_arcanum.sh`
  - generated install files under `.claude/`, `.github/`, `CLAUDE.md`, and `AGENTS.md` in target repositories
  - `.arcanum/runtime/config.json` only if explicitly selected for this repo
- Goal: Add a non-nested default runtime profile that represents native skill/subagent execution.
- Implementation detail:
  - Add adapter id `local-skill` or `native-skill`.
  - Mark `codex-exec` and `codex-bypass` as `legacy-model-cli`.
  - Make default adapter prefer `local-skill` for orchestration commands.
  - Keep `codex-exec` available only through explicit `--adapter codex-exec`.
  - Make `--exec` with `local-skill` emit a stage handoff prompt, output path, and receipt requirement instead of spawning Codex.
- Verification:
  - `bash -n tools/arcanum tools/bootstrap_arcanum.sh tools/install_arcanum.sh`
  - `tools/arcanum --list-adapters`
  - `tools/arcanum --resolve-adapter local-skill`
  - `tools/arcanum --get-default-adapter`

### TASK-ORCH-005: Migrate Orchestration Docs And Command Prompts

- Owner route: `task-session`
- Layer: L3
- Write scope:
  - `.codex/commands/*.md` for orchestration commands
  - `arcana/task-session/*`
  - `spells/invoke/*`
  - `spells/spellcraft` if present
  - `arcana/experiment-harness/*`
- Goal: Make orchestration capabilities say "native skill/subagent first, dispatch-spec for multi-stage routes, legacy CLI only by explicit opt-in".
- Implementation detail:
  - Replace required nested `tools/arcanum --exec` language with parent-owned dispatch and receipt language.
  - Keep deterministic `tools/arcanum --resolve` and dispatch validation where useful.
  - Preserve lifecycle owner boundaries.
- Verification:
  - `rg -n "codex exec|codex-exec|codex-bypass|tools/arcanum --exec" .codex arcana spells tools formulae`
  - Each remaining hit is classified as `legacy`, `deterministic compatibility`, `migration note`, or `blocked anti-pattern`.

### TASK-ORCH-006: Inventory All Codex Exec Surfaces

- Owner route: `task-session`
- Layer: L3
- Write scope:
  - `formulae/dispatch-spec/development/CODEX-EXEC-SURFACE-INVENTORY.md`
  - optional generated grep report under `formulae/dispatch-spec/development/reports/`
- Goal: Identify every active and historical `codex exec` surface before migration edits.
- Implementation detail:
  - Search for `codex exec`, `codex-exec`, `codex-bypass`, `CODEX_BIN`, `run-with-codex`, `observe-run-with-codex`, and `tools/arcanum --exec`.
  - Classify each hit as active runtime code, active installer/config, active command prompt, active documentation, validation fixture, generated historical evidence, or migration note.
  - Assign each active class a target action: migrate, wrap deterministically, mark legacy opt-in, or preserve.
  - Do not edit generated prior-run evidence during this task.
- Verification:
  - Surface inventory exists and has no unclassified active surface class.
  - Follow-up migration tasks reference inventory sections by class.

### TASK-ORCH-007: Migrate Active Runtime And Installer Surfaces

- Owner route: `task-session`
- Layer: L3
- Write scope:
  - `tools/arcanum`
  - `tools/bootstrap_arcanum.sh`
  - `tools/install_arcanum.sh`
  - `tools/arcanum-runtime-run`
  - `framework/runtime/adapters/*`
  - `framework/EXPERIMENT-HARNESS-STANDARD.md`
- Goal: Remove implicit nested Codex CLI defaults from active runtime and install surfaces.
- Implementation detail:
  - Add local/native skill adapter metadata.
  - Change install examples and defaults away from `codex-exec`.
  - Add `--surfaces codex,claude,copilot|all|none` selection.
  - Generate a Claude skill plus bounded stage-worker subagent guidance.
  - Generate Copilot repository/path instructions plus `AGENTS.md` guidance.
  - Keep `codex-exec` fixture docs as explicit legacy adapter evidence.
  - Mark `tools/arcanum-runtime-run` as deterministic/legacy wrapper or replace it with local-skill handoff behavior.
- Verification:
  - Shell syntax passes for touched scripts.
  - Adapter resolution shows native/local default and legacy explicit `codex-exec`.
  - Dry-run and temp installs show `.claude/skills/arcanum-orchestrate/SKILL.md`, `.claude/agents/arcanum-stage-worker.md`, `.github/copilot-instructions.md`, `.github/instructions/arcanum.instructions.md`, `CLAUDE.md`, and `AGENTS.md`.

### TASK-ORCH-008: Migrate Experiment And Example Runner Surfaces

- Owner route: `task-session`
- Layer: L3
- Write scope:
  - `arcana/experiment-harness/*`
  - `spells/invoke/development/run-template-example-with-codex.sh`
  - `spells/invoke/development/run-validation-fixtures.sh`
  - `spells/invoke/development/TEMPLATE-EXAMPLE-RUNBOOK.md`
  - matching `.codex/commands/*experiment-harness*`
- Goal: Replace `codex exec` as the required example-runner primitive.
- Implementation detail:
  - Introduce native skill/subagent example execution as preferred.
  - Keep `run-with-codex.sh` only as an explicit legacy adapter test if still useful.
  - Update validation fixtures that currently require `codex.*exec`.
- Verification:
  - Invoke template validation no longer requires `codex exec` for promotion evidence.
  - Any remaining runner hit is marked legacy explicit opt-in.

### TASK-ORCH-009: Migrate Observability And Command-Surface Surfaces

- Owner route: `task-session`
- Layer: L3
- Write scope:
  - `spells/observed-invocation-loop/*`
  - `framework/observability/*`
  - `.codex/commands/*`
  - `arcana/sigil-runtime-installer/templates/*`
- Goal: Ensure observability and command prompts describe native skill/subagent receipt collection instead of `tools/arcanum --exec` as the only deterministic handoff.
- Implementation detail:
  - Replace "Codex hooks and `tools/arcanum --exec` perform..." with "hooks, native parent receipts, deterministic wrappers, or explicit legacy adapters perform...".
  - Add receipt fallback language wherever observation depends on agent output.
  - Keep command-resolution language where it is deterministic and not model-backed.
- Verification:
  - Observability docs name receipt fallback and do not require nested Codex CLI.

### TASK-ORCH-010: Quarantine Historical Generated Evidence

- Owner route: `task-session`
- Layer: L4
- Write scope:
  - generated-evidence policy artifact only unless cleanup is explicitly approved
- Goal: Prevent prior blocked runs and generated refinement folders from being mistaken for active runtime requirements.
- Implementation detail:
  - Record historical evidence roots such as `*/development/refinement-runs/`, `framework/runtime/development/refinement-runs/`, and benchmark run folders.
  - Mark them preserve-by-default.
  - Optionally propose `.gitignore`, generated classification, or archive cleanup separately.
- Verification:
  - Grep readiness report excludes historical/generated classes from active blocker count.

### TASK-ORCH-011: Benchmark Validation Migration

- Owner route: `task-session`
- Layer: L3
- Write scope:
  - `benchmark/development/`
  - benchmark run scripts only if needed after approval
- Goal: Validate the tool against benchmark smoke tests through Refine, Distill, Invoke, and dispatch-backed subagent receipts.
- Implementation detail:
  - Use benchmark smoke tests as deterministic evidence.
  - Use native subagents for critique, distill, and synthesis roles.
  - Parent coordinator writes one benchmark result manifest.
  - Observer telemetry is appended when available; otherwise the returned receipts are persisted.
- Verification:
  - Existing benchmark smoke command still passes.
  - Benchmark validation result names dispatch id, stage receipts, observer status, and unresolved gaps.

## Smallest Working Units

| SWU | Parent task | Goal | Write scope | Verification |
| --- | --- | --- | --- | --- |
| SWU-ORCH-001 | TASK-ORCH-001 | Validate current dispatch profile. | `formulae/dispatch-spec/development/orchestration-runtime.dispatch.json` | `validate-dispatch.py` returns pass or accepted flag. |
| SWU-ORCH-002 | TASK-ORCH-002 | Add receipt fixture. | `formulae/dispatch-spec/development/fixtures/` | fixture runner passes. |
| SWU-ORCH-003 | TASK-ORCH-003 | Add Refine dispatch template. | `arcana/refine/templates/refine-dispatch.json` | schema validation passes. |
| SWU-ORCH-004 | TASK-ORCH-003 | Add Refine subagent receipt rule. | `arcana/refine/SKILL.md`, `arcana/refine/REFINEMENT-LOOP.md` | run manifest includes receipt contract. |
| SWU-ORCH-005 | TASK-ORCH-004 | Add local-skill adapter. | `tools/arcanum` | adapter resolves and shell syntax passes. |
| SWU-ORCH-006 | TASK-ORCH-004 | Update installers and agent surfaces. | `tools/bootstrap_arcanum.sh`, `tools/install_arcanum.sh` | default adapter install path is deterministic and Claude/Copilot surfaces are generated. |
| SWU-ORCH-007 | TASK-ORCH-006 | Classify all `codex exec` surfaces. | `CODEX-EXEC-SURFACE-INVENTORY.md` | no unclassified active surface class remains. |
| SWU-ORCH-008 | TASK-ORCH-007 | Migrate runtime/install defaults. | `tools/*`, `framework/runtime/*` | native/local adapter default and legacy opt-in verified. |
| SWU-ORCH-009 | TASK-ORCH-008 | Migrate experiment/example runners. | `arcana/experiment-harness/*`, `spells/invoke/development/*` | no promotion path requires `codex exec`. |
| SWU-ORCH-010 | TASK-ORCH-009 | Migrate observability/command prompts. | `spells/observed-invocation-loop/*`, `.codex/commands/*` | receipt fallback language present. |
| SWU-ORCH-011 | TASK-ORCH-010 | Quarantine generated evidence hits. | generated-evidence policy artifact | active grep report excludes historical evidence. |
| SWU-ORCH-012 | TASK-ORCH-011 | Re-run benchmark validation with receipt manifest. | `benchmark/development/` | result manifest exists and benchmark smoke passes. |

## Gates

| Gate | Owner | Condition | On fail |
| --- | --- | --- | --- |
| G-ORCH-001 | dispatch-spec | Dispatch profile validates before runtime changes. | block |
| G-ORCH-002 | Refine | Parent owns stage joins and child subagents do not spawn nested model runtimes. | block |
| G-ORCH-003 | Observed Invocation Loop | Observability is appended or receipt fallback is persisted. | flag |
| G-ORCH-004 | tools/arcanum | Legacy `codex-exec` remains explicit opt-in during migration. | block |
| G-ORCH-005 | surface inventory | Every active `codex exec` surface is classified before edits. | block |
| G-ORCH-006 | generated evidence policy | Historical run artifacts are preserved or separately approved for cleanup. | flag |
| G-ORCH-007 | benchmark | Smoke tests still pass after migration. | block |

## Validation Commands

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py formulae/dispatch-spec/development/orchestration-runtime.dispatch.json
bash -n tools/arcanum tools/bootstrap_arcanum.sh tools/install_arcanum.sh tools/arcanum-runtime-run
tools/arcanum --list-adapters
tools/arcanum --resolve-adapter local-skill
tools/arcanum --exec --adapter local-skill --output /tmp/arcanum-local-skill-output.md invoke "define runtime smoke"
tmp=$(mktemp -d); tools/bootstrap_arcanum.sh --target "$tmp" --surfaces all --sigils task-session --spells none --dry-run
tmp=$(mktemp -d); tools/bootstrap_arcanum.sh --target "$tmp" --surfaces claude,copilot --sigils task-session --spells none --dry-run
rg -n "codex exec|codex-exec|codex-bypass|CODEX_BIN|run-with-codex|observe-run-with-codex|tools/arcanum --exec" .codex arcana spells formulae framework tools benchmark transmutations registry
```

## Current Gaps

- The native subagent API is available to the Codex session, but it is not a shell API that `tools/arcanum` can directly call.
- Hook telemetry exists in this repo, and runtime parent/subagent receipts now have a local-skill handoff contract; a stricter reusable receipt schema fixture is still useful follow-up.
- `tools/arcanum` now resolves `local-skill` and uses it as the no-config fallback.
- Refine native root orchestration now defaults child stage adapter text to `local-skill`.
- Experiment Harness and Invoke example runners now name native skill/subagent execution as preferred; legacy Codex CLI remains explicit adapter evidence.
- Observed Invocation Loop and framework observability docs now describe native receipts plus deterministic wrappers, with Codex observer scripts marked legacy.
- Install/bootstrap now support `--surfaces` for Codex, Claude, and Copilot and default Codex installs to `local-skill`.
- Historical generated refinement and benchmark folders contain many `codex-exec` references that should be preserved as evidence but excluded from active migration readiness.
- The benchmark validation pass should be repeated after TASK-ORCH-003 and TASK-ORCH-004.

## Recommended Execution Order

1. Finish L0 contract proof with dispatch validation and fixture.
2. Prototype Refine parent-owned subagent orchestration against `benchmark/`.
3. Add the local-skill adapter and change defaults behind a small compatibility gate.
4. Inventory all `codex exec` surfaces and classify active vs historical evidence.
5. Migrate runtime/install surfaces, experiment/example runners, and observability/command prompts.
6. Quarantine historical generated evidence in the readiness report.
7. Re-run benchmark smoke validation and record observability receipts.
