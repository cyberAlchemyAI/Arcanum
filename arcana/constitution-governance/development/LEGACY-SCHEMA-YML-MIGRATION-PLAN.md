# Invoke Plan: Legacy Schema YAML Migration

## Mode

`invoke plan`

## Target

Migrate legacy tracked `.schema.json` artifacts to canonical `.schema.yml` format under the Schema Constitution.

## Status

pass

## Source Inputs

- `framework/SCHEMA-CONSTITUTION.md`
- `framework/ARTIFACT-CONSTITUTION.md`
- `tools/validate-artifact-constitution.sh`
- `arcana/constitution-governance/development/INVOKE-SCHEMA-CONSTITUTION-VALIDATION.md`
- `arcana/constitution-governance/development/task-session/SCHEMA-MARKDOWN-BOUNDARY-RESULT.md`

## Legacy Schema Artifacts

| Legacy File | Owner | Target File | Migration Risk |
| --- | --- | --- | --- |
| `arcana/architecture-pattern-inventory/templates/architecture-package/pattern-library/inventory/architecture-inventory.schema.yml` | Architecture Pattern Inventory | `architecture-inventory.schema.yml` | low: isolated template package reference. |
| `formulae/dispatch-spec/dispatch.schema.yml` | Dispatch Spec Formulae | `dispatch.schema.yml` | medium: referenced by validator script, Refine docs/templates, and Formulae docs. |

## Implementation Layers

### L0: Direct Format Migration

Goal: create YAML equivalents and remove the two legacy JSON schema files.

Validation:

```sh
python3 -c 'import yaml; yaml.safe_load(open("...schema.yml"))'
tools/validate-artifact-constitution.sh
```

### L1: Reference Repair

Goal: update tracked source references from `.schema.json` to `.schema.yml`.

Validation:

```sh
git ls-files | xargs rg -n 'dispatch\.schema\.json|architecture-inventory\.schema\.json'
```

Expected remaining matches: none in tracked source files, except historical/generated artifacts deliberately outside the source migration scope.

### L2: Domain Validator Compatibility

Goal: update Dispatch Spec validator to load `dispatch.schema.yml`.

Validation:

```sh
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

### L3: Constitution Closure

Goal: prove Artifact Constitution no longer warns for tracked schema JSON files.

Validation:

```sh
tools/validate-artifact-constitution.sh --self-test
tools/validate-artifact-constitution.sh
```

Expected result: pass. Any remaining warnings should be generated-artifact warnings, not schema-format warnings.

## Work-Pack

| Task | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| MIG-SCHEMA-001 | Convert Architecture Inventory schema to `.schema.yml` and update package docs. | architecture-pattern-inventory schema file and references | YAML parse, reference grep |
| MIG-SCHEMA-002 | Convert Dispatch Spec schema to `.schema.yml` and update validator/docs. | dispatch-spec schema, script, docs, tracked references | fixture validation, reference grep |
| MIG-SCHEMA-003 | Run constitution closure and record task-session evidence. | constitution-governance task-session result | artifact constitution validator |

## Task Session Route

Execute the full migration locally because the plan has no remaining blocker decision and the user requested `task-session` immediately after planning.

Stop if:

- YAML conversion changes schema semantics;
- Dispatch fixture validation fails after updating the validator;
- tracked source references to the old `.schema.json` paths remain;
- artifact constitution still reports schema-format warnings.
