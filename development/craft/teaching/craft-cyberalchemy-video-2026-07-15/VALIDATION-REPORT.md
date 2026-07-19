# Validation Report

Date: 2026-07-15
Verdict: **PASS for production-package readiness; candidate for transport and
learning proof**

## Scope

This report validates the complete text-and-model-input package for the video
essay. It does not validate generated voice quality, generated visual quality,
the final edit, or audience learning.

## Results

| Surface | Evidence | Result |
| --- | --- | --- |
| Human gate | Operator approved the opening, tension, reveal, and 10-12 minute public-explainer shape before full generation. | PASS |
| Narrative | One concrete contradiction carries the full arc; each formal term follows the visible problem that makes it necessary; Craft and CyberAlchemy are named after their mechanisms are witnessed. | PASS |
| Voice | 22 sequential segments, 1,525 words, 11:46 total runtime, and no segment above 150 estimated words per minute. | PASS |
| Written copy | Every segment owns explicit audience-facing written copy; authoring metadata remains outside the projected language. | PASS |
| Visual inputs | Every segment owns an independent prompt, negative prompt, continuity assets, motion, sound, transition, and generation-clip duration. | PASS |
| Source posture | All scene claim references resolve through `SOURCE-TRACE.md`; source, synthesis, analogy, and metaphor postures remain explicit. | PASS |
| Honesty boundary | The script does not claim scientific proof, universal formal validity, automatic epistemic authority, or audience learning. | PASS |
| Generation | `python3 build-video-package.py` generated all six projections from `SHOT-LIST.yml` and completed its schema, timing, pacing, source, and gate checks. | PASS |
| Browser, desktop | Chromium at 1440x900 rendered 22 scenes and five tabs with no horizontal document overflow and zero console errors. Scene controls, ArrowRight navigation, final-scene boundary, comments, and agent payload were exercised. | PASS |
| Browser, mobile | Chromium at 390x844 rendered the scene and tab rails as contained horizontal scrollers with no document overflow. A second 360x800 check confirmed all five tabs and the active final scene are brought into their rails when selected. The full page showed no incoherent overlap. | PASS |

## Browser Evidence

- Review URL during validation:
  `http://127.0.0.1:4177/arcanum/development/craft/teaching/craft-cyberalchemy-video-2026-07-15/review.html`
- Desktop capture:
  `output/playwright/craft-cyberalchemy-video-review-desktop.png`
- Mobile capture:
  `output/playwright/craft-cyberalchemy-video-review-mobile.png`
- Comment export preserved `segment_id`, `issue_type`, selected review surface,
  and comment text. Test comments were removed from browser storage afterward.

## Proof Boundary

The package is ready to enter voice generation, visual generation, and editing.
That readiness is not evidence that a model will interpret every visual prompt
well or that viewers will revise their prior model. Those claims require a
rendered-video review and audience evidence. The wrong-door story remains an
authorial instrument, not empirical validation of Craft.

## Remaining Residue

1. Generate representative visual clips from high-risk scenes 04, 10, 12, 14,
   and 19 before batch production; revise prompts if continuity or relational
   meaning is lost.
2. Review one generated voice pass for natural phrasing, emphasis, pauses, and
   pronunciation before locking edit timing.
3. Run a small audience comprehension check on local versus objective
   validation, residue, coherent layering, and the distinction between Craft
   and CyberAlchemy.
