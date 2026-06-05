# Goal Handoff: Native Refine Orchestration

## Objective

Run the canonical Refine loop for `development/craft/CRAFT-VALIDATION.md` without recursive Codex execution.

## Runtime Mode

- Preset: `standard`
- Research: `no-research`
- Stage dispatch owner: root `tools/arcanum` process
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: `pass`

## Stage Dispatch Contract

The root process dispatches stage commands through:

```bash
tools/arcanum --exec --adapter <stage-adapter> --timeout <seconds> --output <stage-output> <command> <stage-request>
```

The Refine model is not asked to spawn child model-backed CLI processes from inside an agent sandbox.

## Source Request

development/craft/CRAFT-VALIDATION.md --preset standard --research no use existing run folder development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof
