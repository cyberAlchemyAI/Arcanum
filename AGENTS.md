# Agent Instructions

This repository exposes Arcanum capabilities as repo-scoped Codex skills under `.agents/skills/`.

Core rules:

- Invoke skills explicitly with `$skill-name` when the request names a capability.
- When creating or inserting any diagram, always use `$evidence-grounded-diagrams`.
- Use `registry/SIGILS.md` and `registry/SPELLS.md` for capability lookup when available.
- Use `formulae/dispatch-spec/` for route-shape validation when installed.
- Use `spells/invoke/` for lifecycle authoring artifacts.
- Use `arcana/task-session/` for bounded execution.
- Route every real multi-agent fan-out through `$subagent-strategy`; register the
  confirmed temporary JSON in the configured append-only YAML ledger before
  spawning and append the paired close row after all agents are closed.
- For native capability-bound execution, require Orchestrate registration proof
  before spawn and its paired close proof before reporting resolved closeout.
- Keep `tools/arcanum` deterministic: resolve, validate, handoff, and legacy adapter compatibility.
- Prefer native Codex skill execution over nested model-backed CLI execution.
