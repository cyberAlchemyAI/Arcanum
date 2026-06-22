# Implementation Layering — refine-improvement fixes

> Authored by `invoke plan`. Source of truth for issues: `../findings.md` (research
> dispatch 2026-06-18) and `../../../../../.arcanum/observability/reflections/20260618T144353Z-refine-reflection.md`
> (workflow-reflect P1–P3). Value/cost layering: each layer promotes only on evidence
> from the layer below (no preference-only promotion).

## Layer boundary heuristic

Boundaries cut on **trust + dependency**: a fix is in a lower layer when it is cheaper,
higher-trust, and a prerequisite for honestly evaluating the layers above it. Measurement
honesty is L0 because **every other fix is unmeasurable until the harness stops certifying
empty runs as healthy** (findings §4; reflection P1).

## Layers

### L0 — Honest measurement (minimum working unit, highest trust)
- **C6** — `REFINE_LIVE_VALIDATION` must require a *completed run* (terminal artifact +
  no blocked required stage; the shared "completed run" definition, findings §2).
- Owner: harness owner. Witnessed: validator + run (`runs/20260525T002839Z.md`).
- **Promotion evidence to L1:** a fixture all-blocked run yields `flag`/`block`, a
  completed run yields `pass`.

### L1 — Observe the real surface
- **P1** — repoint signal-observer `target_artifact` to native `arcana/refine/SKILL.md`
  and emit on native skill/subagent invocation (today 35/35 signals are the deprecated
  `.codex/commands/refine.md`, `mode: command`).
- **P2** — substantive reflection: carry `workflow_gaps` detail / defer to `workflow-reflect`
  at threshold instead of the fixed two-line boilerplate (11 prior boilerplate reports).
- Owner: observability / signal-observer.
- **Depends on L0:** honest status must exist before we observe it on the native path.
- **Promotion evidence to L2:** a native refine run appends a signal with `mode != command`
  and `target_artifact = arcana/refine/SKILL.md`; a `reflect-now` report names a target section.

### L2 — Fitness at the handoff (refine contract)
- **C3** — hire-ability route predicate: `RESULT.md` `## Recommended Next Route` names ≥1
  owner-unit (SWU/task id) with (i) precondition/ordering, (ii) done-criterion, (iii) no
  unresolved blocker (findings §2 pinned definition; verified discriminating).
- **P3** — missing-target UX: prompt for a target rather than hard-block (gap G2).
- Owner: refine-sigil maintainer (+ ownership-boundary review for C3 vs dispatch-spec).
- **Depends on L1:** need the predicate's pass/fail to be observable on real runs.
- **Promotion evidence to L3:** the predicate passes `schema-readiness/RESULT.md` and fails
  the all-blocked 05-24 run, enforced as a gate (not luck).

### L3 — Hardening
- **C2 / C1** — keep path-to-first-value lean on cold targets: a refined seed reachable
  without a fully validated `REFINE-DISPATCH.json` (cold-start brittleness residue).
- **C7** — borrow `check-tension` *discipline* (behavior, four-test) at refine's spawn gate
  (process step 11), before operator confirm. Not the ledger/dispatch_type form.
- Owner: refine-sigil maintainer.
- **Promotion evidence (release):** cold target produces a seed under the `compact` preset
  even when dispatch validation would block; an untensioned sibling set is returned to the
  strategist before confirm.

## Not a layer — recorded decision
- **C4** — no new `/refine` mode is earned; variation stays carried by preset × overlay ×
  seed-needed decision. Record as a standing decision, do not add modes.

## Deferred (future-work, out of this work-pack)
- **C8** maximal dispatch-algebra integration (owner: dispatch-spec) — referents empty today.
- **C9** early Distill anti-anchor gate — controls timing not adversariality.
- **C10 / `reframe`** Distill emits a solution-independent problem statement; late governed
  Design fork — leading anchoring candidate, promote only when a problem-class the existing
  axes cannot express is witnessed.
