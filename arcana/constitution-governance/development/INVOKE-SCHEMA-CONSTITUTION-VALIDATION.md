# Invoke Validate: Schema Constitution Enforcement Gap

## Mode

`invoke validate`

## Status

flag

Invoke validate mode is still marked deferred in `spells/invoke/validate.md`, so this report is a targeted local validation artifact rather than a complete command-backed Invoke validation run.

## Target

Schema constitution and artifact constitution enforcement.

## Question

Why did schema-shaped artifacts pass validation when schemas should always use YAML?

## Findings

### 1. Artifact constitution validation is running, but the schema matcher is too narrow

`tools/validate-artifact-constitution.sh` runs successfully and is wired into the Codex `PostToolUse` hook through `.codex/hooks.json`.

The current schema rule only detects:

- `*.schema.json`
- `*.schema.yaml`

It treats tracked matching files as legacy warnings and new matching files as failures.

It does not detect schema-shaped Markdown files such as:

- `arcana/inventory/templates/evidence-card-schema.md`
- `arcana/inventory/templates/evidence-set-schema.md`
- `arcana/inventory/templates/schema.md`

This is why the Inventory schema templates were not blocked.

### 2. The Schema Constitution exists, but prose-boundary validation is review-only

`framework/SCHEMA-CONSTITUTION.md` says canonical machine-readable schema artifacts must use `.schema.yml`.

It also says Markdown may discuss schema shape, but must not be treated as the canonical machine-readable schema artifact.

The validator enforces `.schema.json` / `.schema.yaml` format, but it does not enforce the prose-boundary rule. That rule is currently marked as review-only, so Markdown schema templates can pass even when they are the only schema artifact.

### 3. Existing non-YAML schema files are intentionally warnings, not failures

Current non-YAML machine-readable schema files:

- `arcana/architecture-pattern-inventory/templates/architecture-package/pattern-library/inventory/architecture-inventory.schema.yml`
- `formulae/dispatch-spec/dispatch.schema.yml`

The validator reports these as legacy migration warnings because they are tracked files.

This matches the constitution's legacy migration rule, but it also means the repo can still contain old `.schema.json` artifacts until an explicit migration task runs.

### 4. The hook does not help when the validator passes

The Codex `PostToolUse` hook does run `tools/validate-artifact-constitution.sh` after file-writing tools.

The hook records pass/fail, but it cannot block what the validator does not classify as a violation. Because Markdown schema templates are outside the deterministic schema matcher, the hook records a pass.

## Why This Happened

The schema constitution was added after earlier schema-shaped artifacts already existed. Enforcement started with the narrow, low-risk rule:

> fail new `.schema.json` / `.schema.yaml`; warn tracked legacy `.schema.json`.

That rule missed the more important behavioral case:

> a Markdown file named or used as a schema becomes the only canonical schema artifact.

So the problem is not that artifact constitution validation is absent. The problem is that schema constitution enforcement is incomplete.

## Schema-Like Artifacts Found

### Machine-readable non-YAML schema files

- `arcana/architecture-pattern-inventory/templates/architecture-package/pattern-library/inventory/architecture-inventory.schema.yml`
- `formulae/dispatch-spec/dispatch.schema.yml`

### Schema-shaped Markdown files that need classification

- `arcana/inventory/templates/evidence-card-schema.md`
- `arcana/inventory/templates/evidence-set-schema.md`
- `arcana/inventory/templates/schema.md`
- `arcana/ontology-vault/development/BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md`
- `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/WHISPER-SCHEMA.md`
- `research/proofs/ontology-vault-branching/.arcanum/inventory/schema.md`

Some Markdown files may remain valid as schema explainers, candidate notes, or run evidence. They should not be treated as canonical machine-readable schema artifacts unless paired with a `.schema.yml` file or explicitly marked as non-canonical prose.

## Recommended Decision

Add a stricter schema constitution enforcement task:

1. Canonical machine-readable schemas must be `.schema.yml`.
2. New `*-schema.md`, `SCHEMA*.md`, and `schema.md` files must be classified:
   - allowed when they are explicitly prose/candidate/explainer/run evidence;
   - blocked when they are the only canonical schema contract.
3. Schema templates that are intended for machine validation must have a sibling `.schema.yml`.
4. Legacy `.schema.json` files stay warnings until migrated through scoped tasks.
5. The validator self-test must include:
   - bad `example-schema.md` with canonical-schema language and no sibling `.schema.yml`;
   - good `example-schema.md` marked as prose-only;
   - good `example.schema.yml`;
   - legacy tracked `.schema.json` warning behavior.

## Next Route

`task-session` for Constitution Governance:

- patch `tools/validate-artifact-constitution.sh`;
- add schema Markdown boundary checks;
- add self-test fixtures;
- classify or repair the Inventory schema artifacts created in the last task;
- create `.schema.yml` files for canonical Inventory schemas or mark Markdown files as explainers/templates only;
- rerun:

```sh
tools/validate-artifact-constitution.sh --self-test
tools/validate-artifact-constitution.sh
```

## Validation Performed

```sh
tools/validate-artifact-constitution.sh
tools/validate-artifact-constitution.sh --self-test
git ls-files '*schema*' '*SCHEMA*'
git ls-files --others --exclude-standard | rg '(^|/)([^/]*schema[^/]*\.md|SCHEMA[^/]*\.md|.*\.schema\.(json|yaml))$'
```

Current result: `tools/validate-artifact-constitution.sh` passes with warnings, proving the existing validator is alive but under-scoped.

## Resolution

Resolved by `arcana/constitution-governance/development/task-session/SCHEMA-MARKDOWN-BOUNDARY-RESULT.md`.

The validator now includes schema Markdown boundary fixtures, Inventory has `.schema.yml` schema artifacts for evidence-cards and EvidenceSets, and schema-shaped Markdown templates are classified as templates or package conventions instead of standalone canonical machine-readable schemas.

Legacy `.schema.json` migration completed in `arcana/constitution-governance/development/task-session/LEGACY-SCHEMA-YML-MIGRATION-RESULT.md`.
