# UX Evidence Validator Experiment Profile

## Identity

- Artifact: `arcana/ux-evidence-validator`
- Artifact type: sigil
- Profile: `sigil-development`
- Lifecycle owner: Sigil Development
- Experiment owner: Experiment Harness
- Status: initialized

## Purpose

Validate `ux-evidence-validator` as a reusable Arcana sigil by proving it can preserve evidence honesty, generate validator-safe specs, define and run fixtures, and separate deterministic browser failures from cognitive, market, screenshot-review, and human-study residues.

## Required Branches

| Branch ID | Required Evidence | Prompt |
| --- | --- | --- |
| `UEV-FIXTURE-001` | Fixture corpus plan or implementation route from the existing fixture plan. | `example-prompts/UEV-FIXTURE-001.md` |
| `UEV-SPEC-001` | Project-specific validator spec from a bounded frontend scenario. | `example-prompts/UEV-SPEC-001.md` |
| `UEV-BLOCK-001` | Blocked or flagged result when the request asks for subjective UX proof without human evidence. | `example-prompts/UEV-BLOCK-001.md` |

## Validation Commands

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
path = Path("arcana/ux-evidence-validator/development/UX-EVIDENCE-REFERENCE-CARDS.yml")
data = yaml.safe_load(path.read_text())
assert len(data["cards"]) >= 25
print(f"validated {len(data['cards'])} evidence cards")
PY
python3 -m json.tool arcana/ux-evidence-validator/development/ux-playwright-evidence-research.dispatch.json
formulae/dispatch-spec/scripts/validate-dispatch.py arcana/ux-evidence-validator/development/ux-playwright-evidence-research.dispatch.json --json
tools/validate-artifact-constitution.sh
```

## Promotion Boundary

Promotion remains blocked until:

- each required branch has a real user-facing output body,
- fixtures exist and can be run,
- the Playwright evidence output root is populated by at least one fixture calibration run,
- hard gates catch deterministic failures,
- L4/L5 soft flags remain explainable and non-blocking unless independently justified,
- Sigil Development reviews the latest Experiment Harness report.

## Output Storage

Experiment Harness should store:

- prompts in `development/example-prompts/`,
- user-facing outputs in `development/example-outputs/`,
- raw run bundles in `development/example-runs/`,
- reports in `development/runs/`.
