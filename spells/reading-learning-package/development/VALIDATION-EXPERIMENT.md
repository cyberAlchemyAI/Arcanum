# Reading Learning Package Validation Experiment

Status: active reusable-spell fixture harness
Owner: `experiment-harness` for repeatable mechanics, `spellcraft` for lifecycle
readiness

## Purpose

Validate that `reading-learning-package` can compose public-safe learning
packages from a tower-like source fixture while preserving `research-tower` as
source authority and `whisper` as composition authority.

## Fixture Matrix

| Fixture | Purpose | Expected Result |
| --- | --- | --- |
| `deep_voice_reading` | Long-form reading and narration profile. | Compose and validate package outputs. |
| `quick_video` | Short script-shaped package. | Compose and validate package outputs without claiming video rendering. |
| `medium_explanation` | Balanced explanatory guide. | Compose and validate package outputs. |
| `missing-source` | Missing tower claim evidence. | Block before composition and emit `validation-report.md`. |

## Validation Commands

```bash
python3 -m py_compile \
  arcanum/spells/reading-learning-package/runtime/reading_learning_package.py \
  arcanum/spells/reading-learning-package/validation/run-fixtures.py

python3 arcanum/spells/reading-learning-package/validation/run-fixtures.py

python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  arcanum/spells/reading-learning-package/development/reading-learning-package.dispatch.json

bash tools/check_markdown_links.sh \
  arcanum/spells/reading-learning-package/README.md
```

## Current Evidence

| Evidence | Path | Status |
| --- | --- | --- |
| Fixture report | `validation/results/fixture-report.md` | pass |
| Runtime implementation report | `validation/results/implementation-report.md` | pass |
| Dispatch validation | `development/reading-learning-package.dispatch.json` | pass |
| Spell contract | `README.md` | candidate, Spellcraft-reviewed |

## Expected Residue

- Deterministic PDF rendering may be unavailable. In that case,
  `learning-package.html` is the required render artifact and the package
  validation report records a PDF renderer `flag`.
- Generated learning packages remain derived learning artifacts. They do not
  promote claims, terms, or source records into canonical tower authority.

## Promotion Boundary

This experiment proves reusable candidate behavior for the public-safe fixtures.
Registry promotion still requires the repository's normal spell promotion route
and must not be inferred only from runtime execution or Codex Goal evidence.
