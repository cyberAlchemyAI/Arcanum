# Codex Exec Surface Inventory

## Status

`pass`: repository-wide grep found active and historical `codex exec` surfaces, and the Task Session line-level report classified every active surface class. Historical generated evidence remains present and is preserved by default.

## Latest Line-Level Report

- Markdown report: `formulae/dispatch-spec/development/reports/CODEX-EXEC-SURFACE-LINE-REPORT.md`
- JSON report: `formulae/dispatch-spec/development/reports/codex-exec-surface-line-report.json`
- Total hits: `829`
- Unclassified active hits: `0`

### Latest Counts By Class

| Class | Hits |
| --- | ---: |
| `active-capability-doc` | 15 |
| `active-command-prompt` | 14 |
| `active-experiment-runner` | 30 |
| `active-installer-config` | 21 |
| `active-observability-path` | 10 |
| `active-runtime-code` | 40 |
| `active-runtime-documentation` | 8 |
| `historical-generated-evidence` | 475 |
| `migration-note` | 199 |
| `runtime-adapter-doc-fixture` | 17 |

## Search Pattern

```bash
rg -n "codex exec|codex-exec|codex-bypass|CODEX_BIN|run-with-codex|observe-run-with-codex|tools/arcanum --exec" .codex arcana spells formulae framework tools benchmark transmutations registry
```

## Surface Classes

| Class | Examples Found | Migration Action |
| --- | --- | --- |
| Active runtime code | `tools/arcanum`, `tools/arcanum-runtime-run`, `arcana/experiment-harness/scripts/run-with-codex.sh`, `arcana/experiment-harness/scripts/find-codex.sh` | Migrate to local/native skill adapter or mark as explicit legacy adapter harness. |
| Active installer/config code | `tools/install_arcanum.sh`, `tools/bootstrap_arcanum.sh`, `spells/arcanum-bootstrap/README.md` | Change defaults and examples from `codex-exec` to local/native skill runtime; keep legacy opt-in documented. |
| Active command prompts | `.codex/commands/refine.md`, `.codex/commands/task-session.md`, `.codex/commands/arcanum-sigil-experiment-harness.md`, observed-invocation-loop command files | Replace required nested runtime language with dispatch-backed native skill/subagent and receipt language. |
| Active observability docs/scripts | `framework/observability/ARCHITECTURE-OVERVIEW.md`, `framework/observability/OBSERVED-RUNS.md`, `spells/observed-invocation-loop/README.md` | Update to support hooks, deterministic wrappers, native parent receipts, and explicit legacy adapters. |
| Active experiment/example validation | `arcana/experiment-harness/SKILL.md`, `arcana/experiment-harness/README.md`, `spells/invoke/development/run-validation-fixtures.sh`, `spells/invoke/development/TEMPLATE-EXAMPLE-RUNBOOK.md` | Stop requiring `codex exec` as promotion proof; use native skill/subagent execution plus receipts. |
| Runtime adapter documentation and fixtures | `framework/runtime/adapters/codex-exec.md`, `framework/runtime/development/fixtures/codex-exec/*`, task-session runtime adapter docs | Preserve as legacy adapter documentation, but label explicit opt-in and not default orchestration. |
| Active capability docs | `arcana/refine/development/VALIDATION.md`, `arcana/task-session/SKILL.md`, `arcana/sigil-runtime-installer/templates/command-adapter-plan.md` | Update capability contracts to prefer dispatch/native execution and receipt fallback. |
| Historical generated evidence | `*/development/refinement-runs/*`, `benchmark/development/refinement-runs/*`, `framework/runtime/development/refinement-runs/*`, `spells/whisper/development/refinement-runs/*` | Preserve by default; exclude from active readiness blockers after classification. |
| Migration notes and prior design artifacts | `tools/development/refinement-runs/*`, `formulae/dispatch-spec/development/*` | Keep if they explain migration history; update only current plan artifacts. |

## Active Migration Owners

| Owner | Surfaces |
| --- | --- |
| `tools/arcanum` runtime owner | `tools/arcanum`, `tools/arcanum-runtime-run`, adapter profiles, runtime config defaults. |
| Bootstrap owner | `tools/install_arcanum.sh`, `tools/bootstrap_arcanum.sh`, `spells/arcanum-bootstrap/README.md`. |
| Experiment Harness owner | `arcana/experiment-harness/*`, `framework/EXPERIMENT-HARNESS-STANDARD.md`, invoke example runner bridges. |
| Observed Invocation Loop owner | `spells/observed-invocation-loop/*`, `framework/observability/*`, hook docs. |
| Command surface owner | `.codex/commands/*`, sigil runtime installer templates. |
| Task Session owner | `arcana/task-session/*`, runtime adapter docs. |
| Refine owner | `arcana/refine/*`, benchmark refinement route artifacts. |

## Migration Policy

Active surfaces must end in one of these states:

- `migrated-native`: uses native skill/subagent execution and returned receipt contract.
- `deterministic-wrapper`: performs local resolution, validation, artifact writing, or observer closeout without spawning model-backed Codex.
- `legacy-explicit-opt-in`: still supports `codex-exec`, but only when selected explicitly for adapter compatibility testing.
- `historical-preserved`: prior-run evidence or generated artifact; not a current runtime policy.
- `migration-note`: preserved explanation of old behavior and new replacement.

Any active surface still requiring implicit `codex exec`, implicit `codex-exec`, or implicit `codex-bypass` remains a blocker.

## Readiness Gate

Before changing defaults, Task Session should produce a line-level report with:

- path,
- line number,
- matched phrase,
- class,
- owner,
- migration action,
- keep/remove decision,
- follow-up task id.

The classification gate is ready because no active line is unclassified. The default-change gate has now been executed for the core runtime/install/docs path: `local-skill` is the current default adapter, Claude/Copilot install surfaces are generated by bootstrap, and active orchestration docs now describe native skill/subagent receipts first. Remaining hits in active files are expected compatibility references, explicit legacy adapter paths, or historical/generated evidence; a stricter follow-up can regenerate this line report after command-surface snapshots are rebuilt from canonical skills.

## Migration Closeout Update

- `tools/arcanum` now exposes `local-skill` as the native agent skill/subagent handoff adapter.
- The repo-local ignored runtime config now defaults to `local-skill`.
- `tools/bootstrap_arcanum.sh` supports `--surfaces codex,claude,copilot|all|none`.
- Claude installs create `.claude/skills/arcanum-orchestrate/SKILL.md`, `.claude/agents/arcanum-stage-worker.md`, and `CLAUDE.md`.
- Copilot installs create `.github/copilot-instructions.md`, `.github/instructions/arcanum.instructions.md`, and `AGENTS.md`.
- `codex-exec` and `codex-bypass` remain available as explicit legacy adapters, not implicit orchestration defaults.
