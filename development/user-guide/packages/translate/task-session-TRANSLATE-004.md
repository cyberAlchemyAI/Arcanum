# Task Session Report: SWU-TRANSLATE-004

## Task

`SWU-TRANSLATE-004`: define Guide-call contract and research-needed flag.

## Context Pack

Controlling sources:

- `WORK-PACK.md`
- `DESIGN.md`
- `TRANSLATE-RECEIPT-SCHEMA.yml`

## Gate Verdict

`PASS`

Dependency `SWU-TRANSLATE-003` passed validation.

## Files Updated

- `GUIDE-CALL-CONTRACT.md`

## Validation

`PASS`

- Guide-call contract says Guide decides research/subagent dispatch.
- Translate returns `research_need`.
- Translate does not write User ledger rows directly.
