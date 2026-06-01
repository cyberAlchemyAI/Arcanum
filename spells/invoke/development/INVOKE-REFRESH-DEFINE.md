# Invoke Define: Refresh Mode

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: `spells/invoke/development/INVOKE-REFRESH-DEFINE.md`
- Template or recipe selection: invoke mode definition artifact
- Decisions: define `refresh` as a governed artifact-state update mode, not execution
- Unresolved gaps: apply-approved behavior remains later-layer work
- Next route: design

## Objective

Create `invoke refresh`, a mode that inspects new session outputs and updates or proposes updates to existing invoke-authored workflow artifacts through evidence-backed deltas.

## Scope

In scope:

- normalize latest session outputs into typed refresh signals,
- compare signals against target workflow artifacts,
- classify deltas as evidence added, blocker opened/resolved, status changed, route changed, artifact drift, or no-op,
- emit a refresh report and optional patch proposal,
- apply changes only when mutation scope and approval are explicit,
- preserve target lifecycle ownership.

Out of scope:

- executing target tasks,
- inferring completion from weak evidence,
- benchmark scoring,
- whole-document rewrites when a small delta is enough,
- replacing task-session, workflow-reflect, spellcraft, or sigil-development.

## Core Terms

| Term | Definition |
| --- | --- |
| Refresh signal | A normalized claim from source session evidence about artifact state. |
| Delta class | The kind of change a refresh signal implies for target artifacts. |
| Target artifact inventory | The declared list of artifacts that refresh may inspect or propose changing. |
| Mutation mode | Whether refresh is proposal-only or apply-approved. |
| Refresh report | The durable result that records signals, deltas, proposed/applied/skipped changes, blockers, validation, and next route. |

## Acceptance Criteria

- Refresh blocks without source evidence or target artifact inventory.
- Every proposed or applied change maps to a refresh signal.
- No-op is a valid outcome when source evidence is already represented.
- Artifact drift is flagged when the safe correction is not obvious.
- Apply-approved mode requires explicit approval and declared scope.
- Refresh output keeps invoke gaps separate from target-artifact gaps.

## Source Evidence

- [INVOKE-REFRESH-CONTEXT-PACK.md](INVOKE-REFRESH-CONTEXT-PACK.md)
- [INVOKE-REFRESH-HANDOFF.md](INVOKE-REFRESH-HANDOFF.md)
- [INVOKE-REFRESH-DESIGN.md](INVOKE-REFRESH-DESIGN.md)
- [INVOKE-REFRESH-PLAN.md](INVOKE-REFRESH-PLAN.md)

## Gate Result

- Status: pass
- Reason: the mode has a bounded purpose, clear authority boundary, and existing design/plan evidence.
