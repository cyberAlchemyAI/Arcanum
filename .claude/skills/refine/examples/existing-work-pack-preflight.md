# Example: Existing Work-Pack Target

## User Target

```text
refine to arcana/refine/development/WORK-PACK.md --swu SWU-REFINE-002
```

## Refine Seed Proposal

- Target: `arcana/refine/development/WORK-PACK.md`
- Seed needed: no
- Source context: `arcana/refine/development/WORK-PACK.md`, `arcana/refine/SKILL.md`, `arcana/refine/REFINEMENT-LOOP.md`
- Write scope: no implementation mutation during refine
- Done criteria: final refined synthesis names whether the selected SWU is coherent, overbroad, under-specified, or ready for a next route
- Validation surface: `arcana/refine/development/run-validation-fixtures.sh`
- Preset: compact
- Loop count: canonical default loop, compact budget
- Research: research-if-gap-appears
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: pass | block
- Planned execution stages: canonical ten-stage Refine loop
- Runtime default: arcanum-runtime
- Runtime eligibility: pass | block
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Confirmation required: yes for native runtime-backed stages and delegated subagents

## Expected Behavior

Refine does not execute the selected SWU. It uses the work-pack as source context, validates a dispatch-spec route for the discovery/design loop, writes manifest/index evidence, and returns a final synthesis with recommended next routes.
