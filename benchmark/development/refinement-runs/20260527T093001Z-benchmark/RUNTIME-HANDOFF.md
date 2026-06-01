# Runtime Handoff

This run uses native Refine orchestration in `tools/arcanum`.

- target: `benchmark`
- root command: `tools/arcanum --exec refine ...`
- child stage adapter: `codex-bypass`
- child stage timeout: `600`

The purpose of this handoff is to prevent Codex-inside-Codex recursion.
