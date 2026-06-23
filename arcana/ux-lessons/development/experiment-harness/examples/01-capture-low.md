# Example 01 (low) — `capture`

**Mode:** `capture` · **Input:** the x-ray session, move M3 (optional guided tour) · **Expected:** one conformant `lesson`, honestly `anecdote`.

## Output body (real artifact produced)

```yaml
lesson_id: L-xray-03
session_ref: refine-skill-xray.html (x-ray iteration session, 2026-06-23)
context: a layered HTML "x-ray" of a skill; user wanted to convey depth, not just receive layers
iteration_step: added an optional guided tour that constructs the stack one layer at a time
trigger: "instead of just receiving the layers" — user wanted to build understanding by reading
failure_mode: all 13 layers shown at once; the depth/composition was not understood
change: optional "Guided tour" mode; Next/Prev builds the stack layer-by-layer with per-layer narration; off by default
before_after:
  before_ref: full stack shown at load
  after_ref: screenshots 22-24 (tour step 1 -> step 6 -> complete)
  screenshot_refs: [".xray-iter/22-tour-step1.png", ".xray-iter/24-tour-end.png"]
evidence: [screenshot_diff]
signal_strength: anecdote
generalizable_principle: for dense layered explanations, offer an optional progressive build so the user constructs understanding instead of receiving it whole
residue: needs a second session before it can become `repeated`
promoted_to: null
```

## Conformance
- [x] all `evidence[]` values in enum (`screenshot_diff`)
- [x] `signal_strength: anecdote` and `promoted_to: null` (honesty rule satisfied — no hard-gate target)
- [x] `generalizable_principle` is a reusable claim, not a screen description
- [x] composes — no storage/capture mechanics re-implemented; this is just a typed record

**Result: pass.**
