# Goal Handoff: Native Refine Orchestration

## Objective

Run the canonical Refine loop for `benchmark` without recursive Codex execution.

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

target=benchmark; preset=standard; research=research-if-gap-appears; refine the idea of using refine/distill/invoke to validate our tool against the completed benchmark smoke tests; do not mutate benchmark source or recompute benchmark scores
