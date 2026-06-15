# S01 Context Builder: Craft Row Update Evidence Baseline

## Context Pack Summary

- Task: decide whether Craft needs a deterministic row updater tool before CSV import writeback.
- Mode: compact.
- Handoff pack: runtime-local evidence.
- Strict coverage: pass.
- Blockers: 0.

## Obligations

| Obligation | Coverage | Evidence |
| --- | --- | --- |
| Preserve YAML authority. | covered | `arcana/craft/SKILL.md`, `arcana/craft/templates/ledger.schema.yml` |
| Decide between no new tool, narrow updater, or broad import. | covered | `REFINE-DISPATCH.json` route menu |
| Identify row-update safety gates. | covered | prior projection result, dispatch gates, schema validation rules |
| Keep public-boundary rules. | covered | dispatch boundary evidence and Craft source-authority rules |
| Produce non-executed plan only. | covered | seed write scope and Invoke plan contract |

## Included Context

| Source | Selector | Why Included |
| --- | --- | --- |
| `arcana/craft/SKILL.md` | storage contract and linking/indexing contract | Establishes `.craft/ledger.yml` authority and generated index non-authority. |
| `arcana/craft/templates/ledger.schema.yml` | source-of-truth policy, row families, validation rules | Establishes stable row IDs, references, required fields, and index rules. |
| `arcana/craft/development/refinement-runs/20260615T121512Z-craft-ledger-csv-json-indexes/RESULT.md` | import and editing rule, open residue, next route | Establishes broad projection plan and dry-run writeback gate. |
| `arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/work-pack/tasks/TASK-CII-ONEGO.md` | SWU-CII-005 | Shows the existing broad import-dry-run task and why a smaller primitive may be needed. |
| `development/craft/` | historical Craft evidence package | Used as history only; not runtime contract for `$craft`. |

## Evidence-Informed Inference

The row-update problem is smaller than CSV import and larger than CSV parsing.
The actual risky unit is:

```text
source ledger + row selector + proposed field delta -> deterministic patch plan
```

CSV import is one producer of proposed field deltas. A future CLI edit command,
human form, generated projection, or agent action could be another producer.
Putting all reconciliation logic inside `import-csv --dry-run` would make the
first safety proof too broad.

## Context Verdict

Pass. Local evidence is enough to continue without external research.
