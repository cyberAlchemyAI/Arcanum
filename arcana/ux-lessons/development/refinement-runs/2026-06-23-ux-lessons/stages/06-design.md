# Stage 6 — Invoke Redefine / Design

- **Capability:** invoke · **Mode:** design · **Techniques:** x_ray, component_descriptor, route_menu · **Status:** pass

## Route-menu decisions (resolved)

| Decision | Options | Resolved | Why |
| -------- | ------- | -------- | --- |
| capability_shape | sigil / spell / discipline | **thin sigil** | Owns the two typed artifacts + adapters (Role B); composes the 5 owners (Role A). A spell can't own a schema; a net-new full sigil duplicates owners. |
| pattern_store_location | arcanum public / parent private | **arcanum public** | Both consumers must reach it; ux-pattern is a generic UX capability, not private. Operator already chose arcanum staging. |
| store relationship | own new store / borrow inventory | **borrow architecture-pattern-inventory card shape**; ux-patterns stored as its cards under a `ux` tag | Avoids the duplicate-store risk (F1). |

## X-ray structure map (component descriptors)

```
                 ┌─────────────────────── ux-lessons (thin sigil) ───────────────────────┐
 [session] ──▶   │  capture           distill            promote                          │
 iteration       │  ▸ borrows         ▸ uses distill      ▸ writes ux-pattern card         │
 (e.g. x-ray)    │    signal-observer   to reduce N        (arch-pattern-inventory shape)  │
                 │    + workflow-       lessons → 1                                          │
                 │    reflect shape     pattern             ┌── validator adapter ──▶ ux-evidence-validator
                 │         │              │                 │     (claim map across 5 lanes → spec/fixture-plan)
                 │     [lesson]  ──────▶ [ux-pattern] ──────┤
                 │     (schema A)        (schema B)         └── studio adapter ──▶ ui-prototyping-studio
                 │                                               (CommentEvent/MutationTask intents;
                 │     residue → residuality-spec ledger          variant/fitness DEFERRED behind OQ-5)
                 └────────────────────────────────────────────────────────────────────────┘
```

Owned by ux-lessons (solid): the two schemas + the two adapters + the promote step's honesty gate.
Composed (dashed): signal-observer, workflow-reflect shape, distill, architecture-pattern-inventory store, residuality-spec.

## Proposed modes (mirroring the lifecycle)
| Mode | Use when | Output |
| ---- | -------- | ------ |
| `capture` | An iteration session just happened; harvest raw lessons. | `lesson` records (anecdote-tagged). |
| `distill` | ≥1 lessons exist for a recurring move. | A candidate `ux-pattern` card. |
| `promote` | A pattern has cross-session signal. | Validated ux-pattern (status seed→calibrated). |
| `emit-validator` | A pattern should feed evidence validation. | Claim map → ux-evidence-validator `spec`/`fixture-plan` intake. |
| `emit-studio` | A pattern should steer prototyping. | `CommentEvent`/`MutationTask` annotation intents. |

## Artifact schema A — `lesson`
`lesson_id · session_ref · context · iteration_step · trigger · failure_mode · change · before_after{before_ref, after_ref, screenshot_refs} · evidence(validator-replayable shapes) · signal_strength(anecdote|repeated|cross_session) · generalizable_principle · residue · promoted_to(pattern_id|null)`
**Honesty rule:** `signal_strength=anecdote` ⇒ `promoted_to` may not target a validator *hard_gate*.

## Artifact schema B — `ux-pattern` (architecture-pattern-inventory card + 2 intake blocks)
`pattern_id · name · intent · problem · solution · when_to_use · anti_pattern · forces · evidence_link · status(seed|calibrated|promoted) · residue · consumer_intake.validator{claim_class, mode, feeds_field} · consumer_intake.studio{intent, comment_event_template, mutation_task}`
**Anti-overbuild guard (F2/Role B):** a field may only assert a consumer check if it names the exact consumer field it feeds.

## Consumer contracts
- **ux-evidence-validator:** ux-pattern → a **claim map pre-sorted into the validator's five authority classes** (hard_gate / soft_flag / screenshot_review / human_study / not_automatable), entering at `mode=spec` then `fixture-plan`→`calibrate`. ux-lessons never runs the harness. *(Ready path.)*
- **ui-prototyping-studio:** ux-pattern → `CommentEvent{target{odId,selector,elementLabel}, severity, intent, note}` → `MutationTask{odId, changeType}`. The **variant-generation / fitness** intake is a named upgrade **deferred behind studio OQ-5** + a missing axe/layout evaluator. *(Annotation path ready; variant path deferred.)*

## Boundary preserved
ux-lessons = producer/translator only. It emits intents and cards; the consumers own execution. (Dispatch boundary_evidence b1/b2/b3.)
