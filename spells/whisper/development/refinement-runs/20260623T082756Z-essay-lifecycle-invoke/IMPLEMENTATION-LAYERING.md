# Implementation Layering - Whisper Essay Lifecycle Type Model

- Module: whisper-essay-lifecycle
- Status: proposed
- Date: 2026-06-23
- Source review: `WRITING-SEQUENCE-REVIEW.md`

## Layer Summary

| Layer | Goal | Mutation Type | Promotion Gate |
| --- | --- | --- | --- |
| L0 | Review and model essay identity vs draft state. | Development artifact only. | Review and model exist. |
| L1 | Add optional lifecycle/type fields to canonical schema and Whisper contract. | Canonical docs/schema mutation. | Spellcraft accepts route; Task Session executes bounded SWU. |
| L2 | Add examples or series registry entries for Essay 01 and Essay 02. | Example/evidence artifact mutation. | L1 fields exist and parse. |
| L3 | Validate reusable behavior and decide promotion scope. | Evidence and promotion decision. | Fixture matrix proves useful behavior without overfitting to this series. |

## Smallest Coherent Unit

The SCU is: separate essay identity from draft state.

This recomposes into the larger Whisper lifecycle because the same distinction
supports titles, sequences, review links, validation states, publication prep,
and future series navigation.

## First Execution Boundary

The first mutation-capable unit should not rename files. It should update the
canonical contract and schema guidance so future publication work has admitted
types.

Recommended next SWU:

```text
SWU-WEL-002: Add essay lifecycle/type model to Whisper contract and canonical schema guidance.
```

This SWU should be coordinated with the already-ready schema canonization unit
`SWU-WSC-004`, because both touch `arcanum/spells/whisper/README.md` and schema
documentation.

## Deferred Complexity

- Physical publication directory layout.
- Automated validator checks for public openings.
- HTML review integration for sequence-aware comments.
- Generated runtime skill mirror refresh.
- Cross-transport promotion beyond `substack_research_post`.

## Distill Verdict

Pass with coordination flag.

The unit is small enough to execute as a docs/schema addition, but it should not
compete with the active schema-canonization work-pack. It should either become a
named input to `SWU-WSC-004` or execute immediately after that SWU.
