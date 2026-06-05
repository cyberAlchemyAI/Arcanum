# Shared Context: Craft Invoke Define Stage Receipt

## Current Run

`development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof`

## Current Blocker

`Invoke Define` is currently:

- `status=flag`
- `evidence_kind=handoff_prepared`
- `receipt_path=null`

Downstream stages are dependency-blocked because `Invoke Define` did not produce pass evidence.

## Expected Receipt

`development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json`

## Local Skill Resume Surface

Use the repository-local Refine skill contract at `arcana/refine/SKILL.md` to
re-evaluate the current run folder and synchronize receipt-backed evidence.

Do not route this step through `tools/arcanum --exec`, `.codex/commands`, or a
bare command-resolution surface. The stage handoff's older `resume_command`
field is historical runtime text and is not authority for this local-skill
execution path.

## Boundary

This work-pack does not promote Craft, mutate canonical runtime surfaces, reopen Context Builder receipt work, or solve downstream stages before `Invoke Define` has receipt-backed evidence.
