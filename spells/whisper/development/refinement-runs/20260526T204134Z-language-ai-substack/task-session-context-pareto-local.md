# Task Session Context: SWU-WHISPER-PARETO-001

## Scope

- Task: `TASK-WHISPER-SCHEMA-REFRESH`
- SWU: `SWU-WHISPER-PARETO-001`
- Runtime: local
- Strict coverage: pass

## Controlling Sources

| Source | Obligation |
| --- | --- |
| `WORK-PACK.md` | Execute exactly `SWU-WHISPER-PARETO-001`; keep writes scoped to schema, validator, and task-session evidence. |
| `REFRESH-REPORT.md` | `two_tier` Pareto decision is approved; schema and validator gaps are ready. |
| `REFRESH-PATCH-PROPOSAL.md` | Use global tournament plus part-level mini-tournament only for delegated, revised, or failing parts. |
| `text-intent-substrate.yaml` | Preserve existing SRU cores, opening contract, SCU candidate set, composition plan, and draft constraints. |
| `spells/whisper/tools/validate-whisper-draft.py` | Extend existing validator without regressing opening, reference placement, term, word, or character checks. |
| `DRAFT-SUBSTACK-001.md` | Existing draft content should remain stable unless validation requires a direct fix. |

## Hard Constraints

- Do not rewrite the draft as part of this SWU unless schema validation directly fails because of the new contract.
- Do not run part-level tournaments for every paragraph.
- Preserve rejected Pareto alternatives as reusable alternatives, not failures.
- Keep exact Harari quotation/page verification out of this SWU.

## Validation Surface

- `jq empty refresh-report.json`
- Python YAML parse for `text-intent-substrate.yaml`
- `python3 -m py_compile spells/whisper/tools/validate-whisper-draft.py`
- `python3 spells/whisper/tools/validate-whisper-draft.py --schema spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml --draft spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-001.md`
- Negative validation probe against a temporary incomplete Pareto schema.

## Gate Verdict

Pass. The decision blocker was resolved by `/invoke lets go with two tier`, and the work-pack now contains a ready SWU.
