# Context Pack: CRAFT-INVOKE-RECEIPT-001

## Identity

| Field | Value |
| --- | --- |
| Task | `CRAFT-INVOKE-RECEIPT-001` |
| SWU | `SWU-CRAFT-INVOKE-RECEIPT-001` |
| Work-pack | `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md` |
| Mode | lean |
| Strict coverage | pass |
| Created at | 2026-06-02T14:59:30Z |

## Obligation Coverage

| Obligation | Status | Evidence |
| --- | --- | --- |
| Select one ready task from the work-pack. | covered | `CRAFT-INVOKE-RECEIPT-001` is the first not-started ready task. |
| Preserve current blocker. | covered | `Invoke Define` remains `status=flag`, `evidence_kind=handoff_prepared`, and `receipt_path=null` in the current run context. |
| Define exact receipt artifact contract. | covered | Task source contracts include the stage handoff and native receipt contract. |
| Preserve pass and block receipt semantics. | covered | Native receipt contract defines required fields and status mapping. |
| Keep work scoped to contract definition. | covered | Write scope is task contract and optional shared note only. |
| Avoid downstream stage execution. | covered | Work-pack gate says downstream receipts are deferred until validation rerun reveals the next exact blocker. |
| Preserve promotion deferral. | covered | Work-pack non-blocking gaps and gate checks keep Craft promotion deferred. |

## Selected Context

### Work-Pack Control

Source: `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md`

Selectors:

- Control fields: `workPackGateStatus=pass`, `outputMode=split`, `activeLayerWindow=L0-L2`.
- Task board row: `CRAFT-INVOKE-RECEIPT-001` defines the `Invoke Define` receipt artifact contract.
- SWU row: `SWU-CRAFT-INVOKE-RECEIPT-001` is ready and local-fallback owned.
- Gate checks: do not promote Craft; do not count the handoff as pass evidence; do not mutate canonical surfaces.

### Task Contract

Source: `development/craft/work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-001.md`

Selectors:

- Objective: define exact artifact and receipt evidence for current `Invoke Define` stage.
- Source anchors: stage request, expected receipt path, receipt required fields, Invoke define-mode owner contract.
- Done criteria: next worker knows artifact to produce or inspect; next worker knows pass/block receipt shape; no downstream stage included.

### Stage Handoff

Source: `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md`

Selectors:

- `run_id`: `20260601T080122Z-context-builder-receipt-proof`
- `stage`: `Invoke Define`
- `owner`: `invoke`
- `handoff_path`: `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md`
- `expected_receipt_path`: `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json`
- Stage request targets `development/craft/CRAFT-VALIDATION.md` using the seed proposal and Context Builder stage.

### Receipt Contract

Source: `development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md`

Selectors:

- Required fields: `receipt_id`, `run_id`, `stage`, `owner`, `status`, `evidence_kind`, `handoff_path`, `artifact_paths`, `validation`, `blockers`.
- `evidence_kind` must be `receipt`.
- `pass` requires at least one artifact path and passing validation evidence.
- Handoff stubs remain `evidence_kind=handoff_prepared` and are not receipts.

### Invoke Define Contract

Source: `spells/invoke/define.md`

Selectors:

- Define mode produces or updates a governed specification/glossary baseline with decisions, evidence-aware routing, and transport-ready handoff artifacts.
- Define mode may emit implementation-layering seed or record a layering gap.
- No silent upstream mutation; candidate glossary promotion is never automatic.
- Output contract includes mode, spell, phase status, outputs, decisions, gaps, and next route.

## Constraints

- Do not execute `Invoke Define` in this task.
- Do not write `receipts/02-invoke-define.json` in this task.
- Do not mutate canonical Arcanum registry, command, runtime, sigil, or spell surfaces.
- Do not reopen Context Builder receipt work.
- Do not promote Craft.

## Validation Surface

```text
rg -n "Invoke Define|expected receipt|artifact_paths|validation|blockers|receipt_id|handoff_path" development/craft/work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-001.md development/craft/work-packs/invoke-define-stage-receipt/shared/invoke-define-receipt-contract.md
```

## Context Builder Result

- Files selected: 5
- Snippets selected: 5
- Obligation coverage: 100%
- Noise ratio: low
- Strict coverage: pass
- Blockers: 0
