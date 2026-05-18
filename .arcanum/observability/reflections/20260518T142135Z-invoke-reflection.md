# Invocation Signal Reflection

## Scope

- Scope: `capability`
- Capability: `invoke`
- Kind: `spell`
- Signals analyzed: `2`
- Thresholds triggered: `output-threshold,usage-threshold`

## Signal Summary

```json
{
  "count": 2,
  "status_counts": {
    "completed": 2
  },
  "quality_counts": {
    "pass": 2
  },
  "recommendation_counts": {
    "reflect-now": 2
  },
  "thresholds": [
    "output-threshold",
    "usage-threshold"
  ],
  "severe_gaps": 0,
  "output_drift": 0,
  "reflect_now": 2,
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
