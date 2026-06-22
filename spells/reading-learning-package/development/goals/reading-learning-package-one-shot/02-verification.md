# Verification

## Required Validation Commands

Run these checks at minimum:

```bash
find arcanum/spells/reading-learning-package -name '*.md' -print0 | xargs -0 -n1 bash tools/check_markdown_links.sh
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py arcanum/spells/reading-learning-package/development/reading-learning-package.dispatch.json
git -C arcanum diff --check -- spells/reading-learning-package
```

## Required Evidence Surfaces

The final implementation must provide reviewable evidence for:

| Evidence | Proves |
| --- | --- |
| Candidate contract | Spell identity, modes, phases, gates, outputs, observability, and lifecycle boundaries. |
| Tower intake fixture | Valid tower/source input passes and missing source evidence blocks. |
| Preset profile fixture | `deep_voice_reading`, `quick_video`, and `medium_explanation` parse and expose defaults. |
| Interview transcript fixture | Accepted and rejected examples affect `preset-profile.yaml`. |
| Whisper substrate fixture | Resonance, relevance, trajectory, source handles, and validation checks are present. |
| Source trace fixture | Load-bearing claims in `manuscript.md` map to tower/source handles or residue. |
| Renderer fixture | PDF is produced when renderer is available, or HTML plus explicit renderer-gap flag is produced. |
| Final validation report | Spell reports pass/flag/block, no-promotion boundary, residue, and next route. |

## Fixture Policy

Fixtures may be synthetic as long as they are public-safe, local, and explicitly marked as fixtures. Do not introduce private source material or local absolute paths.

## Passing Standard

The final report must say whether the one-shot stream is:

- `pass`: all SWUs implemented and verified,
- `flag`: spell is usable with explicit renderer or fixture residue,
- `block`: a blocker prevents safe completion.
