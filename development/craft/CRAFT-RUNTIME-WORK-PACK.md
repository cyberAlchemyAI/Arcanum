# WORK-PACK: Craft Runtime Command Surface

## Purpose

Create the executable plan for clearing Craft's current Refine validation blocker: missing `dispatch-spec` and `runtime-handoff` command routes.

This work-pack is produced by Invoke plan. It does not execute changes.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for task-session execution. |
| complexity | medium | Command-surface mutation plus validation and package sync. |
| outputMode | split | Task and wave contracts live under `work-packs/craft-runtime/`. |
| executionPackRef | [CRAFT-RUNTIME-EXECUTION-PACK.md](CRAFT-RUNTIME-EXECUTION-PACK.md) | Wave sequencing. |
| layeringArtifactRef | [CRAFT-RUNTIME-IMPLEMENTATION-LAYERING.md](CRAFT-RUNTIME-IMPLEMENTATION-LAYERING.md) | L0-L3 layer model. |
| activeLayerWindow | complete |
| readinessProfile | command-surface-blocker-closure |

## Objective Summary

Expose or repair the missing command routes needed by Refine:

```text
dispatch-spec
runtime-handoff
```

Success means both resolve through `tools/arcanum`, the Craft Refine dispatch still validates, and package state points to rerunning Refine validation rather than promotion.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-RUNTIME-001 | `dispatch-spec` resolves as a bare command route. | L0 | [W0](work-packs/craft-runtime/waves/W0.md) | Source review | `tools/arcanum --resolve dispatch-spec` |
| S-RUNTIME-002 | `runtime-handoff` resolves as a bare command route. | L1 | [W1](work-packs/craft-runtime/waves/W1.md) | S-RUNTIME-001 | `tools/arcanum --resolve runtime-handoff` |
| S-RUNTIME-003 | Command-surface smoke proves the Refine blocker is cleared. | L2 | [W2](work-packs/craft-runtime/waves/W2.md) | S-RUNTIME-001, S-RUNTIME-002 | Resolve both routes and validate `REFINE-DISPATCH.json`. |
| S-RUNTIME-004 | Craft state is synchronized to rerun Refine validation. | L3 | [W3](work-packs/craft-runtime/waves/W3.md) | S-RUNTIME-003 | README/session ledger agree. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [CRAFT-RUNTIME-001](work-packs/craft-runtime/tasks/CRAFT-RUNTIME-001.md) | Add or repair bare `dispatch-spec` command route. | L0 | medium | [W0](work-packs/craft-runtime/waves/W0.md) | `formulae/dispatch-spec/SKILL.md` | pass | completed |
| [CRAFT-RUNTIME-002](work-packs/craft-runtime/tasks/CRAFT-RUNTIME-002.md) | Add or repair bare `runtime-handoff` command route. | L1 | medium | [W1](work-packs/craft-runtime/waves/W1.md) | `arcana/task-session/runtime-adapters/runtime-handoff.md` | pass | completed |
| [CRAFT-RUNTIME-003](work-packs/craft-runtime/tasks/CRAFT-RUNTIME-003.md) | Run command-surface smoke and Craft dispatch validation. | L2 | low | [W2](work-packs/craft-runtime/waves/W2.md) | outputs of CRAFT-RUNTIME-001 and CRAFT-RUNTIME-002 | pass | completed |
| [CRAFT-RUNTIME-004](work-packs/craft-runtime/tasks/CRAFT-RUNTIME-004.md) | Sync Craft state after command blocker closure. | L3 | low | [W3](work-packs/craft-runtime/waves/W3.md) | CRAFT-RUNTIME-003 evidence | pass | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-CRAFT-RUNTIME-001 | [CRAFT-RUNTIME-001](work-packs/craft-runtime/tasks/CRAFT-RUNTIME-001.md) | `formulae/dispatch-spec/SKILL.md`, `formulae/dispatch-spec/scripts/validate-dispatch.py`, `.codex/commands`, `tools/arcanum` | dispatch-spec route | none | `.codex/commands/dispatch-spec.md` or equivalent route file | `tools/arcanum --resolve dispatch-spec` passes. | Command resolution output. | `tools/arcanum --resolve dispatch-spec` | local-fallback | completed |
| SWU-CRAFT-RUNTIME-002 | [CRAFT-RUNTIME-002](work-packs/craft-runtime/tasks/CRAFT-RUNTIME-002.md) | `arcana/task-session/runtime-adapters/runtime-handoff.md`, `arcana/refine/templates/runtime-handoff.md`, `.codex/commands`, `tools/arcanum` | runtime-handoff route | SWU-CRAFT-RUNTIME-001 | `.codex/commands/runtime-handoff.md` or equivalent route file | `tools/arcanum --resolve runtime-handoff` passes. | Command resolution output. | `tools/arcanum --resolve runtime-handoff` | local-fallback | completed |
| SWU-CRAFT-RUNTIME-003 | [CRAFT-RUNTIME-003](work-packs/craft-runtime/tasks/CRAFT-RUNTIME-003.md) | `refinement-runs/20260529T164919Z-validate-craft/REFINE-DISPATCH.json`, command routes | command smoke | SWU-CRAFT-RUNTIME-002 | task-session evidence only | Both commands resolve and dispatch validator passes. | Smoke report. | `tools/arcanum --resolve dispatch-spec`; `tools/arcanum --resolve runtime-handoff`; `python3 formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/refinement-runs/20260529T164919Z-validate-craft/REFINE-DISPATCH.json` | manual | completed |
| SWU-CRAFT-RUNTIME-004 | [CRAFT-RUNTIME-004](work-packs/craft-runtime/tasks/CRAFT-RUNTIME-004.md) | `README.md`, `SESSION-LEDGER.md`, smoke evidence | package sync | SWU-CRAFT-RUNTIME-003 | `development/craft/README.md`, `development/craft/SESSION-LEDGER.md`, this work-pack | Craft state points to rerunning Refine validation. | README/session ledger agreement. | Manual entrypoint review. | manual | completed |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| none | n/a | No blocker prevents starting CRAFT-RUNTIME-001. | n/a | n/a |

## Non-Blocking Gaps

| Gap | Treatment |
| --- | --- |
| Full runtime adapter implementation | Deferred. This work-pack only clears route resolution. |
| Full Refine rerun | Deferred until command smoke passes. |
| Craft promotion | Deferred. |

## Gate Checks

1. Do not execute more than one task at a time unless explicitly approved.
2. Do not promote Craft.
3. Do not change Refine lifecycle semantics.
4. Prefer command aliases that preserve source ownership.
5. If a simple alias is insufficient, block and record the required runtime/sigil owner route.

## Recommended Next Execution

```text
$refine development/craft/CRAFT-VALIDATION.md --preset standard --research no
```
