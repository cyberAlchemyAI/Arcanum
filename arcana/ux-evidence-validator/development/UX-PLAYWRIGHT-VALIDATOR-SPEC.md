# UX Playwright Validator Spec

Status: task-session research output.
Dispatch: `ux-playwright-evidence-research-20260601`.
Inputs: `UX-EVIDENCE-REFERENCE-CARDS.yml` and `UX-EVIDENCE-CLAIM-MAP.md`.

## Objective

Define a Playwright-backed evidence harness for finished frontend interfaces. The harness should produce structured proof of what the browser observed, separate deterministic failures from softer UX risk signals, and preserve residues that require expert or human-study review.

This spec defines the validator contract, not its implementation.

## Non-Goals

- Do not produce a single universal UX score.
- Do not claim subjective quality from automated tests.
- Do not promote cognitive, neuroscience, or market claims into hard gates without fixture calibration.
- Do not replace manual accessibility review or user research.

## Inputs

| Input | Required | Description |
| --- | --- | --- |
| `target_url` | yes | Local or deployed URL to inspect. |
| `scenario_file` | yes | YAML or JSON file defining routes, viewports, tasks, selectors, states, and source-card overlays. |
| `run_id` | yes | Stable ID for evidence paths. |
| `browser_matrix` | yes | Browsers and devices to run. Minimum: Chromium desktop and mobile emulation. |
| `viewport_matrix` | yes | Named viewport sizes and device scale factor. |
| `source_cards` | yes | Path to `UX-EVIDENCE-REFERENCE-CARDS.yml` or promoted card registry. |
| `output_root` | yes | Default: `output/playwright/ux-validator/<run-id>/`. |
| `threshold_profile` | yes | Release, review, exploratory, or fixture-calibration thresholds. |

## Scenario Shape

```yaml
scenario_id: primary_flow
target_url: "http://127.0.0.1:4173"
domain_tags:
  - dashboard
viewports:
  - desktop
  - mobile
entry:
  path: "/"
tasks:
  - id: complete_primary_action
    steps:
      - action: click
        locator:
          role: button
          name: "Create"
      - action: assert_visible
        locator:
          role: status
          name: "Created"
critical_regions:
  - id: main_navigation
    locator:
      role: navigation
  - id: primary_form
    locator:
      role: form
source_card_overlays:
  - ux.std.wcag22
  - ux.pw.aria_snapshots
  - ux.cog.cognitive_load_theory
```

## Output Contract

All runs write under:

`output/playwright/ux-validator/<run-id>/`

Required files:

| Path | Contents |
| --- | --- |
| `run-metadata.json` | Target URL, commit/ref if available, browser, viewport matrix, scenario IDs, validator version, timestamps. |
| `summary.md` | Human-readable result with blocked findings, soft flags, screenshots, traces, and residues. |
| `findings.json` | Structured findings with class, severity, source cards, evidence paths, and proxy limits. |
| `console-network.json` | Console errors, failed requests, response failures, and ignored-noise rules. |
| `accessibility/*.json` | axe output or equivalent structured accessibility results per scenario and viewport. |
| `aria/*.yml` | ARIA snapshots for configured regions and critical states. |
| `screenshots/*.png` | Full-page and clipped screenshots for baseline, states, failures, and soft-flag regions. |
| `measurements/*.json` | Bounding boxes, overflow, clipping, target size, density, and overlap measurements. |
| `traces/*.zip` | Playwright traces for failed or evidence-required flows. |
| `videos/*` | Optional videos for flows where temporal evidence matters. |
| `residue-ledger.yml` | Human-review, user-study, domain-pack, and calibration residues. |

## Status Model

| Status | Meaning |
| --- | --- |
| PASS | No blocking findings and no unreviewed high-risk soft flags under the selected profile. |
| PASS_WITH_FLAGS | Deterministic gates pass, but reviewable UX risks remain. |
| BLOCK | One or more hard gates failed or required evidence was not produced. |
| INCONCLUSIVE | The run could not gather enough evidence because configuration, environment, or fixture assumptions failed. |

## Validator Layers

### L0 Smoke

Purpose: prove the scenario is inspectable.

Checks:

- target URL responds,
- primary route loads,
- required assets load,
- no fatal console/runtime errors in the scenario,
- trace is available when a flow fails.

