---
constitution_id: xray.visual-library
title: x-ray Visual Library Constitution
status: candidate
owner: x-ray
authority_level: candidate
updated_at: 2026-05-29
---

# x-ray Visual Library Constitution

## Purpose

Govern the structure and validation expectations for reusable `x-ray` visual library artifacts so future components, patterns, and user additions remain machine-readable, renderer-ready, and evidence-bound.

## Scope

Applies to:

- `arcana/x-ray/library/components.yml`
- `arcana/x-ray/library/patterns.yml`
- `arcana/x-ray/library/user-shapes-template.yml`
- Markdown companions under `arcana/x-ray/library/`
- future `x-ray` visual library entries consumed by validators or renderers

Does not apply to:

- one-off SVG or HTML inside generated example pages,
- non-canonical explanatory sketches in task-session or invoke reports,
- framework-wide schema format rules governed by `framework/SCHEMA-CONSTITUTION.md`.

## Selection Predicates

Use this constitution when:

- creating or modifying reusable `x-ray` visual components, connectors, charts, patterns, or user-shape templates,
- selecting rules for `x-ray` schema work that validates visual library entries,
- building renderer adapters that consume `x-ray` visual library records,
- deciding whether Markdown or YAML owns a visual-library claim.

Do not load this constitution when:

- a task only updates narrative examples outside `arcana/x-ray/library/`,
- a task validates general schema file naming without touching `x-ray` visual-library semantics.

## Rules

| Rule ID | Rule | Validation Mode | Validator | Status |
| --- | --- | --- | --- | --- |
| `xray.visual-library.canonical-yaml` | Reusable visual component, connector, chart, pattern, and user-shape-template records must be canonical YAML data, not Markdown-only prose. | deterministic | `python3` YAML parse check, future `x-ray` schema validator | candidate |
| `xray.visual-library.markdown-companion` | Markdown files may explain the visual library, but must identify YAML as the source of truth when describing reusable records. | hybrid | `rg` text check plus review | candidate |
| `xray.visual-library.evidence-bound` | Every reusable visual record must declare the lane served and the evidence or inference it represents. | deterministic | future `x-ray` schema validator | candidate |
| `xray.visual-library.renderer-neutral` | Canonical records may include sketches, but must not require a production renderer, remote service, Mermaid, Three.js, or Kroki for baseline validity. | review | task-session review until adapter schemas exist | candidate |

## Examples

Preferred:

- `components.yml` contains a `shape.node` entry with `family`, `intended_lane`, `inputs`, `sketch`, `evidence_rule`, and `when_not_to_use`.
- `patterns.yml` contains a `pattern.dependency-boundary` entry with `target_modes`, `required_lanes`, `recommended_components`, `accessibility_notes`, and `validation_notes`.
- `components.md` summarizes the catalog and links to `components.yml` as canonical data.

Allowed:

- Markdown includes a pseudo-markup sketch for readability when the matching YAML record is canonical.
- A task-session result quotes a component entry for audit purposes.

## Non-Examples

- `components.md` is the only place where `shape.node` fields exist.
- A custom visual is accepted without declaring which `x-ray` lane it serves.
- A reusable pattern requires Three.js before the L0 static HTML/SVG path can be valid.

## Composition

Precedence:

1. Task-specific constitution pack for the active `x-ray` work-pack.
2. This `x-ray` visual library constitution.
3. `framework/SCHEMA-CONSTITUTION.md` for schema artifact file format.
4. `framework/ARTIFACT-CONSTITUTION.md` for artifact class, generated-state, and visual rendering rules.

Conflicts:

- None known.
- If a future framework constitution chooses a different canonical data format, route through Decision Gate before changing `x-ray` library records.

## Validation

Current candidate checks:

```bash
python3 - <<'PY'
import pathlib, yaml
for path in [
    "arcana/x-ray/library/components.yml",
    "arcana/x-ray/library/patterns.yml",
    "arcana/x-ray/library/user-shapes-template.yml",
]:
    data = yaml.safe_load(pathlib.Path(path).read_text())
    assert data, path
PY
rg -n "components.yml|patterns.yml|user-shapes-template.yml|canonical|YAML|source of truth|evidence/inference" arcana/x-ray/library arcana/x-ray/SKILL.md arcana/x-ray/README.md
```

Future promoted checks:

- candidate JSON/YAML schema validation for component records,
- candidate JSON/YAML schema validation for pattern records,
- invalid fixture probe for missing lane or missing evidence field.

## Promotion Boundary

Required before reviewed or canonical status:

- `SWU-XRAY-VIS-005B` creates YAML canonical files and Markdown companions.
- `SWU-XRAY-VIS-006B` adds candidate schema validation for components and patterns.
- At least one valid and one invalid fixture prove the evidence-bound rule.
- Sigil Development review confirms the rule does not overfit the first library slice.

## Maintenance

Split trigger:

- split this constitution if renderer adapter rules grow beyond library data governance.

Retirement trigger:

- retire only if `x-ray` stops maintaining reusable visual library records or adopts a broader visual constitution through Decision Gate.
