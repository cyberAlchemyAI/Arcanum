# Refresh Report: Craft Invoke Define Stage Receipt

## Identity

| Field | Value |
| --- | --- |
| refresh_id | CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-REFRESH-20260602 |
| target | `development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-*` active workflow surfaces |
| mode | apply-approved |
| date | 2026-06-02 |
| requested_by | user correction: active Craft work should use local skill surface, not command surface |

## Source Signals

| Signal | Type | Evidence | Decision |
| --- | --- | --- | --- |
| Active task 003 attempted to follow stale command-surface resume guidance. | artifact_drift | The route referenced `tools/arcanum`/command resolution even though local skills are the intended execution surface. | Refresh active steering artifacts to local skills. |
| User explicitly retired command-surface routing for this work. | route_changed | "everything should use local skill surface" | Treat command-surface references as historical unless they are completed evidence. |
| `Invoke Define` receipt now exists after task 002. | status_changed | `receipts/02-invoke-define.json` and `invoke-define/RESULT.md` exist under the latest run folder. | Change top-level state from receipt-planned to local-skill sync pending. |

## Target Inventory

| Artifact | Action | Reason |
| --- | --- | --- |
| `CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-HANDOFF.md` | refreshed | Original handoff still recommended command-flavored planning and resume language. |
| `CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-IMPLEMENTATION-LAYERING.md` | refreshed | L2 and boundary decisions still described native/command execution. |
| `CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-EXECUTION-PACK.md` | refreshed | W2 still described a rerun rather than local Refine skill review. |
| `CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md` | refreshed | Objective/status language still used parent/native phrasing and command-surface boundaries. |
| `work-packs/invoke-define-stage-receipt/waves/W2.md` | refreshed | Wave title and goal now match local skill validation sync. |
| `work-packs/invoke-define-stage-receipt/tasks/CRAFT-INVOKE-RECEIPT-003.md` | refreshed | Task title and implementation path now name local skill validation sync. |
| `work-packs/invoke-define-stage-receipt/shared/context.md` | preserved | Already identifies `arcana/refine/SKILL.md` and rejects command routing. |
| `README.md` | refreshed | Current verdict and latest-run summary were stale after task 002. |
| `SESSION-LEDGER.md` | refreshed | Status, open gap, and next route needed local-skill wording. |

## Applied Changes

- Active route now uses local `SKILL.md` contracts directly: Invoke for plan semantics, Task Session for bounded execution, and Refine for validation review.
- Generated resume commands, `.codex/commands`, and `tools/arcanum` are explicitly non-authoritative for this Craft workflow.
- Historical command-surface artifacts from completed earlier runtime work remain in place as evidence, not as current instructions.
- Current state now records that the `Invoke Define` owner-stage receipt exists and the next step is local Refine skill review/package sync.

## Validation

Positive local-skill anchors:

```text
rg -n "local Refine skill|local skill surface|arcana/refine/SKILL.md" \
  development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-*.md \
  development/craft/work-packs/invoke-define-stage-receipt
```

Receipt existence:

```text
jq empty development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
test -e development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/invoke-define/RESULT.md
```

Current next route:

```text
rg -n "local task-session skill surface|CRAFT-INVOKE-RECEIPT-003|local Refine skill" \
  development/craft/README.md \
  development/craft/SESSION-LEDGER.md \
  development/craft/CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md
```

## Result

Refresh status: `pass`

The active Craft Invoke Define receipt workflow no longer depends on the old command surface. The next executable step remains `CRAFT-INVOKE-RECEIPT-003`, but it should be executed through local skill instructions and local artifact review.
