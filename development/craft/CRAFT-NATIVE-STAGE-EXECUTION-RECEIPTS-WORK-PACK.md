# WORK-PACK: Craft Native Stage Execution Receipts

## Purpose

Create a narrow receipt-backed path for native Refine stage execution so a parent/native worker can execute an owner stage and return evidence without nested model CLI recursion.

This work-pack is produced by Invoke plan. It does not execute implementation work.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for task-session execution. |
| complexity | medium | Runtime receipt contract, native Refine ingestion, handoff/resume semantics, and validation sync. |
| outputMode | split | Task and wave contracts live under `work-packs/native-stage-execution-receipts/`. |
| executionPackRef | [CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-EXECUTION-PACK.md](CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-EXECUTION-PACK.md) | Wave sequencing. |
| layeringArtifactRef | [CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-IMPLEMENTATION-LAYERING.md](CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-IMPLEMENTATION-LAYERING.md) | L0-L3 layer model. |
| activeLayerWindow | L0 |
| lastUpdatedAt | 2026-06-01 |
| readinessProfile | native-stage-receipt-bridge |

## Objective Summary

Fix the remaining Craft Refine validation blocker by enabling this evidence chain:

```text
runtime-native handoff prepared
-> parent/native owner stage execution
-> receipt written at expected path
-> native Refine ingests receipt
-> downstream stage dependency can evaluate real evidence
```

Success condition:

- Native Refine never counts a handoff as owner-stage pass evidence.
- A valid receipt can mark a stage as receipt-backed `pass`, `flag`, or `block`.
- Craft validation can be rerun and synchronized against receipt-backed evidence.

## Planning Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Latest blocker evidence | Objective Summary and task dependencies | Preserve `Context Builder evidence baseline` as the first blocked handoff-only stage. |
| Layering artifact | Delivery slices and waves | Each wave maps to L0-L3 receipt bridge decisions. |
| Completed receipt semantics work-pack | Gate checks | Preserve no false-pass semantics and validated dispatch generation. |
| Validation strategy | Task validation surfaces | Every task must be checkable with local shell, `jq`, `rg`, or generated Refine evidence. |
| SWU policy | Task files and SWU manifest | One SWU per execution task for task-session readiness. |

## Receipt Contract Draft

The first task may refine this contract, but the work-pack starts with this minimum shape:

```json
{
  "receipt_id": "receipt-<run-id>-<stage-slug>",
  "run_id": "<refine-run-id>",
  "stage": "<stage title>",
  "owner": "<stage owner>",
  "status": "pass | flag | block | interrupted | timeout",
  "evidence_kind": "receipt",
  "handoff_path": "<path to prepared stage handoff>",
  "artifact_paths": ["<owner artifact path>"],
  "validation": [
    {
      "check": "<command or review check>",
      "result": "pass | flag | block",
      "notes": "<short note>"
    }
  ],
  "blockers": [
    {
      "id": "<optional blocker id>",
      "reason": "<actionable reason>",
      "next_action": "<unblock action>"
    }
  ]
}
```

Mapping rule:

