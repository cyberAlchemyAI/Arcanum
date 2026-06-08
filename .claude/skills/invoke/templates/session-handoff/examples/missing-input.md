# Missing Input Example: No Source Session Reference

## Input

- Source session reference: missing
- New session prompt: "Open a new thread for the research direction we just found."
- Handoff type: `research-direction`

## Expected Output

- Phase status: `block`
- Missing input: source session reference
- Context Builder coverage: `block`
- Next route: deferred until a session reference, transcript, run folder, or session evidence path is provided.
