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

## Stress And Adaptation Fixture Matrix

These fixtures expand scenario coverage. A fixture may calibrate a hard gate
only when its expected outcome is independently authorized by a standard,
explicit product contract, or calibrated fixture contract. The external method
cards identify useful coverage but are never sole gate authority.

| Fixture ID | Purpose | Expected Result | Evidence Required |
| --- | --- | --- | --- |
| `bad.localized_long_overflow` | Long localized copy clips or obscures a required control. | BLOCK L2 when the localized profile is required. | Locale/profile metadata, bounding boxes, full and clipped screenshots. |
| `bad.rtl_order_mismatch` | Visual or focus order contradicts the declared logical task order in RTL. | BLOCK L1/L3 when the RTL profile is required. | Direction metadata, DOM/focus log, ARIA snapshot, screenshots. |
| `bad.zoom_200_critical_clipping` | Required content or controls become clipped, overlapping, or unreachable at the configured zoom profile. | BLOCK L1/L2 with applicable standards authority. | Zoom metadata, measurements, keyboard path, screenshots. |
| `bad.reduced_motion_feedback_loss` | Reduced motion removes task-critical loading, success, error, or state feedback. | BLOCK L3 only when the same semantic outcome is required and calibrated. | Paired motion-profile screenshots, status assertions, trace. |
| `bad.hover_only_control` | A required action is exposed only through hover and is unavailable in declared keyboard or touch contexts. | BLOCK L1/L3. | Pointer/keyboard/touch traces, role/state evidence, screenshots. |
| `bad.offline_recovery_missing` | A declared offline-tolerant task has no observable failure state or recovery action. | BLOCK L0/L3 only for a declared recovery contract. | Fault-injection record, status/recovery assertions, trace. |
| `bad.timeout_recovery_missing` | A declared request timeout leaves the task stuck or silently failed. | BLOCK L0/L3 only for a declared recovery contract. | Timeout fixture, console/network log, status assertion, trace. |
| `bad.permission_recovery_missing` | A denied permission produces no declared fallback or next action. | BLOCK L3 only for a declared permission contract. | Permission profile, state assertions, screenshots. |
| `bad.double_submission` | Repeated activation creates duplicate irreversible or conflicting outcomes. | BLOCK L3 when idempotence or submission locking is a declared contract. | Network/action log, task trace, outcome count. |
| `bad.refresh_persistence_loss` | Refresh or back navigation loses state that the product contract says must persist. | BLOCK L3 only for a declared persistence contract. | Before/after state evidence, storage metadata, trace. |
| `bad.theme_state_loss` | A required state distinction disappears in a declared contrast or theme profile. | BLOCK L1/L3 only with applicable authority and calibration. | Theme/profile metadata, accessibility output, paired screenshots. |
| `trap.false_positive_unconventional_visual_language` | Visually unconventional but accessible, operable, and contract-complete UI. | PASS or PASS_WITH_FLAGS low. | Proof that aesthetic preferences and detector labels cannot block. |

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
10. Record `expectation_authority` for every expected block and reject any
    hard-gate fixture whose only authority is `external_noncanonical`.

## Minimum Viewport Matrix

| Name | Width | Height | Notes |
| --- | --- | --- | --- |
| `mobile` | 390 | 844 | Touch-size and clipping evidence. |
| `tablet` | 768 | 1024 | Navigation and two-column behavior. |
| `desktop` | 1440 | 900 | Dashboard and data-dense behavior. |

Viewport sizes are repeatable fixture inputs, not universal breakpoints or
product requirements. Scenario profiles may add orientation, pointer/hover,
keyboard, touch, zoom, reduced-motion, contrast/theme, and connection variants.

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
- Include one visually unconventional route to prove aesthetic-method findings
  remain advisory when deterministic contracts pass.
- Keep fault injection deterministic and local; do not make external network
  availability part of fixture truth.
- Use local images or generated fixtures only when visual hierarchy or asset loading is part of the rule.

## Next Approved Route

The next task can be either:

- fixture implementation and calibration, or
- validator implementation work-pack creation.

The fixture route should come first if the team wants calibrated hard gates before writing reusable validator code.
