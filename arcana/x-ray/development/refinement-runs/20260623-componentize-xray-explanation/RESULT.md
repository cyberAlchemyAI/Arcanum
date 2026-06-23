# Refine Result — Componentize the abstraction-topology x-ray (+ x-ray improvement)

- **Run id:** 20260623-componentize-xray-explanation
- **Target:** `arcana/x-ray/development/refine-abstraction-topology/` (the bespoke explanation) + the idea / process / components behind it, for reuse across other x-ray targets.
- **Status:** flag (MVP-ready plan produced; the headline "componentize for reuse" is only *partially* reusable now — see verdicts).
- **Preset:** standard · **Research:** no-research (local-first; no external gap surfaced).
- **Design engine:** tensioned subagent pair (component-cartographer ↔ reuse-skeptic), anti-bias axis = abstraction-maximizer vs over-generalization-minimizer. Receipts in `stages/`.
- **Evidence baseline:** x-ray library + constitution + schemas + 3 prior runs + 401-row telemetry ledger (`.arcanum/observability/signals/sigil-invocations.jsonl`).

---

## 1. Convergence (tournament / pareto gate)

The two roles disagreed productively. Convergence rule was fixed before the run:
keep a unit only if it (a) recomposes the original page, (b) composes into a
second, different x-ray target with no bespoke edits, and (c) fits the existing
YAML library schema + constitution. Applying it:

| Reuse vector | Cartographer | Skeptic | **Adjudicated verdict** |
| --- | --- | --- | --- |
| **IDEA** — skill/spec as an ordered nudge-stack with an evidence/inference split | propose as artifact-mode profile | GO — genuine transferable lens | **GO now** — register as a documented lens/profile, no code. |
| **COMPONENTS** — extract ~11 UI units | extract, ranked | NO-GO — only 2 of 8 survive a target change | **PARTIAL** — promote exactly **2** now; defer the rest behind 2 schema extensions. |
| **PROCESS** — floor→surface ladder build recipe | reusable recipe | CONDITIONAL — breaks on process/graph targets | **CONDITIONAL** — document, but gate to `ordered-ladder` targets only. |
| **TELEMETRY** (your `/workflow-reflect`) | (out of role) | green-and-thin; proposes signal fields | **GO now** — highest-value, lowest-risk improvement. |

**Decisive test (toy-game, order-ingestion `process` target):** only **2 of ~8**
components composed without bespoke edits — `shape.inspector-rail` and the
evidence/inference color treatment. Six broke on the band model (load-bearing
across 5 components), the single-direction ladder layout (a process branches), or
`refine`-specific content fixtures (`OVERLAY_SET`, `TRACES`). Reuse claim for
those six is **falsified at the first different target.**

---

## 2. What to promote NOW (low cost, compliant, real)

Two library entries into the **existing** `library/components.yml` (do NOT build a
parallel system — `component-library-nudge` + `yaml-library-refresh` already made
YAML-with-`intended_lane` the canonical source of truth):

1. **`shape.inspector-rail`** — cursor-tracking side panel rendering a hovered
   element's `{source_quote, source_ref}` beside its `{device, inference}`.
   Universally useful, light coupling, schema-valid today. The single component
   that survives a mode change.
2. **Evidence/inference visual treatment** — register the solid-border=source /
   dashed-red=inference + text-label marker as the **recommended treatment under
   the existing `pattern.evidence-inference-split`** (patterns.yml), not as new.

Both must be authored as YAML records with declared `intended_lane` +
`evidence_rule`. **Compliance fix:** the `refine-abstraction-topology/README.md`
"Reusable patterns" prose currently asserts reusable components in Markdown,
which violates `xray.visual-library.canonical-yaml`. Either back each claim with a
YAML record or relabel the list as "bespoke, not yet libraryized."

## 3. What to DEFER (blocked on schema/governance, not effort)

These are genuinely valuable but **cannot be schema-valid components today**:

- **Recursion** (`shape.nested-substack`) and **interaction units** (accordion
  push-down, reasoning-trace firing, guided tour) — the component schema's
  `allowed_families` is `shape | connector | chart` only. **Blocker:** no
  `interaction` family. Until added, these are pattern-level behavior notes at
  best.
