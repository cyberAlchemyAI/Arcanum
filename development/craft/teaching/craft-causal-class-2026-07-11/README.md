# From Table to Text

This is presentation one of the beginner Craft class. It starts with one
practical question, lets the room answer through a live Mentimeter word cloud,
turns those answers into a table sketch, and earns `schema` before carrying the
same relation into software that helps people write.

Start with `index.html` or open
`CRAFT-CAUSAL-CLASS-PRESENTATION.html` directly.

## Current Presentation

- Five slides and eleven interaction states.
- One continuous analogy: build needs -> sketch -> schema -> writing mold.
- One learner-created surface: the supplied Mentimeter word cloud.
- One formal term: `schema`.
- One explicit boundary: reusable writing questions do not imply one fixed
  outline for every text type.

## Package

- `CRAFT-CAUSAL-CLASS-SLIDE-SCHEMA.yml`: authoritative deck and interaction data.
- `CRAFT-CAUSAL-CLASS-SLIDE-SCHEMA.md`: author-facing teaching and surface contract.
- `CRAFT-CAUSAL-CLASS-PRESENTATION.html`: generated standalone presentation.
- `presentation.template.html`: table, word-cloud, sketch, schema, and writing renderers.
- `build-deck.py`: deterministic YAML-to-HTML builder.
- `validate-package.py`: YAML/HTML parity and state-contract validator.
- `playwright-checks.js`: Playwright CLI browser matrix.
- `VALIDATION-REPORT.md`: structural and browser evidence.
- `WHISPER-RESULT.md`: composition status and remaining proof boundary.

The three essays and their review pages remain historical development material.
They are not part of this presentation and are not linked from its entry page.

## Mentimeter Preflight

The supplied word-cloud presentation is embedded with the question:

`What would you need to build this?`

Open the cloud once before class, submit one test response, and resolve any
cookie prompt so participants arrive directly at the activity.

## Rebuild

```sh
python3 build-deck.py
python3 validate-package.py
```

Edit the YAML and template, then rebuild. Do not edit the generated presentation
HTML directly.
