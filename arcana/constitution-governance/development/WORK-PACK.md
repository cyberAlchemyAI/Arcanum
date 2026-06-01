# Work Pack: Constitution Governance

Status: candidate
Date: 2026-05-27

## Objective

Promote Constitution Governance from source-contract candidate to validated canonical Arcanum sigil.

## Tasks

| Task | Scope | Acceptance Evidence |
| --- | --- | --- |
| CG-001 | Create source contract and registry entries. | README, SKILL, templates, registry links exist. |
| CG-002 | Add focused validation fixture for chart line-break rule. | Passing and failing fixture show validator behavior. |
| CG-003 | Create example composition pack. | A task-specific pack selects only relevant constitution rules. |
| CG-004 | Validate split/debloat mode against Artifact Constitution. | Report says whether rendering rules should remain in Artifact Constitution or move to a visual-artifact constitution. |
| CG-005 | Prepare command surface installation. | Sigil runtime installer handoff or command file. |
| CG-006 | Add artifact metadata constitution for intent/type-driven validation selection. | Candidate constitution and validation adapter plan exist. |

## Initial Completion State

- CG-001: completed in this package.
- CG-002: completed; validator self-test covers passing and failing chart line-break fixtures.
- CG-003: completed; example chart rendering composition pack exists.
- CG-004: completed; Artifact Constitution split/debloat report recommends no split yet.
- CG-005: completed; command surface resolves through local Arcanum command registry.
- CG-006: completed; candidate Artifact Metadata Constitution and adapter plan exist.

## Blockers

- No blockers remain for the source-contract work-pack.
- Reusable-behavior promotion still needs experiment-harness coverage across Constitution Governance modes.
- A future decision gate is required before splitting or renaming framework constitutions.

## Next Route

Use `experiment-harness` for reusable behavior fixtures before promoting the sigil beyond source-contract readiness.

## Completion Evidence

| Task | Evidence |
| --- | --- |
| CG-001 | `README.md`, `SKILL.md`, templates, registry entries, command files |
| CG-002 | `development/task-session/CG-002-RESULT.md`, validator self-test |
| CG-003 | `development/examples/chart-rendering-composition-pack.md`, `development/task-session/CG-003-RESULT.md` |
| CG-004 | `development/ARTIFACT-CONSTITUTION-SPLIT-REPORT.md`, `development/task-session/CG-004-RESULT.md` |
| CG-005 | `development/COMMAND-SURFACE-READINESS.md`, `development/task-session/CG-005-RESULT.md` |
| Schema Markdown boundary follow-up | `development/task-session/SCHEMA-MARKDOWN-BOUNDARY-RESULT.md`, validator self-test |
| Legacy schema YAML migration | `development/LEGACY-SCHEMA-YML-MIGRATION-PLAN.md`, `development/task-session/LEGACY-SCHEMA-YML-MIGRATION-RESULT.md`, validator self-test |
| Artifact metadata tagging follow-up | `framework/ARTIFACT-METADATA-CONSTITUTION.md`, `development/ARTIFACT-METADATA-VALIDATION-ADAPTER.md` |
