# WORK-PACK: Craft Invoke Define Stage Receipt

## Purpose

Create the narrow plan for clearing the current Craft validation blocker: `Invoke Define` has only a handoff stub and needs a local owner-stage receipt.

This work-pack is produced by Invoke plan semantics. It does not promote Craft, mutate canonical runtime surfaces, redesign runtime adapters, or execute downstream Refine stages.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for bounded task-session execution. |
| complexity | medium | The receipt task is narrow, but it crosses local Refine evidence review, Invoke define ownership, and package synchronization. |
| outputMode | split | Task and wave contracts live under `work-packs/invoke-define-stage-receipt/`. |
| executionPackRef | [CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-EXECUTION-PACK.md](CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-EXECUTION-PACK.md) | Wave sequencing. |
| layeringArtifactRef | [CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-IMPLEMENTATION-LAYERING.md](CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-IMPLEMENTATION-LAYERING.md) | L0-L3 layer model. |
| activeLayerWindow | L0-L2 |
| lastUpdatedAt | 2026-06-02 |
| readinessProfile | native-invoke-define-receipt |

## Objective Summary

Fix the current Craft Refine validation blocker by enabling this evidence chain:

```text
Invoke Define handoff prepared
-> local Invoke Define owner stage executed
-> receipt written at expected path
-> local Refine skill review accepts receipt-backed evidence
-> downstream stages can evaluate the next real blocker
```

Success condition:

- `Invoke Define` is no longer `evidence_kind=handoff_prepared` in the latest run.
- The receipt is valid under `work-packs/native-stage-execution-receipts/receipt-contract.md`.
- Craft README/session ledger name the updated receipt-backed state and next route.

## Planning Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Current Refine evidence | Objective Summary and task dependencies | Preserve `Invoke Define` as the first exact blocker. |
| Stage handoff | Task implementation detail | Reuse `expected_receipt_path` from `stages/02-invoke-define.md`; ignore legacy `resume_command` command-surface text. |
| Receipt contract | Validation surfaces and acceptance evidence | Require receipt fields, artifact paths, validation, and blockers. |
| Invoke define contract | Owner-stage artifact contract | The stage output must reflect actual Invoke Define work, not a handoff stub. |
| Craft promotion readiness | Guardrails | Preserve promotion deferral and local candidate status. |
| SWU policy | Task files and SWU manifest | One SWU per execution task for task-session readiness. |

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-INVOKE-RECEIPT-001 | `Invoke Define` receipt artifact contract is explicit and executable. | L0 | [W0](work-packs/invoke-define-stage-receipt/waves/W0.md) | latest handoff and receipt contract | `rg` confirms exact stage, expected receipt path, artifact paths, validation, and blockers. |
| S-INVOKE-RECEIPT-002 | Current run has a local `Invoke Define` receipt. | L1 | [W1](work-packs/invoke-define-stage-receipt/waves/W1.md) | S-INVOKE-RECEIPT-001 | `jq empty receipts/02-invoke-define.json`; artifact paths exist. |
| S-INVOKE-RECEIPT-003 | Craft validation rerun ingests the receipt and syncs package state. | L2 | [W2](work-packs/invoke-define-stage-receipt/waves/W2.md) | S-INVOKE-RECEIPT-002 | Refine rerun plus evidence-index/README/session-ledger agreement. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [CRAFT-INVOKE-RECEIPT-001](work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-001.md) | Define the `Invoke Define` receipt artifact contract. | L0 | medium | [W0](work-packs/invoke-define-stage-receipt/waves/W0.md) | handoff, receipt contract, Invoke define contract | pass | completed |
| [CRAFT-INVOKE-RECEIPT-002](work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-002.md) | Execute or block the `Invoke Define` owner stage and write the receipt. | L1 | medium | [W1](work-packs/invoke-define-stage-receipt/waves/W1.md) | CRAFT-INVOKE-RECEIPT-001, stage handoff | pass | completed |
| [CRAFT-INVOKE-RECEIPT-003](work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-003.md) | Re-evaluate Craft validation through the local Refine skill and sync receipt-backed state. | L2 | low | [W2](work-packs/invoke-define-stage-receipt/waves/W2.md) | CRAFT-INVOKE-RECEIPT-002, latest run evidence | pass | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-CRAFT-INVOKE-RECEIPT-001 | [CRAFT-INVOKE-RECEIPT-001](work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-001.md) | `stages/02-invoke-define.md`; `receipt-contract.md`; `spells/invoke/define.md` | Contract must prove owner-stage execution, not another handoff. | none | task contract and shared contract note | Artifact contract names pass/block outputs and receipt validation. | Task contract grep/review | `rg -n "Invoke Define|expected_receipt_path|artifact_paths|validation|blockers" ...` | local-fallback | completed |
| SWU-CRAFT-INVOKE-RECEIPT-002 | [CRAFT-INVOKE-RECEIPT-002](work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-002.md) | `stages/02-invoke-define.md`; `REFINE-SEED-PROPOSAL.md`; `context-builder/context-pack.md` | The stage may pass with a real define artifact or block with an actionable owner-stage reason. | SWU-CRAFT-INVOKE-RECEIPT-001 | `stages/02-invoke-define.md`; `receipts/02-invoke-define.json`; invoke-define artifact subfolder | Receipt exists and maps to a real owner-stage artifact. | `jq empty`; artifact path existence; receipt field review | `jq empty <receipt>` and `test -e <artifact>` | manual or local-fallback | completed |
| SWU-CRAFT-INVOKE-RECEIPT-003 | [CRAFT-INVOKE-RECEIPT-003](work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-003.md) | latest `evidence-index.json`; `RESULT.md`; `README.md`; `SESSION-LEDGER.md`; `arcana/refine/SKILL.md` | Promotion remains deferred; downstream blockers should be named honestly. | SWU-CRAFT-INVOKE-RECEIPT-002 | current run evidence; README; SESSION-LEDGER; work-pack status | Package state reflects receipt-backed Invoke Define result and next route. | Local Refine skill re-evaluation and package sync grep | `jq` evidence check; local skill result review; `rg` package sync | manual local-skill | completed |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| none | n/a | No blocker prevents starting CRAFT-INVOKE-RECEIPT-001. | n/a | n/a | n/a |

## Non-Blocking Gaps

| Gap | Treatment |
| --- | --- |
| Legacy command-surface resume text exists in older stage handoffs. | Ignore it for current execution. Craft now uses local skill contracts directly; command-surface repair is not part of this path. |
| Downstream receipts may be needed after Invoke Define. | Defer until validation rerun reveals the next exact owner-stage blocker. |
| Craft promotion remains deferred. | Preserve [CRAFT-PROMOTION-READINESS.md](CRAFT-PROMOTION-READINESS.md). |

## Gate Checks

1. Do not promote Craft.
2. Do not count `stages/02-invoke-define.md` as pass evidence unless it is replaced or backed by a real owner-stage artifact and receipt.
3. Do not mutate canonical registry, command, runtime, sigil, or spell surfaces without a separate reviewed plan.
4. Do not reopen completed Context Builder receipt bridge work.
5. If Invoke Define cannot be executed through the local skill surface, write a `block` receipt with an actionable next action instead of leaving the stage as handoff-only.
6. Validate every receipt with local shell, `jq`, `rg`, or evidence-index inspection.

## Recommended Next Execution

```text
This work-pack is complete. The next route is a new narrow receipt work-pack for `Interrogation refine-review`.
```
