# Runtime Handoff: Skill-Contract Refinement Pass

## Objective

Run the canonical refine loop locally using the real Arcanum skill output contracts, not command-backed `tools/arcanum --exec`.

## Inputs

- `arcana/refine/SKILL.md`
- `.codex/commands/context-builder.md`
- `.codex/commands/invoke.md`
- `.codex/commands/interrogation.md`
- `.codex/commands/distill.md`
- `arcana/distill/SKILL.md`
- prior run: `tools/development/refinement-runs/20260525T161443Z-durable-runtime-interface/`
- prior local run: `tools/development/refinement-runs/20260525T164427Z-durable-runtime-interface-skill-local/`

## Boundary

- Do not use native `/goal`.
- Do not depend on Codex Goal state.
- Do not execute implementation.
- Do not use `tools/arcanum --exec` for stage dispatch.
- Preserve stage artifacts as if each skill had been run from the current session.
