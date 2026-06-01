# Stage 1: Context Builder Evidence Baseline

## Verdict

`pass`

## Execution Mode

`local-skill`

## Evidence Sources

- `arcana/refine/SKILL.md`
- `tools/arcanum`
- `tools/development/refinement-runs/20260525T161443Z-durable-runtime-interface/RESULT.md`
- The prior attempted `tools/arcanum --exec ... context-builder` run, which failed before producing a stage artifact.

## Current State

Refine has a strong loop model but stale runtime vocabulary:

- it still says the loop runs through Codex Goal,
- it still requires `GOAL-HANDOFF.md`,
- it still names `codex-goal-profile`,
- it still configures Context Builder with `--handoff codex-goal`.

`tools/arcanum` has a useful resolver and prompt builder, but `--exec` directly launches Codex CLI. It prepares a single repo-local `CODEX_HOME` at `.arcanum/codex-home`, then runs `codex exec`. That makes the command surface both a resolver and an executor, which is too much responsibility for one script.

The prior refinement run demonstrated the failure mode: command dispatch reached Codex CLI, observer evidence was recorded, but the adapter failed before writing the requested stage output.

## Baseline Conclusion

The redesign should split command resolution, runtime handoff, adapter translation, and execution status into separate durable surfaces. Refine should index runtime child runs rather than assume Codex or any specific adapter owns the loop.
