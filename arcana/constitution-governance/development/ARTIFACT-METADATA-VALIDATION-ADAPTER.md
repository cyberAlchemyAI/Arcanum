# Validation Adapter Plan: Artifact Metadata Tags

## Rule Source

- Constitution: `framework/ARTIFACT-METADATA-CONSTITUTION.md`
- Rule IDs:
  - `artifact.metadata.required-for-governed-source`
  - `artifact.metadata.selector-required`
  - `artifact.metadata.validation-profile-required`
  - `artifact.metadata.companion-boundary`
  - `artifact.metadata.no-path-only-authority`
- Validation mode: hybrid now; deterministic after parser fixtures exist.

## Target Validator

- Existing tool: `tools/validate-artifact-constitution.sh`
- New helper: `tools/validate-artifact-metadata.py`
- Invocation:

```bash
tools/validate-artifact-constitution.sh
python3 tools/validate-artifact-metadata.py --changed --advisory
python3 tools/validate-artifact-metadata.py --self-test
```

## Detection Logic

What the validator should check:

- Identify governed source artifacts from path plus git state.
- Parse metadata from:
  - Markdown YAML frontmatter,
  - top-level `artifact` blocks in YAML,
  - top-level `artifact` objects in JSON,
  - leading script comment blocks,
  - sidecar `<artifact>.artifact.yml` files.
- Require `artifact_id`, `artifact_type`, `intent`, `owner`, `lifecycle_status`, `constitution_selectors`, and `validation_profile` for new governed source artifacts.
- Warn, rather than fail, on legacy untagged artifacts until a migration task touches them.
- Flag mismatches when path heuristics imply one validation profile but metadata declares another.
- Map `constitution_selectors` to known constitution files or registered rule families.
- Map `validation_profile` to executable validators or review-only profiles.

False positives to avoid:

- generated observability ledgers and runtime state,
- vendored third-party files,
- throwaway local notes,
- legacy artifacts not touched by the current task,
- examples that intentionally demonstrate invalid metadata.

False negatives accepted for now:

- binary artifacts without sidecars,
- scripts whose comment metadata is not yet standardized,
- generated examples promoted as durable evidence before sidecar conventions exist.

## Failure Message

```text
governed artifact lacks metadata tags for constitution selection and validation profile: <path>
required fields: artifact_id, artifact_type, intent, owner, lifecycle_status, constitution_selectors, validation_profile
```

## Fixtures

Implemented self-test fixtures:

- Markdown with complete YAML frontmatter.
- YAML with top-level `artifact` block.
- JSON with top-level `artifact` object.
- Markdown source artifact with no frontmatter.
- YAML library-data artifact without `constitution_selectors`.
- JSON durable evidence artifact without `validation_profile`.
- Companion Markdown that describes canonical data without `companion_to`.

## Promotion

This adapter can be treated as enforcing the constitution when:

- fixture self-test covers pass/fail cases for Markdown, YAML, JSON, and companion docs,
- validator runs from the existing artifact constitution hook in advisory mode without excessive noise,
- one scoped capability migration proves metadata-driven constitution selection,
- Constitution Governance has a documented profile registry or mapping for selector names.

## Implementation Status

- Parser helper: implemented in `tools/validate-artifact-metadata.py`.
- Shell validator integration: implemented as changed-file advisory warnings from `tools/validate-artifact-constitution.sh`.
- Advisory scope: ordinary Markdown frontmatter is ignored unless it contains artifact metadata keys, which keeps command/skill frontmatter from becoming false-positive migration noise.
- Strict metadata enforcement: available through `python3 tools/validate-artifact-metadata.py --changed --require-metadata`, but not enabled globally until migration/adoption evidence exists.
