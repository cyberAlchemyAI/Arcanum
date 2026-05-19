# Invocation Signal Reflection

## Scope

- Scope: `capability`
- Capability: `invoke`
- Kind: `spell`
- Since: `2026-05-18T14:21:35Z`
- Signals analyzed: `5`
- Thresholds triggered: `output-threshold,usage-threshold`

## Signal Summary

```json
{
  "count": 5,
  "status_counts": {
    "completed": 4,
    "partial": 1
  },
  "quality_counts": {
    "partial": 1,
    "pass": 4
  },
  "recommendation_counts": {
    "reflect-now": 5
  },
  "thresholds": [
    "output-threshold",
    "usage-threshold"
  ],
  "severe_gaps": 0,
  "output_drift": 0,
  "reflect_now": 5,
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
