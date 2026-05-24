# Blocked Example: Missing Verification

## Input SWU

| Field | Value |
| --- | --- |
| Work-pack | `spells/example/development/WORK-PACK.md` |
| Parent task | `TASK-REFACTOR-004` |
| SWU | `SWU-REFACTOR-004-001` |
| Source | `src/service.ts` |
| Dependencies | unknown |
| Write scope | `src/` |
| Done criteria | Improve the service. |
| Validation | none |
| Handoff pack | none |
| Handoff index | none |
| Strict coverage | block |
| Fallback exploration | block |
| Blockers | acceptance evidence and handoff pack missing |

## Output Profile

No runnable native Codex Goal should be generated.

## Blocked Result

- Readiness: block
- Reason: done criteria are vague, dependencies are unknown, write scope is broad, no verification surface is available, no strict handoff pack/index exists, and fallback exploration cannot be bounded to named gaps.
- Unblock action: define exact outcome, bounded write scope, dependency state, validation command or reviewable evidence, and a Context Builder handoff pack with strict coverage.

## Verdict

Pass as a negative example. The transmutation blocks instead of producing a weak `/goal`.
