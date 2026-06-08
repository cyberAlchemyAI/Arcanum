# Example: Runtime Handoff Blocked

## Refine Seed Proposal

- Target: `arcana/refine`
- Seed needed: no
- Source context: `arcana/refine/SKILL.md`, `arcana/refine/REFINEMENT-LOOP.md`
- Write scope: no implementation mutation during refine
- Done criteria: blocked report names exact unavailable command, handoff, or runtime field
- Validation surface: markdown review and `run-validation-fixtures.sh`
- Preset: standard
- Loop count: canonical default loop, standard budget
- Research: no-research
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: block
- Planned execution stages: canonical ten-stage Refine loop
- Runtime default: arcanum-runtime
- Runtime eligibility: block
- Blocked route/runtime fields: missing strict Context Builder handoff pack, missing handoff JSON/index, unavailable runtime adapter, or invalid dispatch route
- Runtime handoff: `RUNTIME-HANDOFF.md`

## Blocked Behavior

Refine does not silently route to another executor. It records `Status: block`, writes or references the manifest/index when possible, and leaves Task Session or Sigil Development as recommended next routes only after a final synthesis exists.
