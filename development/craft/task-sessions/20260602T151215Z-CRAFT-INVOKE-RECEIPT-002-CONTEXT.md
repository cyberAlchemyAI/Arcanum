# Context Pack: CRAFT-INVOKE-RECEIPT-002

## Identity

| Field | Value |
| --- | --- |
| Task | `CRAFT-INVOKE-RECEIPT-002` |
| SWU | `SWU-CRAFT-INVOKE-RECEIPT-002` |
| Work-pack | `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md` |
| Mode | lean |
| Strict coverage | pass |
| Created at | 2026-06-02T15:12:15Z |

## Obligation Coverage

| Obligation | Status | Evidence |
| --- | --- | --- |
| Execute the current `Invoke Define` owner stage or write a block receipt. | covered | Task contract permits parent-native/local-fallback execution and requires `receipts/02-invoke-define.json`. |
| Use the existing stage request. | covered | `stages/02-invoke-define.md` names the request, handoff path, expected receipt path, and resume command. |
| Preserve receipt semantics. | covered | `shared/invoke-define-receipt-contract.md` and native receipt contract require `evidence_kind=receipt`, artifact paths, validation, and blockers. |
| Cite real owner-stage artifact paths for a pass receipt. | covered | Preferred artifact location is `invoke-define/`. |
| Do not execute downstream stages. | covered | Contract requires explicit boundary that Interrogation, Distill, Invoke Design, Invoke Plan, and final synthesis are not completed here. |
| Keep canonical surfaces untouched. | covered | Work-pack gate forbids registry, command, runtime, sigil, or spell mutation. |

## Selected Context

### Current Stage Handoff

Source: `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md`

Selectors:

- `run_id`: `20260601T080122Z-context-builder-receipt-proof`
- `stage`: `Invoke Define`
- `owner`: `invoke`
- `handoff_path`: `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md`
- `expected_receipt_path`: `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json`
- stage request targets `development/craft/CRAFT-VALIDATION.md`.

### Receipt Contract

Source: `development/craft/work-packs/invoke-define-stage-receipt/shared/invoke-define-receipt-contract.md`

Selectors:

- Pass artifact must show mode `define`, capability `invoke`, target `CRAFT-VALIDATION.md`, source inputs, output interpretation, decisions, gaps, native boundary, and no downstream execution claim.
- Pass receipt must cite at least one owner-stage artifact path and include passing validation checks.

### Source Inputs

Sources:

- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-SEED-PROPOSAL.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/context-builder/context-pack.md`
- `spells/invoke/define.md`

Selectors:

- Target is `development/craft/CRAFT-VALIDATION.md`.
- Preset is `standard`; research is `no-research`.
- Context Builder obligations: no recursion, handoff-only evidence is non-pass, receipt proves owner-stage execution.
- Invoke define produces a governed baseline with explicit decisions, gaps, output paths, and next route.

## Execution Decision

Selected: parent-native/local-fallback pass receipt.

Rationale: all required source inputs are available locally, the owner-stage artifact can be produced directly from the canonical Invoke define contract, and no command/runtime mutation is needed.

## Validation Surface

```text
jq empty development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
jq -r '.artifact_paths[]?' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json | xargs -r -I{} test -e {}
jq '{stage,owner,status,evidence_kind,handoff_path,artifact_paths,validation,blockers}' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
rg -n "Mode: define|Target: development/craft/CRAFT-VALIDATION.md|REFINE-SEED-PROPOSAL|01-context-builder|downstream" development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/invoke-define/RESULT.md
```

## Context Builder Result

- Files selected: 5
- Snippets selected: 5
- Obligation coverage: 100%
- Noise ratio: low
- Strict coverage: pass
- Blockers: 0
