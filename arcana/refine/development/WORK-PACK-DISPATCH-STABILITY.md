---
module: refine-dispatch-stability
version: current
status: draft
updatedAt: 2026-05-29
docType: work-pack
---

# WORK-PACK: Refine Dispatch Stability

## Invoke Plan Result

- Mode: `plan`
- Spell: `invoke`
- Target artifact: `arcana/refine`
- Target type: Arcana sigil hardening plan
- Selected improvement items: 1, 2, 4, 5
- Phase status: `pass`
- Mode contract: [../../../spells/invoke/plan.md](../../../spells/invoke/plan.md)
- Next route: `task-session`

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Execution tasks are bounded and validation surfaces are explicit. |
| complexity | medium | Touches command/skill surfaces, docs, validator fixtures, and a generator script. |
| outputMode | single-file | Medium scope, but four SWUs are still navigable in one package-local work-pack. |
| executionPackRef | n/a | Not required unless this expands into parallel execution. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING-DISPATCH-STABILITY.md](IMPLEMENTATION-LAYERING-DISPATCH-STABILITY.md) | L0-L3 decisions for this hardening route. |
| activeLayerWindow | L0-L3 | Execute in order; later layers depend on earlier evidence. |
| lastUpdatedAt | 2026-05-29 | Plan authored from selected improvement list. |
| readinessProfile | pilot-hardening | Improves stability proof; does not promote Refine. |

## Objective Summary

