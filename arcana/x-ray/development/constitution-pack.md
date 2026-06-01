# Constitution Pack: x-ray YAML Visual Library Correction

## Target

`SWU-XRAY-VIS-005B`: convert the `x-ray` visual component and pattern library to YAML-backed canonical data before schema work continues.

## Selected Constitutions

| Constitution | Selection Rationale |
| --- | --- |
| `arcana/x-ray/development/XRAY-VISUAL-LIBRARY-CONSTITUTION.md` | Governs the target library records and the Markdown/YAML authority split. |
| `framework/SCHEMA-CONSTITUTION.md` | Applies later to schema artifact naming and reinforces YAML for canonical machine-readable schema files. |
| `framework/ARTIFACT-CONSTITUTION.md` | Applies to artifact classification and visual rendering rules. |

## Selected Rules

| Rule ID | Source | Applies To This Task | Validation Mode |
| --- | --- | --- | --- |
| `xray.visual-library.canonical-yaml` | `XRAY-VISUAL-LIBRARY-CONSTITUTION.md` | Create `components.yml`, `patterns.yml`, and `user-shapes-template.yml` as canonical data. | deterministic |
| `xray.visual-library.markdown-companion` | `XRAY-VISUAL-LIBRARY-CONSTITUTION.md` | Update Markdown docs to identify YAML as the source of truth. | hybrid |
| `xray.visual-library.evidence-bound` | `XRAY-VISUAL-LIBRARY-CONSTITUTION.md` | Ensure each YAML record names lane and evidence/inference rule. | deterministic |
| `xray.visual-library.renderer-neutral` | `XRAY-VISUAL-LIBRARY-CONSTITUTION.md` | Keep sketches renderer-neutral and L0-compatible. | review |
| `schema.format.yml` | `framework/SCHEMA-CONSTITUTION.md` | Applies to later schema files, not this SWU's library data. | deterministic |
| Artifact class rules 1-3 | `framework/ARTIFACT-CONSTITUTION.md` | Treat library YAML and Markdown as source artifacts. | review |
| Rendering rule 1 | `framework/ARTIFACT-CONSTITUTION.md` | Avoid literal `\\n` line-break dependence in visual text/sketch labels. | deterministic via framework validator |

## Precedence

1. This task-specific constitution pack.
2. `arcana/x-ray/development/XRAY-VISUAL-LIBRARY-CONSTITUTION.md`.
3. `framework/SCHEMA-CONSTITUTION.md`.
4. `framework/ARTIFACT-CONSTITUTION.md`.

## Conflicts

None known.

## Validators To Run

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
tools/validate-artifact-constitution.sh
git diff --check -- arcana/x-ray/library arcana/x-ray/SKILL.md arcana/x-ray/README.md arcana/x-ray/development
```

## Pass/Flag/Block Semantics

- Pass: YAML files exist, parse, contain lane/evidence fields, and Markdown companions name YAML as canonical.
- Flag: YAML exists but a renderer-neutral or Markdown companion rule needs review.
- Block: YAML files are missing, unparseable, or omit lane/evidence obligations.

## Context Budget

For `SWU-XRAY-VIS-005B`, load only:

- this constitution pack,
- `XRAY-VISUAL-LIBRARY-CONSTITUTION.md`,
- `REFRESH-REPORT.md` for the YAML correction,
- current library Markdown files,
- the work-pack task/SWU rows.
