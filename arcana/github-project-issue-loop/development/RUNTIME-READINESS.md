# Runtime Readiness

## Status

Ready for repository-local Arcanum invocation.

## Expected Generated Runtime Package

- `.agents/skills/github-project-issue-loop/README.md`
- `.agents/skills/github-project-issue-loop/SKILL.md`
- `.agents/skills/github-project-issue-loop/templates/usage-telemetry.md`
- `.agents/skills/github-project-issue-loop/templates/reflection-report.md`
- `.agents/skills/github-project-issue-loop/templates/regression-boundary-map.md`

When installed into a consuming repository, the generated package declares `mutation_policy: regenerate-from-canonical-source` and points back to `arcana/github-project-issue-loop/SKILL.md`.

## Invocation Checks

- `tools/arcanum --list | rg '^github-project-issue-loop$|github-project-issue-loop'`: pass
- `tools/arcanum --resolve github-project-issue-loop`: pass, resolves `.agents/skills/github-project-issue-loop/SKILL.md`
- `tools/arcanum --print-prompt github-project-issue-loop --dry-run --repo ExampleOrg/example-app`: pass
- `tools/arcanum --exec --adapter dry-run --output .arcanum/observability/runs/github-project-issue-loop-readiness-dry-run.md github-project-issue-loop --dry-run --repo ExampleOrg/example-app`: pass
- `tools/arcanum --exec --adapter native-skill --output .arcanum/observability/runs/github-project-issue-loop-native-handoff.md github-project-issue-loop --dry-run --repo ExampleOrg/example-app`: flag as expected native handoff
- `tools/arcanum --exec --adapter codex-skill --output .arcanum/observability/runs/github-project-issue-loop-codex-skill-handoff.md github-project-issue-loop --dry-run --repo ExampleOrg/example-app`: flag as expected Codex skill handoff
- `arcana/github-project-issue-loop/development/run-validation-fixtures.sh`: pass with regression-boundary fixture expectations

## Runtime Receipts

- `.arcanum/observability/runs/github-project-issue-loop-readiness-dry-run.md`
- `.arcanum/observability/runs/github-project-issue-loop-native-handoff.md`
- `.arcanum/observability/runs/github-project-issue-loop-codex-skill-handoff.md`

## Live Run Evidence

- One source-specific issue-loop pass opened a linked PR, passed focused local validation, passed broader local validation, and reached settled CI.
- Source repository, issue, PR, and CI job identifiers are intentionally omitted from this public package.

## Remaining Lifecycle Work

Promotion readiness still needs a fuller low, medium, and complex real-output set. The sigil is ready to run the loop, but not yet promoted as fully proven across all example regimes.

The next live run must fill a dependency map, create/update/reuse focused regression tests before implementation, and report scope-containment evidence in the final output.
