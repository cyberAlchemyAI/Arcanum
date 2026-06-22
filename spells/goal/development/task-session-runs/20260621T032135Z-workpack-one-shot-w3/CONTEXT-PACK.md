# Context Pack: Goal W3 Approval, Evidence, And Generated Readiness

## Context Pack Summary

- Tasks: `TASK-GOAL-APPROVAL-PROMOTION`, `TASK-GOAL-VERIFY-EVIDENCE`
- SWUs: `SWU-GOAL-007`, `SWU-GOAL-008`, `SWU-GOAL-009`, `SWU-GOAL-010`
- Mode: lean
- Strict coverage: pass
- Handoff pack: none; local Task Session and evidence execution
- Session evidence path: `arcanum/spells/goal/development/task-session-runs/20260621T032135Z-workpack-one-shot-w3/`

## Obligations

| ID | Obligation | Evidence |
| --- | --- | --- |
| O-W3-001 | W2 must pass before W3 starts. | `../20260621T031727Z-workpack-one-shot-w2/W2-RESULT.md` |
| O-W3-002 | Approval token must bind exact batch and decision record. | `approval_exact.approval-token.json`, `approval_exact.apply-boundary.json` |
| O-W3-003 | Ambient approval must be rejected. | `ambient_approval.apply-boundary.json` |
| O-W3-004 | Gap discovery terminates by dedupe and budget. | `gap_discovery.gap-discovery.json`, `budget_stop.gap-discovery.json` |
| O-W3-005 | Telemetry signal validates. | `delegation_staging.telemetry-signal.json` |
| O-W3-006 | Experiment Harness evidence covers reusable behavior. | `EXPERIMENT-HARNESS-REPORT.md` |
| O-W3-007 | Installer readiness uses dry-run or approved installer path only. | `INSTALLER-DRY-RUN-RESULT.md` |

## Gate Verdict

Pass. W3 can produce evidence and dry-run installer readiness. It must not
promote registry status, hand-author generated host runtime surfaces, or apply
installer output.
