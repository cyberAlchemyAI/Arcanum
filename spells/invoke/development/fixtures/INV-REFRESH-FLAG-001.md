# INV-REFRESH-FLAG-001

## Scenario

Artifact drift exists, but the safe correction needs review.

## User Request

Refresh the work-pack after the latest session. The task file says the route is blocked, but the work-pack board still says ready.

## Inputs

- Mode: `refresh`
- Source evidence: present
- Target artifact inventory: `WORK-PACK.md`, `work-pack/tasks/TASK-ROUTE.md`
- Refresh scope: route and task-board consistency
- Mutation mode: `proposal-only`
- Evidence date: 2026-05-25

## Expected Result

- Phase status: `flag`
- Source signals: artifact_drift
- Proposed changes: flag conflict and propose review
- Expected next route: deferred

## Expected Output

[INV-REFRESH-FLAG-001.expected.md](INV-REFRESH-FLAG-001.expected.md)
