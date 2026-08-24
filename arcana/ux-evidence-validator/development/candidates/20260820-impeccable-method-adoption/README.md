# UX Evidence Validator

`ux-evidence-validator` is an Arcana sigil seed for turning UX research, accessibility standards, market-tested practice, and browser automation into a Playwright-backed evidence system for finished frontend interfaces.

It is meant for the awkward but important middle ground between "the UI works in the browser" and "the UI is good." The sigil keeps those claims separate: deterministic browser failures can become hard gates, while cognitive, perception, market, and subjective UX claims remain soft flags, screenshot review, human-study prompts, or residue until calibrated.

## Status

Status: seed.

This package defines the research basis, evidence-card model, validator taxonomy,
fixture plan, and lifecycle direction. A deterministic terminal-outcome kernel
has development evidence, but the package is not promoted and does not yet
include executable Playwright browser checks or calibrated fixture evidence.

## Problem It Solves

Frontend review often mixes several kinds of truth:

- accessibility standards,
- browser-observed behavior,
- responsive layout integrity,
- cognitive and perception risk,
- market and design-system heuristics,
- subjective user evidence.

When these are collapsed into one "UX score," the result becomes untrustworthy. `ux-evidence-validator` instead creates a layered evidence contract so a finished interface can produce reviewable artifacts: screenshots, traces, ARIA snapshots, accessibility output, DOM measurements, finding JSON, and a residue ledger.

## Use When

- a frontend interface needs browser-level evidence before being treated as finished,
- UX guidance needs to be translated into validator-safe claims,
- Playwright should capture screenshots, traces, accessibility output, ARIA snapshots, and measurements,
- cognitive science, neuroscience, and market practice should inform checks without being overclaimed,
- a team needs known-good and known-bad fixtures before promoting hard gates,
- an interface review needs a residue ledger for claims that require human judgment or user research.

## Do Not Use When

- the user only wants a quick visual opinion,
- a full usability study is required and no browser evidence is needed,
- the project has no runnable frontend or inspectable interface,
- the request is only accessibility compliance auditing without UX evidence synthesis,
- a subjective product-quality decision is being forced into deterministic automation.

## Evidence Model

| Layer | Purpose | Default Status |
| --- | --- | --- |
| L0 Smoke | Page load, assets, console/network, trace availability. | Hard gate after calibration. |
| L1 Accessibility | axe output, ARIA snapshots, role/name/state, keyboard flow, forms. | Hard gate plus manual review. |
| L2 Layout Integrity | Overflow, clipping, overlap, target size, responsive screenshots. | Hard gate after calibration. |
| L3 Interaction Flow | User-facing locators, task completion, visible state changes. | Hard gate after calibration. |
| L4 Cognitive and Attention Risk | Density, memory burden, salience, visual hierarchy, change visibility. | Soft flag or screenshot review. |
| L5 Domain Practice | Ecommerce, service, dashboard, design-system, or platform rule packs. | Domain-specific soft flag unless deterministic. |
| L6 Human Evidence | Workload, comprehension, trust, confidence, real task success. | Human-study or review residue. |

## Optional Planning And Stress Overlays

The validator may consume a UI or UX plan that declares:

- the surface's success mode and the authority that owns its design contract;
- empty, short, typical, long, localized, bidirectional, and large-collection
  content profiles;
- viewport, orientation, pointer/hover, keyboard, touch, zoom, motion,
  contrast/theme, and connection contexts;
- loading, empty, error, success, recovery, permission, persistence, and
  interruption states.

These declarations create scenario coverage; they do not become findings by
themselves. Observed incumbent values remain observations until an owner adopts
them as normative product contracts.

Public external methods may be represented by revision-pinned evidence cards.
Their default ceiling is planning input, soft flag, screenshot review, or human
residue. No external expert method can independently authorize a reusable hard
gate, numeric threshold, visual preference, or aggregate UX score.

The sigil consumes source cards and scenario files, not an external design
tool's package, hooks, detector, browser runtime, root files, or visual system.

## Development Artifacts

| Artifact | Purpose |
| --- | --- |
| [UX-PLAYWRIGHT-EVIDENCE-RESEARCH-STRATEGY.md](development/UX-PLAYWRIGHT-EVIDENCE-RESEARCH-STRATEGY.md) | Original research route and source lanes. |
| [ux-playwright-evidence-research.dispatch.json](development/ux-playwright-evidence-research.dispatch.json) | Dispatch route that shaped the research pass. |
| [UX-EVIDENCE-REFERENCE-CARDS.yml](development/UX-EVIDENCE-REFERENCE-CARDS.yml) | Normalized source cards and automation candidates. |
| [UX-EVIDENCE-CLAIM-MAP.md](development/UX-EVIDENCE-CLAIM-MAP.md) | Claim classes and proxy limits. |
| [UX-PLAYWRIGHT-VALIDATOR-SPEC.md](development/UX-PLAYWRIGHT-VALIDATOR-SPEC.md) | Future validator/tester contract and evidence output model. |
| [UX-PLAYWRIGHT-FIXTURE-PLAN.md](development/UX-PLAYWRIGHT-FIXTURE-PLAN.md) | Known-good, known-bad, domain, and false-positive fixture plan. |
| [WORK-PACK.md](development/WORK-PACK.md) | Development route from seed package to fixture-calibrated validator. |

## Ownership Model

| Capability | Owner |
| --- | --- |
| Source claim normalization | UX Evidence Validator |
| Browser execution mechanics | Experiment Harness and future Playwright implementation |
| Bounded implementation tasks | Task Session |
| Fixture calibration | UX Evidence Validator plus Experiment Harness |
| Promotion readiness | Sigil Development |
| External source freshness | Future research refresh task-session |

## Promotion Boundary

Promotion requires:

- fixture corpus implemented,
- known-good and known-bad fixture runs,
- Playwright evidence written to the declared output root,
- hard gates catching deterministic failures,
- stress/adaptation fixtures covering declared content, input, motion, zoom,
  recovery, and persistence profiles,
- soft flags remaining explainable and source-card-linked,
- at least one false-positive trap proving density and salience checks do not block expert tools by default,
- Sigil Development review of experiment reports and observability signals.

Until then, this sigil remains a seed in development.
