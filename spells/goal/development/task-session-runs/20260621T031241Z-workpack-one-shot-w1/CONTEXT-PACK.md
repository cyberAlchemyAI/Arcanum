# Context Pack: Goal W1 Read-Only Runtime Skeleton

## Context Pack Summary

- Task: `TASK-GOAL-RUNTIME-SKELETON`
- SWUs: `SWU-GOAL-003`, `SWU-GOAL-004`
- Mode: lean
- Files selected: 8
- Obligation coverage: 100%
- Strict coverage: pass
- Handoff pack: none; local Task Session execution
- Session evidence path: `arcanum/spells/goal/development/task-session-runs/20260621T031241Z-workpack-one-shot-w1/`

## Obligations

| ID | Obligation | Evidence |
| --- | --- | --- |
| O-W1-001 | W0 must pass before W1 starts. | `SPELLCRAFT-REVALIDATION-20260621T030517Z.md` |
| O-W1-002 | Select exact runtime source/write scope before mutation-capable execution. | `RUNTIME-SOURCE-SELECTION.md` |
| O-W1-003 | Bind exactly one source authority or block. | `runtime/goal_loop.py`, `missing_source` fixture |
| O-W1-004 | Emit frontier snapshot shape. | `frontier-snapshot.schema.json`, `read_only_frontier.frontier-snapshot.json` |
| O-W1-005 | Unknown/protected work stops before route or mutation. | `protected_frontier.goal-loop-result.json` |
| O-W1-006 | Emit non-mutating Goal Loop Result. | `goal-loop-result.schema.json`, `fixture-report.md` |
| O-W1-007 | Keep public/private split. | Public-boundary scan and neutral-default profile behavior |

## Included Context

- `arcanum/spells/goal/README.md` - execution phases, read-only boundary, failure policy, output contract.
- `arcanum/spells/goal/decision-profile.schema` - public neutral profile shape; no filled profile data.
- `frontier-snapshot.schema.json` - frontier output contract for `SWU-GOAL-003`.
- `goal-loop-result.schema.json` - result output contract for `SWU-GOAL-004`.
- `RULES.md` - source-authority and fail-closed risk rules.
- `TASK-GOAL-RUNTIME-SKELETON.md` - W1 SWU contract and done criteria.
- `W1.md` - W1 entry/exit gates and stop conditions.
- `SPELLCRAFT-REVALIDATION-20260621T030517Z.md` - W0 pass evidence.

## Extra Sources

| Source | Gap | Effect |
| --- | --- | --- |
| `arcanum/spells/goal/validation/fixtures/*.json` | `G-GOAL-FIXTURE-SET` | Public-safe fixture set for read-only, protected-stop, and source-authority block cases. |
| `arcanum/spells/goal/validation/run-fixtures.py` | `G-GOAL-FIXTURE-SET` | Repeatable validation runner for W1 evidence. |

## Gate Verdict

Pass. W1 may write generic runtime source, public fixtures, validation runner,
validation results, and Task Session receipts. It may not write filled profile
content, generated host runtime surfaces, commits, pushes, PRs, publication, or
parent gitlinks.