- Receipt `status=pass` maps to stage `status=pass`, `evidence_kind=receipt`, and populated `receipt_path`.
- Receipt `status=flag` maps to stage `status=flag`, `evidence_kind=receipt`, and populated `receipt_path`.
- Receipt `status=block`, `interrupted`, or `timeout` maps to non-pass stage evidence with an actionable reason.
- A runtime-native handoff stub without a receipt remains `evidence_kind=handoff_prepared`.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-NATIVE-RECEIPT-001 | Stage receipt contract is explicit and reviewable. | L0 | [W0](work-packs/native-stage-execution-receipts/waves/W0.md) | latest Craft Refine blocker evidence | `rg` confirms required receipt fields and mapping rules. |
| S-NATIVE-RECEIPT-002 | Native Refine can ingest validated receipt files. | L1 | [W1](work-packs/native-stage-execution-receipts/waves/W1.md) | S-NATIVE-RECEIPT-001 | Synthetic receipt affects `stage_evidence[]` without false pass. |
| S-NATIVE-RECEIPT-003 | Stage handoffs name expected receipt path and resume command. | L2 | [W2](work-packs/native-stage-execution-receipts/waves/W2.md) | S-NATIVE-RECEIPT-002 | Generated handoff includes `expected_receipt_path` and `resume_command`. |
| S-NATIVE-RECEIPT-004 | Context Builder stage has first parent-native receipt proof. | L2 | [W2](work-packs/native-stage-execution-receipts/waves/W2.md) | S-NATIVE-RECEIPT-003 | Receipt JSON validates and evidence index shows `evidence_kind=receipt`. |
| S-NATIVE-RECEIPT-005 | Craft validation rerun reflects receipt-backed state. | L3 | [W3](work-packs/native-stage-execution-receipts/waves/W3.md) | S-NATIVE-RECEIPT-004 | Refine rerun plus README/session ledger agreement. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [CRAFT-NATIVE-RECEIPT-001](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-001.md) | Define stage receipt contract. | L0 | medium | [W0](work-packs/native-stage-execution-receipts/waves/W0.md) | latest evidence index, `tools/arcanum` | ready | not-started |
| [CRAFT-NATIVE-RECEIPT-002](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-002.md) | Implement receipt ingestion in native Refine. | L1 | medium | [W1](work-packs/native-stage-execution-receipts/waves/W1.md) | `tools/arcanum` | ready-after-CRAFT-NATIVE-RECEIPT-001 | not-started |
| [CRAFT-NATIVE-RECEIPT-003](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-003.md) | Add parent-native stage handoff and resume flow. | L2 | medium | [W2](work-packs/native-stage-execution-receipts/waves/W2.md) | `tools/arcanum`, generated stage handoff | ready-after-CRAFT-NATIVE-RECEIPT-002 | not-started |
| [CRAFT-NATIVE-RECEIPT-004](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-004.md) | Produce first Context Builder stage receipt. | L2 | medium | [W2](work-packs/native-stage-execution-receipts/waves/W2.md) | Context Builder handoff, `CRAFT-VALIDATION.md` | ready-after-CRAFT-NATIVE-RECEIPT-003 | not-started |
| [CRAFT-NATIVE-RECEIPT-005](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-005.md) | Rerun Craft validation and sync receipt-backed state. | L3 | low | [W3](work-packs/native-stage-execution-receipts/waves/W3.md) | README, SESSION-LEDGER, latest run | ready-after-CRAFT-NATIVE-RECEIPT-004 | not-started |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-CRAFT-NATIVE-RECEIPT-001 | [CRAFT-NATIVE-RECEIPT-001](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-001.md) | latest `stage_evidence[]`, `tools/arcanum` evidence fields | receipt contract draft | none | work-pack or local receipt schema/example | receipt fields and mapping rules are explicit | receipt contract grep/review | `rg -n "receipt_id|evidence_kind|handoff_path|status|validation|blockers" ...` | local-fallback | ready |
| SWU-CRAFT-NATIVE-RECEIPT-002 | [CRAFT-NATIVE-RECEIPT-002](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-002.md) | `tools/arcanum` `run_refine_command_stage`, `record_refine_stage` | receipt ingestion | SWU-CRAFT-NATIVE-RECEIPT-001 | `tools/arcanum` | valid receipt maps into stage evidence | synthetic receipt inspection | `bash -n tools/arcanum`; `jq` evidence check | local-fallback | ready-after-CRAFT-NATIVE-RECEIPT-001 |
| SWU-CRAFT-NATIVE-RECEIPT-003 | [CRAFT-NATIVE-RECEIPT-003](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-003.md) | generated handoff stage, `tools/arcanum` runtime handoff output | parent-native handoff/resume | SWU-CRAFT-NATIVE-RECEIPT-002 | `tools/arcanum` | handoff names expected receipt and resume command | generated handoff inspection | `rg -n "expected_receipt_path|resume_command|stage_request|handoff_path" <stage>` | local-fallback | ready-after-CRAFT-NATIVE-RECEIPT-002 |
| SWU-CRAFT-NATIVE-RECEIPT-004 | [CRAFT-NATIVE-RECEIPT-004](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-004.md) | Context Builder handoff, Context Builder skill, Craft validation target | first owner-stage receipt | SWU-CRAFT-NATIVE-RECEIPT-003 | generated receipt path; optional task evidence | Context Builder stage has receipt-backed evidence | receipt JSON and evidence index | `jq empty <receipt>`; `jq` stage evidence check | subagent or local-fallback | ready-after-CRAFT-NATIVE-RECEIPT-003 |
| SWU-CRAFT-NATIVE-RECEIPT-005 | [CRAFT-NATIVE-RECEIPT-005](work-packs/native-stage-execution-receipts/tasks/CRAFT-NATIVE-RECEIPT-005.md) | latest receipt-backed run, README, SESSION-LEDGER | package sync | SWU-CRAFT-NATIVE-RECEIPT-004 | README; SESSION-LEDGER; work-pack evidence | package state reflects receipt-backed result | Refine rerun and grep | `tools/arcanum --exec ... refine ...`; `rg` package sync | manual | ready-after-CRAFT-NATIVE-RECEIPT-004 |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| none | n/a | No blocker prevents starting CRAFT-NATIVE-RECEIPT-001. | n/a | n/a | n/a |

## Non-Blocking Gaps

| Gap | Treatment |
| --- | --- |
| Full cross-runtime skill execution interface | Deferred to `ARCANUM-SKILL-RUNTIME-HANDOFF.md`; this work-pack only creates a local native Refine receipt bridge. |
| Craft promotion | Deferred by `CRAFT-PROMOTION-READINESS.md`. |
| Downstream owner-stage receipts beyond Context Builder | Defer until the first receipt path works; later tasks can repeat the same pattern for Invoke, Interrogation, Distill, and final synthesis. |

## Gate Checks

1. Do not promote Craft.
2. Do not count a handoff prompt as completed owner-stage work.
3. Do not reintroduce nested model-backed CLI execution as the default native path.
4. Do not reopen completed `dispatch-spec` or `runtime-handoff` command-surface tasks unless a regression proves they broke.
5. Block if the fix requires broad runtime adapter redesign instead of a local receipt bridge.
6. Every mutation-capable task must validate with local shell, `jq`, `rg`, or generated Refine evidence.

## Recommended Next Execution

```text
$task-session development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md --task CRAFT-NATIVE-RECEIPT-001
```
