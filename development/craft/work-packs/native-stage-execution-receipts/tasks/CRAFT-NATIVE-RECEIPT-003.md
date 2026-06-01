# Task CRAFT-NATIVE-RECEIPT-003: Add Parent-Native Stage Handoff And Resume Flow

## Objective

Make native Refine emit enough stage handoff context for a parent-native worker or Task Session to execute the owner stage and write the expected receipt.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L2 |
| Slice | S-NATIVE-RECEIPT-003 |
| Wave | W2 |
| Complexity | medium |
| Status | not-started |

## Source Contracts

- `tools/arcanum`
- `development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md`
- `arcana/task-session/SKILL.md`
- `.codex/commands/context-builder.md`

## Dependencies

- CRAFT-NATIVE-RECEIPT-002 must pass.

## Smallest Working Units

### SWU-CRAFT-NATIVE-RECEIPT-003

Goal: a prepared stage handoff names the exact receipt path and resume/rerun command needed by the parent-native surface.

Source anchors:

- `tools/arcanum` local-skill handoff output path
- latest Context Builder handoff artifact `development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md/stages/01-context-builder.md`

Related context:

- Parent-native execution may be manual, task-session-backed, or subagent-backed.
- This task should not implement generic cross-runtime dispatch.

Write scope:

- `tools/arcanum`
- optional receipt handoff notes under generated run folders

Implementation detail:

1. Extend runtime-native stage handoff output to include:
   - `run_id`
   - `stage`
   - `owner`
   - `stage_request`
   - `handoff_path`
   - `expected_receipt_path`
   - `resume_command`
2. Ensure the generated handoff tells the parent/native worker how to write the receipt.
3. Add or document a resume/rerun path that lets native Refine ingest the receipt without changing the source request.
4. Preserve no-recursion behavior; the handoff instructs the parent surface, not a nested CLI.

Done criteria:

- A handoff-only stage tells the parent worker where to write the receipt.
- The receipt path convention matches CRAFT-NATIVE-RECEIPT-002.
- Resume/rerun instructions are visible in generated stage artifacts.

Acceptance evidence:

- Generated Context Builder handoff contains `expected_receipt_path` and `resume_command`.

Validation:

```text
tools/arcanum --exec --adapter local-skill --timeout 120 --output <tmp>/RESULT.md refine 'development/craft/CRAFT-VALIDATION.md --preset standard --research no'
rg -n "expected_receipt_path|resume_command|stage_request|handoff_path" <generated-run>/stages/01-context-builder.md
```

Execution owner: local-fallback.

Expected result shape:

```yaml
swu_id: SWU-CRAFT-NATIVE-RECEIPT-003
result: pass | flag | block
files_touched:
  - tools/arcanum
validation:
  - generated handoff inspection
blockers:
  - none or resume command ambiguity
handoff_note: parent-native worker can now write the expected receipt
```
