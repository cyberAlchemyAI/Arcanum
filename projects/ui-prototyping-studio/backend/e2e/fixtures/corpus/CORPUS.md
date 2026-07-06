# Studio Fixture Corpus (B2 — `BLK-FIXTURE-CORPUS-001`)

A small, checked-in, self-contained corpus the test/integration surfaces run against. Seeded from the TROQAR login variants and the live `--green` honest-diff case. All HTML is self-contained (inline styles) so `getComputedStyle`/sandboxed preview render faithfully.

## Contents

| Path | What it is | Exercises |
| --- | --- | --- |
| `troqar-login/a.html`, `b.html`, `c.html` | 3 real login variants; each stamps `data-od-id` on annotatable components (a:13, b:12, c:12) — `--from` reads `<label>.html` lowercase. | generate/register variants, baseline select+commit, per-component annotate, honest per-`od-id` diff. |
| `toy-game-theme/baseline-B.html` | Variant B unchanged. | the baseline side of the theme-edit case. |
| `toy-game-theme/candidate-B-desaturated.html` | B with `--green:#1ed97a → #5fa882` (a `<style>` token edit only). | **The honest-diff falsification gate** (per-element refine S4 / `UIIdentityIndex` DD-F5): the per-`od-id` diff reports **0 changed** for this candidate because `<style>` is excluded — the toy-game asserts the surface must *not* claim "no changes." |
| `comments.json` | A sample comment set for baseline B, incl. an `odId:null` untagged-element capture. | comment capture, `listPendingComments` drain, synthesize, the untagged-capture path. |

## Pre-registered toy-game (honest-diff)

Recolor `--green` on `baseline-B.html` → `candidate-B-desaturated.html`, stage it.
**Pass:** the pending diff either shows an attributable CSS-lane row, or the surface explicitly states "theme/global edit — not an attributable per-component change."
**Fail (current code):** zero diff fragments + surface implies "no changes." This is the regression the corpus pins for the deferred S4 honest-diff work.

## Notes

- Self-contained HTML only (no external CSS/fonts) — keeps `getComputedStyle` extraction and sandboxed preview honest.
- The variants are copies (fixtures must be stable); the source of record is `development/prototype-gate/troqar-product-architecture/production-login-variants/`.
