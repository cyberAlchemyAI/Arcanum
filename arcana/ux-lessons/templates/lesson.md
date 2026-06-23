# Lesson — `<lesson_id>`

> One captured iteration unit, still contextual. Fill every field; use `null` / `[]` honestly.

```yaml
lesson_id:                 # kebab id, e.g. L-xray-02
session_ref:               # path / run-id / signal ref of the session
context:                   # what was being built and for whom
iteration_step:            # which move in the session
trigger:                   # what prompted the change
failure_mode:              # the problem the change fixed
change:                    # what was done
before_after:
  before_ref:              # artifact/screenshot before
  after_ref:               # artifact/screenshot after
  screenshot_refs: []      # evidence images
evidence: []               # subset of: dom_measurement | aria_snapshot | screenshot_diff | trace_event
signal_strength:           # anecdote | repeated | cross_session
generalizable_principle:   # the reusable claim
residue:                   # unresolved / parked
promoted_to:               # pattern_id | null
```

## Honesty checks
- [ ] every `evidence[]` value is in the enum
- [ ] `signal_strength` reflects how many sessions actually show this (first capture is usually `anecdote`)
- [ ] if `signal_strength: anecdote`, `promoted_to` does NOT target a validator `hard_gate`
- [ ] `generalizable_principle` is a claim, not a description of this one screen
