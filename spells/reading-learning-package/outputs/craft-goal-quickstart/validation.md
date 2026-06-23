# Validation Report — Craft + Goal Quickstart

- **Spell:** whisper · **Preset:** `learning_distill` · **Transport:** learning_package
- **Status:** pass (with one expected design-maturity flag)

## Composition checks (from the preset)

| Check | Result | Note |
| --- | --- | --- |
| One analogy carried end to end | pass | Single "expedition" analogy: logbook / autopilot / toll booth / conductor. |
| Every jargon term defined on first use | pass | ledger, fail-closed, frontier, control loop, agent runtime, gateway all defined inline. |
| Recipe is ordered and copy-pasteable | pass | §5 is 5 numbered plain-language steps. |
| Fail-closed / approval stated honestly | pass | §3 and §7 state it; no "fully autonomous" claim anywhere. |
| Controller framed as optional conductor | pass | §6 marks it the next step you grow into, not a dependency. |
| Source trace covers every mechanism claim | pass | See `source-trace.md`. |

## Gates (reading-learning-package contract)

| Gate | Result | Evidence |
| --- | --- | --- |
| Source gate | pass | Real source artifacts (craft, goal, integration-spec) cited in `source-trace.md`. |
| Preset gate | pass | `presets/learning_distill/preset-profile.yaml`, preview approved. |
| Whisper gate | pass | `text-intent-substrate.yaml` records all three SCU cores + source-use policy. |
| Trace gate | pass | Load-bearing sections map to source handles. |
| PDF gate | pass | `learning-package.pdf` rendered (6 pp) via pdfkit chrome-print. |
| Promotion gate | pass | Package states it is learning output, not source authority. |

## Flags / residue

- **flag (design maturity):** the controller-agent / OpenClaw section describes a
  *promotion-candidate* integration pattern, not a shipped one-click feature. The
  manuscript and `source-trace.md` both call this out explicitly. Honest framing,
  not a defect.
- **flag (named example):** "Hermes-class controller" is an illustrative example;
  no Hermes integration exists in-repo. Stated as a pattern.

## Self-containment verification (installable tool)

Empirically checked, not just asserted:

| Check | Result |
| --- | --- |
| `goal/runtime/goal_loop.py` imports | stdlib only (`argparse`, `json`, `datetime`, `pathlib`, `typing`) — no third-party, no Arcanum |
| `goal/validation/run-fixtures.py` third-party imports | exactly one: `jsonschema` |
| `craft/` Python files | 0 (pure model-operated skill) |
| Goal runtime + validation run from a bare foreign project | pass — prints `goal-fixtures-pass` |
| Installer (`install.sh`) from the extracted zip into a fresh project | pass — copies 2 skills, validation passes |
| Arcanum *path/import* dependencies in installed tree | 0 (only 2 prose lines naming the upstream "Library spell root" for provenance) |

Verdict: **self-contained**. Install = drop `tools/craft` + `tools/goal` into the
project's skills dir; `pip install jsonschema` only to run Goal's self-check.

## Next route

- Optional: run through `experiment-harness` if `learning_distill` should be
  promoted as a reusable preset across other towers.
- Optional: if the controller-agent pattern becomes real, refresh §6 from the
  finished `integration-spec` boundary discipline doc.
