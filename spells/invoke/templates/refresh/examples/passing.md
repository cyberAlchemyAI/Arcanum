# Passing Example: Evidence-Backed Proposal

## Input

- Source evidence: `sessions/demo/result.md` says a materialization setup proof completed.
- Target artifact inventory: `WORK-PACK.md`, `work-pack/tasks/TASK-001.md`.
- Refresh scope: update blocker/status notes for setup proof only.
- Mutation mode: `proposal-only`.
- Apply approval: not supplied; it is not required to complete a proposal-only artifact.

## Expected Output

- Phase status: `pass`
- Phase status basis: proposal complete; refresh-authoring blockers `0`
- Handoff readiness: `gated`
- Blockers by scope: refresh-authoring `0`; apply-authorization `1`; target-lifecycle `1`; audit `0`
- Source signals: `evidence_added`, `blocker_opened`, `route_changed`
- Proposed changes: mark setup proof represented, keep score smoke blocked, add blocker for real candidate.
- Applied changes: n/a
- Next route: `task-session`
