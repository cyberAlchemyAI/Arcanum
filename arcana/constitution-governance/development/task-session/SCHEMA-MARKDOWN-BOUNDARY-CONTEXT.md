# Task Session Context: Schema Markdown Boundary

## Selected Unit

Patch constitution validation so schema-shaped Markdown cannot silently become the only canonical schema artifact, and repair Inventory schema templates with canonical `.schema.yml` siblings.

## Source Artifacts

- `arcana/constitution-governance/development/INVOKE-SCHEMA-CONSTITUTION-VALIDATION.md`
- `framework/SCHEMA-CONSTITUTION.md`
- `framework/ARTIFACT-CONSTITUTION.md`
- `tools/validate-artifact-constitution.sh`
- `arcana/inventory/templates/evidence-card-schema.md`
- `arcana/inventory/templates/evidence-set-schema.md`
- `arcana/inventory/templates/schema.md`

## Gate Verdict

Pass. The Invoke validation report identified a validator coverage gap, not a blocker decision. The user confirmed the expected rule: schemas should be YAML.

## Controlling Constraints

- Canonical machine-readable schemas use `.schema.yml`.
- Markdown may explain or template schema shape only when it is explicitly non-canonical or paired with `.schema.yml`.
- Legacy tracked `.schema.json` files remain warnings until migrated through separate scoped work.
- Do not migrate unrelated legacy schemas in this task.

## Write Scope

- `tools/validate-artifact-constitution.sh`
- `framework/SCHEMA-CONSTITUTION.md`
- `framework/ARTIFACT-CONSTITUTION.md`
- `arcana/inventory/templates/evidence-card-schema.md`
- `arcana/inventory/templates/evidence-card.schema.yml`
- `arcana/inventory/templates/evidence-set-schema.md`
- `arcana/inventory/templates/evidence-set.schema.yml`
- `arcana/inventory/templates/schema.md`
- `arcana/constitution-governance/development/task-session/SCHEMA-MARKDOWN-BOUNDARY-RESULT.md`

## Done Criteria

- Validator self-test covers schema Markdown boundary cases.
- New schema Markdown under template/source paths fails unless non-canonical or paired with `.schema.yml`.
- Inventory evidence-card and EvidenceSet schema docs have canonical `.schema.yml` siblings.
- Artifact constitution validation passes with only existing legacy warnings.
