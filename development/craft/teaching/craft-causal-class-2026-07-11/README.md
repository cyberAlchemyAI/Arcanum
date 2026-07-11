# Craft Causal Class

This is a clean-room beginner teaching package built around one persistent table history.

Start with `index.html` or open `CRAFT-CAUSAL-CLASS-PRESENTATION.html` directly.

## Package

- `CRAFT-CAUSAL-CLASS-SLIDE-SCHEMA.yml`: authoritative deck and interaction data.
- `CRAFT-CAUSAL-CLASS-SLIDE-SCHEMA.md`: author-facing schema explanation.
- `CRAFT-CAUSAL-CLASS-PRESENTATION.html`: generated standalone presentation.
- `presentation.template.html`: presentation implementation template.
- `build-deck.py`: deterministic YAML-to-HTML builder.
- `validate-package.py`: YAML/HTML parity and state-contract validator.
- `playwright-checks.js`: Playwright CLI browser matrix.
- `essay-01-the-wobble-we-chose.md`: choice to caused mismatch.
- `essay-02-when-the-shim-is-not-the-fix.md`: candidate lower build to validated return.
- `essay-03-the-dashboard-that-looked-finished.md`: software recognition to the name Craft.
- `*.review.html`: commentable Whisper review pages.
- `VALIDATION-REPORT.md`: structural and browser evidence.
- `WHISPER-RESULT.md`: composition substrate and limits.

## Rebuild

```sh
python3 build-deck.py
python3 validate-package.py
```

The HTML presentation is generated. Edit the YAML and template, then rebuild it.

