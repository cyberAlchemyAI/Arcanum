# Expected Output: sigil-observe-medium

## Sigil Development Result

- Mode: observe
- Sigil: handoff-notice
- Status: flag
- Profile ID: sigil-development
- Lifecycle owner: sigil-development
- Observed evidence: 5 meaningful executions; 3 exact round trips; 1 correct missing-boundary rejection; 1 historical accepted digest mismatch.
- Inference: the historical digest acceptance is a severe workflow gap even though the current runtime rejects drift.
- Applied edits: none.
- Quality Bar: partial pending provenance for the historical signal.
- Anti-Pattern hits: accepted digest drift.
- Reflection trigger: severe-gap.
- Recommendation: reflect now, verify the failing runtime/version, and preserve the current fail-closed check.
