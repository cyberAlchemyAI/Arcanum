---
name: MOGT Move To Arcanum Context
description: Bounded context pack for moving the MOGT publication research project into the Arcanum research surface.
created: 2026-06-07
---

# MOGT Move To Arcanum Context

## Task

Move the MOGT agentic conversation research project into the Arcanum repository research surface so the publication strategy and dispatch DAG live beside Arcanum research towers.

## Source

- Previous source folder: `/home/vrondelli/projects/domainspec-core/research/projects/mogt-agentic-conversation`
- Target folder: `research/mogt-agentic-conversation/`

## Controlling Context

- `research/autobayes/` is the local precedent for Arcanum research towers.
- `research/README.md` is the index for Arcanum proof runs, design investigations, framework experiments, and research towers.
- `research/mogt-agentic-conversation/development/mogt-publication-research.dispatch.json` must remain Dispatch Spec valid after relocation.

## Constraints

- Keep the move scoped to MOGT research artifacts.
- Do not mutate Whisper, Dispatch Spec, Experiment Harness, Refine, or Invoke canonical contracts as part of the move.
- Preserve the publication DAG and strategy artifacts.
- Update moved path references from `research/projects/mogt-agentic-conversation` to `research/mogt-agentic-conversation`.
- Validate the moved dispatch route.

## Done Criteria

- MOGT project exists under `research/mogt-agentic-conversation/`.
- Old sibling project folder no longer exists.
- No stale live references to `research/projects/mogt-agentic-conversation` remain in the moved project, except this task-session evidence describing the old source path.
- Dispatch validation passes from the new Arcanum path.
- `research/README.md` indexes the MOGT research tower.
