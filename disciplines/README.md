# Arcanum Disciplines

Disciplines are cross-capability operating practices that Arcanum repeatedly uses but should not force into a sigil, spell, or one large framework document.

A discipline names a durable way of working. It can appear inside many sigils and spells, but its authority lives here when the practice is broad enough to shape long-term framework growth.

## Purpose

Use this layer to:

- formalize recurring practices that are scattered across Arcanum,
- separate method-level discipline from capability-local implementation,
- preserve evidence for why a practice deserves framework attention,
- decide whether a practice needs a constitution, validator, template, spell, sigil, or only a catalog entry,
- prevent hidden practices from becoming inconsistent across capabilities.

## Boundary

Disciplines are not registry entries. They do not replace sigils, spells, formulae, transmutations, arcana, or research packages.

Disciplines may define:

- concepts and criteria for a reusable practice,
- expected evidence and failure modes,
- links to owning framework documents, sigils, spells, or development packages,
- candidate validation rules and templates.

Disciplines must not:

- claim promotion authority for sigils or spells,
- mutate capability-local contracts without the owning lifecycle route,
- treat execution evidence as canonical knowledge without the relevant owner review,
- duplicate the full internals of a sigil or spell.

## Catalog

Start with [DISCIPLINES.md](DISCIPLINES.md) for the current formalization catalog.

Use [development/HIDDEN-DISCIPLINE-SCAN.md](development/HIDDEN-DISCIPLINE-SCAN.md) to see the first evidence-backed scan that identified visible and hidden disciplines.

## Maintenance

New discipline entries should be added when a practice has at least two of these signals:

- it appears across multiple capabilities,
- it already has rules scattered across framework docs, development packages, or validators,
- it has caused drift, rework, or confusion,
- it needs reusable evidence, templates, validation, or routing guidance,
- it is important for future Arcanum growth.

Run the catalog validator after edits:

```bash
python3 disciplines/scripts/validate-discipline-catalog.py
```

Schema guidance for future machine-readable discipline cards lives in [discipline.schema.yml](discipline.schema.yml).
