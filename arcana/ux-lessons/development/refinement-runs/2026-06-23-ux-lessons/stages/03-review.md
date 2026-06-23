# Stage 3 — Interrogation refine-review (with tensioned subagent pair)

- **Capability:** interrogation · **Mode:** refine-review · **Pattern:** fanout (dialectic) · **Join:** parent_synthesis · **Status:** pass

## Subagent receipts joined
- `stages/receipt-precedent-boundary-auditor.md` (Role A, bias: minimize new surface)
- `stages/receipt-reuse-architect.md` (Role B, bias: maximize reuse richness)
- Anti-bias axis: **minimize-new-surface ⇄ maximize-reuse-richness.**

## Role A verdict (summary)
- 5 of 6 pipeline stages already owned (signal-observer/observed-invocation-loop, workflow-reflect, distill, architecture-pattern-inventory, residuality-spec).
- Only genuinely new thing: the UX framing of `lesson`/`ux-pattern` + the two-direction consumer adapter.
- Shape: **spell, not net-new sigil.** Biggest duplication risk: a second pattern store paralleling architecture-pattern-inventory.
- **Anti-bias caveat (load-bearing):** a spell owns no artifact schema, yet lesson/ux-pattern ARE new typed artifacts — if the schema+adapter is rich enough, a *thin sigil composing the owners* beats a schema-less spell.

## Role B verdict (summary)
- Rich `lesson` and `ux-pattern` schemas; honesty rule: anecdote-only lessons cannot promote to a hard gate.
- Validator intake = a pre-sorted claim map across the validator's five authority classes → satisfies its refuse-to-promote rule by construction. **This path is ready.**
- Studio intake = annotation intent (`CommentEvent → MutationTask`) is ready; the **variant/fitness** half is a named upgrade deferred behind studio **OQ-5** + a missing evaluator.
- Worked example: **`detail-beside-the-subject`** (no-divided-attention inspector) from the x-ray session.
- **Anti-bias note:** the studio fitness intake is the over-reach; every schema field must name the consumer field it feeds.

## Parent synthesis (adjudication of the tension)
The two biases converge on a **thin sigil**:
- Role A is right that ux-lessons must NOT own session capture, generic storage, or residue mechanics → **compose** those owners.
- Role B is right that `lesson` + `ux-pattern` are real typed artifacts with a non-trivial two-consumer contract → they need **a single owner with a schema**, which a schema-less spell cannot provide.
- Therefore: **thin sigil that owns ONLY the two artifact schemas + the two adapters, and composes the five existing owners.** This is build-from-owned (Role A's rule) WITH a real contract (Role B's requirement).

## Flags carried forward
- F1 (boundary): never fork architecture-pattern-inventory's store mechanics — borrow its card shape, store ux-patterns through/alongside it. → Design must state the store relationship.
- F2 (honesty): enforce the anecdote→no-hard-gate rule in the schema.
- F3 (scope): ship the **validator adapter + studio annotation adapter** first; defer studio variant/fitness intake behind OQ-5.
