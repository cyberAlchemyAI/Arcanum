# Refine Usage Telemetry

Use this template for meaningful `refine` executions and for Experiment Harness observation of `refine` example runs.

## Meaningful Execution

A meaningful execution is any run where `refine` attempts to produce one of:

- a seed proposal,
- an existing work-pack preflight,
- a research decision,
- a blocked Codex Goal handoff report,
- a Task Session/Codex Goal route,
- a lifecycle handoff to Sigil Development.

## JSONL Shape

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "sigil": "refine",
  "tier": "arcana",
  "mode": "seed-proposal | preflight | blocked-handoff | lifecycle-handoff | observe | reflect",
  "meaningful_execution": true,
  "target": "<target path, idea, design concern, or work-pack>",
  "seed_needed": true,
  "selected_preset": "compact | standard | full | deep",
  "selected_research_mode": "no-research | bounded-research | research-if-gap-appears",
  "research_confirmed": false,
  "planned_execution_stages": {
    "context_builder": "required | blocked | skipped",
    "invoke_define": "required | blocked | skipped",
    "interrogation": "required | blocked | skipped",
    "distill": "required | blocked | skipped",
    "invoke_design_plan": "required | blocked | skipped",
    "sigil_development": "required | blocked | not_applicable"
  },
  "task_session_route": "<command or blocked reason>",
  "codex_goal_eligibility": "pass | block | not_applicable",
  "blocked_handoff_fields": [],
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
