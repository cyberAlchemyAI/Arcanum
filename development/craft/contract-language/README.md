# Contract Language Project Seed

Status: handoff-ready
Date: 2026-06-08

## Purpose

This folder is the start point for a new project: designing a formal language
for writing contracts that can be validated the same way schemas are validated.

The seed comes from the Craft interface work, where:

- contract means behavior, ownership, invariants, and boundaries;
- schema means structured row families, fields, enums, references, and
  validation rules;
- iteration means contract and schema evolve together through examples,
  validation, residue, and recomposition.

## Start Here

1. Read `CONTRACT-LANGUAGE-HANDOFF.md`.
2. Use `CONTEXT-PACK.md` and `context-index.json` as the selected evidence pack.
3. Start the next lifecycle with `invoke define`.

## Recommended First Command

```text
$invoke define development/craft/contract-language/CONTRACT-LANGUAGE-HANDOFF.md
```

## Boundary

This folder does not implement a parser, validator, grammar, sigil, spell, or
runtime. It only hands off enough context to start that lifecycle cleanly.
