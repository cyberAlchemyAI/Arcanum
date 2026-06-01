# UX Playwright Evidence Research Strategy

Status: draft research strategy.
Owner: dispatch-spec for route shape; future validator ownership must be decided before promotion.
Dispatch: `arcana/ux-evidence-validator/development/ux-playwright-evidence-research.dispatch.json`

## Objective

Create a governed research route for turning UX good-practice evidence into a Playwright-backed frontend validation and evidence harness.

The target is not a single "UX score." The target is a layered evidence system that can say:

- which findings are deterministic browser failures,
- which findings are accessibility or interaction failures,
- which findings are cognitive-load or attention-risk proxies,
- which findings need human/user-study evidence,
- which screenshots, traces, measurements, and reports prove the finished interface was inspected.

## Research Question

What academic, standards, neuroscience, cognitive-science, and market-practice references are strong enough to become validator rules, Playwright probes, or human-review prompts for finished frontend interfaces?

## Source Lanes

| Lane | Evidence To Gather | Validator Translation |
| --- | --- | --- |
| Accessibility and standards | WCAG, ARIA semantics, keyboard operation, focus order, contrast, target size, status/error semantics. | Hard Playwright/axe gates where automatable; reviewer gates where human judgment is required. |
| Cognitive science and human factors | Cognitive load, working memory, decision complexity, motor target acquisition, workload, visual hierarchy, attention limits. | Proxy checks such as step count, visible option count, target size, flow interruption count, landmark clarity, dense-region flags, and task-friction reports. |
| Neuroscience and perception | Visual search, salience, grouping, change blindness risk, motion sensitivity, preattentive cues. | Screenshot and DOM-derived risk checks for competing focal points, motion, hidden state changes, contrast hierarchy, and low-salience critical states. |
| Market-tested UX practice | Nielsen Norman heuristics, Baymard benchmark patterns, GOV.UK service manual practices, platform design-system guidance. | Heuristic checklist, domain-specific rule packs, reviewer prompts, and product-flow assertions. |
| Browser evidence and test practice | Playwright locator assertions, ARIA snapshots, screenshot comparisons, trace/video, viewport matrix, console/network inspection. | Evidence harness that stores screenshots, DOM snapshots, accessibility reports, traces, and path-cited result summaries. |

## Seed References

These are starting points for the research lane, not final authority. Links were checked on 2026-06-01.

| Reference | Source | Why It Matters | Translation Candidate |
| --- | --- | --- | --- |
| W3C WCAG 2.2 | <https://www.w3.org/TR/WCAG22/> | Stable accessibility conformance baseline for web interfaces. | Hard and review gates for contrast, focus, pointer gestures, target size, errors, labels, and keyboard behavior. |
| Playwright visual comparisons | <https://playwright.dev/docs/test-snapshots> | Browser-level visual evidence capture. | Screenshot diff, critical-region screenshots, visual regression threshold, trace evidence. |
| Playwright ARIA snapshots | <https://playwright.dev/docs/aria-snapshots> | Repeatable semantic accessibility-tree evidence. | ARIA snapshot assertions for primary regions, dialogs, forms, and navigation. |
| Deque axe-core | <https://github.com/dequelabs/axe-core> | Automated accessibility rule engine mapped to standards. | Required automated accessibility scan, with explicit note that automation is partial. |
| Nielsen Norman Group usability heuristics | <https://www.nngroup.com/articles/ten-usability-heuristics/> | Market-practitioner heuristic baseline for system status, match, control, consistency, error prevention, recognition, and recovery. | Human-review prompts and partial automation around feedback, navigation, labels, and error states. |
| Baymard Institute benchmark research | <https://baymard.com/research> | Domain-specific, tested ecommerce/product-flow UX patterns. | Optional domain packs for checkout, product discovery, forms, filtering, and search flows. |
| GOV.UK Service Manual | <https://www.gov.uk/service-manual/user-research> | Public-sector service design and user-research practice with strong usability-testing norms. | Evidence expectation for task-based user validation when Playwright proxies are insufficient. |
| Cognitive Load Theory | <https://doi.org/10.1016/0364-0213(88)90023-7> | Mechanism for overload risk from unnecessary working-memory burden. | Proxy flags for visible choice count, dense panels, multi-step memory dependency, and avoidable task switching. |
| Fitts' law and motor-control research | <https://doi.org/10.1037/h0055392> | Mechanism for target size and movement difficulty. | Target size, spacing, and pointer travel checks across desktop and mobile viewports. |
| Hick-Hyman choice reaction research | <https://doi.org/10.1080/17470215208416600> and <https://doi.org/10.1037/h0056940> | Mechanism for choice-set complexity. | Choice-count and branching-complexity warnings, especially at decision points. |
| Feature Integration Theory and visual-search work | <https://pubmed.ncbi.nlm.nih.gov/7351125/> | Mechanism for preattentive vs effortful search. | Screenshot/DOM review prompts for hierarchy, grouping, salience, and critical-state visibility. |
| NASA-TLX | <https://doi.org/10.1016/S0166-4115(08)62386-9> | Workload measurement method. | Optional human-study instrument when subjective workload must be measured. |

