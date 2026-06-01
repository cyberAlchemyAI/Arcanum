# Stage 03: Interrogation Refine Review

Status: `pass`

## Critique

The proposed layer is valid, but it must avoid three failure modes.

## Failure Mode 1: CSS Masquerading As Writing Governance

Better spacing, narrower lines, and darker visual treatment can help, but they do not decide whether the text moves from hook to bridge to example to implication. If this becomes only CSS, the next draft can still be a beautiful wall.

Required correction: make readability a schema and validation concern first, then let CSS express the schema.

## Failure Mode 2: Turning Every Paragraph Into A Tournament

Whisper already decided against always-on paragraph-level tournaments. A readability layer should use deterministic checks and targeted triggers before invoking candidate comparison.

Required correction: only run part-local or beat-local alternatives when a unit is delegated, revised, validation-failed, or explicitly commented by the operator.

## Failure Mode 3: Breaking Review Addressability

If a paragraph is split into visual beats, comments must still map back to source text and part ownership. Otherwise the agent cannot safely apply requested changes.

Required correction: introduce `beat_id` as a child of `block_id`, not a replacement for it.

## Verdict

Proceed with a `readability_dynamics` layer, but preserve this ordering:

1. Schema contract.
2. Validator checks.
3. Review renderer.
4. Browser validation.
5. Draft revision from extracted comments.

