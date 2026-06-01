# Runtime Handoff: Close Craft Gaps Refinement

## Status

`blocked`

## Objective

Prepare the canonical Refine loop for closing Craft package gaps before broader architecture planning.

## Dispatch Reference

[REFINE-DISPATCH.json](REFINE-DISPATCH.json)

## Adapter

No runtime adapter was selected for execution.

## Blocked Fields

| Field | Status | Evidence |
| --- | --- | --- |
| `dispatch-spec` command | blocked | `tools/arcanum --resolve dispatch-spec` returned unknown command. |
| `runtime-handoff` command | blocked | `tools/arcanum --resolve runtime-handoff` returned unknown command. |
| command-backed stage execution | blocked | Required dispatch/runtime handoff route is not fully registered in the command surface. |

## Available Local Evidence

- `formulae/dispatch-spec/dispatch.schema.json`
- `formulae/dispatch-spec/scripts/validate-dispatch.py`
- `arcana/task-session/runtime-adapters/runtime-handoff.md`

## Consequence

The dispatch shape can be locally validated with the dispatch-spec script, but the canonical command-backed refine loop must not be reported as executed.
