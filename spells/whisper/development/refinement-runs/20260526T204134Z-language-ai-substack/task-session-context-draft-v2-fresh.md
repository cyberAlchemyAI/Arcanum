# Task Session Context: SWU-WHISPER-DRAFT-V2-001

## Scope

- Task: `TASK-WHISPER-DRAFT-V2-FRESH`
- SWU: `SWU-WHISPER-DRAFT-V2-001`
- Runtime: local
- Strict coverage: pass
- User instruction: create a new draft version from zero, do not use the previous draft as source material, and use the Pareto schema.

## Controlling Sources

| Source | Obligation |
| --- | --- |
| `text-intent-substrate.yaml` | Use the enforced `pareto_tournament`, selected candidate, composition plan, opening contract, citation policy, and length limits. |
| `TASK-SESSION-PARETO-REPORT.md` | Treat the two-tier Pareto schema as completed and enforced; do not reopen the schema refresh. |
| `WORK-PACK.md` | Keep this as a bounded local drafting SWU and synchronize evidence after validation. |
| `spells/whisper/tools/validate-whisper-draft.py` | Validate Pareto completeness, opening contract, external reference placement, required terms, word count, and character count. |

## Explicit Exclusions

- `DRAFT-SUBSTACK-001.md` is not a writing source.
- The old draft may be used only after the new draft exists as a negative comparison for accidental text reuse.
- No publication, fundraising copy, direct Harari quotation, or page citation is in scope.

## Pareto Binding

- Tiering: `two_tier`
- Selected candidate: `executable_language_research_note`
- Selected technique stack:
  - `language_as_executable_medium`
  - `arcanum_as_live_case`
  - `invitation_to_name_a_workflow`
- Hard gates:
  - opening contract compliance
  - citation integrity
  - audience legibility

## Execution Path

1. Draft a new `DRAFT-SUBSTACK-002.md` from the schema and selected Pareto candidate only.
2. Preserve the required composition movement: reader-grounded hook, Harari bridge, research context, core insight, Arcanum example, implications, invitation.
3. Validate with the existing Whisper validator.
4. Run a post-draft freshness check against `DRAFT-SUBSTACK-001.md`.
5. Synchronize `WORK-PACK.md` and write a task-session report.

## Validation Surface

- `python3 -m py_compile spells/whisper/tools/validate-whisper-draft.py`
- YAML parse for `text-intent-substrate.yaml`
- `python3 spells/whisper/tools/validate-whisper-draft.py --schema spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml --draft spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md`
- Freshness comparison: compare normalized 8-word shingles against `DRAFT-SUBSTACK-001.md` and flag if the new draft shares more than a small incidental overlap.

## Gate Verdict

Pass. The schema is already Pareto-enforced, the selected candidate is clear, validation exists, and the previous draft can be excluded from writing inputs.
