# Refine Seed Proposal: Durable Runtime Interface, Skill-Contract Pass

## Target

Design a generic Arcanum durable runtime interface for refine/task-session execution while removing Codex Goal and native `/goal` from the core model.

## Execution Mode

`local-skill-contract`

This run is executed from the current Codex session using the installed Arcanum skill/command contracts as the output shape. It does not use `tools/arcanum --exec` for stage dispatch.

## Primary Question

Can Arcanum have a durable execution run model that executes refinement loops, multiple loops, and nested loops while keeping Codex as one adapter?

## Required Model

```text
orchestrator -> async task handoff -> runtime translator -> runtime executor -> adapter
```

## Stage Contract Requirement

Stage artifacts must preserve the actual skill output shapes:

- Context Builder: `## Context Pack Summary`
- Invoke: `## Invoke Result`
- Interrogation: `## Structured Interview Result`
- Distill: `## Distill Result`

## Expected Final Artifact

`RESULT.md` should be a decision-complete implementation handoff.
