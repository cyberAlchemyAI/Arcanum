# Implementation Layering: Craft Invoke Define Stage Receipt

## Purpose

Plan the smallest receipt-backed path that lets the local Refine skill surface move past the current `Invoke Define` handoff-only blocker without broad runtime redesign or Craft promotion.

This layer model assumes the stage receipt bridge is already complete. It does not reopen receipt ingestion, Context Builder receipt proof, or runtime adapter design. It only plans the next owner-stage receipt: `Invoke Define`, and all follow-on execution is through local skill instructions and local artifacts.

## Source Evidence

| Source | Use |
| --- | --- |
| `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-HANDOFF.md` | Bounded continuation handoff and current blocker statement. |
| `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json` | Mechanical stage evidence: Context Builder has a receipt, Invoke Define has only `handoff_prepared`. |
| `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md` | Owner-stage handoff, stage request, and expected receipt path. Legacy resume text is historical only. |
| `development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md` | Required receipt fields and status mapping. |
| `development/craft/CRAFT-VALIDATION.md` | Validation/recomposition review surface. |
| `spells/invoke/README.md` and `spells/invoke/define.md` | Invoke ownership and define-mode contract. |
| `spells/invoke/plan.md` | Planning contract requiring layer mapping, work-pack, SWUs, and validation strategy. |
| `arcana/refine/SKILL.md` | Local Refine skill surface for receipt-backed validation review. |

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether the `Invoke Define` stage has a precise receipt artifact contract. | A receipt-specific artifact contract for `stages/02-invoke-define.md`. | Stage request interpretation, output artifact path, receipt fields, pass/block evidence, and validation checks. | Actual owner-stage execution and downstream Refine stages. | Task contract names the exact artifact(s) that prove Invoke Define ran. | Continue to receipt execution if contract is unambiguous. |
| L1 | After this layer, we know whether the parent/native surface can produce a valid `Invoke Define` receipt for the current Craft run. | Execute the Invoke Define stage directly and write `receipts/02-invoke-define.json`. | Owner-stage artifact creation or review, receipt JSON, `jq` validation, and artifact-path checks. | Interrogation, Distill, Invoke Design, Invoke Plan, and final synthesis receipts. | Receipt exists at expected path and passes local contract checks. | Continue to validation rerun if the receipt is usable. |
| L2 | After this layer, we know whether local Refine skill review accepts the `Invoke Define` receipt and reveals the next real downstream state. | Re-evaluate the existing run folder through the local Refine skill surface. | Receipt review, manifest/evidence consistency checks, first downstream blocker identification, and README/session-ledger sync. | Solving the next downstream owner-stage receipt unless it is already unblocked by this pass. | `evidence-index.json`, `RUN-MANIFEST.md`, `RESULT.md`, or an explicit local-skill result artifact show receipt-backed Invoke Define state. | Continue to the next exact blocker or close the receipt wave if validation passes. |
| L3 | After this layer, we know whether Craft has enough repeated receipt-backed validation evidence for promotion review. | Promotion-readiness refresh after at least one more real Craft run. | Evidence review only. | Canonical registry, sigil, spell, runtime, scoring, generated index, and role automation promotion. | Updated readiness review either preserves defer or opens an explicit promotion route. | Defer until evidence justifies promotion review. |

## Boundary Decisions

| Decision | Selected | Rationale |
| --- | --- | --- |
| Plan only the `Invoke Define` receipt, not every downstream receipt. | yes | The current exact blocker is `Invoke Define`; downstream stages are dependency-blocked and should be evaluated after this receipt exists. |
| Reuse the native receipt contract unchanged. | yes | The receipt bridge already passed; changing the contract would reopen completed work unnecessarily. |
| Produce an owner-stage artifact or block receipt, not just another handoff. | yes | Native Refine must not count `handoff_prepared` as pass evidence. |
| Keep execution inside `development/craft/` unless a task explicitly proves an owner surface must change. | yes | Craft remains candidate-local and promotion-deferred. |
| Treat Invoke plan semantics as local skill-surface planning, not command execution. | yes | The canonical Invoke plan contract is available as local skill/spell instructions; the command surface is not required for this Craft workflow. |

## Non-Regression Guardrails

- Do not count `stages/02-invoke-define.md` as owner-stage pass evidence by itself.
- Do not mutate canonical Arcanum registry, runtime adapters, sigils, or spells from this plan.
- Do not route follow-on execution through `tools/arcanum`, `.codex/commands`, or generated resume commands.
- Do not reopen completed Context Builder receipt bridge tasks.
- Do not solve Interrogation, Distill, Invoke Design, Invoke Plan, or final synthesis before `Invoke Define` receipt evidence exists.
- Do not promote Craft from this work-pack.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether the `Invoke Define` owner-stage receipt can be executed from a precise local contract.
- Major deferred scope: downstream owner-stage receipts and canonical Craft promotion.