- Objective: harden Refine by synchronizing active surfaces, removing stale current-facing guidance, extending dispatch overlay validation, and adding deterministic dispatch generation.
- Primary inputs: [../SKILL.md](../SKILL.md), [../REFINEMENT-LOOP.md](../REFINEMENT-LOOP.md), [../templates/refine-dispatch.json](../templates/refine-dispatch.json), [../../../formulae/dispatch-spec/TECHNIQUE-CATALOG.md](../../../formulae/dispatch-spec/TECHNIQUE-CATALOG.md), [../../../formulae/dispatch-spec/scripts/validate-dispatch.py](../../../formulae/dispatch-spec/scripts/validate-dispatch.py)
- Success condition: Refine validation is no worse than current `flag` from stale live output, dispatch-spec fixture suite passes, and active surfaces no longer contradict the dispatch-route contract.

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-001 | Active skill and command surfaces align with dispatch-route contract. | L0 | none | grep for active stale Goal wording; command docs mention `REFINE-DISPATCH.json`. |
| S-002 | Stale development guidance is refreshed or marked historical. | L1 | S-001 | targeted grep shows stale wording only in historical/archive contexts. |
| S-003 | Overlay-specific validator fixtures exist and pass. | L2 | S-001 | `formulae/dispatch-spec/development/run-validation-fixtures.sh`. |
| S-004 | Deterministic Refine dispatch generator exists and validates output. | L3 | S-003 | generator fixture output validates through `validate-dispatch.py`; Refine wrapper references generator smoke. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-REFINE-STAB-001 | Sync installed skill and command surfaces. | L0 | medium | Current Refine contract and command docs. | pass | completed |
| TASK-REFINE-STAB-002 | Refresh stale development docs. | L1 | medium | Development docs grep results. | pass | completed |
| TASK-REFINE-STAB-003 | Add overlay-specific validator fixtures. | L2 | medium | Dispatch Spec validator and technique catalog. | pass | completed |
| TASK-REFINE-STAB-004 | Add deterministic dispatch generator. | L3 | medium | Refine dispatch template and validator. | pass | completed |
| TASK-REFINE-STAB-VERIFY | Verify stability package. | L3 | low | All tasks. | flag | completed-with-known-live-output-flag |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-REFINE-STAB-001 | TASK-REFINE-STAB-001 | [../SKILL.md](../SKILL.md), [../templates/refine-dispatch.json](../templates/refine-dispatch.json), `.codex/commands/refine.md`, `.codex/commands/arcanum-sigil-refine.md`, [codex-skill-install/SKILL.md](codex-skill-install/SKILL.md) | Installed skill at `/mnt/c/Users/vlad_/.codex/skills/arcanum-refine/SKILL.md` synced directly. | none | `.codex/commands/refine.md`, installed skill, optional command/install surfaces | Active command/skill-facing docs name `REFINE-DISPATCH.json`, `RUNTIME-HANDOFF.md`, dispatch validation, and technique overlays. | Grep output showed no active `GOAL-HANDOFF`, goal handoff, or Codex Goal wording in active surfaces. | `rg -n "GOAL-HANDOFF|goal handoff|Goal handoff|Codex Goal|codex-goal" /mnt/c/Users/vlad_/.codex/skills/arcanum-refine/SKILL.md .codex/commands/refine.md .codex/commands/arcanum-sigil-refine.md arcana/refine/development/codex-skill-install/SKILL.md` | local-fallback | completed |
| SWU-REFINE-STAB-002 | TASK-REFINE-STAB-002 | [LIVE-EXAMPLE-SEEDS.md](LIVE-EXAMPLE-SEEDS.md), [LIVE-XRAY-RUN-REVIEW.md](LIVE-XRAY-RUN-REVIEW.md), [SIGIL-DEVELOPMENT-OBSERVER-REPORT.md](SIGIL-DEVELOPMENT-OBSERVER-REPORT.md), [REFINE-CONTEXT-PACK.md](REFINE-CONTEXT-PACK.md), [WORK-PACK.md](WORK-PACK.md) | Some files are historical and were marked rather than rewritten as if current. | SWU-REFINE-STAB-001 | Current-facing sections under `arcana/refine/development/` | Stale Codex Goal wording is either removed from current guidance or labelled historical/superseded with dispatch-route replacement. | Historical notes now point to `REFINE-DISPATCH.json`, `RUNTIME-HANDOFF.md`, and dispatch-spec validation. | `rg -n "GOAL-HANDOFF|goal handoff|Codex Goal|codex-goal" arcana/refine/development` | local-fallback | completed |
| SWU-REFINE-STAB-003 | TASK-REFINE-STAB-003 | [../../../formulae/dispatch-spec/scripts/validate-dispatch.py](../../../formulae/dispatch-spec/scripts/validate-dispatch.py), [../../../formulae/dispatch-spec/development/fixtures](../../../formulae/dispatch-spec/development/fixtures), [../../../formulae/dispatch-spec/TECHNIQUE-CATALOG.md](../../../formulae/dispatch-spec/TECHNIQUE-CATALOG.md) | Overlay techniques are route-menu, dialectic, tournament, x-ray, toy-game, memory, protected-context. | SWU-REFINE-STAB-001 | `formulae/dispatch-spec/development/fixtures/`, `formulae/dispatch-spec/development/run-validation-fixtures.sh` | Each overlay has at least one fixture proving pass or intended block/flag behavior; fixture runner passes. | Runner passed with expected block/flag fixtures and final `VALIDATION=pass`. | `formulae/dispatch-spec/development/run-validation-fixtures.sh` | local-fallback | completed |
| SWU-REFINE-STAB-004 | TASK-REFINE-STAB-004 | [../templates/refine-dispatch.json](../templates/refine-dispatch.json), [../../../formulae/dispatch-spec/dispatch.schema.yml](../../../formulae/dispatch-spec/dispatch.schema.yml), [../../../formulae/dispatch-spec/scripts/validate-dispatch.py](../../../formulae/dispatch-spec/scripts/validate-dispatch.py) | Generator materializes JSON from seed + selected overlays; it does not execute stages. | SWU-REFINE-STAB-003 | `arcana/refine/scripts/generate-refine-dispatch.py`, `arcana/refine/development/fixtures/refine-dispatch-seed.json`, validation wrapper | A deterministic generator renders a dispatch from seed fields and overlay choices; output validates. | Generator smoke emitted `VALIDATION=pass`; generated JSON passed `json.tool` and dispatch-spec validation. | `python3 arcana/refine/scripts/generate-refine-dispatch.py --seed arcana/refine/development/fixtures/refine-dispatch-seed.json --output /tmp/refine-generated-dispatch.json --validate` | local-fallback | completed |
| SWU-REFINE-STAB-005 | TASK-REFINE-STAB-VERIFY | [VALIDATION.md](VALIDATION.md), [run-validation-fixtures.sh](run-validation-fixtures.sh), [../../../formulae/dispatch-spec/development/run-validation-fixtures.sh](../../../formulae/dispatch-spec/development/run-validation-fixtures.sh) | Fresh live example rerun remains deferred unless explicitly requested. | SWU-REFINE-STAB-001, SWU-REFINE-STAB-002, SWU-REFINE-STAB-003, SWU-REFINE-STAB-004 | `arcana/refine/development/VALIDATION.md`, validation outputs | Validation docs mention the generator and overlay fixtures; known remaining flag is only stale live output. | Dispatch-spec suite passed; Refine runner ended `VALIDATION=flag` only because old `sigil-new-low` output lacks dispatch-route/runtime-handoff evidence. | `formulae/dispatch-spec/development/run-validation-fixtures.sh && arcana/refine/development/run-validation-fixtures.sh` | local-fallback | completed-with-known-flag |

## Implementation Detail Specs

### TASK-REFINE-STAB-001: Sync Active Surfaces

