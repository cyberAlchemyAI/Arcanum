# SWU-TSGR-001 Material Producer Validation

## Result

The isolated producer stage passes. This is staged-material evidence only;
`mutation_ready` remains `false`.

## Validation matrix

| Check | Result | Evidence |
| --- | --- | --- |
| Current golden policy parity | pass | 25/25 cases |
| Fail-closed cases | pass | 5/5: malformed request, stale policy digest, unknown kind, invalid policy outcome, input overwrite |
| Request/receipt schema discrimination | pass | 4/4 positive/negative checks |
| Evaluator undeclared outputs | pass | 0 |
| Current Task Session policy regression | pass | 25/25; canonical, Codex, and Claude contract-body parity |
| Producer receipt JSON Schema | pass | closed schema with format checking |
| Receipt exact references | pass | 22/22 |
| Canonical target preconditions | pass | 5/5 absent |
| Staged manifest | pass | 5 files; SHA-256 `e555fb7432e7a24cfd86d7ff6b26108be6c9032524b09006fd0599438e0a0a6a` |
| Staged target set | pass | exact match with five canonical preconditions |
| Scoped whitespace check | pass | no errors |

## Commands

From the parent repository root:

```text
python3 arcanum/arcana/task-session/development/invoke-runs/20260730T170810Z-deterministic-governance-runner/refreshes/20260730T181803Z-swu-tsgr-001-producer-handoff/producer/staged/arcanum/arcana/task-session/development/validate-governance-evaluator.py --source-task-session-dir arcanum/arcana/task-session
python3 arcanum/arcana/task-session/development/validate-decision-validation-policy.py . arcanum/arcana/task-session
```

The receipt validator additionally re-read all exact references, checked live target
absence, recomputed the staged manifest, and compared staged/precondition target
sets.

## Observer synthesis

The observer initially returned `partial` with a severe ownership/evidence gap. The
reflection in `REFLECTION.md` resolved it before receipt completion by separating
Sigil Development lifecycle ownership from Task Session target and review
ownership, closing the receipt schema, and preserving the Task Session return
boundary.

## Sigil Development Result

- Target sigil: `task-session`
- Mode: `update`
- Tier: `arcana`
- Files changed: isolated `producer/` staging and evidence only
- Observer pass: `subagent`
- Telemetry updated: yes, by the post-validation Signal Observer append
- Reflection trigger state: `severe-gap`, reflected and resolved in this producer
- Iteration decision: `targeted update`
- Validation: all acceptance-critical producer checks above pass
- Next lifecycle step: `task-session-review`

## Remaining blockers

- Task Session review of the staged producer receipt.
- Exact five-path apply approval.
- Invoke material package plus schema-valid material receipt.
- Strict Task Session context pack and mutation-admission receipt.

No canonical Task Session target, generated mirror, planning record, or historical
Task Session receipt was changed.
