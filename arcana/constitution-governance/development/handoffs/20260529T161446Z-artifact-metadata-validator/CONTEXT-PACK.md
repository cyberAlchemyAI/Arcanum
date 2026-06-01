# Context Pack: Artifact Metadata Validator

## Source Session Reference

- Session: current Codex thread on 2026-05-29
- Repository: `/home/vrondelli/projects/domainspec-core/arcanum`
- Split reason: continue Artifact Constitution / Constitution Governance implementation in a fresh session without carrying the x-ray visual-library work along.

## Target Boundary

This handoff is about implementing the validator path for artifact metadata tags.

In scope:

- `framework/ARTIFACT-METADATA-CONSTITUTION.md`
- `framework/ARTIFACT-CONSTITUTION.md`
- `arcana/constitution-governance/development/ARTIFACT-METADATA-VALIDATION-ADAPTER.md`
- `arcana/constitution-governance/development/WORK-PACK.md`
- `tools/validate-artifact-constitution.sh`
- candidate new helper `tools/validate-artifact-metadata.py`
- fixture/self-test strategy for metadata parsing and validation selection.

Out of scope:

- completing `x-ray` YAML library conversion,
- implementing x-ray component/pattern schemas,
- promoting Constitution Governance beyond current readiness,
- cleaning unrelated generated-artifact warnings.

## Selected Source Context

### User Intent

The user identified that validation failed to catch the Markdown-vs-YAML library issue because files are not tagged with artifact intent/type. They want Constitution Governance to support metadata tags so validators can extract artifact intent and type and know which validation profile should apply.

### Existing Candidate Constitution

`framework/ARTIFACT-METADATA-CONSTITUTION.md` now defines candidate metadata fields for governed artifacts:

- `artifact_id`
- `artifact_type`
- `intent`
- `owner`
- `lifecycle_status`
- `constitution_selectors`
- `validation_profile`

It also defines recommended fields:

- `evidence_role`
- `canonical_format`
- `companion_to`
- `supersedes`
- `expires_when`

The constitution is candidate, not canonical. Its promotion boundary requires parser design, validator fixtures, one capability adoption, metadata-driven constitution selection, and a legacy migration policy.

### Existing Adapter Plan

`arcana/constitution-governance/development/ARTIFACT-METADATA-VALIDATION-ADAPTER.md` proposes:

- existing wrapper: `tools/validate-artifact-constitution.sh`
- new helper candidate: `tools/validate-artifact-metadata.py`
- invocation:

```bash
tools/validate-artifact-constitution.sh
python3 tools/validate-artifact-metadata.py --changed
```

The helper should parse:

- Markdown YAML frontmatter,
- top-level `artifact` blocks in YAML,
- top-level `artifact` objects in JSON,
- leading script comment blocks,
- sidecar `<artifact>.artifact.yml` files.

### Current Validator Limitation

`tools/validate-artifact-constitution.sh` currently relies heavily on path and filename heuristics:

- local runtime path detection,
- generated artifact path detection,
- visual artifact filename/path detection,
- schema artifact filename detection,
- schema Markdown template detection.

It does not yet parse artifact metadata or fail when governed source artifacts omit metadata.

### Related Precedent

`framework/ARTIFACT-CONSTITUTION.md` already classifies source, durable evidence, generated, and local runtime artifacts. It now links to `framework/ARTIFACT-METADATA-CONSTITUTION.md` and records the limitation:

> validation still relies heavily on path and filename heuristics. Metadata-driven constitution selection is governed by the Artifact Metadata Constitution and remains candidate until its validation adapter is implemented.

## Obligations For Next Session

| Obligation | Required Coverage |
| --- | --- |
| Preserve candidate status | Do not claim canonical metadata governance until fixtures and adoption evidence exist. |
| Implement deterministic parser | Add a helper or equivalent code path that extracts metadata from Markdown/YAML/JSON at minimum. |
| Avoid legacy noise | Warn or skip legacy untagged artifacts unless touched by the current task. |
| Integrate with current validator | Wire the metadata helper into `tools/validate-artifact-constitution.sh` or document why a separate command is safer first. |
| Add fixtures/self-test | Include passing and failing fixtures for Markdown frontmatter, YAML `artifact` block, JSON `artifact` object, and companion Markdown. |
| Actionable messages | Failures should name the missing field and path. |
| Selector/profile mapping | At minimum, validate presence of `constitution_selectors` and `validation_profile`; mapping to a registry can be a follow-up if too large. |

## Validation Surface

Expected next-session checks:

```bash
bash -n tools/validate-artifact-constitution.sh
python3 -m py_compile tools/validate-artifact-metadata.py
tools/validate-artifact-constitution.sh --self-test
python3 tools/validate-artifact-metadata.py --self-test
tools/validate-artifact-constitution.sh
git diff --check -- tools framework arcana/constitution-governance/development
```

If the metadata helper is not wired into the shell validator in the first slice, the result must explicitly say the adapter remains separate and why.

## Excluded Context

- x-ray static HTML/SVG example details are excluded; they motivated the rule but are not needed for the validator implementation.
- x-ray component YAML conversion is excluded; that belongs to `SWU-XRAY-VIS-005B`.
- broader generated artifact cleanup is excluded; current validator warnings are known policy debt.
