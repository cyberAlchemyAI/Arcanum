# Experiment Prompt: issue-loop-complex

Run `github-project-issue-loop` for a complex P1 project issue with possible subagent review and CI still in progress.

## Target Artifact

arcana/github-project-issue-loop

## Contract

arcana/github-project-issue-loop/SKILL.md

## User Request

Use the GitHub Project Issue Loop on `https://github.com/orgs/ExampleOrg/projects/2/views/1`. Pick the highest-priority unassigned P1 issue for `ExampleOrg/example-app`, assign it to me, use refine and invoke according to risk, preserve any required subagent confirmation gate, execute one task session, open the PR, and report CI exactly even if one check is still running. Return the full result body. Do not summarize that you saved a file.

## Required Capture

Save only the final artifact result body to `development/example-outputs/issue-loop-complex.output.md`.