Evidence: `run-metadata.json`, `console-network.json`, trace, baseline screenshot.

Block when: the page cannot load, the scenario cannot reach its first stable state, or runtime errors prevent primary work.

### L1 Accessibility

Purpose: prove baseline accessibility and semantic contracts.

Checks:

- automated axe scan,
- role/name/state assertions for critical controls,
- ARIA snapshots for landmarks, forms, dialogs, menus, tabs, tables, and custom widgets,
- keyboard path and visible focus,
- form label, hint, error, and recovery state evidence.

Evidence: `accessibility/*.json`, `aria/*.yml`, focus screenshots, task trace.

Block when: serious or critical automated findings remain unresolved, critical controls are unnamed, keyboard access fails, or required error recovery is not exposed.

### L2 Layout Integrity

Purpose: prove the UI physically fits and remains usable across required viewports.

Checks:

- no horizontal overflow on required pages,
- no incoherent overlap in configured critical regions,
- text is not clipped inside controls, cards, nav, compact panels, or status regions,
- target sizes and spacing satisfy the selected threshold profile,
- responsive screenshots exist for each viewport.

Evidence: full-page screenshots, clipped region screenshots, `measurements/*.json`, visual comparison output when baselines exist.

Block when: content overlaps incoherently, horizontal overflow appears, primary text is clipped, or critical target sizes fail release thresholds.

### L3 Interaction Flow

Purpose: prove primary tasks work through user-facing contracts.

Checks:

- flows are driven by role, label, text, test id, or approved scoped locators,
- each step asserts visible or semantic outcomes,
- async transitions expose loading, saving, success, and failure states,
- undo, cancel, recovery, and destructive-action paths are tested when configured.

Evidence: task trace, screenshots at decision points, `findings.json`, assertions.

Block when: primary tasks cannot complete, user-facing locators fail, or critical state transitions are invisible.

### L4 Cognitive And Attention Risk

Purpose: flag risk proxies that need review.

Checks:

- visible choice count in decision regions,
- dense instruction and control clusters,
- missing persistent summaries in multi-step flows,
- low-salience errors, warnings, selected states, or primary actions,
- competing visual hierarchy around critical regions,
- subtle state changes without clear feedback.

Evidence: screenshots, clipped regions, density measurements, choice counts, reviewer prompts, source cards.

Default status: soft flag or screenshot review. Promote to hard gate only after fixture calibration and owner review.

### L5 Domain Practice

Purpose: apply domain-specific market or design-system rule packs only when declared.

Checks:

- ecommerce checkout, search, product detail, filtering, or form patterns when `domain_tags` match,
- service-design task evidence when service scenarios are declared,
- component state matrices when a design system is declared.

Evidence: domain-pack report, scenario metadata, screenshots, source-card citations.

Default status: soft flag. Block only for deterministic failures already covered by L1-L3.

### L6 Human Evidence

Purpose: preserve claims that browser automation cannot prove.

Checks:

- human-review prompts are generated for subjective claims,
- task scripts and evidence packs are ready for research,
- workload or usability-study residues are explicit.

Evidence: `residue-ledger.yml`, study protocol links, task evidence pack.

Default status: not automatable or human study.

## Hard Gate Policy

A finding may block only when:

1. The claim is deterministic or standards-backed.
2. The browser observation is direct enough to prove the failure.
3. The evidence path exists in the run output.
4. Known-good and known-bad fixtures have calibrated the rule.
5. The finding message names the source card and proxy limit.

## Soft Flag Policy

A soft flag must include:

- source card ID,
- risk statement,
- observed proxy,
- scenario and viewport,
- screenshot or measurement evidence,
- why it is not a hard gate,
- suggested reviewer question.

## Implementation Notes

- Prefer Playwright role and label locators for task flows.
- Keep screenshot baselines deterministic by controlling font loading, motion, clocks, seed data, and viewport.
- Capture traces for failed or evidence-required flows; avoid retaining sensitive data unnecessarily.
- Keep thresholds configurable by project profile.
- Make the first implementation fixture-driven. The validator is not ready until it can pass known-good fixtures and catch known-bad fixtures.

## Promotion Guardrail

This spec may become an implementation work-pack only after the operator chooses that route. Until then, it is research evidence under `arcana/ux-evidence-validator/development/`.
