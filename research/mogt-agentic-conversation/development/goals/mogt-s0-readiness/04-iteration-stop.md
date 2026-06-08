# Goal Part 04 - Iteration And Stop Rules

## Iteration Policy

Work in this order:

1. Read the context pack and JSON index.
2. Read S0 readiness and the publication dispatch.
3. Read Experiment Harness requirements.
4. Decide feasibility.
5. Write `HARNESS-FEASIBILITY.md`.
6. If blocked, write or update `development/WORK-PACK.md` with missing tooling SWUs.
7. Validate the dispatch and report the result.

## Stop With BLOCK If

- The MOGT project folder or publication dispatch is missing.
- Dispatch validation fails and cannot be repaired within MOGT-only scope.
- Experiment Harness feasibility cannot be decided from local evidence.
- Supporting S4 would require mutating canonical tool contracts.
- Any live experiment would be required to decide readiness.

## Stop With FLAG If

- Harness is mostly usable but needs manual scoring, manual replay, or a local substitute before S4.
- Required dry-run fields are known but not yet implemented.
