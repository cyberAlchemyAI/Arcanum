# Stage 03 Gap Review Ledger

## Status

`flag`

## Gap Ledger

| ID | Gap | Severity | Evidence | Owner | Repair |
| --- | --- | --- | --- | --- | --- |
| G-RLP-001 | Candidate spell contract is not installed. | blocker for direct runtime implementation | [WORK-PACK.md](../../../WORK-PACK.md) marks `T-RLP-001` blocked until Spellcraft accepts. | `spellcraft` | Create the candidate spell contract from [SPELL-HANDOFF.md](../../../SPELL-HANDOFF.md). |
| G-RLP-002 | First executable route could be confused with Task Session implementation. | blocker for ordering | [WORK-PACK.md](../../../WORK-PACK.md) says `nextOwner` is `spellcraft`, while later SWUs belong to `task-session`. | `refine` / `spellcraft` | Treat Spellcraft contract creation as the first implementation move; defer Task Session SWUs until accepted. |
| G-RLP-003 | No preset fixtures exist for deep, quick, and medium presets. | blocker for reusable readiness | [WORK-PACK.md](../../../WORK-PACK.md) lists preset fixtures as pending and required before promotion readiness. | `experiment-harness` | Add three preset fixtures after the spell contract exists. |
| G-RLP-004 | No example-driven interview transcript fixture exists. | flag for interview reliability | [PRESET-INTERVIEW.md](../../../PRESET-INTERVIEW.md) defines accepted/rejected examples and preset deltas, but no transcript fixture is present. | `task-session` / `experiment-harness` | Add a transcript fixture showing answers changing `preset-profile.yaml`. |
| G-RLP-005 | PDF renderer is environment-dependent. | flag for PDF completion | [WORK-PACK.md](../../../WORK-PACK.md) and [DESIGN.md](../../../DESIGN.md) require deterministic renderer detection or explicit fallback. | `task-session` | Implement renderer detection and fallback fixture. |
| G-RLP-006 | Custom preset persistence policy is undecided. | non-blocking design gap | [WORK-PACK.md](../../../WORK-PACK.md) names local-output vs `.arcanum` state as unresolved. | `spellcraft` | Decide persistence policy after the L0 contract is accepted. |
| G-RLP-007 | End-to-end behavior is not proven. | blocker for implementation-ready classification | [VALIDATION.md](../../../VALIDATION.md) says validation proves package shape only. | `spellcraft` / `experiment-harness` | Run fixtures for tower intake, preset profile, Whisper substrate, source trace, and PDF fallback. |

## Review Verdict

The plan is not blocked by unclear intent. It is blocked by lifecycle order and missing runtime evidence. That makes the package `repair-needed` for direct implementation but `ready-for-spellcraft-contract`.
