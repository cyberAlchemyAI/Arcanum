# WORK-PACK: Visual Layered x-ray Revision

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Refine result and Invoke define/design artifacts exist. |
| complexity | medium | Contract, examples, validation, and later visual adapters are distinct slices. |
| outputMode | single-package | Work remains under `arcana/x-ray/`. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision boundaries. |
| activeLayerWindow | L5 | L0-L5 revision package completed through candidate lane, component, and pattern schemas. |
| readinessProfile | seed-revision-schema-candidates-complete | No promotion claim. |

## Objective Summary

Revise `x-ray` from a general HTML explainer seed into a dispatch-spec governed visual inspection sigil with explicit modes, lanes, dependency views, and a static layered HTML renderer path.

## Source Contracts

- `INVOKE-DEFINE.md`
- `INVOKE-DESIGN.md`
- `IMPLEMENTATION-LAYERING.md`
- `arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/RESULT.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-XRAY-001 | Canonical README/SKILL contract revised. | L0 | refine and invoke artifacts | `rg` contract checks plus `git diff --check` |
| S-XRAY-002 | Static lane model and HTML/SVG example exist. | L1 | S-XRAY-001 | file checks and HTML parse |
| S-XRAY-003 | Validation harness checks lane/artifact shape. | L2 | S-XRAY-002 | validator run |
| S-XRAY-004 | Optional visual adapter backlog documented. | L3 | S-XRAY-003 | review checklist |
| S-XRAY-005 | Visual component library and user extension nudge exist. | L4 | S-XRAY-004 | file checks and library grep |
| S-XRAY-005B | Visual component library is YAML-backed canonical data. | L4 | S-XRAY-005 | YAML parse and constitution pack checks |
| S-XRAY-006 | Candidate x-ray schemas and validator integration exist. | L5 | S-XRAY-005 | schema parse and validator run |

## Task Status Board

| Task ID | Goal | Layer | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- |
| TASK-XRAY-VIS-001 | Revise canonical `x-ray` contract with modes, lanes, dependency views, and renderer ladder. | L0 | Invoke define/design | ready | completed |
| TASK-XRAY-VIS-002 | Add static layered HTML/SVG example package. | L1 | TASK-XRAY-VIS-001 | ready | completed |
| TASK-XRAY-VIS-003 | Add x-ray artifact validation harness. | L2 | TASK-XRAY-VIS-002 | ready | completed |
| TASK-XRAY-VIS-004 | Document optional Mermaid/CSS3D/Three.js/Kroki adapter backlog. | L3 | TASK-XRAY-VIS-003 | ready | completed |
| TASK-XRAY-VIS-005 | Add visual component library and user extension nudge. | L4 | component-library refine result | ready | completed |
| TASK-XRAY-VIS-005B | Convert visual library records to YAML-backed canonical data. | L4 | yaml-library refresh and constitution pack | ready | completed |
| TASK-XRAY-VIS-006 | Add candidate x-ray schemas and validator integration. | L5 | schema-readiness refine result | ready | completed |

## Task Contract: TASK-XRAY-VIS-001

### Objective

Update the canonical `x-ray` README and skill contract so future execution knows the approved modes, lanes, renderer ladder, and evidence boundary.

### Inputs

- `INVOKE-DEFINE.md`
- `INVOKE-DESIGN.md`
- `IMPLEMENTATION-LAYERING.md`
- `arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/RESULT.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`

### Write Scope

- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`
- this work-pack status fields after validation
- `task-session/TASK-XRAY-VIS-001-RESULT.md`

### Required Behavior

- Keep `x-ray` status as seed.
- Add modes: `object`, `artifact`, `architecture`, `codebase`, `process`, `mixed`.
- Add canonical lanes: `surface`, `properties`, `components`, `internal_dependencies`, `external_dependencies`, `flow`, `lifecycle`, `risk_questions`, `visual_composition`.
- Add renderer ladder: static HTML/SVG first, optional Mermaid, optional CSS3D, optional Three.js/Kroki.
- Add evidence/inference boundary requirements.
- Add anti-patterns for decorative-only visuals and premature 3D.
- Do not implement the renderer or claim promotion.

### Done Criteria

- README and SKILL describe the lane-based visual x-ray model.
- README and SKILL mention internal and external dependencies.
- README and SKILL preserve seed and promotion boundaries.
- Validation commands pass.

### Validation Surface

```bash
rg -n "object|artifact|architecture|codebase|process|mixed" arcana/x-ray/SKILL.md arcana/x-ray/README.md
rg -n "surface|properties|components|internal_dependencies|external_dependencies|visual_composition" arcana/x-ray/SKILL.md arcana/x-ray/README.md
rg -n "renderer ladder|static HTML|SVG|Mermaid|Three\\.js|Kroki|evidence" arcana/x-ray/SKILL.md arcana/x-ray/README.md
git diff --check -- arcana/x-ray/SKILL.md arcana/x-ray/README.md arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray
```

