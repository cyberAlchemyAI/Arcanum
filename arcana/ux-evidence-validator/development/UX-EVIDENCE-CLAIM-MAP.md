# UX Evidence Claim Map

Status: task-session research output.
Dispatch: `ux-playwright-evidence-research-20260601`.
Source cards: `arcana/ux-evidence-validator/development/UX-EVIDENCE-REFERENCE-CARDS.yml`.

## Purpose

This map translates UX references into validator-safe claim classes. The main rule is evidence honesty: Playwright can prove browser-observed behavior, accessibility-tree state, screenshots, layout measurements, console/network failures, and scripted interaction outcomes. It cannot directly prove subjective comprehension, workload, trust, delight, or attention without human evidence.

## Claim Classes

| Class | Meaning | Allowed Evidence | Promotion Rule |
| --- | --- | --- | --- |
| Hard gate | Deterministic browser, accessibility, interaction, or layout failure. | Playwright assertions, axe JSON, ARIA snapshots, screenshots, traces, DOM measurements. | May block only after fixture calibration catches known failures and avoids known false positives. |
| Soft flag | Risk signal grounded in a source but not deterministic enough to block. | Measurements, screenshots, counts, region annotations, reviewer prompts. | Must stay explainable and cite an evidence card. |
| Screenshot review | Visual or perception claim that needs human inspection of captured state. | Full-page screenshot, clipped region, DOM locator map, optional salience metric. | Cannot become a hard gate without calibrated fixtures and owner approval. |
| Human study | Claim that needs user observation, workload instrument, or moderated task evidence. | Task scripts, participant notes, workload instrument, completion/error/time logs. | Cannot be automated as pass/fail. |
| Not automatable | Good-practice claim with no reliable browser proxy in this scope. | Residue ledger and owner decision. | Record as residue or convert to a future human-review checklist. |

## Hard Gate Candidates

| Claim | Source Cards | Playwright Observation | Block When |
| --- | --- | --- | --- |
| Page and primary scenario load reliably. | `ux.pw.trace_viewer`, `ux.pw.assertions` | Navigation, console, network, trace, required assets. | Primary route fails, required asset fails, fatal console/runtime error prevents task. |
| Critical controls expose accessible names, roles, and states. | `ux.std.wcag22`, `ux.std.wai_aria12`, `ux.pw.aria_snapshots`, `ux.pw.locators` | Role locators, ARIA snapshots, axe output. | Required interactive element is unnamed, has wrong role, or cannot be located by user-facing contract. |
| Keyboard users can operate configured flows. | `ux.std.aria_apg`, `ux.std.wcag22` | Keyboard scripts, focus order log, visible focus screenshots. | Focus is trapped incorrectly, invisible, skips required control, or widget keyboard behavior is broken. |
| Form errors and recovery states are exposed. | `ux.std.wcag22`, `ux.market.nng_heuristics`, `ux.pw.assertions` | Error message locators, `aria-describedby`, focus, status region, screenshots. | Invalid state is submitted without exposed error, recovery, or focus guidance. |
| Layout fits required viewports. | `ux.pw.visual_comparisons`, `ux.cog.fitts_law` | Viewport matrix screenshots, bounding boxes, overflow checks, target-size checks. | Horizontal overflow, text clipping, incoherent overlap, or below-threshold critical target size appears in required viewport. |

## Soft Flag Candidates

| Risk | Source Cards | Proxy | Reason It Is Not A Hard Gate Yet |
| --- | --- | --- | --- |
| Excess decision density. | `ux.cog.hick_hyman_choice_complexity`, `ux.cog.cognitive_load_theory` | Count visible peer actions and branches in scenario-defined regions. | Some expert, search, and comparison workflows intentionally expose many options. |
| Cross-step memory burden. | `ux.cog.working_memory_capacity`, `ux.cog.cognitive_load_theory` | Detect hidden prior selections, missing summaries, and dependency on previous instructions. | DOM state only approximates memory burden and needs task context. |
| Low-salience critical state. | `ux.perception.feature_integration`, `ux.perception.saliency_model`, `ux.perception.visual_attention_review` | Screenshot region prominence, contrast, icon/text distinctiveness, nearby distractors. | Salience metrics do not prove actual attention allocation. |
| Subtle async state change. | `ux.perception.change_blindness`, `ux.market.nng_heuristics` | Assert visible loading/saving/success/error state and capture before/after screenshots. | Some subtle transitions are acceptable when the task outcome remains obvious. |
| Domain mismatch. | `ux.market.baymard_research`, `ux.market.uswds_accessibility`, `ux.market.carbon_accessibility` | Scenario domain metadata and component/state matrix. | Market and design-system patterns are not universal. |

## Screenshot Review Claims

Screenshot review is appropriate when the source claim concerns visual hierarchy, salience, grouping, information scent, visual search, or density. The tester should capture:

- full-page screenshots for each required viewport,
- clipped screenshots of critical regions,
- DOM locator overlays or region metadata,
- before/after screenshots for dynamic state changes,
- a reviewer prompt that cites the evidence card and names the proxy limit.

Screenshot review must not be expressed as "good UX score." It should produce findings like: `FLAG: primary submit action is less prominent than secondary promotional region in checkout_step_2 desktop`.

## Human Evidence Claims

Human evidence is required when the claim depends on subjective workload, comprehension, confidence, trust, perceived ease, or whether a representative user can complete a high-risk task under real conditions. Browser automation can prepare supporting evidence by recording task scripts, timing, errors, traces, and screenshots, but the finding remains human-study gated.

Recommended human-evidence residues:

- workload validation using `ux.cog.nasa_tlx`,
- task completion and confusion points using `ux.market.govuk_user_research`,
- expert heuristic review using `ux.market.nng_heuristics`,
- domain-specific review using `ux.market.baymard_research` only when the interface is ecommerce or product discovery.

## Proxy Limits

| Source Family | Safe Translation | Unsafe Translation |
| --- | --- | --- |
| WCAG and ARIA | Browser-observable hard gates plus manual review prompts. | Claiming complete accessibility from automated checks alone. |
| Cognitive load and working memory | Density, visible-context, step-count, and memory-dependency flags. | Claiming measured mental effort from DOM metrics. |
| Fitts and target acquisition | Target size, spacing, and input-modality measurements. | Applying one universal target-size threshold to every interface without product context. |
| Visual search and salience | Screenshot review, critical-state visibility, distractor flags. | Claiming to know where the user looked without eye tracking or user evidence. |
| Market heuristics and benchmarks | Domain packs and expert-review prompts. | Treating every market heuristic as universal release-blocking law. |
| Playwright docs | Evidence capture and deterministic assertions. | Treating passing tests as proof of subjective quality. |

## Validator Hand-Off

The future validator should expose findings with this shape:

```yaml
finding_id: ux.finding.example
class: hard_gate | soft_flag | screenshot_review | human_study | not_automatable
severity: block | high | medium | low | info
source_cards:
  - ux.std.wcag22
scenario_id: primary_checkout
viewport: mobile
evidence:
  - output/playwright/ux-validator/<run-id>/screenshots/primary_checkout-mobile.png
  - output/playwright/ux-validator/<run-id>/accessibility/primary_checkout-mobile.json
interpretation: "What failed or what risk was observed."
proxy_limit: "What the evidence cannot prove."
```

## Synthesis Decision

This research supports a Playwright validator architecture, but it does not yet approve implementation or promotion. The next approved route should either build the fixture corpus or turn this spec into an implementation work-pack.
