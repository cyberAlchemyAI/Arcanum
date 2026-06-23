# UX Evidence Validator — Spec: `skill-anatomy`

- Sigil: `ux-evidence-validator`
- Mode: `spec` + `validate-interface`
- Status: seed harness (this run ships a standalone runnable test; the reusable Playwright harness in the sigil is still seed)
- Target: `arcanum/docs/skill-anatomy.html` (the "Anatomy of a Skill" deep-dive), which embeds
  `arcanum/docs/refine-skill-xray.html` in an iframe.
- Viewport matrix: **desktop 1280×900**, **mobile 390×844**.
- Domain tags: `marketing`, `docs`, `data-tool` (the embedded x-ray is a dense expert interface).

## Reported defect (what triggered this run)

In the x-ray's **Stacked deck** view, the layer-card title (`.pt`) wraps and collides with the
absolutely-positioned band badge (`.pb`): "Invocation contract" renders as "Invo / contract" with the
`CONTRACT` pill overlapping. Cards look cramped/clipped because only a ~56px lip of each stacked card is
visible (`STEP = 56`, card height 150px), so any title wrap is hidden under the next card.

### Root cause (source-backed)

`refine-skill-xray.html` — `.plane .pb` is `position:absolute; top:12px; right:14px`, while
`.plane .pt` is a full-width block with **no reserved right gutter** for the badge. When the deck
column renders narrow (it is the middle of a 3-column layout, so it shrinks as the surrounding chrome
grows), the title text runs into the badge and wraps. This is layout-deterministic and viewport-sensitive
— precisely what a responsive test should catch.

## Evidence boundary

| Lane | What it means here |
| --- | --- |
| **Source-backed** | The skill's own DOM/CSS (`.plane`, `.pt`, `.pb`, `STEP`, `CARDH`) — quoted, not inferred. |
| **Browser-observable (deterministic)** | Geometry the browser actually renders: element rects, line-box count, overflow, console errors. Hard-gate eligible. |
| **Standards-backed** | WCAG target-size and text-size minimums. Soft flags here (dense expert UI → calibrate before blocking). |
| **Proxy / perception** | "Cramped", density, reading width. Soft flags + screenshot review only. |
| **Subjective / human-study** | "Cards behave well", comprehension, trust, delight. Residue, never automated. |

## Validator layers (L0–L6) and checks

| Layer | Check id | What it measures | Claim class | Severity |
| --- | --- | --- | --- | --- |
| **L0 load/integrity** | `L0.page-load` | page reaches `load`, title correct | browser-observable | hard_gate |
| | `L0.no-console-errors` | zero console errors / pageerrors | browser-observable | hard_gate |
| | `L0.iframe-loaded` | x-ray iframe present, same-origin, accessible | browser-observable | hard_gate |
| **L1 layout integrity** | `L1.no-horizontal-overflow` | `documentElement.scrollWidth ≤ innerWidth+1` (page) | browser-observable | hard_gate |
| | `L1.iframe-no-overflow` | x-ray body no horizontal overflow | browser-observable | hard_gate |
| | `L1.card-title-no-wrap` | each visible deck `.pt` renders on **one line** (`getClientRects().length === 1`) — the reported bug | browser-observable | hard_gate |
| | `L1.card-title-badge-clearance` | deck `.pt` first-line text right edge ≤ `.pb` left edge (no horizontal collision) | browser-observable | hard_gate |
| | `L1.strata-title-no-clip` | strata `.srow .pt` not horizontally clipped (`scrollWidth ≤ clientWidth+1`) | browser-observable | hard_gate |
| | `L1.grid-collapses-mobile` | page `.grid-3`/`.grid-2` collapse to 1 column at 390px | browser-observable | hard_gate |
| **L2 component behavior** | `L2.view-toggle` | Stacked deck ↔ Strata toggle flips `aria-pressed` and changes layout | browser-observable | hard_gate |
| | `L2.nav-toggle-mobile` | hamburger reveals nav at 390px, `aria-expanded` flips | browser-observable | hard_gate |
| | `L2.tour-controls-present` | guided-tour controls exist and are operable | browser-observable | soft_flag |
| **L3 standards** | `L3.tap-targets` | interactive controls ≥ 24×24 CSS px (WCAG 2.5.8 AA); note < 44 (2.5.5 AAA) | standards-backed | soft_flag |
| | `L3.text-legibility` | rendered title/body font-size ≥ 12px; no ellipsis truncation of titles | standards-backed | soft_flag |
| | `L3.contrast` | text/background contrast (needs axe) | standards-backed | not_run → residue |
| **L4 perception proxy** | `L4.line-clamp-loss` | `.pm` line-clamp hides content in stacked lip; record how much | proxy | soft_flag |
| | `L4.reading-width` | prose `.narrow` line length within 45–90 chars | proxy | soft_flag |
| **L5 subjective** | `L5.cards-behave` | "cards behave well", aesthetic balance, comprehension, trust | human-study | residue |
| **L6 evidence** | `L6.package` | all required outputs + residue ledger written | process | gate |

## Hard-gate rule (pass/block)

The run **blocks** if any `hard_gate` check fails on either viewport. `L1.card-title-no-wrap` and
`L1.card-title-badge-clearance` are the gates that encode the reported defect; they must be green before
the page is considered fixed.

## Fixture plan (for promoting these into reusable gates)

| Fixture | Purpose | Status |
| --- | --- | --- |
| `live` (the real page) | known-bad at narrow widths — current target | implemented (this run) |
| `known-good` | a `.plane` with `padding-right` reserving the badge gutter; titles never wrap | TODO |
| `known-bad` | a deliberately narrow deck column forcing wrap | TODO (live already exercises it) |
| `false-positive` | a dense but *acceptable* expert card with intentional tight spacing | TODO — required before `L3.tap-targets` / `L4` become blocking |
| `domain` | a marketing/docs hero card to confirm rules don't over-fire on prose | TODO |

Calibration status: **not run** (fixtures beyond `live` not yet built). Until calibrated, only L0–L2
deterministic gates are trustworthy as blockers; L3/L4 are advisory.

## Measurement caveat (load-bearing)

The Stacked deck applies a CSS **3-D transform** (`perspective` on `.deck` + `transform` on
`.deck-inner`). `getBoundingClientRect()` returns *projected* geometry under a transform, so naive
measurement reports false, uniform widths (observed: every card 139px) and produces false collisions.
The validator therefore temporarily removes only the transform/perspective (keeping `.plane` absolute
so each card keeps its true `left:34px; right:2%` width), forces reflow, measures, then restores — and
captures the screenshot *before* mutating. Any future reuse of this harness on transformed UIs must do
the same, or its layout findings are invalid.

## Scenario shape

1. For each viewport ∈ {1280×900, 390×844}:
   1. load page, collect console/network, assert L0.
   2. assert page-level L1 (overflow, grid collapse) and L2 (nav toggle on mobile).
   3. enter iframe; for view ∈ {Stacked deck, Strata}: assert L1 card checks, capture screenshot + measurements.
   4. measure L3 tap targets and text sizes (advisory).
2. Write evidence bundle + residue ledger; emit pass/flag/block.

## How to run

```bash
arcanum/development/ux-validation/skill-anatomy/run.sh
# serves arcanum/docs on a local port, runs ux-validate.mjs against both viewports,
# writes evidence to arcanum/output/playwright/ux-validator/<run-id>/
```

## Residue (never automated)

- Whether the cards *feel* balanced and the stacked metaphor reads clearly (subjective).
- Whether a first-time reader comprehends the layer model faster with deck vs strata (human study).
- Trust/credibility impact of the evidence-boundary framing (human study).
