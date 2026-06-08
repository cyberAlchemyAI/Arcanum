# Claude Code Instructions

Use the project Arcanum skill at `.claude/skills/orchestrate/SKILL.md` for Arcanum work.

Use `.claude/agents/arcanum-stage-worker.md` for bounded sidecar stages when subagent delegation is helpful.

Preserve Arcanum boundaries:

- `dispatch-spec` validates route shape.
- `invoke` authors define/design/plan/handoff/refresh artifacts.
- `task-session` executes one bounded task or SWU.
- `tools/arcanum` is a deterministic resolver, validator, handoff, and legacy adapter surface.
- Native skills and subagents are preferred over nested model-backed CLI execution.

