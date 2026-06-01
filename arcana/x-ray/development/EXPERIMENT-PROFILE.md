# x-ray Experiment Profile

## Identity

- Artifact: `arcana/x-ray`
- Artifact type: sigil
- Profile: `sigil-development`
- Lifecycle owner: Sigil Development
- Experiment owner: Experiment Harness
- Status: initialized

## Purpose

Validate `x-ray` as a reusable Arcana sigil by running realistic examples that exercise the lane model, visual library, schema-backed validation, HTML output shape, and insufficient-context blocking behavior.

## Required Branches

| Branch ID | Required Evidence | Prompt |
| --- | --- | --- |
| `XRAY-COMPONENT-001` | Component/object explanation with properties, components, dependencies, and evidence boundary. | `example-prompts/XRAY-COMPONENT-001.md` |
| `XRAY-PROCESS-001` | Process explanation with actors, steps, decisions, flow, transformations, and HTML-shaped result. | `example-prompts/XRAY-PROCESS-001.md` |
| `XRAY-ARCH-001` | Architecture or codebase explanation with internal and external dependencies. | `example-prompts/XRAY-ARCH-001.md` |
| `XRAY-BLOCK-001` | Blocked or flagged result for insufficient context, without invented structure. | `example-prompts/XRAY-BLOCK-001.md` |

## Validation Commands

```bash
python3 arcana/x-ray/scripts/validate-xray-example.py --lanes arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json --html arcana/x-ray/examples/visual-layered-order-ingestion.html
python3 arcana/x-ray/scripts/validate-xray-library.py
tools/validate-artifact-constitution.sh
```

## Promotion Boundary

Promotion remains blocked until:

- each required branch has a real user-facing output body,
- at least one output includes generated L0 HTML/SVG,
- the blocked/flagged example preserves missing-context questions,
- validation reports show lane, library, and HTML checks passing where applicable,
- Sigil Development reviews the run report and confirms no severe contract gaps.

## Output Storage

Experiment Harness should store:

- prompts in `development/example-prompts/`,
- user-facing outputs in `development/example-outputs/`,
- raw run bundles in `development/example-runs/`,
- reports in `development/runs/`.