## Task Contract: TASK-XRAY-VIS-005

### Objective

Add a documentation-first visual component library for `x-ray`, plus a user-extension template and result-contract nudge for adding custom shapes, charts, and patterns.

### Inputs

- `arcana/x-ray/development/refinement-runs/20260529T122108Z-component-library-nudge/RESULT.md`
- `arcana/x-ray/development/refinement-runs/20260529T122108Z-component-library-nudge/stages/06-design.md`
- `arcana/x-ray/development/refinement-runs/20260529T122108Z-component-library-nudge/stages/08-repair.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`

### Write Scope

- `arcana/x-ray/library/README.md`
- `arcana/x-ray/library/components.md`
- `arcana/x-ray/library/patterns.md`
- `arcana/x-ray/library/user-shapes-template.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`
- this work-pack status fields after validation
- `task-session/TASK-XRAY-VIS-005-RESULT.md`

### Required Behavior

- Add a small starter library only; do not build a renderer engine.
- Include shapes: node, boundary, layer panel, risk marker.
- Include connectors: arrow, branch, feedback loop.
- Include charts: timeline strip, risk matrix.
- Include patterns: process branch, dependency boundary, lifecycle stack, evidence/inference split.
- Add a user-shapes template that asks for lane served and evidence represented.
- Add a gentle user nudge to the x-ray output contract or process.
- Preserve seed status and evidence/inference boundaries.

### Validation Surface

```bash
test -f arcana/x-ray/library/README.md
test -f arcana/x-ray/library/components.md
test -f arcana/x-ray/library/patterns.md
test -f arcana/x-ray/library/user-shapes-template.md
rg -n "node|boundary|layer panel|risk marker|arrow|branch|feedback loop|timeline strip|risk matrix|process branch|evidence/inference|Add your own|custom shape" arcana/x-ray/library arcana/x-ray/SKILL.md arcana/x-ray/README.md
git diff --check -- arcana/x-ray/library arcana/x-ray/SKILL.md arcana/x-ray/README.md arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray
```

## Task Contract: TASK-XRAY-VIS-006

### Objective

Add candidate schemas for `x-ray` generated artifacts, starting with the lane model and then extending to visual components and patterns after the component library exists.

### Inputs