- Purpose: ensure future users and command surfaces invoke the current dispatch-route Refine contract.
- Inputs: repo-local `arcana/refine/SKILL.md`, Refine templates, command docs, installed skill wrapper.
- Outputs: updated active surfaces and, if direct global skill mutation is deferred, a sync note naming the exact installed path.
- Rules:
  1. Active docs must name `REFINE-DISPATCH.json` and `RUNTIME-HANDOFF.md`.
  2. Active docs must not require `GOAL-HANDOFF.md`.
  3. If installed skill is outside repo write scope, write a patch/sync instruction rather than silently skipping it.
- Edge cases: historical development docs may still mention Codex Goal; do not treat those as active surfaces unless they are install or command entrypoints.

### TASK-REFINE-STAB-002: Refresh Stale Development Docs

- Purpose: reduce contradictory guidance in current-facing development materials.
- Inputs: grep results for Codex Goal / GOAL-HANDOFF terms.
- Outputs: refreshed docs or explicit `Historical note` markers.
- Rules:
  1. Do not erase historical evidence.
  2. Current guidance should point to dispatch validation and runtime handoff.
  3. Keep promotion readiness separate from stale-output cleanup.
- Edge cases: old refinement-run artifacts under `development/refinement-runs/` can remain historical.

### TASK-REFINE-STAB-003: Overlay-Specific Fixtures

- Purpose: make overlay validation regression-resistant.
- Inputs: validator, schema, technique catalog, current refine dispatch template.
- Outputs: fixture files and fixture-runner updates.
- Rules:
  1. Dialectic/tournament fixture must prove missing roles or convergence criteria blocks.
  2. X-ray fixture must prove missing handle/artifact output blocks.
  3. Toy-game fixture must prove missing evidence artifact blocks.
  4. Route-menu fixture must prove missing route menu flags or blocks according to validator policy.
  5. Memory/protected-context fixtures must prove technique ids are recognized and reflected.
- Edge cases: avoid making fixture suite too broad; one focused fixture per overlay family is enough.

### TASK-REFINE-STAB-004: Dispatch Generator

- Purpose: avoid hand-edited `REFINE-DISPATCH.json` drift.
- Inputs: seed fields, selected overlay ids, template defaults, dispatch schema.
- Outputs: generated dispatch JSON and tests/fixtures.
- Algorithm:
  1. Load a seed JSON or command-line fields: run id, target, operator request, preset, research mode, selected overlays.
  2. Start from canonical ten-stage dispatch defaults.
  3. Apply overlay profiles by adding dispatch-level techniques, step techniques, roles, convergence criteria, route menu selection, gates, and validation expectations.
  4. Emit JSON with deterministic key ordering or stable object construction.
  5. Run `validate-dispatch.py` on the generated document.
- Edge cases:
  - Unknown overlay id blocks.
  - No selected overlay defaults to `baseline_sequence`.
  - Overlay requiring unavailable evidence marks the dispatch `flag` or emits a blocked field; it does not silently drop the overlay.

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| none | current plan | No blocker for authoring this plan. | n/a | Execute SWUs through Task Session or local fallback. | n/a |

## Gate Checks

1. Active surfaces use dispatch-route vocabulary.
2. Historical docs are not mistaken for current contract.
3. Overlay fixtures fail for the right reasons and pass for valid overlays.
4. Dispatch generator output validates through Dispatch Spec.
5. Refine validation remains honest about stale live output until a fresh run exists.
6. This work-pack does not execute implementation work or claim promotion readiness.

## Validation Strategy

```bash
python3 -m json.tool arcana/refine/templates/refine-dispatch.json
python3 -m py_compile formulae/dispatch-spec/scripts/validate-dispatch.py
python3 -m py_compile arcana/refine/scripts/generate-refine-dispatch.py
python3 arcana/refine/scripts/generate-refine-dispatch.py --seed arcana/refine/development/fixtures/refine-dispatch-seed.json --output /tmp/refine-generated-dispatch.json --validate
formulae/dispatch-spec/scripts/validate-dispatch.py /tmp/refine-generated-dispatch.json
formulae/dispatch-spec/development/run-validation-fixtures.sh
arcana/refine/development/run-validation-fixtures.sh
git diff --check -- arcana/refine formulae/dispatch-spec .codex/commands
```

Expected current-state caveat: `arcana/refine/development/run-validation-fixtures.sh` may remain `VALIDATION=flag` until the stale saved live output is rerun with dispatch-route evidence.

## Recommended Next Route

```text
task-session to arcana/refine/development/WORK-PACK-DISPATCH-STABILITY.md --swu SWU-REFINE-STAB-001
```

Then proceed through SWU-REFINE-STAB-002, SWU-REFINE-STAB-003, SWU-REFINE-STAB-004, and SWU-REFINE-STAB-005 in order.
