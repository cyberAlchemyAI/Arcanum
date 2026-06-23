# Capture — x-ray iteration session, batch 2 (2026-06-23)

> `ux-lessons --mode capture`. Continuation of the founding fixture
> (`refine-skill-xray.html`). The founding run captured L-xray-01/02/03; this batch
> harvests the later iteration moves. Screenshot refs point at the parent-repo
> scratch `.xray-iter/` (evidence pointers, same convention as the founding example).
> Evidence values are enum-constrained: `dom_measurement | aria_snapshot | screenshot_diff | trace_event`.

```yaml
lesson_id: L-xray-04
session_ref: refine-skill-xray.html (x-ray iteration session, 2026-06-23, batch 2)
context: a stacked overlapping-card deck; user scans cards 1 -> 2 -> 3 to read each layer
iteration_step: hovering a card raised z-index to 900, which covered the next card's visible lip
trigger: user reported "i can't go smoothly from 1->2, i need 1->3->2"
failure_mode: the hovered/active card occludes the next card's hit-target, trapping the cursor
change: removed the blanket z-raise; then made it an accordion — hovered card gets .active, every card BELOW gets .pushed down by the active card's real height so its lip stays reachable
before_after:
  before_ref: user screenshot of the clip/trap
  after_ref: .xray-iter/25-accordion.png
  screenshot_refs: [".xray-iter/25-accordion.png"]
evidence: [dom_measurement, screenshot_diff]
signal_strength: repeated
generalizable_principle: in an overlapping stack, never let a hovered/active element occlude the hit-target of the next element; make room by displacing neighbors, not by raising z over them
residue: push distance is imperative (offsetHeight read); the one expandable card still covers the cards below it by design
promoted_to: legible-overlapping-stack
```

```yaml
lesson_id: L-xray-05
session_ref: refine-skill-xray.html (x-ray iteration session, 2026-06-23, batch 2)
context: same overlapping deck; cards must reveal their full body (mechanism text) on activate
iteration_step: removing the z-raise (the L-xray-04 trap fix) also stopped cards from revealing content on hover
trigger: user "now the card is not expanding ... the other cards aren't working, the 6 is working"
failure_mode: the trap fix and the reveal requirement conflict — fixing one broke the other
change: accordion resolves both — the active card pops AND pushes lower cards down by its measured height, so it expands AND the next lip stays reachable
before_after:
  before_ref: .xray-iter/25-accordion.png (pre-accordion regression state)
  after_ref: .xray-iter/25-accordion.png
  screenshot_refs: [".xray-iter/25-accordion.png"]
evidence: [dom_measurement, screenshot_diff]
signal_strength: repeated
generalizable_principle: "reveal-on-hover" and "next item reachable" are jointly satisfiable in an overlapping stack only by displacing neighbors, not by z-stacking
residue: null
promoted_to: legible-overlapping-stack
```

```yaml
lesson_id: L-xray-06
session_ref: refine-skill-xray.html (x-ray iteration session, 2026-06-23, batch 2)
context: the deck on narrow/mobile widths
iteration_step: mobile cards overlapped and the inspector content bled through behind them
trigger: user screenshot "still bugged" on mobile
failure_mode: JS sets an inline deck height (848px) for the absolute cascade; on mobile planes flow relative (~2100px) but the short inline height clips the deck box, so the following content (the rail) renders over the overflowing cards
change: media query `.deck { height: auto !important }` overrides the inline height so the deck sizes to its flowed content
before_after:
  before_ref: .xray-iter/26-mobile-bug.png
  after_ref: .xray-iter/27-mobile-fixed.png
  screenshot_refs: [".xray-iter/26-mobile-bug.png", ".xray-iter/27-mobile-fixed.png"]
evidence: [dom_measurement, screenshot_diff]
signal_strength: cross_session
generalizable_principle: any JS-set inline dimension must be overridable per breakpoint; responsive rules need `!important` (or no inline at all) to beat imperative layout
residue: the cleaner fix is to not set an inline height on narrow widths in the first place (branch the JS on breakpoint)
promoted_to: legible-overlapping-stack
```
> `cross_session` justified: the same overlap / hard-coded-spacer / mobile-illegibility
> failure class was independently found in `arcana/x-ray/.../refinement-runs/20260530T010327Z-ui-playwright-repair` (a different session, 2026-05-30).

