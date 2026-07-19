# Task Session Lifecycle Receipt: SWU-DEE-013

## Identity

- Lifecycle owner: `task-session`
- Spell: `invoke`
- Canonical ID: `invoke`
- Source SWU: `SWU-DEE-013`
- Decision: **accept append-only replay status and Craft continuation route**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-013` appends one superseding status record after the DEE-012 replay. The record binds
the replay result and historical predecessor digest, states that history was not rewritten, and
derives the next continuation from the existing Craft ledger: Task Session on `SWU-WUI-001`.

The route record is not a code-mutation authorization. It exposes continuation eligibility only
when replay status is `pass`, the predecessor digest still matches, and Craft already names the
target as its next move.

## Binding

Execution owner: Task Session, one SWU only.

Exact implementation and evidence scope:

- `arcanum/spells/invoke/development/run-distill-workbench-route-fixture.sh`
- `projects/ide-extension/development/manual-session-bridge-plan/work-pack/evidence/SWU-DEE-013-SUPERSEDING-STATUS.json`
- `projects/ide-extension/development/manual-session-bridge-plan/work-pack/evidence/SWU-DEE-013-CRAFT-CONTINUATION.md`
- `.arcanum/observability/by-sigil/invoke.jsonl`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-013-RESULT.md`

Historical surfaces are read-only inputs:

- `projects/ide-extension/development/manual-session-bridge-plan/work-pack/evidence/SWU-MSB-011-assets/`
- `projects/ide-extension/development/manual-session-bridge-plan/work-pack/shared/traceability.md`
- `projects/ide-extension/.craft/ledger.yml`

## Acceptance Conditions

- the superseding record names DEE-012 as predecessor and preserves its historical digest;
- the status record says `history_mutation: none`;
- the replay pass and Craft `SWU-WUI-001` next move derive a ready continuation route;
- `mutation_handoff_allowed` remains false in the route record;
- one observability JSONL row is appended and parses;
- old Workbench evidence bytes remain unchanged;
- the focused route runner is deterministic and local.

## Next Route

The Distill execution-evidence backend closes after this unit. The derived continuation is
`task-session` on `projects/ide-extension/development/workbench-ui-v1/work-pack/tasks/TASK-WUI-001-SHELL.md`.
