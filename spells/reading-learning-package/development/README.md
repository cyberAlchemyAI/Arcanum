# Reading Learning Package Development

Status: invoke-authored spell development package

Target spell candidate: `reading-learning-package`

Lifecycle owner after this package: `spellcraft`

## Purpose

Design a reusable spell that turns a completed `research-tower` result plus
source artifacts into a reader-facing learning package, then composes that
package into a PDF-ready artifact.

The spell uses:

- `research-tower` for source-backed tower evidence, claim ledgers, definitions,
  notation, residue, and final learning packs.
- `whisper` for author-intent extraction, SCU core selection, preset-sensitive
  composition planning, draft creation, validation, and learning residue.
- a bounded PDF assembly stage that renders the approved manuscript and records
  source traceability.

## Package Files

- `DEFINE.md` - scope, inputs, modes, presets, and glossary baseline.
- `PRESET-INTERVIEW.md` - preset selection and example-driven core interview.
- `DESIGN.md` - six-view spell design and phase/gate contract.
- `IMPLEMENTATION-LAYERING.md` - L0-L3 delivery boundaries.
- `WORK-PACK.md` - implementation plan, SWUs, validation, and handoff.
- `SPELL-HANDOFF.md` - Invoke-to-Spellcraft handoff.
- `reading-learning-package.dispatch.json` - validated route shape.

## Boundary

This package does not install the spell at `arcanum/spells/reading-learning-package/README.md`.
It prepares the spellcraft handoff and implementation plan. Spellcraft owns
spell lifecycle mutation, validation, observability, reflection, and promotion
readiness.
