# Experiment Prompt: sigil-reflect-complex

Run the target sigil through the sigil-development experiment profile.

## Target Artifact

arcana/refine

## Contract

arcana/refine/SKILL.md

## Lifecycle Owner

sigil-development

## User Request

Use Refine on `/home/vrondelli/projects/domainspec-core/arcanum/framework/observability/development`, the observability architecture, and the whole observability package.

The refinement should prepare a full architecture/design refinement loop, not execute the loop directly. It must keep Refine as the preflight controller and Task Session as the executor through Codex Goal. The planned loop should use the installed skills as execution-stage obligations: `context-builder`, `invoke`, `interrogation`, `distill`, and `sigil-development` when lifecycle work is needed.

Return a `Refine Seed Proposal` with bounded source context, write scope, done criteria, validation surface, selected preset, research decision, planned execution stages, blocked handoff fields if any, and proposed Task Session route.

Return the full user-facing result body. Do not summarize that you saved an output file.

## Required Capture

Save only the final artifact result body to `development/example-outputs/sigil-reflect-complex.output.md`.
