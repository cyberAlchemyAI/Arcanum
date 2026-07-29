# Subagent Strategy Usage Telemetry

Record one compact JSON object for each meaningful strategy execution.

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "sigil": "subagent-strategy",
  "tier": "arcana",
  "mode": "inline | propose | run | close",
  "meaningful_execution": true,
  "profile_id": "<id-or-unavailable>",
  "dispatch_type": "<type-or-none>",
  "trigger_decision": "inline | dispatch | blocked",
  "triggers": ["synthesis | context-protection | isolation | parallelism"],
  "group_count": 0,
  "agent_count": 0,
  "preflight_status": "pass | flag | block | not_configured",
  "preflight_design_consequence": "<summary-or-none>",
  "confirmation_readiness": "pass | warning | block | not_configured",
  "confirmation_readiness_obligations": {
    "form_and_version": "pass | block | not_configured",
    "type_owner_prerequisites": "pass | block | not_configured",
    "agent_and_approver_eligibility": "pass | block | not_configured",
    "digest_owned_tension_evidence": "pass | block | not_configured",
    "publication_boundary": "pass | block | not_configured"
  },
  "form_schema_expected": "<version-or-unknown>",
  "form_schema_observed": "<version-or-unknown>",
  "projection_drift_warning": "<summary-or-none>",
  "preconfirm_revision_count": 0,
  "tension_gate": "pass-pass | revision | unavailable | not_applicable",
  "confirmation_request_count": 0,
  "avoidable_confirmation_request_count": 0,
  "preventable_post_confirmation_revision_count": 0,
  "confirmation_state": "awaiting | confirmed-frozen | not_applicable",
  "registration_state": "unregistered | registered | blocked | not_applicable",
  "execution_state": "not_started | completed | partial | failed | not_applicable",
  "agents": {
    "open": 0,
    "joined": 0,
    "failed": 0,
    "closed": 0
  },
  "ledger_pair_state": "paired | pending | blocked | not_applicable",
  "generated_output_count": 0,
  "quality_bar_status": "pass | partial | fail | not_checked",
  "anti_pattern_hits": [],
  "workflow_gaps": [
    {
      "category": "trigger | profile | preflight | tension | confirmation | registration | dependency | approval | closeout | publication | observability",
      "severity": "low | medium | high | severe",
      "summary": "<gap>",
      "evidence": "<artifact-or-observation>"
    }
  ],
  "output_contract_drift": false,
  "observer_recommendation": "none | targeted-update | reflect-now",
  "reflection_trigger": "none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap"
}
```

Severe gaps include execution without confirmation or registration, unpaired
dispatch/close events, unsafe scope expansion, private evidence leakage,
companion-only gate evidence, a repeated confirmation caused by a
deterministically discoverable pre-confirmation defect, and agents left open
after the parent returns.
