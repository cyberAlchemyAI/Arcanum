# WORK-PACK: Craft Index Improvements

## Purpose

Canonical executable plan for implementing Craft readiness indexes and generated
JSON/CSV projections in one governed execution sequence.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for a gated native Codex Goal execution. |
| complexity | medium | Multiple source surfaces, fixtures, scripts, generated mirrors, and validation gates. |
| outputMode | split | Uses task and wave files under `work-pack/`. |
| executionPackRef | `work-pack/waves/` | Wave files define ordering. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision boundaries. |
| activeLayerWindow | L0-L3 ordered | One goal may execute all waves if gates pass. |
| currentExecutionTarget | `TASK-CII-ONEGO` | Selected task for Codex Goal profile. |
| readinessProfile | pilot | Public-safe local implementation, no publication by default. |

## Objective Summary

- Add optional execution-readiness indexes.
- Add generated `.craft/index.json` contract and `.craft/projections/*.csv`
  projection contract.
- Add a public-safe fixture and deterministic build/validate tooling.
- Add CSV import dry-run only, not direct writeback.
- Refresh generated runtime mirrors only after canonical validation passes.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-CII-001 | Unified schema/docs/SKILL contract. | L0 | W0 | none | YAML parse and targeted grep. |
| S-CII-002 | Public-safe fixture and expected outputs. | L1 | W1 | S-CII-001 | YAML/JSON/CSV checks and boundary scan. |
| S-CII-003 | Build/validate projection tooling. | L2 | W2 | S-CII-002 | Tool fixture checks and stale detection. |
| S-CII-004 | CSV dry-run import and status/export integration. | L3 | W3 | S-CII-003 | Dry-run patch plan and all-status fast-path checks. |
| S-CII-005 | Generated mirrors and publication-prep checks. | L3 | W4 | S-CII-004 | mirror grep, diff-check, optional bump-check. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-CII-ONEGO](work-pack/tasks/TASK-CII-ONEGO.md) | Execute all Craft index improvements in one gated Codex Goal session. | L0-L3 | medium | [W0](work-pack/waves/W0.md), [W1](work-pack/waves/W1.md), [W2](work-pack/waves/W2.md), [W3](work-pack/waves/W3.md), [W4](work-pack/waves/W4.md) | two refine runs and this invoke bundle | ready | planned |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SWU-CII-001` | [TASK-CII-ONEGO](work-pack/tasks/TASK-CII-ONEGO.md) | `arcana/craft/templates/ledger.schema.yml`, `arcana/craft/SKILL.md`, `arcana/craft/README.md` | readiness + projection refine results | none | schema/docs/SKILL only | combined contract added additively | grep + YAML parse | targeted `rg`, YAML parse | local-fallback | ready |
| `SWU-CII-002` | [TASK-CII-ONEGO](work-pack/tasks/TASK-CII-ONEGO.md) | `arcana/craft/examples/`, new fixture path | public boundary | `SWU-CII-001` | `arcana/craft/fixtures/craft-index-improvements/` | fixture covers row families and readiness/projections | fixture parse + denylist scan | YAML/JSON/CSV checks | local-fallback | ready-after-SWU-CII-001 |
| `SWU-CII-003` | [TASK-CII-ONEGO](work-pack/tasks/TASK-CII-ONEGO.md) | fixture + schema | deterministic projections | `SWU-CII-002` | `arcana/craft/scripts/` | build/validate commands pass on fixture | generated output checks | script fixture run | local-fallback | ready-after-SWU-CII-002 |
| `SWU-CII-004` | [TASK-CII-ONEGO](work-pack/tasks/TASK-CII-ONEGO.md) | Craft all-status contract | fast reads | `SWU-CII-003` | `arcana/craft/SKILL.md`, script integration docs | all-status fast path defined with stale fallback | grep + fixture check | targeted checks | local-fallback | ready-after-SWU-CII-003 |
| `SWU-CII-005` | [TASK-CII-ONEGO](work-pack/tasks/TASK-CII-ONEGO.md) | projection tool + fixture | import safety | `SWU-CII-003` | `arcana/craft/scripts/` | import dry-run emits patch plan and blocks unsafe edits | dry-run report | script fixture run | local-fallback | ready-after-SWU-CII-003 |
| `SWU-CII-006` | [TASK-CII-ONEGO](work-pack/tasks/TASK-CII-ONEGO.md) | canonical source changes | generated mirrors | `SWU-CII-001` through `SWU-CII-005` | generated runtime packages only | mirrors include updated Craft wording | mirror grep | bootstrap/generation + grep | local-fallback | gated |
| `SWU-CII-007` | [TASK-CII-ONEGO](work-pack/tasks/TASK-CII-ONEGO.md) | all changed public outputs | publication prep | `SWU-CII-006` | no content edits unless validation fix | diff-check and optional bump-check pass | command output | `git diff --check`; `make bump-check` if publishing | manual/local-fallback | gated |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| B-CII-001 | publication | Commit/push/parent gitlink movement is not part of this goal unless explicitly requested after validation. | maintainer | Stop and report publication-ready state. |
| B-CII-002 | import writeback | Direct CSV-to-YAML mutation is blocked until dry-run fixture proof passes. | Craft maintainer | Keep `import-csv` dry-run-only. |
| B-CII-003 | public boundary | Public fixtures and generated outputs must not include private paths or project details. | validator | Run denylist scan before validation closeout. |

## Gate Checks

1. Pack-first execution: read `CONTEXT-PACK.md` and `context-index.json` before edits.
2. Keep write scope to declared Craft paths.
3. No private decision-profile details in public `arcanum`.
4. No commit, push, PR, or parent gitlink movement.
5. Stop on failed schema parse, fixture parse, public-boundary scan, or generated mirror mismatch.
