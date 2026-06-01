# Runtime Handoff: Durable Runtime Interface Refinement

## Objective

Run the Arcanum refinement loop as sub-agent stages to design a generic durable runtime interface for refine/task-session execution.

## Execution Rule

Use the repository-local Arcanum command surface for command-backed stages:

```bash
tools/arcanum --resolve <command>
tools/arcanum --exec --output <stage-output> <command> <stage-request>
```

If a stage cannot run, record `BLOCK` with the exact missing command, adapter, context, or safety field.

## Stage Outputs

Write sub-agent outputs to:

```text
tools/development/refinement-runs/20260525T161443Z-durable-runtime-interface/stages/
```

## Target

Design a generic Arcanum runtime system where refine and task-session no longer depend on Codex Goal or native `/goal`.

## Required Boundary

- Do not use native `/goal`.
- Do not design around Codex Goal state.
- Do not make Task Session or Sigil Development stages in the refine loop.
- Codex is one adapter behind a generic runtime executor.

## Final Synthesis

The final synthesis should be written to `RESULT.md` and should be implementation-handoff quality.
