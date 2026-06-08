# Refine Usage Telemetry

Use this template for meaningful `refine` executions and for Experiment Harness observation of `refine` example runs.

## Meaningful Execution

A meaningful execution is any run where `refine` attempts to produce one of:

- a seed proposal,
- a research decision,
- a dispatch-spec route,
- a runtime handoff report,
- native capability or approved subagent stage receipt evidence,
- a run manifest and evidence index,
- a final refined synthesis.

## JSONL Shape

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "sigil": "refine",
  "tier": "arcana",
  "mode": "seed-proposal | runtime-handoff | loop-run | blocked | observe | reflect",
  "meaningful_execution": true,
  "target": "<target path, idea, design concern, work-pack, or repository area>",
  "selected_preset": "compact | standard | full | deep",
  "selected_research_mode": "no-research | bounded-research | research-if-gap-appears",
  "research_confirmed": false,
  "dispatch_route": "<path or blocked reason>",
  "dispatch_validation_status": "pass | flag | block | not_run",
  "dispatch_techniques": [],
  "dispatch_technique_overlays": [],
  "runtime_handoff": "<path or blocked reason>",
  "runtime_status": "pass | flag | block | not_run",
  "planned_execution_stages": {
    "context_builder_evidence_baseline": "required | pass | flag | block",
    "invoke_define": "required | pass | flag | block",
    "interrogation_refine_review": "required | pass | flag | block",
    "research_decision": "required | pass | flag | block",
    "distill": "required | pass | flag | block",
    "invoke_redefine_design": "required | pass | flag | block",
    "interrogation_refine_design_review": "required | pass | flag | block",
    "distill_repair": "required | pass | flag | block",
    "invoke_plan": "required | pass | flag | block",
    "final_interrogation_synthesis": "required | pass | flag | block"
  },
  "stage_receipts": [
    {
      "stage": "<stage>",
      "capability_ref": "<capability-id>",
      "capability_source": "<native capability source or candidate metadata>",
      "mode_config": "<mode/config>",
      "output": "<path or none>",
      "receipt_kind": "native-stage | subagent | handoff | blocked",
      "receipt_artifact": "<path or none>",
      "status": "pass | flag | block",
      "observer_status": "<status or n/a>",
      "blocked_reason": "<reason or none>"
    }
  ],
  "run_manifest": "<path or none>",
  "evidence_index": "<path or none>",
  "result": "<path or none>",
  "recommended_next_routes": [],
  "quality_bar_status": "pass | partial | fail | not_checked",
  "anti_pattern_hits": [],
  "workflow_gaps": [
    {
      "category": "trigger | input | process | quality-bar | anti-pattern | output-contract | observability | reflection",
      "severity": "low | medium | high | severe",
      "summary": "<gap summary>",
      "evidence": "<file, output, user correction, or observed behavior>"
    }
  ],
  "output_contract_drift": false,
  "observer_recommendation": "none | targeted-update | reflect-now",
  "reflection_trigger": "none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap"
}
```

## Reflection Counters

Default triggers:

- 5 meaningful executions,
- 10 generated or materially updated artifacts,
- 3 related workflow gaps,
- 1 severe workflow gap.
