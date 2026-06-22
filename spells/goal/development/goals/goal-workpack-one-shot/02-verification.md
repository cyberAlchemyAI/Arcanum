# Verification: Goal Work-Pack One-Shot

## Stream Verification Matrix

| Wave | SWUs | Required Evidence |
| --- | --- | --- |
| W0 | SWU-GOAL-001, SWU-GOAL-002 | Spellcraft validation report; staged source-state sync proposal or explicit deferral. |
| W1 | SWU-GOAL-003, SWU-GOAL-004 | Bound source authority or block; frontier snapshot; risk tiers; non-mutating Goal Loop Result; protected/unknown stop case. |
| W2 | SWU-GOAL-005, SWU-GOAL-006 | Valid dispatch route; terminal receipt; audit verdict; staged delta; no active mutation. |
| W3 | SWU-GOAL-007, SWU-GOAL-008, SWU-GOAL-009, SWU-GOAL-010 | Approval-token scenario; ambient-approval rejection; gap-discovery termination; telemetry evidence; Experiment Harness report; installer dry-run or approved installer evidence. |

## Required Receipts

Each attempted SWU must return:

```yaml
swu_id: <SWU-GOAL-NNN>
result: pass | flag | block | interrupted
capability_ref: <spellcraft | task-session | experiment-harness | runtime-installer | local-fallback>
receipt_kind: native-stage | handoff | blocked
receipt_artifact: <path or none>
files_touched:
  - <path or none>
validation:
  - <command or review check and result>
blockers:
  - <blocker or none>
residue:
  - <residue or none>
reroute: <next owner or none>
handoff_note: <what the parent coordinator needs next>
```

## Validation Surface

Use the surfaces named by each task file. Minimum closeout checks for the
profile itself:

```bash
python3 -m json.tool arcanum/spells/goal/development/goals/goal-workpack-one-shot/handoff-index.json
find arcanum/spells/goal/development/goals/goal-workpack-one-shot -name '*.md' -print0 | xargs -0 -n1 bash tools/check_markdown_links.sh
git -C arcanum diff --check -- spells/goal definitions
```

Runtime validation commands or review checks must be added by the executing SWU
receipts as implementation files and fixtures become concrete.
