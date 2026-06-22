# Experiment Prompt: issue-loop-low

Run `github-project-issue-loop` against a supplied project view in dry-run mode.

## Target Artifact

arcana/github-project-issue-loop

## Contract

arcana/github-project-issue-loop/SKILL.md

## User Request

Use the GitHub Project Issue Loop on `https://github.com/orgs/ExampleOrg/projects/2/views/1` for repository `ExampleOrg/example-app`, but do it as `--dry-run`. Choose the best open P1 or P2 issue, explain why, and return the full result body. Do not summarize that you saved a file.

## Required Capture

Save only the final artifact result body to `development/example-outputs/issue-loop-low.output.md`.
