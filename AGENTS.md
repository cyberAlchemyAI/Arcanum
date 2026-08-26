# Agent Instructions

This repository exposes Arcanum capabilities as repo-scoped Codex skills under `.agents/skills/`.

Core rules:

- Invoke skills explicitly with `$skill-name` when the request names a capability.
- Use `registry/SIGILS.md` and `registry/SPELLS.md` for capability lookup when available.
- Use `formulae/dispatch-spec/` for route-shape validation when installed.
- Use `spells/invoke/` for lifecycle authoring artifacts.
- Use `arcana/task-session/` for bounded execution.
- Keep `tools/arcanum` deterministic: resolve, validate, handoff, and legacy adapter compatibility.
- Prefer native Codex skill execution over nested model-backed CLI execution.

