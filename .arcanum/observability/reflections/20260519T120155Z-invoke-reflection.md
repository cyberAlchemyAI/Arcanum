# Invocation Signal Reflection

## Scope

- Scope: `capability`
- Capability: `invoke`
- Kind: `spell`
- Since: `2026-05-19T09:50:38Z`
- Signals analyzed: `3`
- Thresholds triggered: `output-threshold`

## Signal Summary

```json
{
  "count": 3,
  "status_counts": {
    "completed": 3
  },
  "quality_counts": {
    "pass": 3
  },
  "recommendation_counts": {
    "none": 2,
    "reflect-now": 1
  },
  "thresholds": [
    "output-threshold"
  ],
  "severe_gaps": 0,
  "output_drift": 0,
  "reflect_now": 1,
  "capabilities": [
    {
      "id": "invoke",
      "kind": "spell"
    }
  ]
}
```

## Proposed Iterations

- Review threshold-backed gaps before mutating any capability.
- Route approved capability changes through the appropriate lifecycle spell or sigil.

## Contract Preservation

- This reflection report did not edit observed capabilities.
- Hook operation rows remain separate from capability telemetry.

## Decision

- Recommended next action: targeted update
