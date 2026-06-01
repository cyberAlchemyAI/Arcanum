# Refine Seed Proposal: Durable Runtime Interface, Local Skill Pass

## Target

Refine the durable Arcanum runtime interface design using local skill execution from this Codex session instead of command-backed `tools/arcanum --exec` sub-agent dispatch.

## Reason For Second Pass

The previous run proved that the current command-backed path can fail at the nested Codex runtime layer before producing stage artifacts. This run preserves the canonical refine loop while executing the stages directly as local skill-mode artifacts.

## Primary Question

How should Arcanum implement a generic durable execution run model for refine and task-session, with Codex only as an adapter?

## Required Model

```text
orchestrator -> async task handoff -> runtime translator -> runtime executor
```

## Constraints

- Do not use native `/goal`.
- Do not design around Codex Goal state.
- Do not dispatch command-backed stages with `tools/arcanum --exec`.
- Treat each stage as a local skill/sub-agent role with its own artifact.
- Keep all outputs under this run folder.
- Preserve the canonical ten-stage refine loop.

## Expected Result

A decision-complete implementation handoff that improves the previous result by making the execution model more generic, more precise about adapter boundaries, and clearer about how multiple refinement loops compose.
