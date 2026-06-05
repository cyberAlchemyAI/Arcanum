# Session Handoff: Craft Invoke Define Stage Receipt

## Refresh Note

Refreshed 2026-06-02 after the command-surface route was retired for this Craft workflow. The historical `$invoke plan` and generated resume-command language below has been replaced by local skill-surface execution: use the Invoke, Task Session, and Refine `SKILL.md` contracts directly, and do not route this work through `tools/arcanum`, `.codex/commands`, or generated resume commands.

## Identity

- Source session reference: Craft durable development session in `development/craft/`
- Destination label: Craft Invoke Define stage receipt
- Handoff type: execution-continuation
- Target project or lifecycle: Craft validation / local Refine receipt review
- Created for: preserving the original blocker context while steering follow-on work through local skills

## New Session Prompt

```text
Continue the Craft development session focused only on the next receipt blocker.

Use development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-HANDOFF.md as the source handoff.

Goal: execute the next bounded work-pack task using local skill surfaces so Refine validation can move past the current `handoff_prepared` blocker.

Current route:

task-session development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md --task CRAFT-INVOKE-RECEIPT-003

Use the local task-session, invoke, and refine skill instructions directly. Do not call tools/arcanum, .codex/commands, or generated resume commands. Do not promote Craft. Do not mutate canonical Arcanum registry, runtime adapters, sigils, or spells unless a reviewed plan explicitly approves that mutation. Keep the work inside development/craft/ unless the plan proves another owner must take it.
```

## Route Rationale

- Recommended next route: `task-session development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md --task CRAFT-INVOKE-RECEIPT-003`
- Rationale: the `Invoke Define` owner-stage receipt now exists; the remaining active step is local Refine skill review and package-state synchronization.
- Lifecycle owner: task-session for bounded execution, refine for local receipt-backed validation review

## Context Builder Selection

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| Identify the current blocker. | covered | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json` | Shows `Invoke Define` as `status=flag`, `evidence_kind=handoff_prepared`, and no `receipt_path`. |
| Preserve the completed receipt bridge. | covered | `development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md` | Confirms CRAFT-NATIVE-RECEIPT-001 through 005 are completed and should not be reopened. |
| Preserve the receipt contract. | covered | `development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md` | Defines required fields and status mapping for the next owner-stage receipt. |
| Preserve package state and next route. | covered | `development/craft/README.md`, `development/craft/SESSION-LEDGER.md` | Both name the next move as `CRAFT-INVOKE-DEFINE-STAGE-RECEIPT`. |
| Preserve promotion boundary. | covered | `development/craft/CRAFT-PROMOTION-READINESS.md` | Craft promotion remains deferred. |

Strict coverage: pass

## Selected Session Context

### Current State

Craft status is:

```text
refine-validation-invoke-define-receipt-blocked-promotion-deferred
```

The latest durable Refine validation run is:

```text
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof
```

That run has dispatch validation `pass`, Context Builder receipt evidence `pass`, and a downstream block at `Invoke Define`.

### Completed Work To Preserve

The native stage receipt work-pack is complete:

```text
CRAFT-NATIVE-RECEIPT-001: done
CRAFT-NATIVE-RECEIPT-002: done
CRAFT-NATIVE-RECEIPT-003: done
CRAFT-NATIVE-RECEIPT-004: done
CRAFT-NATIVE-RECEIPT-005: done
```

Completed capabilities:

- local Refine review preserves stage evidence kinds without false pass semantics,
- runtime-native handoff stubs remain `evidence_kind=handoff_prepared`,
- valid receipt files can mark a stage as `evidence_kind=receipt`,
- generated stage handoffs include expected receipt paths; generated resume commands are historical only,
- Context Builder now has durable parent-native receipt proof.

### Blocking Evidence

From the latest `evidence-index.json`:

```text
Stage: Invoke Define
Owner: invoke
Evidence kind: handoff_prepared
Status: flag
Receipt path: null
Verdict: Stage produced a runtime-native handoff stub only; owner-stage execution receipt is still required.
```

Downstream stages block because `Invoke Define` did not produce pass evidence.

### Receipt Contract To Reuse

The next receipt should follow the local stage receipt contract:

```text
receipt_id
run_id
stage
owner
status
evidence_kind=receipt
handoff_path
artifact_paths
validation
blockers
created_at
worker
```

For `status=pass`, the receipt must include at least one owner-stage artifact path and passing validation evidence.

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| Full Craft initial formal model | Too broad for this execution-continuation thread. |
| Recursive ledger schema details | Not needed to plan the Invoke Define stage receipt. |
| Runtime interface side-thread | Already split into `ARCANUM-SKILL-RUNTIME-HANDOFF.md`; related but not the immediate blocker. |
| Priority scoring and role delegation ideas | Deferred product concerns, not receipt-bridge blockers. |
| Full prior conversation transcript | Replaced by obligation-linked artifact context above. |

## Target Boundary

In scope for the new thread:

- define the minimum owner-stage receipt path for `Invoke Define`,
- decide what artifact(s) prove the Invoke Define stage actually ran,
- create an Invoke plan/work-pack for that receipt path,
- keep downstream validation tied to `CRAFT-VALIDATION.md`,
- preserve Refine's no-false-pass rule.

Out of scope for the new thread:

- promoting Craft,
- redesigning all runtime adapters,
- routing through canonical command surfaces,
- changing canonical Arcanum runtime surfaces without explicit reviewed plan approval,
- reopening completed Context Builder receipt work,
- solving every downstream stage receipt in the same pass.

Prior decisions to preserve:

- Craft stays under `development/craft/` until explicit promotion.
- Handoff preparation is not owner-stage pass evidence.
- Receipt-backed validation is required before downstream stages can proceed.
- The next exact blocker is `Invoke Define`.

## Gaps And Blockers

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| `Invoke Define` owner-stage execution receipt. | Craft / Invoke planning | resolved | Receipt exists at `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json`. |
| Downstream Refine stages depend on Invoke Define pass evidence. | Refine validation | open | Review the existing run through the local Refine skill surface and synchronize package state. |
| Craft promotion evidence is still insufficient. | Craft readiness | deferred | Continue local receipt-backed validation before promotion. |

## Next-Session Start Prompt

```text
Use development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-HANDOFF.md as the source handoff.

We are continuing Craft from the latest blocker. The native stage receipt bridge is complete and Context Builder now has durable receipt-backed pass evidence in:

development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof

The current blocker is `Invoke Define`: its stage evidence is `status=flag`, `evidence_kind=handoff_prepared`, and `receipt_path=null`. Downstream Refine stages block because Invoke Define has not produced owner-stage pass evidence.

Continue with:

task-session development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md --task CRAFT-INVOKE-RECEIPT-003

Use local skill surfaces only. The output should be a local Refine skill review and package-state sync for the existing Invoke Define receipt. Reuse the receipt contract at development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md. Do not promote Craft or mutate canonical runtime surfaces unless the plan explicitly gates that decision.
```

## Provenance

- Source refs:
  - `development/craft/README.md`
  - `development/craft/SESSION-LEDGER.md`
  - `development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md`
  - `development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md`
  - `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json`
- Context Builder mode: standard, artifact-selected
- Evidence date: 2026-06-01
- Output path: `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-HANDOFF.md`

## Gate Result

- Status: pass
- Reason: the handoff has a concrete next route, source evidence, strict obligation coverage, and a bounded execution-continuation target.
