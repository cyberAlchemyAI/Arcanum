# UX Playwright Fixture Plan

Status: task-session research output.
Dispatch: `ux-playwright-evidence-research-20260601`.
Validator spec: `arcana/ux-evidence-validator/development/UX-PLAYWRIGHT-VALIDATOR-SPEC.md`.

## Objective

Design a calibration corpus for a future Playwright UX evidence validator. The corpus should prove that hard gates catch deterministic failures, soft flags remain explainable, and subjective UX claims do not become fake automation.

## Fixture Root

Recommended future root:

`fixtures/ux-playwright-validator/`

Recommended output root:

`output/playwright/ux-validator/<run-id>/`

No fixture implementation is approved by this research task-session.

## Baseline Fixture Matrix

| Fixture ID | Purpose | Expected Result | Evidence Required |
| --- | --- | --- | --- |
| `good.dashboard_basic` | Known-good responsive dashboard with accessible navigation, form, status, and primary action. | PASS | Desktop/mobile screenshots, axe JSON, ARIA snapshots, flow trace, measurements. |
| `bad.accessible_name_missing` | Button or input lacks accessible name while visually appearing usable. | BLOCK L1 | Role locator failure, axe result, ARIA snapshot, screenshot. |
| `bad.keyboard_trap_dialog` | Modal or menu traps focus or cannot be dismissed by keyboard. | BLOCK L1/L3 | Keyboard trace, focus log, dialog ARIA snapshot, screenshot. |
| `bad.text_clipping_mobile` | Compact mobile viewport clips button text or navigation labels. | BLOCK L2 | Mobile screenshot, bounding-box measurement, clipping finding. |
| `bad.horizontal_overflow` | Layout creates horizontal scroll at required mobile width. | BLOCK L2 | Viewport measurement JSON and full-page screenshot. |
| `bad.overlap_critical_region` | Primary action overlaps status or content in a critical region. | BLOCK L2 | Overlap measurement and clipped screenshot. |
| `bad.invisible_async_status` | Save action changes state but gives no visible loading, success, or error feedback. | BLOCK L3 or FLAG L4 depending scenario | Before/after screenshot, status locator failure, task trace. |
| `bad.choice_density` | Decision panel exposes many ungrouped peer actions and weak hierarchy. | PASS_WITH_FLAGS L4 | Choice count, density measurement, screenshot review prompt. |
| `bad.memory_dependency` | Multi-step flow hides prior selections needed to decide the next step. | PASS_WITH_FLAGS L4 | Step screenshots, missing-summary finding, reviewer prompt. |
| `bad.low_salience_error` | Error state is present but visually buried among distractors. | PASS_WITH_FLAGS L4 | Error locator, clipped screenshot, salience or contrast proxy. |
| `domain.ecommerce_checkout_missing_recovery` | Ecommerce checkout form lacks recovery help after payment or address error. | BLOCK L1/L3 and FLAG L5 | Domain metadata, error assertions, screenshots, trace. |
| `trap.false_positive_dense_expert_tool` | Dense expert interface that is intentionally scan-heavy but grouped and keyboard-operable. | PASS or PASS_WITH_FLAGS low | Proof that L4 density findings are suppressible with scenario metadata and reviewer notes. |

## Calibration Protocol

1. Implement fixture pages as small, deterministic HTML or app routes.
2. Freeze data, fonts, animations, time, and viewport matrix.
3. Run the future validator against all fixtures.
4. Confirm every deterministic bad fixture blocks at the expected layer.
5. Confirm every soft fixture produces a cited, explainable flag rather than a block.
6. Confirm the false-positive trap does not fail release thresholds.
7. Store evidence under `output/playwright/ux-validator/calibration-<date>/`.
8. Tune thresholds only when a finding has a clear source card and fixture result.
9. Record unresolved ambiguity in `residue-ledger.yml`.

## Minimum Viewport Matrix

| Name | Width | Height | Notes |
| --- | --- | --- | --- |
| `mobile` | 390 | 844 | Touch-size and clipping evidence. |
| `tablet` | 768 | 1024 | Navigation and two-column behavior. |
| `desktop` | 1440 | 900 | Dashboard and data-dense behavior. |

## Required Evidence Per Fixture

Each fixture run should write:

- `run-metadata.json`,
- `summary.md`,
- `findings.json`,
- `console-network.json`,
- `accessibility/<fixture>-<viewport>.json`,
- `aria/<fixture>-<viewport>.yml`,
- `screenshots/<fixture>-<viewport>-full.png`,
- `screenshots/<fixture>-<viewport>-critical-<region>.png`,
- `measurements/<fixture>-<viewport>.json`,
- `traces/<fixture>.zip` when the fixture includes interaction,
- `residue-ledger.yml` when a finding is subjective, domain-specific, or ambiguous.

## Rule Promotion Threshold

| Rule Type | Promotion Requirement |
| --- | --- |
| L0 smoke | Good fixture loads and a broken route fixture blocks. |
| L1 accessibility | Known failures block; good fixture has no serious/critical automated findings; keyboard scripts pass. |
| L2 layout | Known overflow, clipping, and overlap fixtures block; good fixture passes all required viewports. |
| L3 flow | Known broken flow blocks; good fixture completes by keyboard and pointer when configured. |
| L4 cognitive/attention | Bad fixtures produce explainable flags; false-positive trap remains non-blocking. |
| L5 domain | Rule runs only when matching `domain_tags` are present. |
| L6 human evidence | Generates residues and study prompts; never blocks without an approved human-evidence requirement. |

## Fixture Implementation Notes

- Keep fixture pages visually plain but realistic enough to exercise actual DOM, CSS, and accessibility behavior.
- Include one route with custom widgets so ARIA and keyboard behavior can be tested.
- Include one route with dynamic async state so change visibility can be tested.
- Include one high-density route to calibrate soft flags without punishing expert workflows.
- Use local images or generated fixtures only when visual hierarchy or asset loading is part of the rule.

## Next Approved Route

The next task can be either:

- fixture implementation and calibration, or
- validator implementation work-pack creation.

The fixture route should come first if the team wants calibrated hard gates before writing reusable validator code.
