# Goal Handoff: Native Refine Orchestration

## Objective

Run the canonical Refine loop for `arcana/inventory` without recursive Codex execution.

## Runtime Mode

- Preset: `standard`
- Research: `no-research`
- Stage dispatch owner: root `tools/arcanum` process

## Stage Dispatch Contract

The root process dispatches stage commands through:

```bash
tools/arcanum --exec --adapter <stage-adapter> --timeout <seconds> --output <stage-output> <command> <stage-request>
```

The Refine model is not asked to spawn child `codex-exec` processes from inside a Codex sandbox.

## Source Request

target=arcana/inventory; preset=standard; research=no; refine the completed evidence-card work-pack so future task-session runs can execute multiple disjoint tasks without foreseeable blockers; include validator agent/runtime surface shell+jq, deferred human UI surface, batch execution rules, blocker pre-resolution, and next non-executed work-pack updates
