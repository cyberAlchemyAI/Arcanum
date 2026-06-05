# Invoke Result: Define

## Identity

| Field | Value |
| --- | --- |
| Mode | define |
| Spell | invoke |
| Canonical ID | invoke |
| Scope | library |
| Phase status | pass |
| Target | development/craft/CRAFT-VALIDATION.md |
| Execution surface | parent-native local-fallback |

Validation keywords:

```text
Mode: define
Target: development/craft/CRAFT-VALIDATION.md
```

## Source Inputs

| Source | Use |
| --- | --- |
| `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-SEED-PROPOSAL.md` | Seed proposal identifying the refinement target and runtime configuration. |
| `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/01-context-builder.md` | Runtime-native Context Builder stage handoff and context source. |
| `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/context-builder/context-pack.md` | Context Builder evidence baseline and obligations. |
| `spells/invoke/define.md` | Canonical Invoke define-mode contract. |
| `development/craft/work-packs/invoke-define-stage-receipt/shared/invoke-define-receipt-contract.md` | Local receipt contract for this owner-stage proof. |

## Define Output Interpretation

The refinement target is already a governed Craft validation guide:

```text
development/craft/CRAFT-VALIDATION.md
```

The Define stage does not need to create a new top-level Craft definition. Its owner-stage contribution is to make the current refinement request explicit enough for downstream review stages:

1. Target artifact: `development/craft/CRAFT-VALIDATION.md`.
2. Requested refinement mode: standard, no external research.
3. Current evidence state: Context Builder has receipt-backed pass evidence.
4. Current blocker: downstream stages require `Invoke Define` to return owner-stage evidence rather than a handoff stub.
5. Native output contract: preserve stage artifacts, receipts, and no-recursion behavior.

## Decisions

| Decision | Selected | Rationale |
| --- | --- | --- |
| Treat this as an update/clarification define stage rather than a new Craft definition. | yes | The target artifact already exists and the request is a refinement of its validation path. |
| Use parent-native local-fallback execution. | yes | The canonical Invoke define contract and all source inputs are available locally; no nested model-backed runtime is needed. |
| Defer downstream stage execution. | yes | Interrogation, Distill, Invoke Design, Invoke Plan, and final synthesis are separate stages and must wait for native Refine to ingest this receipt. |
| Keep promotion out of scope. | yes | Craft promotion remains deferred by the Craft readiness review. |

## Outputs

| Output | Path | Status |
| --- | --- | --- |
| Define-stage owner artifact | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/invoke-define/RESULT.md` | pass |
| Stage receipt | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json` | prepared by task-session |

## Unresolved Gaps

| Gap | Classification | Next Route |
| --- | --- | --- |
| Downstream stage evidence remains unevaluated until native Refine ingests this receipt. | deferred | `CRAFT-INVOKE-RECEIPT-003` reruns validation and names the next exact blocker. |
| Bare `$invoke` command is not exposed through `tools/arcanum --resolve invoke`. | non-blocking for this receipt | Keep command-surface repair out of this task unless a later plan reopens it. |
| Craft promotion evidence remains insufficient. | deferred | Continue local receipt-backed validation before promotion review. |

## Native Output Boundary

This artifact is the `Invoke Define` owner-stage output only. It does not execute, complete, or validate the downstream Interrogation, Distill, Invoke Design, Invoke Plan, or final synthesis stages.

It also does not mutate canonical Arcanum registry, command, runtime, sigil, spell, scoring, generated-index, or role-automation surfaces.

## Next Route

```text
$task-session development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md --task CRAFT-INVOKE-RECEIPT-003
```
