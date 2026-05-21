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
| Blockers | acceptance evidence missing |

## Output Profile

No runnable native Codex Goal should be generated.

## Blocked Result

- Readiness: block
- Reason: done criteria are vague, dependencies are unknown, write scope is broad, and no verification surface is available.
- Unblock action: define exact outcome, bounded write scope, dependency state, and validation command or reviewable evidence.

## Verdict

Pass as a negative example. The transmutation blocks instead of producing a weak `/goal`.
