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
| `surface_mode` | no | Planning context such as persuade, operate, read, or experience; never gate authority. |
| `design_authority` | no | Provenance map separating observed incumbent values from owner-confirmed normative contracts. |
| `content_profiles` | no | Named empty, short, typical, long, localized, bidirectional, numeric, and collection-size ranges. |
| `context_matrix` | no | Named viewport, orientation, pointer/hover, keyboard, touch, zoom, motion, contrast/theme, and connection contexts. |
| `state_contract` | no | Required loading, empty, error, success, recovery, permission, interruption, and persistence outcomes. |

## Scenario Shape

```yaml
scenario_id: primary_flow
target_url: "http://127.0.0.1:4173"
surface_mode: operate
design_authority:
  observed_incumbent: "design-audit.json"
  normative_contract: "owner-approved-ui-contract.yml"
domain_tags:
  - dashboard
viewports:
  - desktop
  - mobile
content_profiles:
  - typical
  - localized_long
context_profiles:
  - pointer_desktop
  - keyboard_desktop
  - touch_mobile
  - zoom_200
  - reduced_motion
state_contract:
  required:
    - loading
    - success
    - recoverable_error
    - refresh_persistence
entry:
  path: "/"
tasks:
  - id: complete_primary_action
    expectation_authority: product_contract
    steps:
      - action: click
        locator:
          role: button
          name: "Create"
      - action: assert_visible
        locator:
          role: status
          name: "Created"
  - id: recover_from_timeout
    expectation_authority: product_contract
    fault_profile: timeout_primary_request
    steps:
      - action: click
        locator:
          role: button
          name: "Retry"
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

## Planning Overlay Compilation

`spec` mode may compile an owner-supplied UI/UX plan into scenario variants. It
must not invent unsupported states, devices, thresholds, or expected outcomes.

1. Resolve each observed incumbent value and normative contract separately.
2. Expand declared content, context, state, and fault profiles into a bounded
   scenario matrix.
3. Attach `expectation_authority` to every asserted outcome.
4. Use external expert methods only to suggest missing coverage or reviewer
   prompts; record their pinned evidence-card IDs.
5. Preserve real-device, comprehension, trust, and other non-browser claims in
   the residue ledger.

Supported profile dimensions may include long and empty content, localization,
RTL/CJK/emoji, large numbers and collections, zoom, reduced motion,
contrast/theme, pointer/hover, keyboard, touch, orientation, offline/slow or
timeout faults, permission failures, repeated submission, reload/back
persistence, and no-JavaScript behavior. A profile is optional until a standard
or explicit product contract requires it.

## Output Contract

All runs write under:

`output/playwright/ux-validator/<run-id>/`

Required files:

| Path | Contents |
| --- | --- |
| `run-metadata.json` | Target URL, commit/ref if available, browser, viewport matrix, scenario IDs, validator version, timestamps. |
| `summary.md` | Human-readable result with blocked findings, soft flags, screenshots, traces, and residues. |
| `findings.json` | Structured findings with class, severity, expectation authority, source cards, evidence paths, and proxy limits. |
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
2. Its expected outcome is authorized by a standard, explicit product
   contract, or calibrated fixture contract. An external expert method alone is
   insufficient.
3. The browser observation is direct enough to prove the failure.
4. The evidence path exists in the run output.
5. Known-good and known-bad fixtures have calibrated the rule.
6. The finding message names the expectation authority, source card, and proxy limit.

## Soft Flag Policy

A soft flag must include:

- source card ID,
- risk statement,
- observed proxy,
- scenario and viewport,
- screenshot or measurement evidence,
- why it is not a hard gate,
- suggested reviewer question.

## Independent Review Protocol

When screenshot review and deterministic checks both apply, preserve their
provenance as two passes:

1. Record an unanchored visual/interaction review before revealing detector or
   automated findings to that reviewer.
2. Record deterministic browser, accessibility, layout, and interaction
   evidence separately.
3. Synthesize agreements and conflicts without inventing an aggregate score.

This protocol reduces anchoring; it does not require a particular external
detector, subagent, overlay, or runtime.

## Implementation Notes

- Prefer Playwright role and label locators for task flows.
- Keep screenshot baselines deterministic by controlling font loading, motion, clocks, seed data, and viewport.
- Capture traces for failed or evidence-required flows; avoid retaining sensitive data unnecessarily.
- Keep thresholds configurable by project profile.
- Treat source-card methods as declarative inputs; do not install external
  design runtimes, hooks, detectors, or root-file protocols to execute them.
- Make the first implementation fixture-driven. The validator is not ready until it can pass known-good fixtures and catch known-bad fixtures.

## Promotion Guardrail

This spec may become an implementation work-pack only after the operator chooses that route. Until then, it is research evidence under `arcana/ux-evidence-validator/development/`.
