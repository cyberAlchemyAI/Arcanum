# Craft Refine Missing Strategy: First Live Test

## Scope

This is the first bounded live test for the strategy artifact, not the full Craft build test.

It validates that the dispatch-backed strategy can:

1. pass Dispatch Spec validation,
2. read the current Craft evidence baseline,
3. identify the first remaining blocker,
4. detect stale blocker text,
5. preserve local skill-surface and promotion boundaries.

## Stale Blocker Check

Expected current truth:

```text
Invoke Define: pass, evidence_kind=receipt
Interrogation refine-review: block, missing owner-stage pass evidence
```

Observed mismatch:

```text
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/03-interrogation-refine-review.md
```

The stage handoff still says:

```text
Dependency blocked. Invoke Define did not produce pass evidence.
```

Strategy interpretation: this is stale evidence text. It must be repaired or superseded when the Interrogation receipt work-pack is created. It does not reopen the completed Invoke Define receipt.

## Live Test Result

| Check | Result |
| --- | --- |
| Dispatch JSON exists. | pass |
| Dispatch validator passes. | pass |
| Evidence index names Invoke Define as receipt-backed pass. | pass |
| Evidence index names Interrogation refine-review as first remaining block. | pass |
| Stage handoff stale reason is detected. | pass |
| Full Refine run/subagents not executed. | pass |
| Craft promotion not changed. | pass |

Validation commands:

```text
formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/CRAFT-REFINE-MISSING-STRATEGY-DISPATCH.json --json
jq '.stage_evidence[] | select(.stage == "Invoke Define" or .stage == "Interrogation refine-review") | {stage,status,evidence_kind,receipt_path,blocked_reason}' development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json
rg -n "Dependency blocked\\. Invoke Define did not produce pass evidence|Interrogation refine-review|Invoke Define" development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/stages/03-interrogation-refine-review.md development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json
```

Dispatch validator output:

```json
{
  "validation": "pass",
  "blocks": [],
  "flags": []
}
```

## Next Route

The approved subagent run executed the first live-test task:

```text
CRAFT-MISSING-INTERROGATION-001
```

Result:

```text
Interrogation refine-review: pass, evidence_kind=receipt
Distill: block, missing owner-stage pass evidence
```

Task-session evidence:

```text
development/craft/task-sessions/20260605T184704Z-CRAFT-MISSING-INTERROGATION-001-CONTEXT.md
development/craft/task-sessions/20260605T184704Z-CRAFT-MISSING-INTERROGATION-001-RESULT.md
```

Next route: create or block the Distill owner-stage receipt through local skill-surface execution.
