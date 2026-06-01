# Implementation Layering: Craft Native Stage Execution Receipts

## Purpose

Plan the smallest receipt-backed path that lets native Refine continue after a runtime-native stage handoff without counting the handoff itself as completed owner-stage work.

This plan does not implement a full cross-runtime skill execution interface. It creates a narrow parent-native receipt bridge for Refine stage evidence: handoff prepared -> owner stage executed by the parent/native surface -> receipt ingested -> downstream stages may proceed.

## Source Evidence

| Source | Use |
| --- | --- |
| `development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md/evidence-index.json` | Current blocker: Context Builder stage is `flag` with `evidence_kind=handoff_prepared`. |
| `development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md/RUN-MANIFEST.md` | Human-readable stage evidence and next route. |
| `development/craft/CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-WORK-PACK.md` | Completed prerequisite work-pack proving false-pass semantics are repaired. |
| `tools/arcanum` | Native Refine orchestration and stage evidence implementation surface. |
| `spells/invoke/plan.md` | Planning contract requiring layer mapping, work-pack, SWUs, and validation strategy. |

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether a stage receipt has a stable local contract. | Receipt schema and expected fields. | Receipt fields, statuses, artifact references, blocker shape, and validation rule. | Executing owner stages. | Receipt schema/example can be inspected and validated. | Continue to ingestion if contract is sufficient. |
| L1 | After this layer, we know whether native Refine can ingest a receipt instead of treating a handoff as pass. | Receipt discovery and classification in `tools/arcanum`. | Receipt path convention, JSON validation, pass/flag/block mapping, evidence index propagation. | Parent-native worker orchestration. | A synthetic receipt changes the stage from handoff-only flag to receipt-backed pass/block. | Continue to parent handoff/resume if ingestion is reliable. |
| L2 | After this layer, we know whether a parent-native stage worker can receive a strict handoff and return a receipt. | Stage handoff/resume contract. | Handoff artifact fields, expected receipt path, resume/rerun behavior, context-builder stage receipt path. | Full generic runtime adapter API across Codex/Claude/Copilot. | A task-session or native worker can produce a receipt for the Context Builder stage. | Continue to Craft validation rerun if the receipt path is usable. |
| L3 | After this layer, we know whether Craft validation can proceed with receipt-backed native stage evidence. | Craft validation rerun and state sync. | Refine rerun, README/session-ledger sync, promotion deferral preservation. | Craft promotion. | Latest Craft Refine run is either pass with real receipts or block with a later exact receipt gap. | Package or defer based on evidence. |

## Boundary Decisions

| Decision | Selected | Rationale |
| --- | --- | --- |
| Build a receipt bridge, not a full runtime execution substrate. | yes | The current blocker is missing owner-stage receipt evidence, not command resolution or false-pass classification. |
| Keep initial implementation inside native Refine orchestration. | yes | `tools/arcanum` owns the current stage evidence and can ingest receipt files without spawning nested model CLIs. |
| Let Task Session or the parent runtime produce stage receipts. | yes | The shell wrapper cannot itself perform model reasoning; the parent/native surface must execute the owner skill and write the receipt. |
| Preserve `handoff_prepared` as non-pass evidence. | yes | A handoff is a request for work, not proof that the owner stage ran. |
| Defer cross-runtime adapter design. | yes | That broader interface remains covered by `ARCANUM-SKILL-RUNTIME-HANDOFF.md` and should not block this narrow Craft validation repair. |

## Non-Regression Guardrails

- Do not count a handoff prompt as completed owner-stage work.
- Do not reintroduce nested Codex CLI execution as the default native stage path.
- Do not promote Craft from this work-pack.
- Do not require broad runtime adapter redesign to validate a single receipt-backed stage path.
- Preserve validated `REFINE-DISPATCH.json` generation from the previous work-pack.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether the receipt contract is precise enough for `tools/arcanum`, Task Session, and parent-native workers to share.
- Major deferred scope: generalized cross-runtime skill execution and registry promotion.
