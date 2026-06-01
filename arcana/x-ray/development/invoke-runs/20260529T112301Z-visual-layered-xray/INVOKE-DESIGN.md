# Invoke Design: Visual Layered x-ray

Status: pass
Mode: design
Date: 2026-05-29
Target: `arcana/x-ray`

## Request

Convert the define baseline into a governed sigil design that can update the canonical `x-ray` contract and prepare a static layered HTML proof.

## Canonical Sources Used

- `spells/invoke/README.md`
- `spells/invoke/design.md`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/INVOKE-DEFINE.md`
- `arcana/x-ray/development/refinement-runs/20260529T110749Z-visual-layered-xray/RESULT.md`

## Six Design Views

### 1. Context View

`x-ray` sits in Arcana as a context-explanation sigil. It consumes user-provided context or a local path and produces a reviewable HTML explanation artifact. It does not mutate the inspected target.

### 2. High-Level Structure View

```text
target input
  -> target resolver
  -> mode selector
  -> evidence boundary ledger
  -> lane dispatcher
  -> lane handles
  -> visual composition model
  -> static HTML/SVG artifact
```

### 3. Low-Level Components View

| Component | Responsibility |
| --- | --- |
| Target resolver | Resolve text or path input and record source boundaries. |
| Mode selector | Choose `object`, `artifact`, `architecture`, `codebase`, `process`, or `mixed`. |
| Lane dispatcher | Select required lanes for the mode and record omitted-lane reasons. |
| Lane analyzers | Produce source-backed and inferred handles for each lane. |
| Visual composer | Convert lane handles into layer definitions. |
| HTML renderer | Emit a single local HTML artifact with inline SVG controls. |
| Validator | Check required lanes, evidence boundary fields, dependency sections, and HTML parse. |

### 4. Workflow Process View

1. Resolve the target and ask only for blocker clarification.
2. Select mode and lane set.
3. Produce lane handles with evidence/inference labels.
4. Compose the layer stack and dependency views.
5. Emit the HTML artifact.
6. Validate structure and report gaps.

### 5. Decision Flow View

- If target type is unclear and changes lane selection, ask one clarification question.
- If target evidence is insufficient, return `flag` or `block` with missing context.
- If architecture/codebase context is large, require a bounded path or scope.
- If visual adapter support is unavailable, fall back to L0 static HTML/SVG.
- If output would expose sensitive context through a remote renderer, block remote use.

### 6. Dependency Interface View

| Interface | Direction | Notes |
| --- | --- | --- |
| `dispatch-spec` techniques | input | `x_ray`, `component_descriptor`, and `entity_component_reference` govern lane-shaped handoffs. |
| Static HTML/SVG | output | Required L0 renderer. |
| Mermaid | optional output adapter | For flow, dependency, and architecture diagrams after conservative syntax validation. |
| CSS3D/Three.js | optional output adapter | For later layer-depth affordances only. |
| Kroki | optional external adapter | Only when privacy/network policy allows remote or self-managed rendering. |

## Design Decisions

- First Task Session should update the canonical README/SKILL contract only.
- Example HTML and validators should be a separate SWU so the contract can be reviewed before renderer behavior is claimed.
- Keep registry status as seed.

## Risks

- Visual ambition can obscure the explanatory task.
- Codebase mode can sprawl without explicit scope.
- Mermaid syntax can fail if generated too freely.
- Optional 3D can create validation burden before L0 is useful.

## Implementation Layering Seed

Use `IMPLEMENTATION-LAYERING.md` in this run folder.

## Next Route

`invoke plan`

