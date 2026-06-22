# Fixture: issue-loop-medium

## Request

Claim one ready issue from a project view, refine context, choose the minimum useful invoke depth, execute through Task Session, validate, open a linked PR, and update status.

## Inputs

- Project: `https://github.com/orgs/ExampleOrg/projects/2/views/1`
- Repository: `ExampleOrg/example-app`
- Issue: `#42`
- Base branch: `dev`
- Expected validation: `npm test -- --run src/example.test.ts`
- Mutation policy: execution-authorized

## Required Behavior

- Assign the issue before implementation.
- Create a branch or worktree.
- Map upstream dependencies and downstream dependents before implementation.
- Create, update, or explicitly reuse focused regression tests before the fix.
- Use refine and at least one invoke artifact if the issue has ambiguity.
- Execute one task session.
- Validate focused regression behavior and at least one scope-containment check before broader validation.
- Open a PR with `Closes #42`.
- Return validation and telemetry status.
