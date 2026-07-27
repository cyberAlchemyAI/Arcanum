# TASK-DRE-02: Direct Telemetry And Emission Status

## Objective

Make direct Distill invocations observable exactly once and distinguish producer
evidence state from execution evidence and telemetry recording.

## SWU-DRE-004 — Direct Distill Telemetry

- Primary behavior: append one direct Distill signal with no caller lineage.
- Split analysis: envelope validation, observer delegation, and dedupe are one
  observation transaction.
- Dependencies: DRE-003.
- Write scope:
  - `arcanum/arcana/distill/scripts/observe-direct-invocation.sh`
  - direct telemetry fixtures and runner under Distill development
- Done: meaningful direct run records once; duplicate dedupes; any lineage or
  non-Distill capability blocks.
- Validation: isolated observability directory, central-ledger assertions.
- Execution owner: manual through Sigil Development.

## SWU-DRE-005 — Evidence-Emission Status

- Primary behavior: report producer state independently at Distill closeout.
- Split analysis: the vocabulary and its output/telemetry projection must change
  together to be observable.
- Dependencies: DRE-004.
- Write scope:
  - `arcanum/arcana/distill/SKILL.md`
  - `arcanum/arcana/distill/templates/usage-telemetry.md`
  - evidence-status fixtures and focused runner
- Done: all five statuses classify correctly; emitted status cannot alter
  verdict or mutation authority; invoked append ownership remains caller-only.
- Validation: status matrix plus semantic non-regression assertions.
- Execution owner: manual through Sigil Development.
