# Work Pack

## Work Pack ID

WP-IDD-20260619

## Objective

Implement early-mode Dispatch/Distill hardening for `invoke define` and `invoke design`, then validate the updated contracts through Invoke fixtures.

## Source Artifacts

- `INVOKE-DEFINE.md`
- `INVOKE-DESIGN.md`
- `IMPLEMENTATION-LAYERING.md`

## Tasks

### TASK-IDD-001: Harden define/design Dispatch and Distill contracts

Status: ready-for-task-session

#### SWU

SWU-IDD-001

#### Scope

- Patch `arcanum/spells/invoke/define.md`.
- Patch `arcanum/spells/invoke/design.md`.
- Patch `.agents/skills/invoke/define.md`.
- Patch `.agents/skills/invoke/design.md`.
- Patch `arcanum/spells/invoke/development/run-validation-fixtures.sh`.
- Patch define/design expected fixture outputs.
- Record Task Session context and result under this package.

#### Acceptance Criteria

- `define` contract records required Dispatch techniques and conditional Distill status.
- `design` contract records required Dispatch techniques and design-unit Distill status.
- Mode output contracts include `Dispatch techniques:` and `Distill validation:`.
- Validation harness checks the new canonical phrases and expected output fields.
- Standalone and integration define/design expected outputs include those fields.
- Full Invoke fixture validation passes.

#### Constraints

- Do not add execution or mutation authority to `define` or `design`.
- Do not weaken existing `plan`, `full`, or `validate` automatic Distill validation.
- Keep edits scoped to Invoke contracts, generated Invoke mirror files, fixtures, and this development package.
- Preserve public `arcanum` boundary; do not introduce private project content.

#### Validation Commands

```bash
bash -n arcanum/spells/invoke/development/run-validation-fixtures.sh
arcanum/spells/invoke/development/run-validation-fixtures.sh
git diff --check -- arcanum/spells/invoke .agents/skills/invoke
```

## Dispatch Technique Trace

| Technique | Use |
| --- | --- |
| `scu_swu_reduction` | One SWU carries the implementation. |
| `artifact_contract_bridge` | Acceptance criteria map to concrete files and validation checks. |
| `owner_boundary_check` | Early modes stay non-executing. |
| `execution_receipt_handoff` | Task Session must return changed files, validation results, and residual risks. |

## Distill Validation

- Status: pass
- Selected SWU: `SWU-IDD-001`
- Gap check: no separate task needed for `.claude/skills/invoke` because this generated mirror currently has no `define.md` or `design.md` files.
- Next route: task-session
