# Correction - Native Skill Surface Supersedes Legacy Command Blocks

## What Changed

The initial run interpreted missing `tools/arcanum --resolve invoke` and
`tools/arcanum --resolve interrogation` routes as hard blockers.

That was stale for the current Arcanum skill surface.

The newer canonical Refine contract in `arcanum/arcana/refine/SKILL.md` and the
generated native package in `arcanum/.claude/skills/refine/SKILL.md` say:

- Refine must emit and validate `REFINE-DISPATCH.json`.
- Dispatch Spec owns route-shape validation.
- Stage completion is based on native capability handles and receipts.
- Deprecated command files, slash commands, and command-resolution checks are not
  active Refine success gates.
- `tools/arcanum` may remain as legacy compatibility or deterministic handoff,
  but a missing command interface must not block a stage when the native
  capability is available through the current host runtime.

## Corrected Interpretation

This run remains `flag`, but for a different reason:

- not because `invoke` and `interrogation` command routes are absent;
- but because the run did not collect full native stage receipts for every stage.

The TDD synthesis remains useful. The evidence model is corrected by adding
`REFINE-DISPATCH.json` and updating the manifest/index/result language.
