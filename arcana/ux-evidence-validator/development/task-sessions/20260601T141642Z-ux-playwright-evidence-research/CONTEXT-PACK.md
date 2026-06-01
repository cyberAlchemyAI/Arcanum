# Task Session Context Pack: UX Playwright Evidence Research

Status: strict coverage pass.
Created: 2026-06-01.
Dispatch: `ux-playwright-evidence-research-20260601`.

## Scope

| Field | Value |
| --- | --- |
| Task | Run the UX evidence research route from the dispatch strategy. |
| Goal | Produce reference cards, a claim map, a Playwright validator contract, a fixture plan, and a task-session receipt. |
| Working root | `/home/vrondelli/projects/domainspec-core/arcanum` |
| Write boundary | `arcana/ux-evidence-validator/development/` and this task-session evidence directory. |
| Implementation boundary | No validator code or fixture code is implemented in this session. |
| Promotion boundary | Research remains development evidence until owner review and calibration. |

## Controlling Task Contract

The operator asked to run research for academic and market UX references mixing cognitive science, neuroscience, tested market practices, and Playwright evidence so a future validator/tester can produce evidence for finished frontend interfaces.

The dispatch selected the multi-lane evidence route and required:

- source evidence cards,
- claim mapping into hard gates, soft flags, screenshot review, human study, and not-automatable classes,
- a validator taxonomy,
- a Playwright evidence contract,
- a fixture calibration plan,
- explicit guardrails against overclaiming automation.

## Source Evidence

| Source | Role In Session |
| --- | --- |
| `arcana/ux-evidence-validator/development/UX-PLAYWRIGHT-EVIDENCE-RESEARCH-STRATEGY.md` | Initial route strategy and seed source map. |
| `arcana/ux-evidence-validator/development/ux-playwright-evidence-research.dispatch.json` | Controlling dispatch, gate list, output paths, and promotion guardrails. |
| `arcana/task-session/SKILL.md` | Task-session execution frame: context pack, gate checks, result receipt, validation, synchronization. |
| `transmutations/context-builder/SKILL.md` | Context bundle and obligation-to-source coverage frame. |
| `arcana/distill/development/LITERATURE-RESEARCH.md` | Local cognitive-load and working-memory background used as a repo-local sanity check. |
| W3C WCAG 2.2, WAI-ARIA, ARIA APG, and WCAG-EM | Standards lane for accessibility and evaluation method. |
| Deque axe-core and Playwright docs | Browser automation and evidence lane. |
| Cognitive load, working memory, Fitts, Hick-Hyman, NASA-TLX literature | Cognitive and human-factors lane. |
| Feature integration, salience, visual attention, change blindness, and guided search literature | Neuroscience and perception lane. |
| Nielsen Norman Group, Baymard, GOV.UK, USWDS, IBM Carbon | Market-practice and design-system lane. |

## Hard Constraints

- Do not implement the Playwright validator in this session.
- Do not treat cognitive or neuroscience claims as deterministic browser truths.
- Do not treat market-practice evidence as universal outside declared domain tags.
- Do not treat automated accessibility checks as complete accessibility proof.
- Do not promote these artifacts into inventory, ontology, glossary, sigil, spell, or runtime surfaces without owner review.
- Store summaries and links, not copied full external documents.

## Decisions

| Decision | Rationale |
| --- | --- |
| Run as local task-session synthesis, not spawned agent delegation. | The dispatch authorizes a multi-lane research route; this pass can satisfy the research outputs without requiring additional subprocess coordination. |
| Keep every external claim in card form before validator form. | This preserves source, strength, proxy limits, and freshness. |
| Use L0-L6 validator layers. | This keeps deterministic browser evidence separate from cognitive, market, and human-study residues. |
| Put fixture calibration before implementation promotion. | The validator should be proven on known-good and known-bad cases before it becomes reusable. |

## Gate Verdict

| Gate | Verdict | Evidence |
| --- | --- | --- |
| Source evidence required | PASS | `UX-EVIDENCE-REFERENCE-CARDS.yml` includes URL, type, strength, automation candidate, contraindication, and freshness rule. |
| Automation honesty | PASS | `UX-EVIDENCE-CLAIM-MAP.md` separates hard gates, soft flags, screenshot review, human study, and not-automatable claims. |
| Playwright evidence contract | PASS | `UX-PLAYWRIGHT-VALIDATOR-SPEC.md` names required evidence files and output root. |
| Calibration before promotion | PASS for research; implementation not run | `UX-PLAYWRIGHT-FIXTURE-PLAN.md` defines known-good, known-bad, and false-positive fixtures. |
| No automatic promotion | PASS | Artifacts stay under development paths. |

## Coverage Statement

This context pack covers the approved research run and its immediate outputs. It intentionally stops before fixture implementation, browser execution, or validator source creation.
