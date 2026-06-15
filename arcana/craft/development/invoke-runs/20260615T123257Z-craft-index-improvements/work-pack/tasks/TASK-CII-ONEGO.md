# TASK-CII-ONEGO: Execute Craft Index Improvements In One Goal

## Objective

Execute the complete Craft index improvement bundle in one native Codex Goal
session, preserving gated execution and stopping before publication.

## Layer And Slice Mapping

- L0 / S-CII-001: source contract.
- L1 / S-CII-002: public-safe fixture.
- L2 / S-CII-003: build/validate tooling.
- L3 / S-CII-004 and S-CII-005: fast-path integration and dry-run import.
- L3 / S-CII-006 and S-CII-007: generated mirrors and publication-prep checks.

## Source Contracts

- `INVOKE-DESIGN-ARCHITECTURE.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `../refinement-runs/20260614T200439Z-craft-feature-readiness-indexes/RESULT.md`
- `../refinement-runs/20260615T121512Z-craft-ledger-csv-json-indexes/RESULT.md`
- `arcana/craft/templates/ledger.schema.yml`
- `arcana/craft/SKILL.md`
- `arcana/craft/README.md`

## Dependencies

- Read private handoff pack first.
- Use private decision profile only for execution posture; do not copy profile
  content into public artifacts.
- Preserve submodule discipline.

## Smallest Working Units

### SWU-CII-001: Add Combined Contract

- Goal: update schema/docs/SKILL with readiness index and projection contracts.
- Dependencies: none.
- Write scope: `arcana/craft/templates/ledger.schema.yml`,
  `arcana/craft/SKILL.md`, `arcana/craft/README.md`.
- Done criteria: contracts mention readiness, generated index metadata,
  `.craft/projections/`, stale detection, YAML authority, and non-execution
  boundary.
- Acceptance evidence: targeted grep and YAML parse.
- Validation surface:
  - `python3 - <<'PY' ... yaml.safe_load(...)`
  - `rg -n "execution_readiness|projections|ledger_sha256|pending_by_node|YAML" arcana/craft`
- Execution owner: local-fallback.

### SWU-CII-002: Add Public-Safe Fixture

- Goal: add synthetic fixture and expected projection outputs.
- Dependencies: `SWU-CII-001`.
- Write scope: `arcana/craft/fixtures/craft-index-improvements/`.
- Done criteria: fixture covers contexts, artifacts, typed items, decisions,
  relations, gaps, descriptions/definitions, route handoffs, receipts,
  recomposition, readiness, and links.
- Acceptance evidence: YAML/JSON/CSV parse and public-boundary scan.
- Execution owner: local-fallback.

### SWU-CII-003: Add Build/Validate Tooling

- Goal: add deterministic projection generator and validator.
- Dependencies: `SWU-CII-002`.
- Write scope: `arcana/craft/scripts/`.
- Done criteria: build emits deterministic `index.json` and CSV projections;
  validate detects stale source, unsupported row families, bad references, and
  non-deterministic headers.
- Acceptance evidence: fixture command output.
- Execution owner: local-fallback.

### SWU-CII-004: Integrate Fast-Path Status Contract

- Goal: document and validate `pending_by_node` and readiness fast-path
  behavior with stale fallback.
- Dependencies: `SWU-CII-003`.
- Write scope: `arcana/craft/SKILL.md`, `arcana/craft/README.md`, possibly
  `arcana/craft/scripts/`.
- Done criteria: all-status contract can use fresh generated index and must
  fall back to YAML on stale/missing index.
- Acceptance evidence: grep checks and fixture validation.
- Execution owner: local-fallback.

### SWU-CII-005: Add CSV Import Dry Run

- Goal: add `import-csv --dry-run` patch-plan behavior.
- Dependencies: `SWU-CII-003`.
- Write scope: `arcana/craft/scripts/`.
- Done criteria: dry-run blocks stale projections, ID churn, unresolved
  references, and unsupported read-only nested-field edits.
- Acceptance evidence: fixture dry-run report.
- Execution owner: local-fallback.

### SWU-CII-006: Refresh Generated Runtime Mirrors

- Goal: regenerate generated Craft runtime surfaces after canonical validation.
- Dependencies: `SWU-CII-001` through `SWU-CII-005`.
- Write scope: generated runtime copies only.
- Done criteria: generated mirrors include new canonical wording.
- Acceptance evidence: generation command and targeted grep.
- Execution owner: local-fallback.
- Gate: do not run if canonical checks fail.

### SWU-CII-007: Final Validation And Publication Prep

- Goal: produce validation-ready state without committing or pushing.
- Dependencies: `SWU-CII-006`.
- Write scope: no content edits unless fixing validation residue.
- Done criteria: diff-check passes; publication blockers are explicit.
- Acceptance evidence:
  - `git -C arcanum diff --check -- arcana/craft`
  - parent `make bump-check` only if publication is requested.
- Execution owner: manual/local-fallback.

## Synchronization Rules

- Update this work-pack or task file only if the execution changes scope,
  validation, or blockers.
- Keep generated artifacts source-derived; do not hand-edit generated outputs.
- Final report must list files touched, checks run, pass/flag/block verdict, and
  any extra source used outside the handoff pack.