```yaml
lesson_id: L-xray-07
session_ref: refine-skill-xray.html (x-ray iteration session, 2026-06-23, batch 2)
context: the resting (non-hovered) cascade on desktop
iteration_step: each card's title was clipped by the next card
trigger: user "fix the overlapping of the cards" with a screenshot of clipped titles
failure_mode: an in-flow band pill consumed a line, pushing the title to 43-61px, while the lip step was 56px -> the title's bottom was clipped
change: measured content offsets (title 43-61, device 66-83) and set the lip step to 90 to clear band + title + device
before_after:
  before_ref: user screenshot of clipped titles
  after_ref: .xray-iter/29-noclip.png
  screenshot_refs: [".xray-iter/29-noclip.png"]
evidence: [dom_measurement, screenshot_diff]
signal_strength: repeated
generalizable_principle: a stacked-card lip height must be derived from measured content, not a guessed constant; in-flow chrome (pills/badges) changes the lip a card needs
residue: null
promoted_to: legible-overlapping-stack
```

```yaml
lesson_id: L-xray-08
session_ref: refine-skill-xray.html (x-ray iteration session, 2026-06-23, batch 2)
context: reading the deck on narrow/touch, where the detail rail sits below the whole deck and there is no hover
iteration_step: on mobile the user "can only see the card" — the per-layer device/nudge was off-screen below
trigger: user "is it possible adding infinite scroll and changing where the descriptions of nudge and device happens"
failure_mode: hover-driven detail and a below-fold rail both fail on touch
change: an IntersectionObserver makes the scroll-centered card drive the detail; on mobile the rail becomes a fixed bottom sheet with device + nudge ordered first
before_after:
  before_ref: user screenshot (card only)
  after_ref: .xray-iter/28-scrollsync.png
  screenshot_refs: [".xray-iter/28-scrollsync.png"]
evidence: [dom_measurement, screenshot_diff]
signal_strength: anecdote
generalizable_principle: when hover is unavailable (touch), drive "detail beside the subject" by scroll position and pin the detail as a sheet so it follows the reader
residue: this is a touch realization of `detail-beside-the-subject` — evidence toward promoting THAT pattern to `repeated` once a second independent session shows it
promoted_to: detail-beside-the-subject
```

```yaml
lesson_id: L-xray-09
session_ref: refine-skill-xray.html (x-ray iteration session, 2026-06-23, batch 2)
context: adding a third "Calls / loop" view to the page
iteration_step: switching to the new view rendered a blank page
trigger: the loop view showed nothing; debug found <main class="root loop"> had display:none
failure_mode: the same class name `.loop` was used for BOTH the root view-state flag AND the view container, so `.loop { display:none }` matched the root <main>
change: renamed the container class to `.loopview`
before_after:
  before_ref: blank render
  after_ref: .xray-iter/30-loopview.png
  screenshot_refs: [".xray-iter/30-loopview.png"]
evidence: [dom_measurement]
signal_strength: anecdote
generalizable_principle: never reuse one class for both a state flag on a root element and a component selector; namespace state classes (is-/view-) separately from component classes
residue: this is an engineering/CSS lesson more than a UX pattern — keep as a lesson, do NOT promote to a ux-pattern
promoted_to: null
```

## Honesty checks (batch)
- every `evidence[]` value is in the enum (`dom_measurement`, `screenshot_diff`, `trace_event` only used).
- `signal_strength` tagged by sessions: L-06 `cross_session` (ui-playwright-repair corroborates); L-04/05/07 `repeated` (multiple within-session sub-iterations of the same force); L-08/09 `anecdote`.
- anecdote lessons (L-08, L-09) do NOT target a validator `hard_gate`. L-09 targets no pattern at all.
- principles are reusable claims, not descriptions of this one screen.
