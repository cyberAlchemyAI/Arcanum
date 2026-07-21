# INV-REFRESH-BLOCK-001

## Scenario

Refresh cannot proceed because target artifact inventory is missing.

## User Request

Refresh the artifacts from this result.

## Inputs

- Mode: `refresh`
- Source evidence: present
- Target artifact inventory: missing
- Refresh scope: ambiguous
- Mutation mode: `proposal-only`

## Expected Result

- Phase status: `block`
- Phase status basis: mandatory target inventory and declared scope are missing
- Handoff readiness: `blocked`
- Blockers by scope: refresh-authoring 2; apply-authorization 0; target-lifecycle 0; audit 0
- Missing input: target artifact inventory
- Expected next route: deferred

## Expected Output

[INV-REFRESH-BLOCK-001.expected.md](INV-REFRESH-BLOCK-001.expected.md)
