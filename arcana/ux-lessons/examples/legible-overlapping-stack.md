# Example — `legible-overlapping-stack`

Second pattern from the x-ray HTML iteration session (`refine-skill-xray.html`), distilled
from capture batch 2 (`../development/captures/2026-06-23-xray-session-2.md`). Distinct from
the founding `detail-beside-the-subject`: this one is about the **stack mechanics**, not the
detail panel.

## Source lessons (capture)

`L-xray-04` (hover z-trap → push, `repeated`), `L-xray-05` (expand-vs-navigate → accordion,
`repeated`), `L-xray-06` (mobile inline-height overlap, **`cross_session`** — corroborated by
the 2026-05-30 `ui-playwright-repair` run), `L-xray-07` (title clip → measured lip, `repeated`).
See the capture file for full records and `dom_measurement` / `screenshot_diff` evidence.

## Distilled pattern

```yaml
pattern_id: legible-overlapping-stack
name: Legible overlapping stack
intent: show depth via overlapping cards while keeping every card legible AND navigable
problem: >
  overlapping cards fail three ways at once — they trap the cursor (z-raise occludes the next
  card's hit-target), clip content (a guessed lip is shorter than the card's real content), and
  overflow on mobile (a JS-set inline height beats the responsive rule and the next content bleeds through)
solution: >
  (1) size the lip from MEASURED content offsets, not a guessed constant; (2) on activate, PUSH
  neighbors down by the active card's real height instead of raising z over them; (3) make any
  JS-set inline dimension breakpoint-overridable (or do not set it on narrow widths)
when_to_use: a vertical stack of overlapping cards/layers that must show both an at-rest lip and an expanded detail
anti_pattern: a guessed lip constant; raising z-index over the next card on hover; a JS inline height with no responsive override
forces: [depth cue, legibility, hit-target reachability, responsive flow]
evidence_link: >
  L-xray-04..07 — dom_measurement (elementFromPoint next-lip reachability all-OK; clipped:[] across 13 cards;
  overlaps:[]; deckInline 848px vs deckComputed 2100px) + screenshot_diff (.xray-iter/25, 27, 29)
status: seed
residue: push distance is imperative (offsetHeight); the expandable card covers the cards below by design
consumer_intake:
  validator:
    - claim_class: hard_gate
      mode: spec
      feeds_field: "no card's title/device bottom exceeds the next card's top (no clip)"
    - claim_class: hard_gate
      mode: spec
      feeds_field: "for each card, the topmost element at the next card's lip is the next card (hit-target reachable)"
    - claim_class: hard_gate
      mode: spec
      feeds_field: "no container has a fixed height less than its flowed content height at the tested breakpoint (no overflow-bleed)"
    - claim_class: screenshot_review
      mode: spec
      feeds_field: "depth cue (overlap + shadow) still reads as a stack"
  studio:
    intent: restructure
    comment_event_template:
      target: { odId: "deck", selector: "[data-od-id=deck]", elementLabel: "overlapping card stack" }
      severity: major
      note: "size the lip to measured content; push neighbors on expand; make inline height responsive"
    mutation_task:
      odId: "deck"
      changeType: layout-restructure
```

## Honesty note

The three `hard_gate` claims are **mechanically checkable** — they are exactly the
`dom_measurement` assertions already run in this session (`elementFromPoint` reachability,
`clipped:[]`, `deckInline` vs `deckComputed`). Per the honesty rule a `hard_gate` proposal is
allowed here because the load-bearing overlap force is **`cross_session`** (L-xray-06 +
ui-playwright-repair), not anecdote.

It is still **`status: seed`**: no experiment-harness fixtures exist yet. Promotion requires
`emit-validator → --mode spec → fixture-plan → calibrate` with good / bad / false-positive
fixtures (clean stack vs clipped-title vs cursor-trap vs mobile-bleed) before any gate is real.
The `screenshot_review` claim ("still reads as a stack") is deliberately NOT a hard gate — depth
legibility is a perceptual judgment, not a measurement.
