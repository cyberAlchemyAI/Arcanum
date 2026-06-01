# Runtime Handoff

This run uses native Refine orchestration in `tools/arcanum`.

- target: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/REFINE-SEED-PROPOSAL.md`
- root command: `tools/arcanum --exec refine ...`
- child stage adapter: `codex-exec`
- child stage timeout: `900`

The purpose of this handoff is to prevent Codex-inside-Codex recursion.
