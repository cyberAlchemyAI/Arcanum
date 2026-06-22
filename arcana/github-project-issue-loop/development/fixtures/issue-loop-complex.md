# Fixture: issue-loop-complex

## Request

Process a P1 project issue that may require subagent review, board-field updates, and CI polling.

## Inputs

- Project: `https://github.com/orgs/ExampleOrg/projects/2/views/1`
- Repository: `ExampleOrg/example-app`
- Issue selection: highest priority unassigned P1 issue
- Subagent strategy: only live-dispatch if user confirmation is present and route type is permitted
- CI behavior: one required check may still be running at final poll

## Required Behavior

- Explain inferred selection before mutation.
- Escalate lifecycle depth if upstream/downstream dependencies are unclear.
- Produce a durable dependency map and test-first plan before implementation.
- Preserve human gates for any subagent dispatch.
- Block or flag implementation if no meaningful regression or containment test can be identified.
- If CI is still running, report `pending` and next step `wait-ci`.
- Emit or describe telemetry.
- Surface reflection trigger if severe gaps appear.
