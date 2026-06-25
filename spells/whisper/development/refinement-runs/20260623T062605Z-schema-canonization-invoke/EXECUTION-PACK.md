# Execution Pack - Whisper Schema Canonization

- Work-pack: `WORK-PACK.md`
- Complexity: medium
- Execution mode: one SWU at a time
- Current selected SWU: `SWU-WSC-004` (ready)

## Wave Plan

| Wave | Layer | Tasks | Entry Gate | Exit Evidence |
| --- | --- | --- | --- | --- |
| W0 Audit | L0 | `TASK-WSC-001` | Spellcraft accepted L0 execution in `SPELLCRAFT-RESULT.md`. | Complete: `SCHEMA-ARTIFACT-AUDIT.md` classifies schema-bearing artifacts. |
| W1 Package Design | L1 | `TASK-WSC-002` | Complete: W0 pass and Spellcraft package-spec acceptance in `SPELLCRAFT-PACKAGE-SPEC-RESULT.md`. | Complete: `CANONICAL-SCHEMA-PACKAGE-SPEC.md`. |
| W2 Package Creation | L1 | `TASK-WSC-003` | Complete: W1 package spec exists and names validation. | Complete: `arcanum/spells/whisper/schemas/` files exist and validate. |
| W3 Contract Refresh | L2 | `TASK-WSC-004` | Complete: W2 pass. | README/validator references point at canonical schema home and accepted optional essay lifecycle/type model. |
| W4 Promotion Evidence | L3 | `TASK-WSC-005` | W3 pass. | Experiment or fixture matrix plus Spellcraft promotion decision. |

## Parallelization

No parallel execution in W0. Later waves may split review and fixture validation
only after the canonical package spec exists.

## Stop Conditions

- Stop before L1 if Spellcraft does not accept the lifecycle route.
- Stop before copying any development artifact into `schemas/` until W0 classifies
  article-specific fields.
- Stop before generated runtime mirror changes unless canonical source changes
  are accepted and a regeneration path is selected.

## Current Gate State

W0, W1, and W2 are complete. W3 contract refresh is ready and should consume the
essay lifecycle/type packet from
`../20260623T082756Z-essay-lifecycle-invoke/`. W4 promotion evidence remains
blocked until the contract refresh completes.

## Receipt Expectations

Every wave returns:

- selected SWU,
- files touched,
- validation commands and results,
- unresolved blockers,
- whether canonical authority changed,
- next owner.
