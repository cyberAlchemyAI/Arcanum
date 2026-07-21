# INV-REFRESH-PASS-001

## Scenario

Latest session evidence should produce a reviewable refresh proposal.

## User Request

Refresh the current invoke-authored work-pack from this latest session result: materialization setup proof completed, but score smoke still needs a real candidate and worker profile.

## Inputs

- Mode: `refresh`
- Source evidence: present
- Target artifact inventory: `WORK-PACK.md`, `work-pack/tasks/TASK-SCORE.md`
- Refresh scope: status and blocker notes only
- Mutation mode: `proposal-only`
- Apply approval: not supplied; proposal authoring does not require it
- Evidence date: 2026-05-25

## Expected Result

- Phase status: `pass`
- Phase status basis: proposal complete; refresh-authoring blockers 0
- Handoff readiness: `gated`
- Blockers by scope: refresh-authoring 0; apply-authorization 1; target-lifecycle 1; audit 0
- Source signals: evidence_added, blocker_opened, route_changed
- Proposed changes: update setup proof status; keep score smoke blocked; add next route to candidate/profile prep
- Expected next route: `task-session`

## Expected Output

[INV-REFRESH-PASS-001.expected.md](INV-REFRESH-PASS-001.expected.md)
