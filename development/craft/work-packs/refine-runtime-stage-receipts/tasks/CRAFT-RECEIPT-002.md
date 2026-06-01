# Task CRAFT-RECEIPT-002: Materialize Refine Dispatch In Native Runs

## Objective

Ensure native Refine runs write and validate `REFINE-DISPATCH.json` before runtime-backed stages.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L1 |
| Slice | S-RECEIPT-002 |
| Wave | W1 |
| Complexity | medium |
| Status | completed |

## Source Contracts

- `tools/arcanum`
- `arcana/refine/templates/refine-dispatch.json`
- `formulae/dispatch-spec/scripts/validate-dispatch.py`
- `formulae/dispatch-spec/dispatch.schema.yml`

## Dependencies

- CRAFT-RECEIPT-001 must pass.

## Smallest Working Units

### SWU-CRAFT-RECEIPT-002

Goal: native Refine run folders include a validated `REFINE-DISPATCH.json`.

Write scope:

- `tools/arcanum`
- optional task-session evidence artifact

Implementation detail:

1. Add or adapt a native dispatch writer in `run_native_refine`.
2. Preserve the canonical ten-stage loop, selected preset, research mode, and no-subagent strategy unless explicitly changed later.
3. Run the dispatch validator before stage dispatch.
4. If validation fails, write the dispatch and stop with `block` before stage execution.
5. Include dispatch path and validation status in `RUNTIME-HANDOFF.md`, `RUN-MANIFEST.md`, and `evidence-index.json`.

Done criteria:

- `REFINE-DISPATCH.json` exists in the native run folder.
- Dispatch validation passes before stage execution.

Validation:

```text
python3 formulae/dispatch-spec/scripts/validate-dispatch.py <generated-run>/REFINE-DISPATCH.json
```

Execution owner: local-fallback.

## Completion Evidence

| Check | Result |
| --- | --- |
| Dependency `CRAFT-RECEIPT-001` | pass |
| `REFINE-DISPATCH.json` materialized | pass: generated in `development/craft/development/refinement-runs/20260601T012206Z-craft-validation-md/` |
| Dispatch validator | pass |
| Dispatch route in `RUNTIME-HANDOFF.md` | pass |
| Dispatch route and validation in `RUN-MANIFEST.md` | pass |
| Dispatch route and validation in `evidence-index.json` | pass |

## Validation Run

```text
ARCANUM_REFINE_STAGE_TIMEOUT_SECONDS=30 ARCANUM_REFINE_STAGE_OUTPUT_GRACE_SECONDS=1 tools/arcanum --exec --adapter local-skill --timeout 120 --output /tmp/craft-receipt-002b/RESULT.md refine 'development/craft/CRAFT-VALIDATION.md --preset standard --research no'
```

Generated run:

```text
development/craft/development/refinement-runs/20260601T012206Z-craft-validation-md
```

Dispatch validation:

```text
python3 formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/development/refinement-runs/20260601T012206Z-craft-validation-md/REFINE-DISPATCH.json
VALIDATION=pass
```
