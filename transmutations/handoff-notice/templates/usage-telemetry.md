# Handoff Notice Usage Telemetry

Record one compact JSON object per meaningful `publish`, `resolve`, or `inspect` attempt. Do not copy the notice body, subject, key points, questions, or private source text into telemetry.

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "sigil": "handoff-notice",
  "tier": "transmutations",
  "version": "0.1.0",
  "mode": "publish | resolve | inspect",
  "meaningful_execution": true,
  "repository_fingerprint": "<sha256>",
  "notice_type": "session-handoff",
  "notice_status": "open",
  "recipient_kind": "person",
  "source_kind": "agent",
  "notice_code": "HN-...",
  "notice_digest": "<sha256>",
  "artifact_path": ".arcanum/handoff-notices/notices/HN-....json",
  "schema_validation": "pass | fail",
  "boundary_presence": "pass | fail",
  "open_call_count": 0,
  "source_reference_count": 0,
  "next_action_count": 0,
  "collision_check": "pass | extended | fail",
  "registry_update": "created | idempotent | failed | not-applicable",
  "resolution": "exact | missing | malformed | digest-mismatch | out-of-scope | superseded | not-applicable",
  "authority_disclaimer": "present | missing",
  "terminal_receipt_pointer": false,
  "owner_route_hint": false,
  "downstream_owner": "none",
  "quality_bar_status": "pass | partial | fail | not_checked",
  "anti_pattern_hits": [],
  "workflow_gaps": [],
  "output_contract_drift": false,
  "user_correction": false,
  "reflection_trigger": "none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap"
}
```

Default reflection triggers:

- 5 meaningful executions,
- 10 generated or modified artifacts,
- 3 related locator, schema, or routing gaps,
- 1 severe gap.
