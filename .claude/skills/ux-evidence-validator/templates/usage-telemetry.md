# UX Evidence Validator Usage Telemetry

Use this template to record meaningful `ux-evidence-validator` executions.

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "sigil": "ux-evidence-validator",
  "tier": "arcana",
  "mode": "research | spec | fixture-plan | calibrate | validate-interface | report",
  "meaningful_execution": true,
  "target_type": "url | local-html | scenario | screenshot-set | research-artifact | unknown",
  "scenario_count": 0,
  "generated_output_count": 0,
  "validator_layers": ["L0", "L1", "L2", "L3", "L4", "L5", "L6"],
  "hard_gate_count": 0,
  "soft_flag_count": 0,
  "screenshot_review_count": 0,
  "human_study_residue_count": 0,
  "source_card_count": 0,
  "fixture_calibration": "pass | flag | block | not_run",
  "browser_evidence_output_root": "<path-or-none>",
  "quality_bar_status": "pass | partial | fail | not_checked",
  "anti_pattern_hits": [],
  "workflow_gaps": [
    {
      "category": "source-evidence | automation-honesty | fixture | browser-evidence | output-contract | promotion",
      "severity": "low | medium | high | severe",
      "summary": "<gap summary>",
      "evidence": "<file, run output, or user correction>"
    }
  ],
  "output_contract_drift": false,
  "observer_recommendation": "none | targeted-update | reflect-now",
  "reflection_trigger": "none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap"
}
```

Default reflection triggers:

- 5 meaningful executions,
- 10 generated outputs,
- 3 related workflow gaps,
- 1 severe workflow gap,
- any promoted hard gate that later fails a false-positive trap.
