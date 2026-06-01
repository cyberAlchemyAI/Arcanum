# Runtime Handoff: Local Skill Refinement Pass

## Objective

Run the refine loop locally from this Codex session, using skill-role stage artifacts rather than `tools/arcanum --exec` command dispatch.

## Stage Execution Mode

`local-skill`

## Stage Output Directory

```text
tools/development/refinement-runs/20260525T164427Z-durable-runtime-interface-skill-local/stages/
```

## Inputs

- Prior runtime design result:
  `tools/development/refinement-runs/20260525T161443Z-durable-runtime-interface/RESULT.md`
- Current refine contract:
  `arcana/refine/SKILL.md`
- Current Arcanum command surface:
  `tools/arcanum`

## Runtime Boundary

The design must remove Codex Goal and native `/goal` from the core runtime model. Codex may remain as an adapter behind a generic runtime executor.
