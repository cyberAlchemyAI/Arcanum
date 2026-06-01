# Stage 09: Invoke Plan

Status: `pass`

## Non-Executed Plan

### SWU-WHISPER-READABILITY-001

Add `readability_dynamics` to the schema without changing draft content.

Files:

- `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml`
- `spells/whisper/tools/validate-whisper-draft.py`

Validation:

- YAML parses.
- Existing draft validator still passes for current checks.
- New readability validator flags known block-wall cases.

### SWU-WHISPER-READABILITY-002

Add renderer support for rhythm units.

Files:

- `spells/whisper/tools/build-whisper-review-html.py`
- `spells/whisper/templates/draft-review-base.html`
- `spells/whisper/review/README.md`

Validation:

- Existing paragraph-only drafts still render.
- Beat-level draft renders with stable `block_id`, `beat_id`, and `part_id`.
- `window.WhisperReview.getAgentPayload()` includes beat references where present.

### SWU-WHISPER-READABILITY-003

Regenerate and browser-check the current Substack review HTML.

Files:

- `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.review.html`
- task-session evidence report

Validation:

- Serve over localhost before Playwright checks.
- Desktop and mobile screenshots show no overlapping text or broken comments panel.
- Agent payload can identify the block or beat that received a comment.

### SWU-WHISPER-READABILITY-004

Use review comments to revise a specific part.

Input:

- Playwright-extracted review payload.

Output:

- Revision proposal with multiple change options per targeted beat or block.

Validation:

- Proposed changes preserve transport schema and opening contract.
- Part-level mini-tournament runs only for commented, revised, delegated, or validation-failed parts.

