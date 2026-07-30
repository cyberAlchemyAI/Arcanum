# Implementation Plan

## Strategy

Build one development-only, standard-library fixture harness in serial layers.
Each mutation SWU writes an exact inventory and closes through Task Session
plus Spellcraft validation. No successor is automatically selected.

## Milestones

| Milestone | SWUs | Result |
| --- | --- | --- |
| M0 Contracts | SWU-DFE-001 | versioned schemas, fail-closed graph validation, synthetic fixtures |
| M1 Pure frontier | SWU-DFE-002 | reason-complete deterministic projection |
| M2 State controls | SWU-DFE-003, 004 | claims and proposal-only reconciliation |
| M3 Boundaries | SWU-DFE-005, 006, 007 | HITL, Way Clear, and decision/execution non-collapse |
| M4 Closure | VERIFY-DFE-001, READINESS-DFE-001 | independent evidence reconciliation and lifecycle decision |

## Implementation Constraints

- Python standard library only unless a selected Task Session proves a smaller
  repository-native option.
- Canonical JSON uses sorted keys, compact separators, UTF-8, and a final
  newline.
- The reducer is pure: inputs in, projection out.
- File writes use temporary sibling plus atomic replacement.
- All identities and paths are synthetic and repository-relative.
- No network, process daemon, model call, tracker API, adapter implementation,
  or canonical write.

## Review Gates

1. Spellcraft accepts this plan and selects exactly one L0 SWU.
2. Each SWU captures its exact target baseline before mutation.
3. Task Session closes with terminal evidence.
4. Spellcraft issues an owner receipt.
5. The next SWU becomes eligible, never selected.
6. L3 decides between abandon, revise, run paired workflow evidence, or open a
   new canonical Invoke Design route.
