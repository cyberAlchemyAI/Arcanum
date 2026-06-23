# Example 03 (complex) — `capture` + `promote` + `emit-studio`

**Modes:** `capture` → `promote` → `emit-studio` · **Input:** move M1 (the 3D tilt), which **recurred within the session** · **Expected:** demonstrate the promote path and a studio intent — while being honest that true *cross-session* promotion is not yet provable.

## Step A — `capture` output body (real artifact)

```yaml
lesson_id: L-xray-01
session_ref: refine-skill-xray.html (x-ray iteration session, 2026-06-23)
context: dense 13-layer stack of text-heavy cards
iteration_step: 3D isometric tilt was added, reverted (illegible), re-added gentler, reverted again
trigger: desire to convey depth/"stacked layers"
failure_mode: aggressive 3D transform skewed/overlapped text and overflowed the container -> illegible
change: reverted to a 2.5D offset cascade (depth via overlap + shadow, text stays level)
before_after:
  before_ref: screenshots 01, 09-10 (3D tilt)
  after_ref: screenshots 03, 14 (offset cascade)
  screenshot_refs: [".xray-iter/01-stack.png", ".xray-iter/10-3d-tilt.png", ".xray-iter/14-reverted.png"]
evidence: [screenshot_diff]
signal_strength: repeated        # learned twice WITHIN this one session (added/reverted x2)
generalizable_principle: on text-dense layered views, prefer 2.5D depth cues (overlap + shadow) over 3D rotation; rotation trades legibility for spectacle
residue: within-session repetition only; needs a 2nd distinct session to reach cross_session
promoted_to: avoid-3d-rotation-on-text-dense-layers
```

## Step B — `promote` output body

```yaml
pattern_id: avoid-3d-rotation-on-text-dense-layers
name: Prefer 2.5D depth over 3D rotation for text-dense layers
status_before: seed
status_after: calibrated          # one notch — backed by `repeated` signal
promotion_rule_applied: "anecdote -> repeated requires recurrence; demonstrated WITHIN one session"
honesty_gate: "NOT promoted to `promoted` and NO validator hard_gate emitted — `repeated` here is within-session, not cross_session. cross_session requires a 2nd distinct session."
forces: [legibility, depth perception, container bounds]
```

## Step C — `emit-studio` output body (real intent, shape-validated against ui-prototyping-studio SPEC)

```yaml
pattern_id: avoid-3d-rotation-on-text-dense-layers
handoff: ui-prototyping-studio (annotation intake)
comment_event:
  target: { odId: "layer-stack", selector: "[data-od-id=layer-stack]", elementLabel: "layer stack" }
  severity: major
  intent: restructure
  note: "drop the 3D rotation on this text-dense stack; use 2.5D overlap+shadow so text stays level and legible"
mutation_task:
  odId: "layer-stack"
  changeType: restructure
deferred:
  variant_fitness_intake: "blocked on studio OQ-5 + an axe-core/layout-overflow fitness evaluator (would auto-score legibility/overflow across variants)"
```

## Conformance
- [x] lesson + pattern conform to schemas; `evidence[]` in enum
- [x] honesty gate enforced: `repeated` is within-session → **no** cross_session status, **no** validator hard_gate
- [x] studio intent matches `CommentEvent`/`MutationTask` shape; variant/fitness correctly deferred with named unblock
- [~] **FLAG:** true cross-session promotion not demonstrated — only one real session exists

**Result: flag** (path proven; cross-session evidence pending a 2nd session).
