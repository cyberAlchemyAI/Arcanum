# Sigil Development Readiness: x-ray

## Summary

- Sigil: `x-ray`
- Tier: arcana
- Mode: update
- Status: seed
- Readiness: implementation package complete; promotion blocked on live experiment evidence
- Review date: 2026-05-29

## Observer Pass

Observer pass: local fallback.

Signals reviewed:

- current `README.md` and `SKILL.md`,
- visual revision work-pack,
- task-session results through `SWU-XRAY-VIS-006B`,
- YAML visual library,
- candidate schemas,
- validators,
- experiment seed.

## Findings

| Area | Status | Evidence |
| --- | --- | --- |
| Contract | pass | `SKILL.md` has modes, lanes, renderer ladder, output contract, quality bar, anti-patterns, observability, and promotion gate. |
| README | pass | `README.md` explains seed status, output model, visual library, and ownership model. |
| Visual library | pass | YAML-backed component, pattern, and user-shape-template records exist. |
| Validation | pass | `validate-xray-example.py` and `validate-xray-library.py` validate lane and library structures. |
| Negative probes | pass | Invalid lane and component fixtures block as expected. |
| Experiment harness | flag | Profile and prompts now exist, but live runs are not executed. |
| Promotion readiness | block | Required live examples and insufficient-context run evidence are missing. |

## Lifecycle Decision

Iteration decision: targeted update complete.

No core contract change is needed now. The next lifecycle step is experiment evidence, not more contract rewriting.

## Experiment Harness State

Initialized:

- `development/EXPERIMENT-PROFILE.md`
- `development/example-prompts/XRAY-COMPONENT-001.md`
- `development/example-prompts/XRAY-PROCESS-001.md`
- `development/example-prompts/XRAY-ARCH-001.md`
- `development/example-prompts/XRAY-BLOCK-001.md`
- `development/regimes/xray-promotion-regime.yml`

Pending:

- live output bodies,
- run reports,
- observation from experiment reports,
- Sigil Development review after reports exist.

## Validation Commands

```bash
python3 arcana/x-ray/scripts/validate-xray-example.py --lanes arcana/x-ray/examples/visual-layered-order-ingestion.lanes.json --html arcana/x-ray/examples/visual-layered-order-ingestion.html
python3 arcana/x-ray/scripts/validate-xray-library.py
tools/validate-artifact-constitution.sh
git diff --check -- arcana/x-ray
```

## Promotion Boundary

Do not promote `x-ray` until Experiment Harness produces evidence for:

- one object/component example,
- one process example,
- one architecture or codebase example,
- one generated L0 HTML/SVG output body,
- one insufficient-context block or flag,
- validation passing against lane/library/HTML checks.

## Next Route

Use Experiment Harness:

```bash
experiment-harness run arcana/x-ray XRAY-COMPONENT-001 --type sigil --profile sigil-development
```

Then continue through the remaining prompts, report, observe, and return to Sigil Development for review.
