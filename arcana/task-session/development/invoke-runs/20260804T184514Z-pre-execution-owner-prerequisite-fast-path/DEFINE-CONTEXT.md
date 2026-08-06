# Define Context

## User intent

Fix the workflow behavior that spent minutes rebuilding Task Session evidence even though the work pack already declared Invoke Refresh as a prerequisite. The desired experience is to run the needed route directly when authorized, or identify it immediately when authorization or material is missing.

## Bounded source signals

- Task Session currently builds normal execution context before terminal continuation routing.
- Optional continuation dispatch currently requires `--follow-next-route` and an exact route authorization.
- Continuation-triggered Invoke Refresh defaults to `proposal-only`; direct-user Refresh defaults to `apply-approved` only for an exact declared scope and valid material package.
- Work Pack Readiness Audit and Task Session already implement an opt-in `selected-unit-at-task-session` profile that proves one semantic plan epoch and avoids an expected pre-execution Refresh.
- The failure was orchestration order and adoption, not checksum cost.

## Scope decision

Author a Task Session-owned, cross-capability development package. Do not modify canonical sources in this Invoke run. Preserve Invoke, Continuation Router, Work Pack Readiness Audit, and Task Session authority boundaries.

## Discovery waiver

`discovery_waiver_reason`: the target is an existing, source-evidenced workflow defect with a bounded owner surface; repository-wide discovery would add no material scope information.
