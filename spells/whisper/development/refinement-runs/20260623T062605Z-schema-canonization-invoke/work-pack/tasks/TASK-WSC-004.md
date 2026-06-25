# TASK-WSC-004 - Whisper Contract And Validator Refresh

- Layer: L2 contract refresh
- Status: ready
- Parent work-pack: `../../WORK-PACK.md`

## Objective

Refresh the canonical Whisper contract and validator guidance so the stable
schema home is `arcanum/spells/whisper/schemas/`, while development runs remain
provenance and examples. Also consume the accepted essay lifecycle/type model so
series writing can distinguish public essay identity from development draft
state.

## Smallest Working Units

| SWU ID | Goal | Dependencies | Write Scope | Done Criteria | Validation | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-WSC-004 | Update contract/docs to reference canonical schema home and accepted optional essay lifecycle/type model. | SWU-WSC-003 complete in `../../TASK-SESSION-SWU-WSC-003-REPORT.md`; essay lifecycle packet at `../../../20260623T082756Z-essay-lifecycle-invoke/` | `arcanum/spells/whisper/README.md`; validator docs/help if needed; schema guidance if needed. | Canonical docs name schema home, no longer imply development-run schema authority, and distinguish `essay_artifact` from `draft_artifact` for series work. | Path scan, YAML parse, validator checks, optional generated mirror plan. | task-session |

## Generated Surface Policy

If README changes affect generated runtime skill surfaces, regenerate from the
canonical source. Do not hand-edit generated mirrors as source authority.

## Gate Evidence

The canonical schema package exists under `arcanum/spells/whisper/schemas/` and
validated in `../../TASK-SESSION-SWU-WSC-003-REPORT.md`.

Spellcraft accepted the essay lifecycle/type model in
`../../../20260623T082756Z-essay-lifecycle-invoke/SPELLCRAFT-RESULT.md`. The
next contract refresh should treat that model as an input, not as a competing
parallel workpack.
