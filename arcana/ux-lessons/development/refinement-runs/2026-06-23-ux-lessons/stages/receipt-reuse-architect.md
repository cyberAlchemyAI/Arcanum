---
role_id: reuse_architect
run: 2026-06-23-ux-lessons
stage: refinement-runs / receipt
confidence: med
---

# Receipt — reuse_architect

`role_id`: **reuse_architect** (tensioned pair member; bias = **maximize reuse richness**)

## findings

Four deliverables, all grounded in the two consumers' real intake contracts:

- **Consumer #1 — `ux-evidence-validator`** (`arcanum/arcana/ux-evidence-validator/SKILL.md`): modes `research | spec | fixture-plan | calibrate | validate-interface | report`; turns UX claims into one of five claim classes (`hard_gate | soft_flag | screenshot_review | human_study | not_automatable`); layered L0–L6 validator contract; refuses to promote cognitive/market claims into hard gates without a conservative UI **proxy** + fixture evidence. A `ux-pattern` must therefore arrive already pre-sorted into "what is a deterministic proxy check" vs. "what is a soft flag / screenshot-review / human-study residue."
- **Consumer #2 — `ui-prototyping-studio`** (`projects/ui-prototyping-studio/SPEC.md` §2,§4,§5): the explore/annotate/mutate loop. Real intake contracts are the `CommentEvent` `{target:{odId,selector,elementLabel}, severity, intent, note}`, the `MutationTask {odId, changeType: add|remove|change}`, `GenerationMode {explore, exploit}`, and the **deferred** L5+ UX-constraint fitness (`FitnessSignal`/`FitnessVector`, hard-gate-vs-soft-gradient split, blocked by **OQ-5**). A `ux-pattern` must emit annotation/variant intents that snap onto exactly these fields and nothing the studio can't consume.

The 1 worked example is **`detail-beside-the-subject`** (a.k.a. *no-divided-attention inspector*), distilled from the x-ray session's move from a popup/drill overlay to a sticky right-rail inspector sitting **beside** the layer stack.

---

## lesson_schema

A `lesson` is one captured unit from a single page-iteration session — the raw, still-contextual record before distillation. Fields:

| field | type | meaning |
|---|---|---|
| `lesson_id` | slug | stable id, e.g. `2026-06-22-refine-xray/inspector-beside-stack` |
| `session_ref` | path/url | the iteration session it came from (e.g. `refine-skill-xray.html`) |
| `captured_at` | date | when the lesson was lifted |
| `context` | text | what was being built + the surface (artifact type, viewport, domain tag — reuses validator domain tags: dashboard/authoring/data-tool/…) |
| `iteration_step` | text | which move in the session (`revert-3D → offset-cascade → in-place nested sub-stack → right-rail inspector → guided "build the stack" tour`) |
| `trigger` | text | the felt problem that forced the change (the "why we touched it") |
| `failure_mode` | enum-ish | named UX failure the trigger is an instance of (e.g. `divided-attention`, `hover-trap`, `cold-start-overwhelm`, `false-depth`) |
| `change` | text | the concrete edit made to the page |
| `before` | {desc, evidence_ref} | prior state + screenshot/measurement path |
| `after` | {desc, evidence_ref} | new state + screenshot/measurement path |
| `evidence` | list | screenshots, DOM measurements, ARIA snapshots, console/network — **same shapes the validator emits** under `output/playwright/ux-validator/<run-id>/` so a lesson's evidence is validator-replayable |
| `signal_strength` | enum | `anecdote \| repeated-in-session \| cross-session` (honesty floor on how proven it is) |
| `generalizable_principle` | text | the candidate one-liner that could outlive this page (the seed of a `ux-pattern`) |
| `residue` | list | subjective/comprehension/trust claims that are **human-study**, kept as residue, never auto-promoted |
| `promoted_to` | pattern_id\|null | the `ux-pattern` this lesson was distilled into (null until distilled) |

Honesty rule (mirrors validator quality-bar): a lesson with only `signal_strength: anecdote` may be captured but **must not** be promoted into a `hard_gate` intake on either consumer — only into soft/screenshot/human-study lanes.

---

## ux_pattern_schema

A `ux-pattern` is the reusable distillate — pattern-card shaped (mirrors `architecture-pattern-inventory` concept-card form) **plus two consumer-intake blocks** so it is honestly consumable, not just readable. Fields:

