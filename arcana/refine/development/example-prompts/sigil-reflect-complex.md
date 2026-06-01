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

The refinement should validate `REFINE-DISPATCH.json` through dispatch-spec, then run the canonical discovery/design refinement loop through deterministic `tools/arcanum` stage dispatch. The planned loop should use the installed stage commands: `context-builder`, `invoke`, `interrogation`, and `distill`.

Return a `Refine Result` with bounded source context, write scope, done criteria, validation surface, selected preset, research decision, planned execution stages, dispatch route validation, runtime handoff status, command dispatch evidence or blocked fields, and final synthesis.

Return the full user-facing result body. Do not summarize that you saved an output file.

## Required Capture

Save only the final artifact result body to `development/example-outputs/sigil-reflect-complex.output.md`.
