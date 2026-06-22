# Task Session Context Pack

## Task

- Work pack: `WP-IDD-20260619`
- Task: `TASK-IDD-001`
- SWU: `SWU-IDD-001`
- Objective: harden `invoke define` and `invoke design` with early-mode Dispatch/Distill contract fields and validation evidence.

## Selected Context

| Path | Reason |
| --- | --- |
| `arcanum/spells/invoke/README.md` | Root discipline says every invoke mode records Dispatch trace and plan/full/validate run automatic Distill validation. |
| `arcanum/spells/invoke/define.md` | Canonical define mode contract. |
| `arcanum/spells/invoke/design.md` | Canonical design mode contract. |
| `arcanum/spells/invoke/plan.md` | Reference for stronger mutation-handoff Distill language. |
| `arcanum/formulae/dispatch-spec/TECHNIQUE-CATALOG.md` | Dispatch technique ids and validation expectations. |
| `arcanum/spells/invoke/development/run-validation-fixtures.sh` | Fixture validation harness. |
| `arcanum/spells/invoke/development/fixtures/*DEFINE*.expected.md` | Define expected output evidence. |
| `arcanum/spells/invoke/development/fixtures/*DESIGN*.expected.md` | Design expected output evidence. |
| `.agents/skills/invoke/define.md` | Generated Codex skill mirror. |
| `.agents/skills/invoke/design.md` | Generated Codex skill mirror. |

## Obligations

- Add Dispatch technique trace obligations to `define` and `design`.
- Add Distill validation status obligations at the right lifecycle depth:
  - `define`: conditional sanity check when scope is broad, ambiguous, or split-prone.
  - `design`: design-unit check unless the mode blocks before design material exists.
- Add `Dispatch techniques:` and `Distill validation:` fields to mode output contracts.
- Update validation harness to require canonical phrases and expected output fields.
- Update standalone and integration define/design expected outputs.
- Sync generated `.agents` mirror files.

## Boundaries

- Do not add work-pack or execution authority to `define` or `design`.
- Do not weaken `plan`, `full`, or `validate` automatic Distill validation.
- Do not touch unrelated dirty files.
- Do not introduce private content into public `arcanum` sources.

## Validation Plan

```bash
bash -n arcanum/spells/invoke/development/run-validation-fixtures.sh
arcanum/spells/invoke/development/run-validation-fixtures.sh
git diff --check -- arcanum/spells/invoke .agents/skills/invoke
```

## Dispatch Technique Trace

- `frame_handoff`: Invoke package handed this bounded context to Task Session.
- `artifact_contract_bridge`: obligations map to concrete contract and fixture fields.
- `validation_loop`: implementation is complete only after fixture validation.

## Distill Validation

- Status: pass
- Unit: one SWU with coherent contract, mirror, and fixture changes.
- Gaps: none blocking.
