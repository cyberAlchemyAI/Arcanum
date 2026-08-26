# Artifact Metadata Constitution

Status: candidate
Date: 2026-05-29
Owner: Constitution Governance

## Purpose

Artifact validation should be selected from declared artifact intent and type, not only from file paths, names, or extensions.

This constitution defines the metadata tags that let Constitution Governance, Context Builder, and validators identify what a file is trying to be and which validation rules should apply.

## Scope

Applies to:

- new source artifacts that define reusable behavior, schemas, constitutions, templates, sigils, spells, examples, or validation fixtures,
- new durable evidence artifacts that are promoted as proof or acceptance evidence,
- new canonical machine-readable files intended for validation, rendering, generation, or reuse,
- task-specific constitution packs and work-pack artifacts that drive execution.

Does not apply to:

- generated runtime logs and cache files,
- local runtime state,
- vendored third-party files,
- legacy artifacts until they enter a scoped migration task,
- tiny prose notes that are not used as source, durable evidence, or validation input.

## Core Metadata

Every governed artifact should expose enough metadata for validators to answer:

1. What is this artifact?
2. Why does it exist?
3. Who owns the rules for it?
4. Which constitutions should be selected?
5. Which validation profile should run?

Required fields for governed artifacts:

| Field | Meaning |
| --- | --- |
| `artifact_id` | Stable local identifier for this artifact. |
| `artifact_type` | Structural kind, such as `constitution`, `schema`, `work-pack`, `skill-contract`, `library-data`, `example`, `validation-report`, `composition-pack`, `template`, or `script`. |
| `intent` | One-sentence purpose of the file. |
| `owner` | Capability, framework area, spell, sigil, or module responsible for the artifact. |
| `lifecycle_status` | `candidate`, `reviewed`, `canonical`, `deprecated`, `generated`, or `local-runtime`. |
| `constitution_selectors` | Constitutions or rule families that should be considered for this artifact. |
| `validation_profile` | Named validator profile or command family that should run. |

Recommended fields:

| Field | Meaning |
| --- | --- |
| `evidence_role` | Whether the artifact is `source`, `durable-evidence`, `generated`, or `local-runtime`. |
| `canonical_format` | Expected canonical format when the artifact has a machine-readable source of truth. |
| `companion_to` | Target artifact when this file is explanatory companion prose. |
| `supersedes` | Prior artifact this file replaces. |
| `expires_when` | Condition where the artifact should be retired or refreshed. |

## Encoding Rules

Markdown artifacts should use YAML frontmatter:

```yaml
---
artifact_id: xray.visual-library.constitution
artifact_type: constitution
intent: Govern x-ray visual library data shape and validation selection.
owner: x-ray
lifecycle_status: candidate
constitution_selectors:
  - framework.artifact-metadata
  - xray.visual-library
validation_profile:
  - artifact-metadata
  - constitution-pack
---
```

YAML artifacts should include a top-level `artifact` block:

```yaml
artifact:
  artifact_id: xray.library.components
  artifact_type: library-data
  intent: Canonical reusable x-ray visual components.
  owner: x-ray
  lifecycle_status: candidate
  constitution_selectors:
    - framework.artifact-metadata
    - xray.visual-library
  validation_profile:
    - yaml-parse
    - xray-visual-library
components: []
```

JSON artifacts should include a top-level `artifact` object when they are canonical source or durable evidence.

Scripts should declare equivalent metadata in a leading comment block when they are canonical source artifacts and are expected to be selected by governance.

Binary or format-constrained artifacts may use a sidecar file named
`<artifact>.artifact.yml`. Codex-native `SKILL.md` requires `name` and
`description` for activation and may carry runtime-supported optional keys such
as `metadata`, `license`, and `allowed-tools` when applicable. Arcanum
repository-governance metadata belongs in `SKILL.md.artifact.yml`, not in the
runtime frontmatter. That sidecar may additionally record `tier`, `domain`,
`version`, and `origin` for sigil lifecycle governance.

## Rules

| Rule ID | Rule | Validation Mode | Validator | Status |
| --- | --- | --- | --- | --- |
| `artifact.metadata.required-for-governed-source` | New governed source artifacts must declare artifact metadata using the encoding supported by their format. | hybrid | future `tools/validate-artifact-constitution.sh` profile plus review | candidate |
| `artifact.metadata.selector-required` | Governed artifacts must declare `constitution_selectors` so Constitution Governance can select applicable rule packs. | deterministic | future metadata parser | candidate |
| `artifact.metadata.validation-profile-required` | Governed artifacts must declare `validation_profile` so validators know which checks to run. | deterministic | future metadata parser | candidate |
| `artifact.metadata.companion-boundary` | Companion prose must identify the canonical artifact it explains when the source of truth is machine-readable. | hybrid | future metadata parser plus review | candidate |
| `artifact.metadata.no-path-only-authority` | Path and extension heuristics may bootstrap validation, but they must not be the only authority for promoted or canonical governed artifacts. | review | Constitution Governance review until metadata parser exists | candidate |

## Examples

Preferred:

- `framework/SCHEMA-CONSTITUTION.md` declares `artifact_type: constitution`, selectors for schema and artifact metadata, and validation profile for constitution checks.
- `arcana/x-ray/library/components.yml` declares `artifact_type: library-data`, `canonical_format: yml`, selectors for `xray.visual-library`, and a validation profile for YAML parsing plus visual-library rules.
- `arcana/x-ray/library/components.md` declares `artifact_type: companion-doc` and `companion_to: arcana/x-ray/library/components.yml`.

Allowed during migration:

- a task-specific constitution pack may select rules manually while metadata adoption is incomplete.
- legacy files may remain untagged until touched by a scoped task.

## Non-Examples

- A validator chooses schema rules only because the filename contains `schema`.
- A Markdown catalog is treated as canonical data without declaring whether it is a companion or source of truth.
- A work-pack marks an artifact complete without naming the validation profile that proves its type-specific obligations.

## Composition

Precedence:

1. task-specific constitution pack,
2. artifact-type constitution selected by metadata,
3. domain or capability constitution selected by metadata,
4. framework constitution selected by metadata,
5. repository-wide fallback heuristics.

Conflicts:

- If metadata selectors and path heuristics disagree, report `flag` and require review before promotion.
- If `validation_profile` is missing but path heuristics imply a known profile, run the heuristic profile as a fallback and report a metadata gap.

## Validation

Candidate review checks:

```bash
rg -n "artifact_id|artifact_type|intent|constitution_selectors|validation_profile" framework arcana/constitution-governance arcana/x-ray
tools/validate-artifact-constitution.sh
```

Future deterministic checks:

- parse Markdown frontmatter for governed source paths,
- parse top-level `artifact` blocks in YAML and JSON,
- verify required metadata fields,
- map `constitution_selectors` to known constitutions or rule families,
- map `validation_profile` to known validator commands,
- flag path/metadata conflicts.

## Promotion Boundary

Required before canonical status:

- metadata parser design is approved,
- validator adapter has passing and failing fixtures,
- at least one capability adopts metadata tags end to end,
- Context Builder or Constitution Governance can select constitutions from metadata without loading unrelated rules,
- legacy migration policy is documented.

## Maintenance

Split trigger:

- split into per-format metadata constitutions if Markdown, YAML, JSON, and script tagging rules become too large.

Retirement trigger:

- retire only if the repository adopts a different typed artifact registry that provides equivalent selector and validation-profile behavior.
