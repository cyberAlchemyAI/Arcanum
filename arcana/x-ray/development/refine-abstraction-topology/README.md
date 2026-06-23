# x-ray default explanation — Refine: abstraction & nudge topology

A reusable, self-contained x-ray that dissects the `refine` sigil into the stack
of language layers it uses to steer an LLM. Saved as a **default explanation**
example for the `x-ray` sigil: a worked demonstration of an *extended* renderer
(beyond the baseline four-lane L0 page).

- **Artifact:** [`refine-abstraction-topology.html`](./refine-abstraction-topology.html) — open directly in a browser. No build, no network, no remote rendering.
- **Target:** `arcana/refine/SKILL.md` (v0.2.0).
- **x-ray mode:** `artifact` (the lane focus is the *abstraction stack* of a skill spec, not a system's runtime).
- **Renderer level:** L0 (HTML/CSS only). Not the canonical four-lane toggle page, so it intentionally does **not** satisfy `scripts/validate-xray-example.py`; it lives here in `development/`, not in the validated `examples/` set.

## What it explains

A skill file is not one instruction — it is a **stack of control layers**, each
using a different linguistic device (a "nudge") at a different altitude of
abstraction. The page renders `refine` as **13 layers across 8 bands**, floor →
surface:

| # | Layer | Band | Nudge device (inference) |
|---|-------|------|--------------------------|
| 1 | Invocation contract | Contract | trigger phrasing + tool allow-list |
| 2 | Identity frame | Frame | role naming + domain mystique vocabulary |
| 3 | Mission objective | Frame | one compound sentence spanning the whole arc |
| 4 | Invariant skeleton | Structure | fixed ordered list + "do not remove" guard |
| 5 | Ownership partition | Structure | who-owns-what table |
| 6 | Conditional overlays | Discretion | "use X when Y" rules + named overlay enums |
| 7 | Mode enums + defaults | Discretion | closed enum of named modes with a default |
| 8 | Stop gates | Control | imperative stop conditions + blocking verbs |
| 9 | Proof obligation | Proof | validity predicate + artifact-or-blocked rule |
| 10 | Negative space | Control | prohibition lists + named failure modes |
| 11 | Acceptance rubric | Proof | self-evaluation checklist |
| 12 | Output schema | Form | fill-in template with fixed fields |
| 13 | Reflexive telemetry | Reflexive | post-run signal field list |

### Recursion: Layer 6 is itself a stack

The **Conditional overlays** layer expands in place into its own sub-topology:
atomic techniques chunked into 8 named, evidence-gated overlays (1 default +
7 optional), each with its own trigger, technique bundle, validation rule, and
its own device + nudge. The same chunk-and-gate move the whole skill makes,
made again one level down. Source: `arcana/refine/SKILL.md`
`<technique-overlay-policy>` (lines 107–132).

## Interaction modes (in the page)

- **Stacked deck** — the 13 layers as an accordion; hovering a card pops it open
  (full mechanism text) while the cards below slide down so the next lip stays
  reachable. Hovering Layer 6 opens its nested overlay stack inline.
- **Right rail inspector** — tracks the cursor: shows the hovered layer's (or
  nested overlay's) source quote + device + nudge beside the stack, so reading
  the stack and its explanation share one focus.
- **Drill-in panel** — the full Layer-6 overlay sub-topology (triggers, bundles,
  validation, per-overlay device + nudge).
- **Reasoning traces** — pick a moment ("`$refine … MVP-ready`", "tempted to do
  external research", "wants to skip a stage") and watch which layers fire, in
  order — proof that one reasoning act is steered by several layers at once.
- **Guided tour** *(optional)* — constructs the stack one layer at a time with a
  narration of *why* each layer is added next; ← → keys, progress bar, exit.
- **Strata · flat** — all 13 layers fully expanded for linear reading.

## Evidence boundary

- **Source-backed:** every quote, section name, line reference, and the overlay
  triggers / technique bundles / validation rules are lifted verbatim from
  `SKILL.md`.
- **Inference (flagged in red-dashed UI):** the "device" labels, the "how it
  nudges the LLM" column, the band groupings, and the trace orderings are an
  interpretation of *why* the language is shaped that way — not claims the skill
  makes about itself. Trace orderings are illustrative, not guaranteed execution
  order.

## Reuse

Treat this as the default reference when an x-ray target is **a skill / prompt /
spec viewed as a layered abstraction stack** (rather than a runtime system).

Libraryization status (per the componentize run,
`refinement-runs/20260623-componentize-xray-explanation/RESULT.md`). Reuse claims
must be YAML records with a declared `intended_lane`, not prose — so:

- **Promoted to the canonical library now:** the cursor-tracking rail
  (`shape.inspector-rail` in `library/components.yml`) and the source/inference
  visual treatment (recommended under `pattern.evidence-inference-split` in
  `library/patterns.yml`).
- **Bespoke candidates, not yet libraryized:** the floor→surface layer ladder,
  band grouping, in-place recursive sub-stack, reasoning traces, and the guided
  tour. These are blocked on two governance additions before they can be
  schema-valid reusables: an `interaction` component family (now added) with
  real records, and an `ordered-ladder` lane genre enforced by the example
  validator (declared in the lane-model schema; enforcement still TODO). The
  toy-game test showed only the two promoted units survive a change of target.

> Note: this folder lives inside the public `arcanum` submodule. Per submodule
> discipline, commit here first and bump the parent gitlink second; nothing is
> committed by saving the files.
