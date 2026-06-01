# Stage 1: Context Builder Evidence Baseline

## Verdict

`BLOCK`

## Command

```bash
tools/arcanum --exec --output tools/development/refinement-runs/20260525T161443Z-durable-runtime-interface/stages/01-context-builder.md context-builder "<request>"
```

## Resolution Evidence

- `context-builder` resolved to `.codex/commands/context-builder.md`.
- The command dispatch reached Codex CLI execution.
- The command failed before producing the requested output artifact.
- Observer evidence was recorded for the failed command.

## Blocked Reason

The current `tools/arcanum --exec` implementation directly invokes Codex CLI through shared repo-local Codex state at `.arcanum/codex-home`. In this run, nested Codex execution could not connect to the backend from the command surface and exited failed. No `01-context-builder.md` output was created by the command itself.

This is material evidence for the runtime redesign: command-backed Arcanum stages need a durable executor that can record adapter failure, preserve run status, and avoid relying on implicit Codex Goal or shared Codex runtime state.

## Local Evidence Baseline

The local files inspected before this run establish the current coupling:

- `arcana/refine/SKILL.md` still defines the objective as running through Codex Goal and refers to `GOAL-HANDOFF.md`.
- `arcana/refine/REFINEMENT-LOOP.md` preserves the useful canonical ten-stage loop but still names Codex Goal handoff in stage configuration and blocked output language.
- `arcana/task-session/runtime-adapters/codex-goal.md` defines Task Session delegation around native `/goal`.
- `tools/arcanum` currently resolves command markdown and, for `--exec`, builds a prompt and runs `codex exec` directly.
- `tools/arcanum` prepares one repo-local Codex home by default, `.arcanum/codex-home`, instead of per-run isolated adapter state.

## Baseline Conclusion

The refine loop shape is still valuable. The runtime model beneath it is the weak part. Refine and task-session should stop targeting Codex Goal and instead target a generic durable runtime contract where Codex is only one adapter.
