# Craft Causal Class Validation Report

## Result

The package passes structural, interaction, rendering, and public-boundary checks.

Pedagogical effectiveness is not established by these checks. A learner trial is still required.

## Structured Package

- YAML authority parsed successfully with PyYAML.
- Deck count: 14 slides.
- Interaction-state count: 32 states.
- Slide IDs and state IDs are unique.
- Every transition points to the next declared state or terminates.
- Every earned term belongs to the seven-term deck vocabulary.
- The surface contract forbids projecting authoring metadata.
- Projected titles, prompts, and details pass the authoring-language leak guard.
- Embedded HTML data exactly matches the YAML deck object.
- Canonical deck-data SHA-256: `956ca20a54139fb8b19ac45dd795222729d4cf4f12d1407a1634255f892a27d4`.

Run:

```sh
python3 build-deck.py
python3 validate-package.py
```

## Browser Evidence

Browser: Playwright CLI with Firefox 152.0. Chrome was unavailable in the environment because the expected system Chrome distribution was not installed.

The CLI-driven browser run completed 374 assertions across:

- `1280x720`
- `1366x768`
- `390x844`
- `360x800`

Checks covered:

- pointer reveal behavior;
- Enter and Space on a focused scene;
- ArrowRight, ArrowLeft, PageDown, and PageUp ownership;
- terminal states that do not reset implicitly;
- hash navigation;
- notes overlay and `aria-pressed` state;
- the approved opening language audition;
- first reveal clue buckets and second reveal concrete materials, dimensions, and order;
- Mentimeter as the first interaction state, supplied sandbox, external frame loading, and explicit poll-to-story transition;
- absence of projected story-state, consequence, validation, and chapter metadata;
- all 14 slides and all 32 states;
- desktop one-viewport fit;
- mobile witness, prompt, and primary action before the first fold;
- horizontal overflow;
- browser console errors.

Result: 374 passed, zero local deck console errors.

Firefox reports Mentimeter cross-site cookie rejection notices from inside the
third-party iframe. These are classified separately from local deck errors. The
poll still loads, shows its participation code and results, accepts interaction,
and does not advance the parent deck when clicked.

A focused slide-2 geometry check also confirmed at `1280x720` and `390x844`
that the side rail sits below the tabletop, above the leg midpoint, spans only
between the legs, remains horizontal, and creates no overflow. The compact
side-by-side mobile comparison was then covered by the complete `360x800`
matrix.

Focused Mentimeter checks at `1280x720` and `360x800` confirmed that the frame
is the first state, no explanatory profile appears while voting, and `Keep the
vote` unmounts the iframe before the plain-table pause. Slide 2 then shows both
front profiles without repeating the poll.

## Screenshots

- `output/playwright/desktop-1280-01.png`
- `output/playwright/desktop-1280-08.png`
- `output/playwright/desktop-1280-11.png`
- `output/playwright/desktop-1280-13.png`
- `output/playwright/desktop-1280-14.png`
- matching `1366`, `390`, and `360` viewport receipts for those moments

## Review Surfaces

Each essay has a canonical Whisper review page with stable paragraph blocks and `window.WhisperReview.getAgentPayload()`:

- `essay-01-the-wobble-we-chose.review.html`: 19 blocks
- `essay-02-when-the-shim-is-not-the-fix.review.html`: 20 blocks
- `essay-03-the-dashboard-that-looked-finished.review.html`: 20 blocks

Playwright opened all three pages and confirmed the review payload API.

## Public Boundary

The package does not contain non-public project names, local absolute paths, email addresses, or copied non-public prose. It uses only public-safe Craft concepts and synthetic table/dashboard examples.

## Remaining Validation

Before presenting:

1. Remove the unconfigured `Option 3` from the Mentimeter presentation.
2. Open slide 2 once and accept or reject Mentimeter's cookie prompt so the
   first live view opens directly on the poll.

Then run a beginner trial that checks:

1. independent choices before reveal;
2. explanation of why a choice produced a consequence;
3. delayed recall of schema, artifact, validation, residue, layer, and return;
4. transfer from the table witness to a new software example.
