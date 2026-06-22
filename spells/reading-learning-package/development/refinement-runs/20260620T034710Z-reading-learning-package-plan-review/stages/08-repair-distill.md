# Stage 08 Repair Distill

## Status

`pass`

## Distilled Repair

The plan needs one ordering clarification, not a rewrite:

```text
Spellcraft contract first
  -> L0 tower intake and preset proof
  -> L1 manuscript and source trace
  -> L2 PDF renderer/fallback
  -> L3 fixtures and reusable readiness
```

## Must-Hold Constraints

- Do not copy full `research-tower` or `whisper` instructions into the spell.
- Do not claim source authority from a generated PDF.
- Do not skip accepted/rejected example evidence for SCU cores.
- Do not mark PDF pass without deterministic renderer evidence.
- Do not promote reusable spell readiness without preset fixtures.

## Owner Handoff

| Next action | Owner | Blocking? |
| --- | --- | --- |
| Create candidate spell contract | `spellcraft` | yes, before runtime implementation |
| Add L0 intake/preset proof | `task-session` | yes, after contract |
| Add fixtures | `experiment-harness` | yes, before reusable readiness |
| Decide persistence policy | `spellcraft` | no, can defer until after L0 |
