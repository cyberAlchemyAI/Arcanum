# x-ray Validation

## Seed Validation Summary

| Check | Result | Evidence |
| --- | --- | --- |
| Work-pack exists. | pass | `development/WORK-PACK.md` defines `TASK-XRAY-SIGIL-001`. |
| Refine seed exists. | pass | `development/REFINE-SEED.md` preserves the x-ray refinement output. |
| README exists. | pass | `README.md` defines purpose, boundary, inputs, outputs, and lifecycle owner. |
| SKILL exists. | pass | `SKILL.md` defines objective, applicability, process, quality bar, anti-patterns, and output contract. |
| Experiment seed exists. | pass | `development/EXPERIMENT-SEED.md` defines component, process, and architecture/plan branches. |
| Example stub exists. | pass | `examples/context-to-html-shape.md` defines an input/output-shape example. |
| Registry discoverability exists. | pass | `registry/SIGILS.md` and `arcana/README.md` list `x-ray` as a seed sigil. |

## Validation Commands

```bash
test -f arcana/x-ray/README.md
test -f arcana/x-ray/SKILL.md
test -f arcana/x-ray/development/VALIDATION.md
test -f arcana/x-ray/development/EXPERIMENT-SEED.md
test -d arcana/x-ray/examples
rg -n "x-ray|HTML|context|data flow|actors|relationships|sigil-development|experiment-harness" arcana/x-ray registry/SIGILS.md arcana/README.md
git diff --check -- arcana/x-ray registry/SIGILS.md arcana/README.md
```

## Promotion Status

Status: seed.

`x-ray` is not promotion-ready. Promotion requires live Experiment Harness runs and Sigil Development review.

Required live branches:

- component explanation,
- process explanation,
- architecture or plan explanation,
- insufficient-context block or flag.

## Visual Layered Example Validation

The visual layered revision added an L0 static HTML/SVG example and local validator:

```bash
python3 arcana/x-ray/scripts/validate-xray-example.py \
  --lanes arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json \
  --html arcana/x-ray/examples/visual-layered-order-ingestion.html
```

Expected result:

```text
XRAY_EXAMPLE_VALIDATION=pass
```

Browser proof for generated HTML artifacts should be recorded through a localhost run, Playwright snapshot, and screenshot. The first visual example proof is:

- snapshot: `output/playwright/xray-visual-layered-order-ingestion.snapshot.txt`
- screenshot: `output/playwright/xray-visual-layered-order-ingestion.png`

Optional adapters and their entry gates are documented in `development/VISUAL-ADAPTER-BACKLOG.md`.

## Schema And Library Validation

The visual revision now includes candidate schemas and YAML-backed visual library validation:

```bash
python3 arcana/x-ray/scripts/validate-xray-example.py \
  --lanes arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json \
  --html arcana/x-ray/examples/visual-layered-order-ingestion.html

python3 arcana/x-ray/scripts/validate-xray-library.py
```

Negative probes:

```bash
! python3 arcana/x-ray/scripts/validate-xray-example.py \
  --lanes arcana/x-ray/development/fixtures/invalid-missing-lane.lanes.json \
  --lanes-only

! python3 arcana/x-ray/scripts/validate-xray-library.py \
  --components arcana/x-ray/development/fixtures/invalid-component-library.yml \
  --components-only
```

## Sigil Development Readiness

Sigil Development readiness is tracked in `development/SIGIL-DEVELOPMENT-READINESS.md`.

Experiment Harness scaffold:

- `development/EXPERIMENT-PROFILE.md`
- `development/example-prompts/`
- `development/regimes/xray-promotion-regime.yml`

Current lifecycle state: implementation package complete; promotion remains blocked until live Experiment Harness evidence exists.
