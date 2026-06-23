# Whisper Preset — `veritasium`

- Preset ID: `veritasium`
- Spell: `whisper`
- Status: L0 proof preset (first run: `skill-anatomy` deep-dive surface for the CyberAlchemy docs)
- Lineage: named for the explanatory style of Derek Muller's *Veritasium* — and grounded in his
  education-research finding that exposition only sticks once the reader's **existing (wrong or
  partial) mental model is surfaced and broken first**. Confusion-then-resolution beats clean telling.

## What this preset is

A preset is a **frozen, reusable selection across the three Whisper SCU cores plus a technique
set** — a saved "voice + stance + movement" that the composition plan (Phase 4) can load instead of
re-deriving from scratch. It does **not** skip the lifecycle: intake, distillation, the SCU
tournament, validation, and residue still run. The preset seeds the tournament with a strong,
opinionated default and tells validation what "good" looks like for this voice.

Use `veritasium` when the transport is **explanatory / didactic** — teaching one counter-intuitive
idea to a curious non-expert by demolishing the obvious model first, then rebuilding it with a
concrete instrument the reader can manipulate, and finally zooming out to the governing principle.

## SCU core selection

### `resonance_core` — the felt meaning

| Field | Value |
| --- | --- |
| tone | curious, warm, slightly conspiratorial — "let me show you something weird" |
| voice | second person, present tense, direct address; the author is a guide standing next to the reader, not a lecturer above them |
| style register | plain language, short declaratives, one idea per sentence; technical terms are earned, never assumed |
| emotional residue | the satisfying *click* of a model snapping into place — "oh, it was never what I thought" |
| value signal | honesty about the limits of the claim; the reader is trusted to handle "here's what I actually know vs. what I'm inferring" |
| forbidden feels | smug, encyclopedic, brochure-like, "as we all know", front-loaded jargon, hype |

### `relevance_core` — why it belongs to this reader

| Field | Value |
| --- | --- |
| target public | a curious, intelligent reader who is **not** an expert in the subject; assumes a wrong-but-reasonable prior model |
| reader state | mildly skeptical, time-pressured, has seen explainers before and distrusts the genre's tendency to flatter |
| domain | any single concept with a load-bearing counter-intuitive core (here: "a skill is layered control, not a list of instructions") |
| authority mode | demonstrate-don't-assert; lean on an instrument the reader can poke at, and on a visible source/inference boundary |
| assumptions | the reader already holds a default mental model worth naming out loud |
| objections | "this is obvious", "this is hand-wavy", "you're overcomplicating it" — each must be pre-empted by showing, not telling |

### `trajectory_core` — the movement the text performs

| Field | Value |
| --- | --- |
| objective | replace one wrong/partial model with a sharper one, and make the upgrade *felt*, not just stated |
| transport type | `explanatory_deep_dive` (extension of the L0 substrate; not fundraising, not pure post) |
| narrative anchor | **one** concrete artifact the whole piece dissects (the worked example), e.g. the `/refine` skill |
| structure | misconception → dissonance → reveal → instrument → guided walk → boundary → zoom-out-to-principle |
| introduction policy | open on a curiosity gap or a named wrong assumption; never open on a definition or a table of contents |
| body parts | (1) name the obvious model, (2) break it, (3) the one true idea, (4) hand over the instrument, (5) walk the parts using the instrument, (6) the honesty boundary, (7) close the loop to the larger system |
| ending | zoom out: the specific case was an instance of a general principle; route the reader onward |
| length | medium-long; long enough to earn the reveal, short enough that every section pays for itself |

## Technique set (narrative primitives)

| Technique | Job in this preset |
| --- | --- |
| **misconception-first** | State the reader's likely current model in plain words *before* correcting it. This is the load-bearing move — skipping it makes the reveal land flat. |
| **curiosity gap** | Pose a question whose answer is withheld, so the reader reads on to close it. |
| **concrete-before-abstract** | Always a tangible instance first; the principle is *induced* from it, never declared up front. |
| **the turn / reveal** | A pivot sentence — "but here's the strange part" — that marks the shift from old model to new. |
| **show-don't-tell instrument** | Hand the reader something interactive/manipulable (here: the x-ray) so the claim is *demonstrated*, not asserted. |
| **honest boundary** | Explicitly separate what is established from what is interpretation (maps to the x-ray's quote=source vs mechanism=inference, and to CyberAlchemy's claim≤proof discipline). |
| **zoom-out close** | End by connecting the single example to the governing system, so the reader leaves with a transferable principle, not a trivia fact. |

## Pareto note

`veritasium` deliberately spends its budget on **trajectory** (the misconception→reveal→zoom-out arc)
and the **honest boundary** of resonance. It is *non-dominated* against a plain "explainer" candidate
because it trades a little length and up-front tension for far higher model-update and retention — the
documented Veritasium effect. Do not let a competing candidate win purely on brevity or polished tone;
under this preset, a piece that explains correctly but never first names and breaks the wrong model has
**failed the core gate**, not merely scored lower.

## Validation checklist (what a `veritasium` draft must pass)

1. The reader's prior/obvious model is **named explicitly** before it is corrected.
2. There is a clear **turn** — a single identifiable pivot from old model to new.
3. The new model is **demonstrated** via a concrete instrument or example, not only asserted.
4. The piece states its **honesty boundary** (what is known vs. inferred).
5. It **zooms out** at the end to a principle larger than the worked example, with an onward route.
6. No section opens cold on jargon or a definition; every term is earned.
7. Forbidden feels (smug / brochure / encyclopedic) are absent.

## First proof run

- Transport: `explanatory_deep_dive`
- Artifact produced: `arcanum/docs/skill-anatomy.html` — a deep-dive mini-course that uses the existing
  `refine-skill-xray.html` as the show-don't-tell instrument, teaching "a skill is a layered stack of
  nudges" and closing the loop back to the CyberAlchemy method.
- Residue: see the spell's learning residue for this run.