## Evidence Card Shape

Every imported reference should become a small evidence card before it becomes a validator rule:

```yaml
id: ux.ref.short-id
source_url: https://example.invalid/source
source_type: standard | academic | market_practice | design_system | tool_doc
claim: one narrow claim
evidence_strength: deterministic | empirical | expert_heuristic | market_benchmark | hypothesis
ui_scope: navigation | forms | layout | visual_hierarchy | interaction | content | accessibility | performance
automation_candidate: hard_gate | soft_flag | screenshot_review | human_study | not_automatable
playwright_probe: short description or null
human_review_prompt: short description or null
contraindications: where this claim should not be generalized
freshness_rule: fixed | check_latest | domain_specific
```

## Validator Taxonomy

The eventual Playwright harness should separate hard failures from weaker risk signals.

| Layer | Examples | Evidence Artifact |
| --- | --- | --- |
| L0 Smoke | Page loads, no fatal console errors, no broken required assets, primary route exists. | `smoke.json`, trace, console log. |
| L1 Accessibility | axe scan, keyboard navigation, focus visibility, role/name assertions, form labels and errors. | `accessibility.json`, ARIA snapshot, focus-order log. |
| L2 Layout Integrity | No horizontal overflow, no incoherent overlap, text fits controls, responsive breakpoints render. | Desktop/mobile screenshots, bounding-box measurements. |
| L3 Interaction Flow | Core user tasks complete through keyboard and pointer paths. | Flow trace, video, route assertions, task receipt. |
| L4 Cognitive/Attention Risk | Dense decision points, unclear hierarchy, hidden system status, excess simultaneous choices, poor progressive disclosure. | Risk report with screenshot regions and reviewer prompts. |
| L5 Domain Practice | Checkout, search, filtering, onboarding, dashboard scanning, or form-specific market rules. | Domain-pack report and cited reference cards. |
| L6 Human Evidence | Moderated usability notes, workload instruments, SUS/UMUX-lite if selected later. | Study protocol, task results, residue ledger. |

## Playwright Evidence Contract

A finished-interface test run should produce:

- run metadata: target URL, commit/ref, viewport matrix, browser, timestamp, scenario id,
- screenshots: full-page and clipped regions for critical states,
- trace/video where an interaction flow is tested,
- DOM and ARIA snapshots for semantically important regions,
- automated accessibility scan output,
- layout measurements for overflow, overlap, and text fitting,
- console/network failure summary,
- task-flow result receipts,
- reviewer-prompt report for non-automatable UX claims,
- residue ledger for findings that require design judgment or human testing.

## Hard Gates

Block the interface when:

- the primary scenario cannot load or complete,
- required interactive controls are unreachable by keyboard,
- focus is invisible or trapped incorrectly,
- required accessible names/roles are missing,
- automated accessibility scan reports serious or critical issues,
- content overlaps incoherently or creates horizontal overflow at required viewports,
- text is clipped in controls, cards, nav, or compact panels,
- required images/assets are missing,
- critical forms do not expose errors and recovery states,
- console/runtime errors break primary flows.

## Soft Flags

Flag the interface for review when:

- a decision point exposes too many simultaneous choices,
- a dense region has weak hierarchy or low contrast emphasis,
- instructions depend on memory from an earlier step,
- system status is hidden during loading, saving, or failure,
- destructive actions lack confirmation or recovery affordances,
- market-practice references apply only to a specific domain,
- a neuroscience or cognitive-science claim has no reliable automatable proxy.

## Calibration Plan

Before promoting any validator:

1. Build a fixture set with known-good and known-bad interfaces.
2. Include at least one responsive layout failure, one accessibility failure, one flow failure, one cognitive-load risk, and one false-positive trap.
3. Run the Playwright harness over the fixtures.
4. Record screenshots, traces, axe output, ARIA snapshots, and measurement JSON.
5. Tune rules until hard gates catch deterministic failures and soft flags remain explainable.
6. Keep unresolved subjective UX claims in a human-study lane.

## Authority Boundaries

- Dispatch Spec validates this research route, not the future UI validator itself.
- Playwright evidence can prove browser-observed behavior; it cannot prove subjective delight, trust, comprehension, or workload without human evidence.
- Academic and neuroscience claims must be translated into conservative UI proxies, not overconfident brain-based assertions.
- Market practices are domain-weighted and must not become universal rules without fixture and product-context proof.
- Execution evidence must not promote canonical Arcanum knowledge without owner review.

## Next Route

Use this strategy to run a `robot-talks` or task-session research pass that produces:

- `UX-EVIDENCE-REFERENCE-CARDS.yml`
- `UX-PLAYWRIGHT-VALIDATOR-SPEC.md`
- `UX-PLAYWRIGHT-FIXTURE-PLAN.md`
- a future implementation work-pack for the validator and tester.
