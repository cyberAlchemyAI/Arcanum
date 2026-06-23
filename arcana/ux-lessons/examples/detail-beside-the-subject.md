# Example — `detail-beside-the-subject`

Founding example. Distilled from the x-ray HTML iteration session (`refine-skill-xray.html`); falsification-tested in
`../development/refinement-runs/2026-06-23-ux-lessons/stages/08-toygame-xray-session.md` (toy_game **survived**: emitted to both consumers with zero invented fields).

## Source lessons (capture)

```yaml
lesson_id: L-xray-02
session_ref: refine-skill-xray.html (x-ray iteration session, 2026-06-23)
context: a layered HTML "x-ray" explaining a skill as a stack of layers; user reads layers while needing per-layer detail
iteration_step: moved layer detail from a drill panel BELOW the stack to a sticky right-rail BESIDE it
trigger: the detail panel below the stack split attention from the layers being read
failure_mode: divided attention — eye travel between the layer and its explanation
change: sticky inspector rail adjacent to the stack; updates on hover of a layer or a nested overlay
before_after:
  before_ref: screenshot 15 (drill panel below)
  after_ref: screenshots 19-21 (right-rail beside stack, updates on hover)
  screenshot_refs: [".xray-iter/19-left-insp.png", ".xray-iter/20-rail-layer.png", ".xray-iter/21-rail-overlay.png"]
evidence: [screenshot_diff]
signal_strength: anecdote
generalizable_principle: keep explanatory detail co-visible with the thing it explains
residue: needs a second session to become `repeated`
promoted_to: detail-beside-the-subject
```

## Distilled pattern

```yaml
pattern_id: detail-beside-the-subject
name: Detail beside the subject (no divided attention)
intent: keep explanatory detail co-visible with the element it explains
problem: a separate or below detail panel forces eye travel, splitting attention during active reading
solution: a sticky inspector adjacent to the inspected structure that updates on hover/selection
when_to_use: a layered or structured artifact a user reads while needing per-item detail
anti_pattern: a modal or below-the-fold panel for per-item detail during active reading
forces: [reading continuity, screen width, per-item depth]
evidence_link: L-xray-02 (screenshot_diff; screenshots 19-21)
status: seed
residue: anecdote signal — one session; cannot drive a validator hard gate yet
consumer_intake:
  validator:
    - claim_class: hard_gate        # proxy: co-visibility is mechanically checkable
      mode: spec
      feeds_field: "detail panel is in-viewport adjacent to the inspected element (no scroll/modal to read it)"
  studio:
    intent: reposition
    comment_event_template:
      target: { odId: "inspector", selector: "[data-od-id=inspector]", elementLabel: "detail panel" }
      severity: major
      note: "make detail co-visible with the subject (sticky rail), not below"
    mutation_task:
      odId: "inspector"
      changeType: layout-reposition
```

## Honesty note
`signal_strength: anecdote` — this pattern is `seed`. The validator `hard_gate` entry is a **spec/fixture proposal**, not a promoted gate; it needs `fixture-plan` → `calibrate` with good/bad/false-positive fixtures (panel beside target vs below-fold vs adjacent-but-occluded) and a second session before promotion.
