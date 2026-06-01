# Command Adapter Plan

## Target

- Runtime: codex
- Command: {command}
- Path: .codex/commands/{command}.md

## Command Contract

- Resolve observer envelope task zero.
- Route request to the selected sigil or spell.
- Use the embedded canonical artifact snapshot.
- Execute or guide the selected process.
- Preserve primary result, validation, files changed, gaps, and next route.
- Apply Observed Invocation Loop closeout through native receipts, Codex hooks, deterministic wrappers, or explicit legacy adapters.
- Report selected route and validation.

<!-- arcanum:capability-id {capability-id} -->
<!-- arcanum:capability-kind {capability-kind} -->
<!-- arcanum:capability-tier {capability-tier} -->
<!-- arcanum:command {command} -->
<!-- arcanum:runtime {runtime} -->

Optional runtime-sensitive metadata:

```markdown
<!-- arcanum:runtime-goal-adapter {adapter-id} -->
```

Use this for commands such as `task-session`, where the installed runtime needs an explicit goal-like adapter, for example `codex-goal`.

## Notes

- Keep this command focused on one capability or on orchestration.
- Do not generate `.arcanum/runtimes/`.
- Keep canonical behavior in Arcanum source; generated commands are installed snapshots.
