# INV-REFRESH-APPLY-PASS-001

## Scenario

An exact refresh is directly requested by the user, resolves its omitted
mutation mode to `apply-approved`, and passes its declared validation.

## User Request

Refresh the task status from its approved receipt and validate the changed
work-pack row.

## Inputs

- Mode: `refresh`
- Source evidence: approved task receipt
- Target artifact inventory: `WORK-PACK.md`, `work-pack/tasks/TASK-READY.md`
- Refresh scope: one task-status row and its evidence link
- Activation source: `direct-user`
- Mutation mode: omitted; resolves to `apply-approved`
- Mutation mode source: `default-direct-user`
- Apply approval: supplied by the direct request for this exact scope
- Validation commands: compare task status and receipt selector
- Evidence date: 2026-07-20

## Expected Result

- Phase status: `pass`
- Phase status basis: approved delta applied and validated
- Resolved mutation mode: `apply-approved`
- Mutation mode source: `default-direct-user`
- Handoff readiness: `ready`
- Blockers by scope: refresh-authoring 0; apply-authorization 0; target-lifecycle 0; audit 0
- Source signals: evidence_added, status_changed
- Applied changes: update one status row and evidence link
- Expected next route: `task-session`

## Expected Output

[INV-REFRESH-APPLY-PASS-001.expected.md](INV-REFRESH-APPLY-PASS-001.expected.md)
