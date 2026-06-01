# Passing Example: Evidence-Backed Proposal

## Input

- Source evidence: `sessions/demo/result.md` says a materialization setup proof completed.
- Target artifact inventory: `WORK-PACK.md`, `work-pack/tasks/TASK-001.md`.
- Refresh scope: update blocker/status notes for setup proof only.
- Mutation mode: `proposal-only`.

## Expected Output

- Phase status: `pass`
- Source signals: `evidence_added`, `blocker_opened`, `route_changed`
- Proposed changes: mark setup proof represented, keep score smoke blocked, add blocker for real candidate.
- Applied changes: n/a
- Next route: `task-session`
