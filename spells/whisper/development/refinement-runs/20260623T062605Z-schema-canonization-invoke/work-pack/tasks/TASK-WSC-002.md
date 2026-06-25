# TASK-WSC-002 - Canonical Schema Package Specification

- Layer: L1 package design
- Status: complete
- Parent work-pack: `../../WORK-PACK.md`

## Objective

Define the canonical schema package surface before files are promoted.

## Smallest Working Units

| SWU ID | Goal | Dependencies | Write Scope | Done Criteria | Validation | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-WSC-002 | Write a canonical package spec. | SWU-WSC-001, Spellcraft acceptance in `../../SPELLCRAFT-PACKAGE-SPEC-RESULT.md` | This invoke run folder. | Spec names target files, field ownership, example policy, and validation commands. | Review against audit matrix and Whisper README lifecycle contract; path-scope check proving `schemas/` was not created. | task-session |

## Candidate Package Shape

```text
arcanum/spells/whisper/schemas/
  README.md
  text-intent-substrate.schema.yaml
  examples/
    substack-research-post.yaml
    object-first-abstraction.yaml
    readability-dynamics.yaml
```

The package spec should decide whether the base schema is YAML, JSON Schema, or
a human-plus-fixture contract. The first implementation should choose the
smallest form that the current validator can enforce.

## Gate Evidence

Spellcraft accepted this L1 package-spec lane in
`../../SPELLCRAFT-PACKAGE-SPEC-RESULT.md`.

Do not create `arcanum/spells/whisper/schemas/` in this SWU. The expected
package-spec artifact is `../../CANONICAL-SCHEMA-PACKAGE-SPEC.md`.

## Completion

`SWU-WSC-002` completed on 2026-06-23.

Acceptance evidence:

- `../../CANONICAL-SCHEMA-PACKAGE-SPEC.md`
- `../../TASK-SESSION-CONTEXT-SWU-WSC-002.md`
- `../../TASK-SESSION-SWU-WSC-002-REPORT.md`

The next Task Session unit is `SWU-WSC-003`.
