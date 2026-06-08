# Usage Telemetry Template

Use this template to record a meaningful sigil execution.

Telemetry should be compact, factual, and useful for later reflection. It should not attempt to rewrite the sigil. Its job is to preserve enough signal for a future observer to identify patterns.

## JSONL Shape

Each execution can be recorded as one JSON object per line:

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "sigil": "<sigil-name>",
  "tier": "formulae | transmutations | arcana",
  "mode": "new | update | observe | reflect | execute",
  "meaningful_execution": true,
  "generated_output_count": 0,
  "quality_bar_status": "pass | partial | fail | not_checked",
  "anti_pattern_hits": ["<anti-pattern-id-or-summary>"],
  "workflow_gaps": [
    {
      "category": "trigger | input | process | quality-bar | anti-pattern | output-contract | template | observability | reflection",
      "severity": "low | medium | high | severe",
      "summary": "<gap summary>",
      "evidence": "<file, output, user correction, or observed behavior>"
    }
  ],
  "output_contract_drift": false,
  "user_correction": false,
  "observer_recommendation": "none | targeted-update | reflect-now",
  "reflection_trigger": "none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap"
}
```

## Field Guidance

- `meaningful_execution`: true when the sigil produced or attempted a user-facing result.
- `generated_output_count`: count files, reports, decisions, or artifacts created or materially updated.
- `quality_bar_status`: use `partial` when some criteria were not checked.
- `anti_pattern_hits`: include only observed misuse or near-miss cases.
- `workflow_gaps`: preserve actionable evidence, not impressions.
- `output_contract_drift`: true when the result does not match the declared output contract.
- `observer_recommendation`: the observer's recommendation before the main agent decides what to edit.

## Reflection Counters

Maintain counters since the last reflection:

- meaningful executions,
- generated outputs,
- related workflow gaps,
- severe workflow gaps,
- Quality Bar failures,
- output-contract drift events.

Default reflection triggers:

- 5 meaningful executions,
- 10 generated outputs,
- 3 related workflow gaps,
- 1 severe workflow gap.