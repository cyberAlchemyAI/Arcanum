# Experiment Prompt: issue-loop-medium

Run `github-project-issue-loop` for a normal single-ticket implementation flow.

## Target Artifact

arcana/github-project-issue-loop

## Contract

arcana/github-project-issue-loop/SKILL.md

## User Request

Use the GitHub Project Issue Loop for `ExampleOrg/example-app#42` from `https://github.com/orgs/ExampleOrg/projects/2/views/1`. Assign it to me, refine the issue context, invoke define/design/plan only as needed, execute one task session, validate with `npm test -- --run src/example.test.ts`, open a PR to `dev`, and return the full result body. Do not summarize that you saved a file.

## Required Capture

Save only the final artifact result body to `development/example-outputs/issue-loop-medium.output.md`.
