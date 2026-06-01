---
name: ux-evidence-validator
description: "Use when: translating UX research, accessibility standards, market practice, and Playwright browser evidence into validator-safe checks, fixture plans, or evidence reports for finished frontend interfaces."
argument-hint: "<target-url-or-artifact> [--mode research|spec|fixture-plan|calibrate|validate-interface|report] [--scenario <path>] [--output <path>]"
tier: arcana
domain: frontend-ux-evidence
version: 0.1.0-seed
origin: created from the UX Playwright evidence research task-session on 2026-06-01
allowed-tools: Read, Write, Glob, Grep, Bash, Task
---

# Sigil: UX Evidence Validator

<objective>
Turn UX evidence into a layered, Playwright-ready validation contract that proves browser-observed frontend behavior while preserving cognitive, perception, market, and subjective claims as calibrated flags or human-review residues.
</objective>

<logic-type>
Arcana: evidence-governed frontend validation and promotion boundary management.
</logic-type>

<status>
Seed. The research artifacts and validator contract exist, but executable Playwright harness code and calibrated fixture evidence are not yet implemented.
</status>

<modes>
| Mode | Use When | Output |
| --- | --- | --- |
| `research` | Source references or UX claims need normalization before validator design. | Evidence cards and claim map. |
| `spec` | A project needs a Playwright evidence contract before implementation. | Validator spec and scenario shape. |
| `fixture-plan` | The validator needs known-good, known-bad, and false-positive fixtures. | Fixture corpus plan. |
| `calibrate` | Fixture pages and harness exist and need rule calibration. | Calibration report and threshold recommendations. |
| `validate-interface` | A runnable frontend should be tested once the harness exists. | Evidence report under `output/playwright/ux-validator/<run-id>/`. |
| `report` | Existing evidence should be summarized for review or promotion. | Findings summary and residue ledger. |
</modes>

<applicability>
Use this sigil when:

- a finished frontend needs browser evidence rather than prose-only review,
- UX references need to become validator-safe claims,
- accessibility, cognitive science, perception research, market heuristics, and Playwright evidence must be kept in separate authority lanes,
- hard gates need fixture calibration before promotion,
- screenshot review and human-study residues must be explicit,
- a future implementation should produce screenshots, traces, ARIA snapshots, accessibility output, DOM measurements, findings JSON, and a residue ledger.
</applicability>

<non-applicability>
Do not use this sigil when:

- the user only wants a quick subjective design critique,
- no frontend route, HTML artifact, screenshot, or scenario exists to inspect,
- the task is pure WCAG auditing with no UX evidence synthesis,
- a human usability study is required but browser evidence is irrelevant,
- the request would collapse subjective quality into a deterministic score.
</non-applicability>

<inputs>
Expected inputs, if available:

- target URL, local route, HTML artifact, or interface screenshot set,
- scenario file or user-task description,
- viewport and browser matrix,
- product domain tags such as dashboard, ecommerce, authoring, service, marketing, game, or data tool,
- source-card set or research artifact path,
- fixture corpus path when calibrating,
- desired output root, defaulting to `output/playwright/ux-validator/<run-id>/`.
</inputs>

<process>
1. Resolve mode. If no mode is provided, infer the smallest mode that fits the request and state the inference.
2. Identify the evidence boundary: source-backed standards, browser-observable behavior, proxy claims, domain heuristics, and subjective/human-study claims.
3. Load or create evidence cards before creating rule candidates.
4. Map claims into `hard_gate`, `soft_flag`, `screenshot_review`, `human_study`, or `not_automatable`.
5. Refuse to promote cognitive, neuroscience, or market claims directly into hard gates without a conservative UI proxy and fixture evidence.
6. For `spec`, produce or update the L0-L6 validator contract and scenario shape.
7. For `fixture-plan`, define known-good, known-bad, domain, and false-positive fixtures before implementation.
8. For `calibrate`, run the harness against fixtures, compare expected vs observed findings, and tune thresholds only with source-card evidence.
9. For `validate-interface`, drive Playwright with user-facing locators where possible and collect the required evidence outputs.
10. For `report`, summarize findings with source cards, evidence paths, proxy limits, status, and residue.
11. Preserve residues for subjective workload, comprehension, trust, confidence, delight, and real-user task success.
12. Return the output contract and the next lifecycle step.
</process>

<evidence-output-contract>
Browser evidence runs should write under:

```text
output/playwright/ux-validator/<run-id>/
```

Required outputs:

- `run-metadata.json`,
- `summary.md`,
- `findings.json`,
- `console-network.json`,
- `accessibility/*.json`,
- `aria/*.yml`,
- `screenshots/*.png`,
- `measurements/*.json`,
- `traces/*.zip` when interaction evidence is required,
- `residue-ledger.yml`.
</evidence-output-contract>

<quality-bar>
A successful run must:

- keep deterministic browser failures separate from UX risk proxies,
- cite source cards for every non-trivial UX claim,
- name what Playwright observed and what it cannot prove,
- use hard gates only for deterministic or standards-backed failures,
- require fixture calibration before promoting reusable hard gates,
- capture screenshots, traces, accessibility output, ARIA snapshots, DOM measurements, console/network summaries, and residues when running browser validation,
- keep domain-specific market rules behind explicit domain tags,
- report human-study claims instead of pretending automation can measure them,
- preserve development status when fixture or implementation evidence is missing.
</quality-bar>

<anti-patterns>
Avoid:

- producing a single universal UX score,
- claiming automated accessibility scans prove complete accessibility,
- converting neuroscience or cognitive science references into deterministic browser truth,
- treating market heuristics as universal rules outside their domain,
- blocking dense expert interfaces without false-positive calibration,
- accepting screenshot diffs without stable fonts, data, motion, and viewport controls,
- treating a good spec as implementation or promotion evidence.
</anti-patterns>

<observability>
For meaningful executions, record:

- mode,
- target URL or artifact type,
- scenario count,
- generated output count,
- validator layer coverage L0-L6,
- hard gate count,
- soft flag count,
- screenshot review count,
- human-study residue count,
- source-card coverage,
- fixture calibration status,
- quality bar status,
- anti-pattern hits,
- reflection trigger recommendation.
</observability>

<promotion-gate>
Promotion requires:

- implemented fixture corpus,
- at least one known-good fixture,
- accessibility, keyboard, layout, interaction, cognitive-risk, domain, and false-positive fixtures,
- Playwright evidence reports for fixture runs,
- hard gates catching expected deterministic failures,
- L4/L5 claims remaining explainable and non-blocking unless independently justified,
- Experiment Harness report,
- Sigil Development review.
</promotion-gate>

<output-contract>
Return:

```markdown
## UX Evidence Validator Result

- Status: pass | flag | block | seed-only
- Mode: research | spec | fixture-plan | calibrate | validate-interface | report
- Target: <url, artifact, scenario, or research path>
- Evidence cards: <path or status>
- Claim classes: <hard gates, soft flags, screenshot review, human study, not automatable>
- Browser evidence: <output root or not run>
- Fixture calibration: pass | flag | block | not run
- Findings: <summary or path>
- Residue: <human-review or user-study claims>
- Validation: <checks performed>
- Next lifecycle step: <step>
```
</output-contract>
