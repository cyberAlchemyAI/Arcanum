# Experiment Prompt: strategy-close-complex

Use `subagent-strategy` to close the confirmed fixture graph described in
`development/fixtures/strategy-close-complex.md`. Preserve one explorer's
partial failure downstream, keep feedback non-blocking, use the parent as final
approver, and report exactly one dispatch event plus one close event.

Return the full `## Subagent Strategy Result`. Do not claim a clean success.