- `arcana/x-ray/development/refinement-runs/20260529T124546Z-schema-readiness/RESULT.md`
- `arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json`
- `arcana/x-ray/scripts/validate-xray-example.py`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/library/` after `SWU-XRAY-VIS-005`

### Write Scope

- `arcana/x-ray/schemas/`
- `arcana/x-ray/scripts/validate-xray-example.py`
- `arcana/x-ray/development/`
- this work-pack status fields after validation
- `task-session/TASK-XRAY-VIS-006A-RESULT.md`
- `task-session/TASK-XRAY-VIS-006B-RESULT.md`

### Required Behavior

- Keep schemas candidate/local until multiple examples prove stability.
- Add lane-model schema first using the repo's canonical `.schema.yml` format.
- Integrate lane-model schema into the existing Python validator before HTML-specific checks.
- Add invalid fixtures or a negative probe so schema validation is not only happy-path.
- Add component and pattern schemas only after `arcana/x-ray/library/` exists.
- Do not attempt to validate full HTML with JSON Schema.

### Validation Surface

```bash
test -f arcana/x-ray/schemas/xray-lane-model.schema.yml
python3 - <<'PY'
import pathlib, yaml
data = yaml.safe_load(pathlib.Path("arcana/x-ray/schemas/xray-lane-model.schema.yml").read_text())
assert data and data.get("schema"), "schema missing"
PY
python3 arcana/x-ray/scripts/validate-xray-example.py --lanes arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json --html arcana/x-ray/examples/visual-layered-order-ingestion.html
! python3 arcana/x-ray/scripts/validate-xray-example.py --lanes arcana/x-ray/development/fixtures/invalid-missing-lane.lanes.json --lanes-only
git diff --check -- arcana/x-ray/schemas arcana/x-ray/scripts arcana/x-ray/development
```

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
- Preserve all starter components and patterns from `TASK-XRAY-VIS-005`.
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

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Dependencies | Write Scope | Done Criteria | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-XRAY-VIS-001 | TASK-XRAY-VIS-001 | `INVOKE-DEFINE.md`, `INVOKE-DESIGN.md`, refine `RESULT.md` | none | `arcana/x-ray/SKILL.md`, `arcana/x-ray/README.md` | Contract revised and seed boundary preserved. | TASK-XRAY-VIS-001 validation surface | local-fallback | completed |
| SWU-XRAY-VIS-002 | TASK-XRAY-VIS-002 | revised README/SKILL | SWU-XRAY-VIS-001 | `arcana/x-ray/examples/` | Static lane and HTML example exists. | HTML parse plus file checks | local-fallback | completed |
| SWU-XRAY-VIS-003 | TASK-XRAY-VIS-003 | example package | SWU-XRAY-VIS-002 | `arcana/x-ray/development/`, optional `arcana/x-ray/scripts/` | Validation harness exists and passes. | validator run | local-fallback | completed |
| SWU-XRAY-VIS-004 | TASK-XRAY-VIS-004 | validation result | SWU-XRAY-VIS-003 | `arcana/x-ray/development/` | Adapter backlog and browser-validation requirements documented. | review checklist | local-fallback | completed |
| SWU-XRAY-VIS-005 | TASK-XRAY-VIS-005 | `arcana/x-ray/development/refinement-runs/20260529T122108Z-component-library-nudge/RESULT.md` | SWU-XRAY-VIS-004 | `arcana/x-ray/library/`, `arcana/x-ray/README.md`, `arcana/x-ray/SKILL.md` | Starter components, patterns, and user-shapes template exist; result contract nudges user extension without breaking evidence boundaries. | component library file checks and grep | local-fallback | completed |
| SWU-XRAY-VIS-005B | TASK-XRAY-VIS-005B | `arcana/x-ray/development/invoke-runs/20260529T135625Z-yaml-library-refresh/REFRESH-REPORT.md` | SWU-XRAY-VIS-005 | `arcana/x-ray/library/`, `arcana/x-ray/README.md`, `arcana/x-ray/SKILL.md` | Canonical YAML library exists and Markdown docs point to it. | YAML parse, library grep, diff check | local-fallback | completed |
| SWU-XRAY-VIS-006A | TASK-XRAY-VIS-006 | `arcana/x-ray/development/refinement-runs/20260529T124546Z-schema-readiness/RESULT.md` | SWU-XRAY-VIS-005B | `arcana/x-ray/schemas/`, `arcana/x-ray/scripts/validate-xray-example.py`, `arcana/x-ray/development/` | Candidate lane model schema exists and validator uses it before HTML-specific checks. | schema parse, validator run, invalid fixture probe | local-fallback | completed |
| SWU-XRAY-VIS-006B | TASK-XRAY-VIS-006 | component library docs and schema-readiness refine result | SWU-XRAY-VIS-006A | `arcana/x-ray/schemas/`, `arcana/x-ray/library/`, `arcana/x-ray/development/` | Candidate component and pattern schemas exist after the visual library shape is real. | schema parse and library shape checks | local-fallback | completed |

## Gate Checks

1. One SWU per Task Session unless write scopes are disjoint.
2. No promotion status changes in this work-pack.
3. No renderer implementation during SWU-XRAY-VIS-001.
4. No remote rendering dependency may become required.
5. Browser validation is required before any generated HTML artifact is claimed.

## Next Route

No ready SWUs remain in this visual revision work-pack. Next route is `sigil-development` or `experiment-harness` for live behavior evidence before promotion.

## Completion Evidence

| Task | Evidence |
| --- | --- |
| TASK-XRAY-VIS-001 | `task-session/TASK-XRAY-VIS-001-RESULT.md`; README/SKILL contract checks pass. |
| TASK-XRAY-VIS-002 | `task-session/TASK-XRAY-VIS-002-RESULT.md`; static source, lane JSON, HTML, parser check, and browser proof exist. |
| TASK-XRAY-VIS-003 | `task-session/TASK-XRAY-VIS-003-RESULT.md`; validator script exists, compiles, and passes against the example. |
| TASK-XRAY-VIS-004 | `task-session/TASK-XRAY-VIS-004-RESULT.md`; adapter backlog and browser-validation requirements are documented. |
| TASK-XRAY-VIS-005 | `task-session/TASK-XRAY-VIS-005-RESULT.md`; visual component library, pattern catalog, user-shapes template, and execution nudge are documented. |
| TASK-XRAY-VIS-005B | `task-session/TASK-XRAY-VIS-005B-RESULT.md`; YAML canonical library, Markdown companion docs, constitution-selected validation, and existing artifact constitution checks pass. |
| TASK-XRAY-VIS-006A | `task-session/TASK-XRAY-VIS-006A-RESULT.md`; candidate lane-model schema exists, validator loads it before HTML checks, and invalid fixture probe blocks as expected. |
| TASK-XRAY-VIS-006B | `task-session/TASK-XRAY-VIS-006B-RESULT.md`; candidate component and pattern schemas exist, library validator passes, and invalid component fixture blocks as expected. |
