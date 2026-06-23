# Stage 8 — Distill Repair

- **Capability:** distill · **Mode:** validate · **Evidence:** stages/08-toygame-xray-session.md · **Status:** pass

The toy_game **survived** — the coherent unit (thin sigil, two schemas, two adapters) is validated against a real session. Repairs applied to the three design-review flags (DR-1..3):

| Flag | Repair |
| ---- | ------ |
| DR-1 (modes risk re-stating workflow-reflect) | `capture`/`distill` modes are specified as **calls into** distill + workflow-reflect's analysis shape, not re-implementations. ux-lessons owns only the lesson/pattern typing applied to their output. |
| DR-2 (vague OQ-5 deferral) | Named the minimum the studio variant/fitness intake needs before it can ship: **an axe-core + layout-overflow evaluator producing a fitness delta** (studio L5). Until that exists, only the annotation intake is live. |
| DR-3 (underspecified evidence shapes) | `lesson.evidence` constrained to an enum: `{dom_measurement, aria_snapshot, screenshot_diff, trace_event}` — the exact replayable shapes ux-evidence-validator already consumes. |

## Repaired coherent unit (final)
Thin `ux-lessons` sigil · owns `lesson` + `ux-pattern` schemas (with evidence enum + honesty rule) + two adapters (validator: ready; studio: annotation ready, variant deferred behind named evaluator) · composes 5 owners · stores patterns as `ux`-tagged architecture-pattern-inventory cards.

Residue (to residuality-spec ledger): anecdote-signal patterns accumulate until cross-session signal promotes them; the studio variant intake is parked with a named unblock condition.
