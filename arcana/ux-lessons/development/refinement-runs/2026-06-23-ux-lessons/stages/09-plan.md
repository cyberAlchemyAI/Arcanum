# Stage 9 — Invoke Plan (non-executed)

- **Capability:** invoke · **Mode:** plan · **Status:** pass · **This is a plan, not execution.**

## Build route
Recommended next route: **sigil-development** (create the thin `ux-lessons` sigil package). Not spellcraft — the artifact schemas need a single owner.

## Layered plan (MWU → hardening)

**L0 — Minimum working unit (prove the transform).**
- Author `arcanum/arcana/ux-lessons/SKILL.md` (seed) with the 5 modes, `lesson` + `ux-pattern` schemas, honesty rule, evidence enum, boundary section.
- Add `templates/lesson.md`, `templates/ux-pattern.md`.
- Hand-run `capture`→`distill`→`emit-*` on the x-ray session (already proven in stage 8) and commit it as the first example under `examples/`.
- Done when: one real session → one ux-pattern → both consumer intents, no invented fields.

**L1 — Validator adapter (the ready consumer).**
- Specify `emit-validator`: ux-pattern → claim map across the 5 authority classes → handoff into ux-evidence-validator `mode=spec`. No harness code here.
- Done when: a ux-pattern produces a validator-ingestable claim map with good/bad/false-positive fixture stubs.

**L2 — Studio annotation adapter (ready half).**
- Specify `emit-studio`: ux-pattern → `CommentEvent`→`MutationTask`. Validate the shape against ui-prototyping-studio SPEC.
- Done when: a ux-pattern emits a studio-valid annotation intent.

**L3 — Store integration.**
- Store ux-patterns as `ux`-tagged architecture-pattern-inventory cards; no new store.

**L4+ — Deferred (named unblock conditions).**
- Studio variant/fitness intake — blocked on studio OQ-5 + an axe/layout fitness evaluator.
- Cross-session promotion (anecdote→repeated→cross_session) — needs accumulated lessons.
- External UX-pattern-format alignment — bounded-research follow-up.

## Validation surface for the build
- Each adapter names the exact consumer field it feeds (anti-overbuild guard).
- Honesty rule enforced in the schema/template.
- No duplication of the 5 composed owners (boundary check).
- claim ≤ proof: ships as seed; promotion needs experiment-harness evidence.

## Out of scope (not this build)
Consumer-side code changes in ux-evidence-validator or ui-prototyping-studio; running the validator harness; promotion to non-seed status.
