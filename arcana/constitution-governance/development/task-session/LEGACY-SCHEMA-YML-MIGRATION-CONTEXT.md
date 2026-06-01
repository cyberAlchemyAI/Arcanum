# Task Session Context: Legacy Schema YAML Migration

## Selected Unit

Execute the Invoke plan in `arcana/constitution-governance/development/LEGACY-SCHEMA-YML-MIGRATION-PLAN.md`.

## Source Artifacts

- `arcana/constitution-governance/development/LEGACY-SCHEMA-YML-MIGRATION-PLAN.md`
- `framework/SCHEMA-CONSTITUTION.md`
- `tools/validate-artifact-constitution.sh`
- `arcana/architecture-pattern-inventory/templates/architecture-package/pattern-library/inventory/architecture-inventory.schema.json`
- `formulae/dispatch-spec/dispatch.schema.json`
- `formulae/dispatch-spec/scripts/validate-dispatch.py`
- `formulae/dispatch-spec/development/run-validation-fixtures.sh`

## Gate Verdict

Pass. The migration had no remaining blocker decision after the schema Markdown boundary task. The user requested Invoke planning followed by Task Session execution.

## Controlling Constraints

- Canonical machine-readable schema files must use `.schema.yml`.
- Preserve schema semantics during JSON to YAML conversion.
- Update live tracked/source references to the new schema names.
- Keep historical refinement-run evidence out of the acceptance gate.
- Remove schema-format warnings from `tools/validate-artifact-constitution.sh`.

## Write Scope

- Architecture Pattern Inventory schema file and references.
- Dispatch Spec schema file, validator script, docs, and live references.
- Constitution Governance plan/result evidence.

## Done Criteria

- `architecture-inventory.schema.json` is migrated to `architecture-inventory.schema.yml`.
- `dispatch.schema.json` is migrated to `dispatch.schema.yml`.
- Dispatch validator loads YAML schema.
- Dispatch fixture suite passes.
- Artifact constitution validator passes without schema-format warnings.
- JSON Schema self-check passes for both migrated YAML schemas.
