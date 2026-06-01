# Schema Constitution

Status: canonical
Date: 2026-05-28
Owner: Constitution Governance

## Purpose

Schema artifacts should be readable, diffable, and consistent across Arcanum.
Canonical machine-readable schema files must use YAML in `.schema.yml` files.

## Scope

Applies to:

- new machine-readable schema artifacts,
- canonical schema files intended for validation, generation, or reuse,
- schema files created by Arcanum sigils, spells, templates, or tools.

Does not apply to:

- Markdown documents that discuss schema concepts,
- TypeScript, JavaScript, Python, or shell code that implements schema behavior,
- generated or local runtime artifacts,
- upstream third-party files under benchmark fixtures or external materializations,
- legacy tracked schema files that require a separate migration plan.

## Rules

| Rule ID | Rule | Validation Mode | Validator | Status |
| --- | --- | --- | --- | --- |
| `schema.format.yml` | New canonical machine-readable schema artifacts must be stored as `.schema.yml`, not `.schema.json`, `.schema.yaml`, or prose-only schema files. | deterministic | `tools/validate-artifact-constitution.sh` | canonical |
| `schema.format.prose-boundary` | Markdown may describe schema shape, but new schema Markdown under template/source paths must either declare itself non-canonical or have a `.schema.yml` counterpart. | deterministic | `tools/validate-artifact-constitution.sh` | canonical |
| `schema.format.legacy-migration` | Existing tracked non-YML schema artifacts are legacy warnings until migrated through an explicit task. | deterministic | `tools/validate-artifact-constitution.sh` | canonical |

## Examples

Preferred:

- `arcana/example/templates/example.schema.yml`
- `framework/runtime/config.schema.yml`

Not preferred:

- `arcana/example/templates/example.schema.json`
- `arcana/example/templates/example.schema.yaml`
- `arcana/example/templates/example-schema.md` as the only canonical schema artifact

Allowed Markdown companion:

- `arcana/example/templates/example-schema.md` paired with `arcana/example/templates/example.schema.yml`
- `arcana/example/templates/example-schema.md` containing `Schema Artifact Role: non-canonical` when it is only explanatory prose

## Validation

Run:

```bash
tools/validate-artifact-constitution.sh
```

Fixture self-test:

```bash
tools/validate-artifact-constitution.sh --self-test
```

## Promotion Boundary

This constitution is canonical for new schema artifacts immediately.

Existing non-YML schema artifacts should be migrated only through scoped task-session work that preserves downstream references.

## Maintenance

Split trigger:

- schema rules expand beyond format governance into schema semantics, evolution, compatibility, or registry behavior.

Retirement trigger:

- Arcanum adopts a different canonical machine-readable schema format through Decision Gate.
