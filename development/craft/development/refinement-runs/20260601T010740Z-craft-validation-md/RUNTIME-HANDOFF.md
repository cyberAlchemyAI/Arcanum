# Runtime Handoff

This run uses native Refine orchestration in `tools/arcanum`.

- target: `development/craft/CRAFT-VALIDATION.md`
- root command: `tools/arcanum --exec refine ...`
- child stage adapter: `local-skill`
- child stage timeout: `30`

The purpose of this handoff is to prevent Codex-inside-Codex recursion.
