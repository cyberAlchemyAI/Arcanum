# Stage 06 Design Repair

## Status

`flag`

## Repair Position

No source design rewrite is required before the first implementation move. The repair is an execution-order repair:

1. Create the Spellcraft candidate contract first.
2. Only then run Task Session SWUs for runtime implementation.
3. Treat fixtures as part of implementation readiness, not as optional polish.

## Design Adjustments For Implementation

| Area | Current design state | Repair recommendation |
| --- | --- | --- |
| Lifecycle | Clear handoff to `spellcraft`. | Preserve it as the first implementation gate. |
| Preset interview | Concrete contract with examples. | Add transcript fixture before claiming interview reliability. |
| Whisper bridge | Defined output names and SCU requirements. | Add substrate fixture after L0 intake/preset proof. |
| PDF assembly | Deterministic renderer or fallback is required. | Implement renderer detection as its own SWU, with HTML-only fallback as a valid flag. |
| Persistence | Custom preset persistence undecided. | Defer until after one package output proves useful; default to output-root local state. |

## Source Edit Decision

Do not patch the source work-pack yet. The existing work-pack already carries the correct next-owner signal and gap list. This review adds an implementation-order handoff rather than replacing the plan.
