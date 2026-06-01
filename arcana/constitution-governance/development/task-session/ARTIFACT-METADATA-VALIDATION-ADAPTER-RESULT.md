# Task Session Result: Artifact Metadata Validation Adapter

## Summary

Implemented the first deterministic artifact metadata validation slice.

The new helper parses artifact metadata from:

- Markdown YAML frontmatter,
- YAML top-level `artifact` blocks,
- JSON top-level `artifact` objects,
- leading script comment metadata,
- sidecar `<artifact>.artifact.yml` files.

The shell Artifact Constitution validator now invokes the helper in changed-file advisory mode. Strict missing-metadata enforcement remains available but is not globally enabled because the metadata constitution is still candidate and legacy migration is incomplete.

Advisory mode validates only explicit artifact metadata blocks. Ordinary Markdown command or skill frontmatter without artifact metadata keys is not treated as an incomplete artifact tag block.

## Files Updated

- `tools/validate-artifact-metadata.py`
- `tools/validate-artifact-constitution.sh`
- `arcana/constitution-governance/development/ARTIFACT-METADATA-VALIDATION-ADAPTER.md`
- `arcana/constitution-governance/development/task-session/ARTIFACT-METADATA-VALIDATION-ADAPTER-RESULT.md`
- `arcana/constitution-governance/development/task-session/ARTIFACT-METADATA-VALIDATION-ADAPTER-observation.json`

## Validation

```bash
python3 -m py_compile tools/validate-artifact-metadata.py
python3 tools/validate-artifact-metadata.py --self-test
bash -n tools/validate-artifact-constitution.sh
tools/validate-artifact-constitution.sh --self-test
python3 tools/validate-artifact-metadata.py --changed --advisory
tools/validate-artifact-constitution.sh
git diff --check -- tools framework arcana/constitution-governance/development
```

Result: pass. The full Artifact Constitution validator still reports pre-existing generated-artifact warnings, and metadata advisory mode reports scoped warnings for changed files that already contain partial artifact metadata.

## Remaining Follow-Up

- Add a selector/profile registry before enforcing selector/profile mapping.
- Run one scoped capability migration to prove metadata-driven constitution selection.
- Decide when to enable strict `--require-metadata` mode globally.
