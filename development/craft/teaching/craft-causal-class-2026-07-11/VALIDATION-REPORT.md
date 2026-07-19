# From Table to Text Validation Report

Date: 2026-07-15

## Result

The refreshed package passes structural, interaction, rendering, responsive,
and local-browser checks.

Editorial status remains `flag` until the operator reviews the table-to-writing
transition aloud. The supplied Mentimeter word cloud loads, but its live
response flow still needs a presenter preflight. Pedagogical effectiveness
remains unproven until a beginner trial.

## Structured Package

- YAML authority parsed successfully with PyYAML.
- Deck count: five slides.
- Interaction-state count: eleven states.
- Formal-term vocabulary: only `schema`.
- `schema` is earned once, in the final state of slide three.
- The opening sequence is exactly `table -> cloud -> gathered`.
- Projected language excludes later-lesson Craft terms and the discarded desk
  story.
- Slide IDs and state IDs are unique.
- Every transition points to the next declared state or terminates.
- Embedded HTML data exactly matches the YAML deck object.
- Canonical deck-data SHA-256:
  `5fe176c047d789e0f7312127ff6e37c7f013341cb518d4e5c8c2e1fe77689fba`.

Run:

```sh
python3 build-deck.py
python3 validate-package.py
```

## Narrative Boundary

The browser assertions verify this order:

1. The table appears with fifteen seconds of private thinking time.
2. Mentimeter mounts only after that pause, then unmounts when the room's words
   are brought back.
3. Materials, tools, measurements, and steps feed the sketching decision.
4. The annotated sketch preserves dimensions, material, attachment, and a
   testable stability condition.
5. Picture and buildable structure are compared before `schema` is revealed.
6. An empty writing surface asks for the writing equivalent of the table sketch.
7. Purpose, audience, meaning, evidence, shape, voice, and ending form the
   candidate writing mold.
8. A rigid universal outline is rejected in favor of stable questions plus
   text-specific structure.

## Browser Evidence

Browser: Playwright CLI with Firefox.

The browser run completed 179 assertions across:

- `1280x720`
- `1366x768`
- `390x844`
- `360x800`

Checks covered pointer and keyboard transitions, terminal-state behavior, hash
navigation, notes overlay, all five slides and eleven states, local-console
errors, horizontal overflow, desktop viewport fit, mobile first-fold behavior,
Mentimeter mount/unmount, the schema gate, and the adaptable-mold ending.

Result: 179 passed, zero local deck console errors. The Mentimeter frame loaded
on the opening slide. Firefox reported two third-party `SameSite` cookie
rejections from Mentimeter; they did not prevent the embedded presentation from
loading.

Screenshots are under `output/playwright/`, including:

- `desktop-1280-opening-table.png`
- `desktop-1280-schema-01.png`
- `desktop-1280-schema-04.png`
- `desktop-1280-schema-05.png`
- the corresponding complete desktop and mobile matrix

## External Dependency

The iframe URL and sandbox are valid and the remote frame loads. The supplied
word-cloud question is:

`What would you need to build this?`

Before class, open the embedded state once, submit a test word, and confirm the
participant response path and cookie state.

## Remaining Validation

1. Read the table-to-schema and schema-to-writing transitions aloud at
   presentation pace.
2. Confirm the live Mentimeter response flow with one test word.
3. Run a beginner trial that checks whether learners can explain why the sketch
   acts as a schema and propose an equivalent structure for a chosen text type.
