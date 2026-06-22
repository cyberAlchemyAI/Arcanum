# Experiment Harness Report: Goal W3 Reusable Behavior

## Experiment Harness Result

- Mode: report
- Artifact: `arcanum/spells/goal`
- Artifact type: spell
- Profile: goal-workpack-one-shot
- Selection: W1-W3 public-safe fixture set
- Output: `arcanum/spells/goal/validation/results/fixture-report.md`
- Report: `arcanum/spells/goal/development/experiment-runs/20260621T032135Z-workpack-one-shot-w3/EXPERIMENT-HARNESS-REPORT.md`
- Validation: pass
- Profile validation: pass
- Observation: skipped; no persistent observer write requested for this work-pack
- Next unrun: none for W3 fixture coverage

## Scenario Coverage

| Scenario | Evidence | Result |
| --- | --- | --- |
| Low/read-only | `read_only_frontier` | PASS; frontier and result schemas pass. |
| Protected mutation | `protected_frontier` | STOP with `t3-node`; no route or mutation. |
| Source authority block | `missing_source` | BLOCK with `source-authority`. |
| Delegation and terminal receipt | `delegation_staging` | Dispatch route validates; receipt is terminal. |
| Audit veto | `audit_veto` | Audit blocks apparent success; no staged delta emitted. |
| Approval token | `approval_exact` | Batch-specific token validates; Craft apply request is owner-bound and direct apply is false. |
| Ambient approval rejection | `ambient_approval` | BLOCK with `ambient-approval`. |
| Gap discovery termination | `gap_discovery` | Dedupe terminates with one proposal and one duplicate. |
| Budget ceiling | `budget_stop` | STOP with `budget-ceiling`. |
| Telemetry | `delegation_staging.telemetry-signal.json` | Telemetry schema validates. |

## Quality Bar

- Fail-closed behavior is covered by protected mutation, ambient approval, source authority, and budget scenarios.
- Gap discovery waits for an empty frontier fixture and dedupes by `(kind, target)`.
- Runtime evidence and reusable validation evidence remain separate: runtime results live under `validation/results/`; this report is promotion evidence only.
- No filled profile content is used; all scenarios use `neutral-default` or public-safe fixture payloads.

## Anti-Pattern Review

- No generated host runtime surface was hand-authored.
- No staged delta is treated as active Craft truth without approval.
- No registry status is promoted by this report.
- No private profile instance or local private path appears in public output.

## Validation Commands

- `python3 -m py_compile arcanum/spells/goal/runtime/goal_loop.py arcanum/spells/goal/validation/run-fixtures.py`
- `python3 arcanum/spells/goal/validation/run-fixtures.py`
- `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py arcanum/spells/goal/validation/results/delegation_staging.dispatch.json --json`
- `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py arcanum/spells/goal/validation/results/audit_veto.dispatch.json --json`
- JSON schema validation for approval token, execution receipt, staged delta, telemetry signal, frontier snapshot, and goal loop result artifacts.
