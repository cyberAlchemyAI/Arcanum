# Work-Pack: Craft Row Update Planner

## Purpose

Add a deterministic dry-run row update planner for Craft so CSV import writeback
can reuse a tested reconciliation primitive.

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass |
| activeLayerWindow | L0 |
| currentExecutionTarget | `SWU-CRU-001` |
| blockedMutationScope | direct-yaml-apply, arbitrary-nested-update, generated-runtime-refresh |
| blockedPublicationScope | commit, push, parent-gitlink |

## SWU Manifest

| SWU | Goal | Write Scope | Verification |
| --- | --- | --- | --- |
| `SWU-CRU-001` | Add row update planner contract and toy fixture expectations. | `arcana/craft/templates/ledger.schema.yml`, `arcana/craft/README.md`, `arcana/craft/SKILL.md`, `arcana/craft/fixtures/craft-row-update-planner/` | YAML parse, fixture parse, targeted grep. |
| `SWU-CRU-002` | Implement internal deterministic planner and patch-plan report. | `arcana/craft/scripts/` | fixture pass/block/no-op cases, stable JSON output. |
| `SWU-CRU-003` | Integrate CSV import dry-run as planner caller. | `arcana/craft/scripts/` | edited CSV fixture emits row-level patch plans. |
| `SWU-CRU-004` | Refresh mirrors and publication-prep checks. | generated runtime mirrors only after canonical checks | diff check and generation evidence. |

## Task Detail: SWU-CRU-001

Goal: make the row update planner contract explicit before any implementation.

Inputs:

- `REFINE-SEED-PROPOSAL.md`
- `stages/S06-INVOKE-DESIGN.md`
- `stages/S08-DISTILL-REPAIR.md`
- `arcana/craft/SKILL.md`
- `arcana/craft/templates/ledger.schema.yml`

Outputs:

- docs/schema text defining row update planner;
- public-safe fixture directory with expected pass/block/no-op cases.

Algorithm details:

1. Add schema/docs language defining row selector, proposed delta, patch plan,
   stale source, editable field allowlist, and read-only fields.
2. Add a toy ledger fixture with minimal contexts/artifacts/decisions/references.
3. Add expected patch-plan fixtures for pass, no-op, stale hash, ID churn,
   invalid enum, missing reference, and read-only nested edit.
4. Verify all fixture files parse.
5. Do not add direct mutation or runtime mirror refresh.

Acceptance evidence:

- YAML parse for schema and toy ledger.
- JSON parse for expected reports if JSON expectations are added.
- `rg` confirms row update planner, dry-run, patch plan, stale source, and
  read-only language.

Expected result shape:

```yaml
swu_id: SWU-CRU-001
result: pass | flag | block
files_touched:
  - arcana/craft/templates/ledger.schema.yml
  - arcana/craft/README.md
  - arcana/craft/SKILL.md
  - arcana/craft/fixtures/craft-row-update-planner/
validation:
  - YAML parse
  - JSON parse if applicable
  - targeted rg checks
blockers:
  - none or exact blocker
residue:
  - deferred implementation details
```

## Next Route

`task-session` for `SWU-CRU-001`.