- **The abstraction-stack renderer itself** — the lane model + `validate-xray-example.py`
  hard-code a 4-lane toggle page (`toggle-surface/flow/deps/risk` + `data-lane`).
  The ladder is a different visual genus. **Blocker:** no `ordered-ladder` lane
  genre; any ladder component lands in a validation desert.

## 4. x-ray IMPROVEMENT — telemetry / observability upgrade (your `/workflow-reflect`)

**Finding (proven):** every x-ray-touching telemetry row is
`quality_bar_status:pass`, `anti_pattern_hits:[]`, `workflow_gaps:[]`,
`output_contract_drift:false` — yet `reflection_trigger:usage-threshold` fires
repeatedly. A row at `2026-05-24T22:04:31Z` has an observer block **identical** to
a `none` row but fires `reflect-now` — proving the trigger is an **invocation
count**, not a quality signal. The real iteration we just lived (3D tilt rejected
for readability; z-index hover-trap → accordion-push; left-rail → right-rail;
nested-expand) left **zero telemetry trace**. The `ui-playwright-repair` run had
already named the recurring defect classes (overlap, hard-coded spacers, mobile
illegibility) — also invisible to telemetry.

**Proposed signal fields x-ray should emit** (none exist today):

| Field | Type | Catches |
| --- | --- | --- |
| `renderer_level_attempted` / `renderer_level_shipped` | enum L0–L4 | the 3D→L0 downgrade (single most informative UX signal) |
| `renderer_downgrade_reason` | enum {readability, validation, perf, mobile} | *why* a renderer was dropped |
| `ux_revision_count` | int | post-first-render layout reworks (hover-trap, rail move) |
| `interaction_defects_found` | list {overlap, hover-trap, hardcoded-spacer, mobile-illegible, z-index-collision} | the `ui-playwright-repair` defect classes |
| `ux_validation_evidence` | enum {none, screenshot, playwright, manual} | eyeballed vs Playwright-verified |
| `validator_status` | enum {pass, block, n/a-bespoke} | share of unvalidatable artifacts (e.g. this one) |
| `lane_genre` | enum {orthogonal-toggle, ordered-ladder, graph} | surfaces genre the validator can't cover |

**Evidence-based reflection thresholds** (replace the clock): fire `reflect-now`
when `ux_revision_count ≥ 2` in a run, OR `interaction_defects_found` non-empty,
OR `renderer_level_attempted > shipped` recurs ≥2 runs, OR `validator_status:n/a-bespoke`
exceeds a share of recent x-ray runs. Today's trigger fires on a clock and finds
nothing; these fire on evidence of rework.

---

## 5. Recommended next routes (NOT executed by this refine run)

1. **Task Session** — implement the 2 YAML library records (`shape.inspector-rail`
   + evidence/inference treatment), with `intended_lane`, and the README
   compliance fix. Smallest real reuse win; cheap; reversible.
2. **sigil-development (x-ray observability)** — add the 7 telemetry fields +
   evidence-based reflection thresholds to the x-ray signal/observer schema. This
   is the highest-leverage improvement and directly answers `/workflow-reflect`.
3. **sigil-development (lane model + validator)** — add an `interaction` family to
   `xray-component-library.schema.yml` and an `ordered-ladder` lane genre to
   `xray-lane-model.schema.yml` + `validate-xray-example.py`, so the ladder
   becomes a first-class, validatable mode.
4. **experiment-harness** — pre-register a falsifiable test: "the extracted
   components compose a second-genre (process) x-ray with ≤1 bespoke edit" before
   claiming the components reusable. (The toy-game already falsified the strong
   form; this would gate any promotion.)
5. **Register the IDEA** — document `pattern.abstraction-stack` (artifact/object
   modes) as a lens in `library/patterns.yml`, honest about its `ordered-ladder`
   precondition.

## 6. Honesty / evidence boundary

- Source-backed: telemetry fields/values, library file existence, schema field
  names, validator required-controls, prior-run outputs — all cited and re-read.
- Inference: band taxonomy, device/nudge labels, trace orderings, reuse-value
  rankings, and the proposed schema extensions are interpretation.
- This run used a **condensed subagent-driven design pass**, not the full native
  10-stage invoke/interrogation/distill chain; `REFINE-DISPATCH.json` was authored
  but **not** run through the formal `dispatch-spec` validator (flagged in
  `RUN-MANIFEST.md`). No files outside this run folder were changed; nothing was
  committed.
