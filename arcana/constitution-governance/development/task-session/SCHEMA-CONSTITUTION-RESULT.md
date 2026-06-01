# Task Session Result: Schema Constitution

## Summary

Added a framework-level Schema Constitution requiring new canonical
machine-readable schema artifacts to use `.schema.yml`.

The validator now:

- fails new untracked `.schema.json` or `.schema.yaml` artifacts,
- accepts `.schema.yml`,
- warns for existing tracked non-YML schema artifacts so they can be migrated by
  scoped follow-up work without breaking the repository immediately.

## Files Updated

- `framework/SCHEMA-CONSTITUTION.md`
- `framework/ARTIFACT-CONSTITUTION.md`
- `tools/validate-artifact-constitution.sh`

## Validation

```bash
bash -n tools/validate-artifact-constitution.sh
tools/validate-artifact-constitution.sh --self-test
tools/validate-artifact-constitution.sh
```

Result: pass, with legacy warnings for existing tracked generated artifacts and
tracked non-YML schema artifacts.

## Follow-Up

Migrate legacy `.schema.json` files to `.schema.yml` through separate scoped
task-session work if they are still canonical.
