# Refresh Patch Proposal: Insert YAML Library SWU

## Rationale

`x-ray` needs reusable visual components and patterns that future validators and renderers can consume. Markdown is good for explanation, but it should not be the canonical machine-readable library format.

## Proposed Work-Pack Insertion

Add this task after `TASK-XRAY-VIS-005` and before `TASK-XRAY-VIS-006`.

```markdown
## Task Contract: TASK-XRAY-VIS-005B

### Objective

Convert the visual component and pattern library to YAML-backed canonical data while keeping Markdown as human-readable reference documentation.

### Inputs

- `arcana/x-ray/library/components.md`
- `arcana/x-ray/library/patterns.md`
- `arcana/x-ray/library/user-shapes-template.md`
- `arcana/x-ray/development/invoke-runs/20260529T135625Z-yaml-library-refresh/REFRESH-REPORT.md`
- `arcana/x-ray/development/XRAY-VISUAL-LIBRARY-CONSTITUTION.md`
- `arcana/x-ray/development/constitution-pack.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`

### Write Scope

- `arcana/x-ray/library/components.yml`
- `arcana/x-ray/library/patterns.yml`
- `arcana/x-ray/library/user-shapes-template.yml`
- `arcana/x-ray/development/XRAY-VISUAL-LIBRARY-CONSTITUTION.md`
- `arcana/x-ray/development/constitution-pack.md`
- `arcana/x-ray/library/README.md`
- `arcana/x-ray/library/components.md`
- `arcana/x-ray/library/patterns.md`
- `arcana/x-ray/library/user-shapes-template.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`
- this work-pack status fields after validation
- `task-session/TASK-XRAY-VIS-005B-RESULT.md`

### Required Behavior

- YAML is the canonical source of reusable component, pattern, and user-shape-template records.
- The YAML authority rule is governed by `XRAY-VISUAL-LIBRARY-CONSTITUTION.md`.
- Task execution must select `arcana/x-ray/development/constitution-pack.md` before mutation.
- Markdown remains a readable guide that links to or describes the YAML records.
- Preserve all starter components: node, boundary, layer panel, risk marker, arrow, branch, feedback loop, timeline strip, risk matrix.
- Preserve all starter patterns: process branch, dependency boundary, lifecycle stack, evidence/inference split.
- Each YAML component entry includes id, family, intended lane, purpose, inputs, sketch, evidence rule, and when-not-to-use.
- Each YAML pattern entry includes id, target modes, required lanes, recommended components, accessibility notes, and validation notes.
- The user-shapes YAML template includes shape name, target domain, lane served, source evidence represented, visual sketch, and anti-pattern warning.
- Do not add JSON Schema yet; this SWU prepares stable YAML inputs for schema work.
- Preserve seed status and evidence/inference boundaries.

### Validation Surface

```bash
test -f arcana/x-ray/library/components.yml
test -f arcana/x-ray/library/patterns.yml
test -f arcana/x-ray/library/user-shapes-template.yml
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
rg -n "components.yml|patterns.yml|user-shapes-template.yml|canonical|YAML|evidence/inference" arcana/x-ray/library arcana/x-ray/SKILL.md arcana/x-ray/README.md
rg -n "xray.visual-library.canonical-yaml|xray.visual-library.evidence-bound|components.yml|patterns.yml|user-shapes-template.yml" arcana/x-ray/development/XRAY-VISUAL-LIBRARY-CONSTITUTION.md arcana/x-ray/development/constitution-pack.md
tools/validate-artifact-constitution.sh
git diff --check -- arcana/x-ray/library arcana/x-ray/SKILL.md arcana/x-ray/README.md arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray
```
```

## Proposed SWU Row

```markdown
| SWU-XRAY-VIS-005B | TASK-XRAY-VIS-005B | `arcana/x-ray/development/invoke-runs/20260529T135625Z-yaml-library-refresh/REFRESH-REPORT.md` | SWU-XRAY-VIS-005 | `arcana/x-ray/library/`, `arcana/x-ray/README.md`, `arcana/x-ray/SKILL.md` | Canonical YAML library exists and Markdown docs point to it. | YAML parse, library grep, diff check | local-fallback | ready |
```

## Route Change

Change next route from:

```bash
task-session to arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md --swu SWU-XRAY-VIS-006A
```

to:

```bash
task-session to arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md --swu SWU-XRAY-VIS-005B
```

After `SWU-XRAY-VIS-005B` passes, restore the route to `SWU-XRAY-VIS-006A`.
