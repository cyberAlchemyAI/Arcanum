# WORK-PACK: Refine Runtime Stage Receipts

## Purpose

Repair native Refine runtime evidence classification so generated handoff stubs are not counted as completed owner-stage artifacts.

This work-pack is produced by Invoke plan. It does not execute implementation work.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for task-session execution. |
| complexity | medium | Runtime semantics, evidence contract, regression validation, and package sync. |
| outputMode | split | Task and wave contracts live under `work-packs/refine-runtime-stage-receipts/`. |
| executionPackRef | [CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-EXECUTION-PACK.md](CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-EXECUTION-PACK.md) | Wave sequencing. |
| layeringArtifactRef | [CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-IMPLEMENTATION-LAYERING.md](CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-IMPLEMENTATION-LAYERING.md) | L0-L3 layer model. |
| activeLayerWindow | L3 |
| readinessProfile | runtime-stage-receipt-semantics |

## Objective Summary

Fix the native Refine wrapper so:

- `REFINE-DISPATCH.json` is materialized and validated before runtime-backed stages,
- `local-skill` handoff stubs are classified as handoffs, not owner-stage pass evidence,
- run manifests and evidence indexes distinguish handoff, receipt, artifact, flag, and block states,
- Craft validation can be rerun without false pass semantics.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-RECEIPT-001 | Handoff stubs cannot mark a stage `pass`. | L0 | [W0](work-packs/refine-runtime-stage-receipts/waves/W0.md) | Source review | Synthetic or real local-skill stage classifies as `flag`/`block`. |
| S-RECEIPT-002 | Native Refine writes and validates `REFINE-DISPATCH.json`. | L1 | [W1](work-packs/refine-runtime-stage-receipts/waves/W1.md) | S-RECEIPT-001 | Dispatch exists and validates before stages. |
| S-RECEIPT-003 | Manifest/index carry stage evidence kinds and contract checks. | L2 | [W2](work-packs/refine-runtime-stage-receipts/waves/W2.md) | S-RECEIPT-002 | Evidence index inspection and JSON validation. |
| S-RECEIPT-004 | Craft Refine validation rerun produces honest status and package sync. | L3 | [W3](work-packs/refine-runtime-stage-receipts/waves/W3.md) | S-RECEIPT-003 | Refine rerun plus README/session ledger agreement. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [CRAFT-RECEIPT-001](work-packs/refine-runtime-stage-receipts/tasks/CRAFT-RECEIPT-001.md) | Classify native handoff stubs separately from completed owner artifacts. | L0 | medium | [W0](work-packs/refine-runtime-stage-receipts/waves/W0.md) | `tools/arcanum` | pass | completed |
| [CRAFT-RECEIPT-002](work-packs/refine-runtime-stage-receipts/tasks/CRAFT-RECEIPT-002.md) | Materialize and validate `REFINE-DISPATCH.json` in native Refine runs. | L1 | medium | [W1](work-packs/refine-runtime-stage-receipts/waves/W1.md) | `arcana/refine/templates/refine-dispatch.json` | pass | completed |
| [CRAFT-RECEIPT-003](work-packs/refine-runtime-stage-receipts/tasks/CRAFT-RECEIPT-003.md) | Harden run manifest and evidence index contract. | L2 | medium | [W2](work-packs/refine-runtime-stage-receipts/waves/W2.md) | `arcana/refine/templates/evidence-index.json` | pass | completed |
| [CRAFT-RECEIPT-004](work-packs/refine-runtime-stage-receipts/tasks/CRAFT-RECEIPT-004.md) | Rerun Craft Refine validation and sync package state. | L3 | low | [W3](work-packs/refine-runtime-stage-receipts/waves/W3.md) | `CRAFT-VALIDATION.md` | pass | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-CRAFT-RECEIPT-001 | [CRAFT-RECEIPT-001](work-packs/refine-runtime-stage-receipts/tasks/CRAFT-RECEIPT-001.md) | `tools/arcanum` functions `run_refine_command_stage`, `refine_artifact_is_usable`, `write_runtime_handoff` | local-skill stage classification | none | `tools/arcanum`; optional focused test/evidence artifact | local-skill handoff stub does not produce stage `pass` without receipt evidence. | Before/after command output or fixture inspection. | rerun local-skill Refine or focused shell fixture | local-fallback | completed |
| SWU-CRAFT-RECEIPT-002 | [CRAFT-RECEIPT-002](work-packs/refine-runtime-stage-receipts/tasks/CRAFT-RECEIPT-002.md) | `tools/arcanum` `run_native_refine`, `arcana/refine/templates/refine-dispatch.json`, `formulae/dispatch-spec/scripts/validate-dispatch.py` | dispatch materialization | SWU-CRAFT-RECEIPT-001 | `tools/arcanum`; optional generated dispatch helper | native Refine run folder contains validated `REFINE-DISPATCH.json`. | Validator output. | `python3 formulae/dispatch-spec/scripts/validate-dispatch.py <run>/REFINE-DISPATCH.json` | local-fallback | completed |
| SWU-CRAFT-RECEIPT-003 | [CRAFT-RECEIPT-003](work-packs/refine-runtime-stage-receipts/tasks/CRAFT-RECEIPT-003.md) | `tools/arcanum` `record_refine_stage`, `write_native_refine_outputs`, `arcana/refine/templates/evidence-index.json` | evidence index and manifest | SWU-CRAFT-RECEIPT-002 | `tools/arcanum`; optional evidence fixture | evidence index records `evidence_kind`, artifact paths, handoff paths, and blocked/flagged reason accurately. | `jq` inspection of rerun evidence index. | `jq` checks against generated evidence index | local-fallback | completed |
| SWU-CRAFT-RECEIPT-004 | [CRAFT-RECEIPT-004](work-packs/refine-runtime-stage-receipts/tasks/CRAFT-RECEIPT-004.md) | `development/craft/CRAFT-VALIDATION.md`, latest run audit, README, SESSION-LEDGER | Craft validation rerun | SWU-CRAFT-RECEIPT-003 | `development/craft/README.md`; `development/craft/SESSION-LEDGER.md`; generated run evidence | Craft state reflects honest Refine rerun status. | Refine result plus package sync grep. | `tools/arcanum --exec --adapter local-skill ... refine 'development/craft/CRAFT-VALIDATION.md --preset standard --research no'` | manual | completed |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| none | n/a | No blocker prevents starting CRAFT-RECEIPT-001. | n/a | n/a |

## Non-Blocking Gaps

| Gap | Treatment |
| --- | --- |
| Full cross-runtime skill execution interface | Deferred to `ARCANUM-SKILL-RUNTIME-HANDOFF.md`; this plan only fixes native Refine evidence semantics. |
| Craft promotion | Deferred; this work only enables honest validation. |
| Stage owner artifact quality | Later owner-specific improvements may be needed after receipt semantics are honest. |

## Gate Checks

1. Do not promote Craft.
2. Do not reopen the completed `dispatch-spec` and `runtime-handoff` command-surface tasks unless a regression proves they broke.
3. Do not count a handoff prompt as completed owner-stage work.
4. Do not remove the native no-recursion safeguard.
5. Block if the fix requires broad runtime redesign outside `tools/arcanum` without a new design artifact.

## Recommended Next Execution

```text
$invoke plan development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS
```
