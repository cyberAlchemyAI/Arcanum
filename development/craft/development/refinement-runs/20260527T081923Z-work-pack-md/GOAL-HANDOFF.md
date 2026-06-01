# Goal Handoff: Native Refine Orchestration

## Objective

Run the canonical Refine loop for `development/craft/WORK-PACK.md` without recursive Codex execution.

## Runtime Mode

- Preset: `standard`
- Research: `research-if-gap-appears`
- Stage dispatch owner: root `tools/arcanum` process

## Stage Dispatch Contract

The root process dispatches stage commands through:

```bash
tools/arcanum --exec --adapter <stage-adapter> --timeout <seconds> --output <stage-output> <command> <stage-request>
```

The Refine model is not asked to spawn child `codex-exec` processes from inside a Codex sandbox.

## Source Request

development/craft/WORK-PACK.md --task CRAFT-REFINE-001
