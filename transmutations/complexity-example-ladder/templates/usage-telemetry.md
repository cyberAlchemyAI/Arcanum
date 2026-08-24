# Complexity Example Ladder Usage Telemetry

Append one compact JSON object per meaningful execution when repository-local
observability is available.

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "sigil": "complexity-example-ladder",
  "tier": "transmutations",
  "mode": "execute",
  "meaningful_execution": true,
  "trigger_kind": "user-request | caller-contract | uncertainty",
  "caller": "<capability or direct-user>",
  "ladder_mode": "explanatory | comparative",
  "rungs_required": ["low", "medium", "complex"],
  "rungs_produced": ["low", "medium", "complex"],
  "complexity_axes": ["<axis>"],
  "shared_invariant_preserved": true,
  "options_required": ["<option-id>"],
  "options_covered_by_rung": {
    "low": ["<option-id>"],
    "medium": ["<option-id>"],
    "complex": ["<option-id>"]
  },
  "hypothetical_count": 0,
  "unsupported_claim_count": 0,
  "unequal_option_coverage": false,
  "decision_effect": "none | not-applicable",
  "quality_bar_status": "pass | partial | fail | not_checked",
  "anti_pattern_hits": [],
  "workflow_gaps": [],
  "output_contract_drift": false,
  "user_correction": false,
  "observer_recommendation": "none | targeted-update | reflect-now",
  "reflection_trigger": "none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap"
}
```

Default reflection triggers: 5 meaningful executions, 10 generated outputs,
3 related workflow gaps, or 1 severe gap.
