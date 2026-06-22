# Fixture: issue-loop-low

## Request

Use `github-project-issue-loop` in dry-run mode on a GitHub Project view. List open issues, select the strongest candidate, and explain what would happen next without assigning, branching, committing, or opening a PR.

## Inputs

- Project: `https://github.com/orgs/ExampleOrg/projects/2/views/1`
- Repository filter: `ExampleOrg/example-app`
- Status filter: not Done
- Priority preference: P1 before P2
- Mutation policy: dry-run

## Required Behavior

- Do not mutate GitHub.
- Do not create a branch.
- Map the likely upstream/downstream dependency boundary even though no mutation occurs.
- Identify which focused test would be created, updated, or reused before an execution run.
- Return the output contract.
- Include selection reason and blocked mutation notes.
