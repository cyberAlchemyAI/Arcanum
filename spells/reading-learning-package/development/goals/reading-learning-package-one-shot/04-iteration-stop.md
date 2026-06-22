# Iteration And Stop Policy

## Iteration Policy

1. Read this goal folder first.
2. Read the handoff pack and work-pack artifacts.
3. Execute the SWUs in order.
4. After each SWU, run the smallest relevant validation and record pass/flag/block evidence.
5. Do not move to reusable readiness until the fixture suite exists.
6. Finish with final validation and a concise implementation report.

## Fallback Exploration

Fallback exploration is limited to named gaps from the Refine result:

- G-RLP-001: candidate contract not installed,
- G-RLP-003: preset fixtures absent,
- G-RLP-004: transcript fixture absent,
- G-RLP-005: PDF renderer behavior unresolved,
- G-RLP-006: custom preset persistence undecided,
- G-RLP-007: runtime behavior only shape-validated.

Allowed default for G-RLP-006: use output-root local preset state until repeated use justifies a stronger persistence route.

## Stop With BLOCK If

Stop and report `BLOCK` if:

- any step requires writes outside `arcanum/spells/reading-learning-package/`,
- source authority or Whisper composition authority cannot be preserved,
- fixtures require private content or local absolute paths,
- PDF validation cannot distinguish renderer absence from spell failure,
- a blocker-level decision cannot be safely defaulted,
- external research or subagents would be required without explicit approval,
- validation fails for a reason outside the goal write scope.
