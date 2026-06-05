# Native Refine Stage Receipt Contract

## Purpose

A stage receipt is structured evidence that a native Refine owner stage actually ran after a runtime-native handoff was prepared.

The receipt is not the owner artifact itself and it is not the handoff prompt. It is the execution closeout record that lets native Refine decide whether downstream stages may proceed.

## Required Fields

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `receipt_id` | string | yes | Stable id for this receipt, unique within the Refine run. |
| `run_id` | string | yes | Refine run id the receipt belongs to. |
| `stage` | string | yes | Exact stage title from `stage_evidence[]`. |
| `owner` | string | yes | Stage owner command or capability, such as `context-builder`. |
| `status` | string | yes | One of `pass`, `flag`, `block`, `interrupted`, or `timeout`. |
| `evidence_kind` | string | yes | Must be `receipt` for owner-stage execution receipts. |
| `handoff_path` | string | yes | Path to the prepared stage handoff that requested the work. |
| `artifact_paths` | array of strings | yes | Owner-stage artifacts produced or inspected by the worker. Empty only when status is non-pass and the blocker explains why. |
| `validation` | array of objects | yes | Checks performed by the worker, each with `check`, `result`, and optional `notes`. |
| `blockers` | array of objects | yes | Empty when no blocker remains; otherwise each blocker has `id`, `reason`, and `next_action`. |
| `created_at` | string | recommended | UTC timestamp for receipt creation. |
| `worker` | object | recommended | Execution surface and actor information when available. |

## Status Mapping

| Receipt Status | Native Refine Stage Status | Stage Evidence Kind | Required Evidence |
| --- | --- | --- | --- |
| `pass` | `pass` | `receipt` | At least one artifact path and passing validation evidence. |
| `flag` | `flag` | `receipt` | Artifact or partial evidence plus a reason the result needs review. |
| `block` | `block` | `receipt` | At least one blocker with an actionable `next_action`. |
| `interrupted` | `flag` | `receipt` | Blocker or note explaining the interruption and recovery path. |
| `timeout` | `flag` | `receipt` | Blocker or note explaining timeout and retry path. |

## Non-Receipt Rule

A runtime-native handoff stub is not a receipt, even when it is well-formed. A handoff has `evidence_kind=handoff_prepared`; a receipt has `evidence_kind=receipt` and proves that the owner-stage work was attempted by the parent/native surface.

## Minimal Context Builder Pass Receipt

```json
{
  "receipt_id": "receipt-20260601T015552Z-craft-validation-md-context-builder",
  "run_id": "20260601T015552Z-craft-validation-md",
  "stage": "Context Builder evidence baseline",
  "owner": "context-builder",
  "status": "pass",
  "evidence_kind": "receipt",
  "handoff_path": "development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md/stages/01-context-builder.md",
  "artifact_paths": [
    "development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md/context-builder/context-pack.md",
    "development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md/context-builder/context-index.json"
  ],
  "validation": [
    {
      "check": "context-index-json",
      "result": "pass",
      "notes": "context-index.json parsed successfully"
    }
  ],
  "blockers": [],
  "created_at": "2026-06-01T00:00:00Z",
  "worker": {
    "execution_surface": "parent-native",
    "capability_ref": "context-builder"
  }
}
```

## Minimal Block Receipt

```json
{
  "receipt_id": "receipt-20260601T015552Z-craft-validation-md-context-builder-block",
  "run_id": "20260601T015552Z-craft-validation-md",
  "stage": "Context Builder evidence baseline",
  "owner": "context-builder",
  "status": "block",
  "evidence_kind": "receipt",
  "handoff_path": "development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md/stages/01-context-builder.md",
  "artifact_paths": [],
  "validation": [
    {
      "check": "parent-native-execution",
      "result": "block",
      "notes": "parent-native execution surface was unavailable"
    }
  ],
  "blockers": [
    {
      "id": "BLK-PARENT-NATIVE-EXECUTION",
      "reason": "The parent runtime could not execute the context-builder owner stage.",
      "next_action": "Run the Context Builder stage through Task Session or another parent-native worker and write a receipt."
    }
  ]
}
```

## Validation Rule

A receipt is locally valid when:

1. Required fields exist and are non-empty.
2. `evidence_kind` equals `receipt`.
3. `status` is one of the allowed receipt statuses.
4. `validation` is an array.
5. `blockers` is an array.
6. `artifact_paths` is non-empty when `status=pass`.
7. Non-pass statuses include either a blocker or validation note that explains the recovery path.
