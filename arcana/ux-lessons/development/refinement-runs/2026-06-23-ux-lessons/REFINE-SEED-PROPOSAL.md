# Refine Seed Proposal — `ux-lessons`

- **Run id:** 2026-06-23-ux-lessons
- **Owner:** refine
- **Preset:** standard
- **Research mode:** research-if-gap-appears
- **Staging:** `arcanum/arcana/ux-lessons/development/refinement-runs/2026-06-23-ux-lessons/` (public arcanum, operator-selected)

## Raw operator intent

> Create a new sigil called `ux-lessons`. It translates what a session like this — iterating a page (the x-ray HTML: revert-3D → offset cascade → nested overlay sub-stack → right-rail inspector → optional guided tour) — into "lessons learned," saves each as a **lesson**, and the lesson is transformed into a reusable **ux-pattern** we want to save and reuse. Later this is consumed by `projects/ui-prototyping-studio/` and `arcanum/arcana/ux-evidence-validator/`.

## Target boundary

The **capability design** of `ux-lessons` — its pipeline, artifacts, owner boundaries, and consumer contracts. NOT its implementation, and NOT the build of the package (that is a recommended next route).

## Refinement objective

Produce a refined seed + design + non-executed plan that:

1. Maps the pipeline `session evidence → lesson → ux-pattern → consumer intake`.
2. Resolves whether `ux-lessons` is a **sigil**, a **spell** (composition), or a **discipline**.
3. Names the **lesson** and **ux-pattern** artifact schemas.
4. Resolves owner boundaries against in-repo precedent (build-from-owned, not net-new).
5. Defines the **two consumer contracts**:
   - `ux-evidence-validator` — pattern → validator-safe checks / fixture intents.
   - `ui-prototyping-studio` — pattern → variant-generation / annotation intents.
6. Recommends the build route (sigil-development or spellcraft).

## Source context (in-repo precedent — build-from-owned)

| Owner | What it already does | Relation to `ux-lessons` |
| --- | --- | --- |
| `workflow-reflect` | accumulated observability signals → workflow improvement proposals | closest cousin for "session → lessons"; reuse its session-analysis shape |
| `architecture-pattern-inventory` | reusable pattern inventory package (concept cards, dependency rules) | precedent for the "save reusable pattern" half; mirror its store shape |
| `signal-observer` / observed-invocation-loop / observability | per-run telemetry substrate | the session-signal input substrate |
| `distill` | reduce to smallest coherent unit | lesson → pattern distillation |
| `residuality-spec` / `whisper` residue | learning residue precedent | residue ledger shape |
| `ux-evidence-validator` (consumer) | UX evidence → Playwright validator checks/fixtures | downstream consumer #1 |
| `ui-prototyping-studio` (consumer) | explore/annotate/mutate UI loop, governance | downstream consumer #2 |

## Write scope

Only this run folder under arcanum. No package creation, no consumer-side edits, no commits.

## Done criteria

- `REFINE-DISPATCH.json` authored and validated (or blocked with exact missing fields).
- 10-stage loop materialized with receipts or blocked reasons.
- Tensioned subagent receipts (Role A precedent/boundary auditor, Role B reuse architect) recorded.
- `toy_game` falsification run on the x-ray session, with an evidence artifact.
- `RESULT.md` with refined synthesis + recommended next route.

## Validation surface

- dispatch-spec route-shape validation.
- evidence/inference boundary preserved in every stage artifact.
- precedent sweep completed before any net-new verdict (build-from-owned rule).
- toy_game produces a concrete ux-pattern from the x-ray session that both consumers can ingest, or the design is flagged.

## Planned stage configuration

Canonical 10-stage loop at `standard` depth. Subagent pair (recommended, approved) runs at stages 3 and 7. Overlays: `baseline_sequence`, `xray_for_hidden_structure`, `route_menu_for_ambiguity`, `memory_residue_for_context_recovery`, `toy_game_for_low_cost_falsification`. Conditional: `tournament_for_alternatives`, `dialectic_for_tension` (trigger only if Design surfaces scored alternatives / contested ownership).