| field | meaning |
|---|---|
| `pattern_id` | stable slug, e.g. `detail-beside-the-subject` |
| `name` | human name |
| `intent` | one-sentence "what it buys the user" |
| `problem` | the recurring UX failure it answers (links the lesson `failure_mode`) |
| `solution` | the structural move, stated independent of any one page |
| `when_to_use` | observable trigger conditions (the "use X when Y" guard form the x-ray session itself models) |
| `anti_pattern` | the wrong-but-tempting alternative it displaces (e.g. modal/popup that hides the subject) |
| `forces` | the trade-offs in tension (screen real-estate vs. context retention, etc.) |
| `evidence_link` | back-refs to the source `lesson_id`(s) + their evidence paths; `signal_strength` carried up |
| `consumer_intake.validator` | **block A** — see consumer_mappings (claim class + mode + proxy) |
| `consumer_intake.studio` | **block B** — see consumer_mappings (annotation + variant intents) |
| `status` | `seed \| calibrated \| promoted` (a pattern is `seed` until at least one validator fixture and one studio variant have exercised it) |
| `residue` | un-automatable claims kept explicit |

Anti-overbuild guard baked into the schema: every field except the two `consumer_intake` blocks is **descriptive**; the consumer blocks are the only fields that may assert a check or a generation rule, and each such assertion **must name the exact consumer field it feeds** (validator claim-class or studio `CommentEvent`/`MutationTask`/`FitnessSignal` field). A pattern that cannot fill at least one real consumer field is a note, not a `ux-pattern`.

---

## consumer_mappings

### (a) `ux-pattern → ux-evidence-validator`  (`consumer_intake.validator`)

The pattern is pre-sorted into the validator's five claim classes; each entry names the **mode** that ingests it and the **proxy** it feeds (so cognitive claims never enter a hard gate raw):

| pattern aspect | claim_class | feeds mode | what it becomes |
|---|---|---|---|
| structural/deterministic part (e.g. "detail panel and subject are both in-viewport together; no occluding overlay") | `hard_gate` | `spec` → `fixture-plan` → `calibrate` | a layout/DOM-measurement proxy check (bounding-box co-visibility, `aria-modal` absence) with known-good/known-bad/false-positive fixtures |
| attention/comprehension benefit | `soft_flag` | `spec` | a non-blocking flag with a conservative UI proxy, cited to the source lesson |
| visual "reads clearly beside the subject" | `screenshot_review` | `validate-interface` → `report` | a screenshot-review item under `screenshots/*.png`, stable-viewport |
| "reduces cognitive load / divided attention" | `human_study` | `report` (residue) | a residue-ledger entry — reported, never automated |
| anything geometry the pure lane can't judge | `not_automatable` | — | left to the studio accept-diff human eye (mirrors studio `AC-L0-16`) |

Net: a `ux-pattern` arrives at the validator already shaped as a **claim map**, so its `research`/`spec` modes have less to invent, and its refusal-to-promote rule is satisfied by construction.

### (b) `ux-pattern → ui-prototyping-studio`  (`consumer_intake.studio`)

Two sub-intents, both snapping onto fields that exist in code (SPEC §4/§5):

1. **Annotation intent** → a `CommentEvent` template: `{target:{odId, selector, elementLabel}, severity ∈ {blocker,high,medium,low}, intent, note}`. The pattern supplies a reusable `intent` verb + canned `note` and a target *role hint* (which `data-od-id` role to attach to), so reviewing a fresh prototype against the pattern emits ready comments → folds to `MutationTask {odId, changeType: add|remove|change}`.
2. **Variant/fitness intent** → drives `GenerationMode`: as an `explore` **boundary** (sample variants that all satisfy the pattern's hard-gate proxy) or an `exploit` **gradient** (climb the pattern's soft score from head). This rides the **deferred** L5+ UX-constraint fitness (`FitnessSignal`/`FitnessVector`) — explicitly gated by **OQ-5** (soft-score weights uncalibrated) and dependent on the Playwright axe/layout evaluator that "does not exist in code." So this intent ships as a **named upgrade**, not a live claim: today it lands only as the lighter heuristic + the annotation intent above.

---

## worked_example

`ux-pattern: detail-beside-the-subject` — fully filled:

- **pattern_id**: `detail-beside-the-subject`
- **name**: Detail beside the subject (no-divided-attention inspector)
- **intent**: Let a reader inspect a thing's detail *without losing sight of the thing*.
- **problem**: `divided-attention` — a popup/drill/modal shows detail but occludes or scrolls away the subject, forcing the reader to hold the subject in memory.
- **solution**: Render detail in a persistent surface laid **alongside** the subject (sticky side rail), so subject + detail are co-visible; reserve full-overlay drill only for genuinely deeper sub-topology.
- **when_to_use**: the user hovers/selects items in a list/stack AND needs the item's properties while keeping positional context (the x-ray layer stack ↔ inspector rail).
- **anti_pattern**: a centered modal / tooltip-that-covers-the-row / a drill panel that replaces the stack — detail at the cost of the subject. (The session literally reverted a popup/3D treatment toward the side rail.)
- **forces**: horizontal real-estate (needs ~330–384px rail) vs. context retention; collapses to stacked single-column under ~980px (responsive escape hatch present in the source page's media query).
- **evidence_link**: `lesson_id: 2026-06-22-refine-xray/inspector-beside-stack`; before = drill-only overlay; after = sticky `.inspector-rail` beside `.deck`; `signal_strength: repeated-in-session` (the session converged on it across iterations). Evidence: layout bounding-box co-visibility + screenshots (to be captured under the validator's run root).
- **status**: `seed` (no validator fixture / studio variant has exercised it yet).
- **consumer_intake.validator**:
  - `hard_gate` (mode `spec`→`fixture-plan`→`calibrate`): proxy = "inspector container and selected-subject container are both within viewport bounds AND no ancestor has `aria-modal=true`/occluding overlay over the subject." Fixtures: good = side-rail page; bad = modal-over-subject page; false-positive = legitimately dense expert layout (don't over-block).
  - `soft_flag` (mode `spec`): "detail reachable without dismissing context."
  - `screenshot_review`: rail-beside-stack render at stable viewport.
  - `human_study` (residue): "reduces divided-attention cognitive load" — reported, not measured.
- **consumer_intake.studio**:
  - annotation intent → `CommentEvent {target:{odId:"inspector.rail"|"detail.panel"}, severity:"high", intent:"relocate-detail-beside-subject", note:"move this detail out of the overlay into a side rail co-visible with the subject"}`.
  - variant intent → `explore` boundary: "generate variants whose detail surface is a side rail, all clearing the co-visibility hard-gate proxy"; `exploit` gradient deferred behind OQ-5.
- **residue**: the cognitive-load and "feels less effortful" claims stay human-study; the responsive-collapse threshold is a tuning value, not a universal.

---

## anti_bias_note

My declared bias is **maximize reuse richness** — I want the `ux-pattern` schema to carry as many honestly-consumable facets as possible (claim map + dual intake + forces + residue). Where this risks over-building:

1. **`consumer_intake.studio` variant/fitness intent** is the biggest over-reach risk: it leans on the studio's L5+ UX-constraint fitness, which is **deferred and OQ-5-blocked**, with no axe/layout evaluator in code. I marked it a *named upgrade*, not a live field — but a richness-maximizer (me) is tempted to spec it as if shippable. The tensioned minimalist should push the live `ux-pattern` to ship with **only** the annotation intent (block B reduced to the `CommentEvent` template) until OQ-5 closes.
2. The `forces`, `signal_strength`, `residue`, and `failure_mode` fields are rich but only earn their place if *something* reads them. `failure_mode`/`signal_strength` are load-bearing (they gate hard-gate promotion); `forces` is currently human-read only — a candidate to drop if nothing consumes it.
3. Risk of a pattern with five claim-class entries but zero fixtures: the `status: seed→calibrated` gate exists precisely to stop a rich-looking pattern from masquerading as proven. Keep it strict.

Counter-bias hook for my pair: challenge every field that does **not** name a consumer field it feeds.

## blocked_reason

none. All four deliverables produced and grounded in read evidence (validator SKILL, studio SPEC §2/§4/§5, pattern-inventory card shape, the x-ray session). One soft dependency flagged, not blocking: the studio variant/fitness intake (block B, part 2) cannot be claimed live until **OQ-5** (soft-score weights) closes and the Playwright axe/layout evaluator exists in code.
