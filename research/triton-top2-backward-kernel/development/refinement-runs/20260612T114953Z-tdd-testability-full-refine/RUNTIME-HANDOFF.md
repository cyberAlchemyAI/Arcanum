# Runtime Handoff - TDD/Testability Full Refine

## Objective

Refine the testability and TDD strategy for the Triton top-2 backward kernel
research tower without implementing code.

## Adapter

- Preferred command surface: `arcanum/tools/arcanum` from the private parent.
- Required by skill text: `tools/arcanum` inside the `arcanum` submodule.
- Runtime mode used here: deterministic command resolution plus dry-run adapter
  for resolvable stages.

## Stage Dispatch Contract

The original handoff was written against the older command-dispatch model. The
correct current model is:

- Refine emits and validates `REFINE-DISPATCH.json`.
- Dispatch Spec validates route shape.
- Native skills or approved subagents produce stage receipts.
- `tools/arcanum` is legacy compatibility/deterministic handoff only, not an
  active success gate for native skill availability.

When a native capability is unavailable, the stage is recorded as `block`.
When a legacy command route is missing but the native capability exists, the
stage should be `not_run` or `flag` until a true native receipt is collected.

## Corrected Native Capability Status

Known after correction:

- `context-builder`: legacy dry-run receipt collected.
- `distill`: legacy dry-run receipts collected.
- `invoke`: native skill available in `~/.codex/skills/invoke/SKILL.md`; no
  native receipt collected in the original run.
- `interrogation`: native skill available in
  `~/.codex/skills/interrogation/SKILL.md`; no native receipt collected in the
  original run.
- `dispatch-spec`: corrected route validates.

## Blocked Fields

- Full native Define/Design/Plan receipts were not collected.
- Full native Interrogation review receipts were not collected.
- The old command-resolution blockers are preserved as historical stage files,
  but they are no longer the correct readiness diagnosis.

## Runtime Status

`flag`: the run produced a useful Refine-owned synthesis and a validated
dispatch route, but should be rerun through the current native skill receipt
model before being treated as a clean full Refine execution.
