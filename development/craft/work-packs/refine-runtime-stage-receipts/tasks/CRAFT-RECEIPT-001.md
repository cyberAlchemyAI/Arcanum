# Task CRAFT-RECEIPT-001: Separate Handoff Stubs From Stage Pass Evidence

## Objective

Change native Refine stage classification so a `local-skill` runtime-native handoff stub is not recorded as a completed owner-stage artifact.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L0 |
| Slice | S-RECEIPT-001 |
| Wave | W0 |
| Complexity | medium |
| Status | completed |

## Source Contracts

- `tools/arcanum`
- `arcana/refine/SKILL.md`
- `arcana/refine/REFINEMENT-LOOP.md`
- `development/craft/development/refinement-runs/20260601T002813Z-craft-validation-md/CONTRACT-AUDIT.md`

## Dependencies

None.

## Smallest Working Units

### SWU-CRAFT-RECEIPT-001

Goal: make native Refine classify handoff-only stage artifacts as `flag` or `block`, not `pass`.

Write scope:

- `tools/arcanum`
- optional focused test or task-session evidence artifact

Implementation detail:

1. Inspect `run_refine_command_stage` and `refine_artifact_is_usable`.
2. Add a classifier for runtime-native handoff stubs, for example content containing `# Arcanum Runtime-Native Handoff` with `STATUS: flag`.
3. Ensure that handoff-only outputs are recorded with an evidence kind such as `handoff_prepared` and status `flag` or `block`.
4. Preserve the existing no-recursive-Codex behavior.
5. Do not require fully executing native skill stages in this task.

Done criteria:

- A local-skill handoff stub cannot produce stage status `pass`.
- Existing block behavior for missing artifacts still works.

Validation:

```text
tools/arcanum --exec --adapter local-skill --timeout 120 --output <tmp>/RESULT.md refine 'development/craft/CRAFT-VALIDATION.md --preset standard --research no'
rg -n "handoff|flag|block|pass" <generated-run>/RUN-MANIFEST.md <generated-run>/evidence-index.json
```

Execution owner: local-fallback.

## Completion Evidence

| Check | Result |
| --- | --- |
| Runtime-native handoff stub classifier | pass: `tools/arcanum` now detects `# Arcanum Runtime-Native Handoff` plus `STATUS: flag` |
| Stage status for local-skill handoff stub | pass: `Context Builder evidence baseline` is `flag`, not `pass` |
| Downstream dependency behavior | pass: later command-backed stages are `block` because the first owner stage did not pass |
| Existing no-recursion behavior | preserved: local-skill still emits handoff/receipt prompt instead of spawning a nested model CLI |

## Validation Run

```text
ARCANUM_REFINE_STAGE_TIMEOUT_SECONDS=30 ARCANUM_REFINE_STAGE_OUTPUT_GRACE_SECONDS=1 tools/arcanum --exec --adapter local-skill --timeout 120 --output /tmp/craft-receipt-001/RESULT.md refine 'development/craft/CRAFT-VALIDATION.md --preset standard --research no'
```

Generated run:

```text
development/craft/development/refinement-runs/20260601T010740Z-craft-validation-md
```

Observed result:

```text
Context Builder evidence baseline | context-builder | flag | Stage produced a runtime-native handoff stub only; owner-stage execution receipt is still required.
Invoke Define | invoke | block | Dependency blocked. Context Builder evidence baseline did not produce pass evidence.
```
