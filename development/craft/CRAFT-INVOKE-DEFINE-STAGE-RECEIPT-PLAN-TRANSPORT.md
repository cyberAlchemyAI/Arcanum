# Plan Transport: Craft Invoke Define Stage Receipt

## Purpose

Record the provenance for the Invoke plan output targeting the next Craft validation blocker.

## Invocation

```text
$invoke plan development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT
```

## Execution Surface

The local repo helper does not currently expose a bare `invoke` command through `tools/arcanum --resolve invoke`. This plan was therefore authored directly from the canonical Invoke skill/spell contracts.

Follow-on execution should also use local skill contracts directly. Command-surface resume text in older generated handoffs is historical and is not authority for this Craft receipt path.

- `/mnt/c/Users/vlad_/.codex/skills/invoke/SKILL.md`
- `spells/invoke/README.md`
- `spells/invoke/plan.md`
- `spells/invoke/define.md`

## Source Selection

| Source | Role |
| --- | --- |
| `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-HANDOFF.md` | Continuation boundary and exact blocker. |
| `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json` | Mechanical proof that Invoke Define is `handoff_prepared`. |
| `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/02-invoke-define.md` | Stage request, expected receipt path, and resume command. |
| `development/craft/work-packs/native-stage-execution-receipts/receipt-contract.md` | Required receipt structure and status mapping. |
| `development/craft/CRAFT-PROMOTION-READINESS.md` | Promotion deferral boundary. |

## Produced Artifacts

| Artifact | Purpose |
| --- | --- |
| `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-IMPLEMENTATION-LAYERING.md` | L0-L3 decision boundaries. |
| `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md` | Executable work-pack and SWU manifest. |
| `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-EXECUTION-PACK.md` | Wave sequencing. |
| `development/craft/work-packs/invoke-define-stage-receipt/tasks/` | Split task contracts. |
| `development/craft/work-packs/invoke-define-stage-receipt/waves/` | Split wave contracts. |

## Gate Result

| Gate | Result |
| --- | --- |
| Approved design/source refs available | pass |
| Layering artifact produced | pass |
| Work-pack produced | pass |
| Split execution pack produced | pass |
| SWU manifest included | pass |
| Promotion boundary preserved | pass |
| Runtime mutation avoided | pass |

## Recommended Next Route

```text
$task-session development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md --task CRAFT-INVOKE-RECEIPT-001
```
