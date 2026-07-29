# HTML Preview Server Usage Telemetry

Record one JSON object per meaningful execution through the standard Arcanum
post-run observability hook.

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "sigil": "html-preview-server",
  "tier": "formulae",
  "mode": "open | start | status | stop",
  "meaningful_execution": true,
  "target_kind": "file | directory-index",
  "root_policy": "containing-directory | explicit-root",
  "port_policy": "dynamic | explicit",
  "server_state": "started | reused | running | stopped | already-stopped | blocked",
  "http_verification": "pass | fail | not_run",
  "browser_navigation": "observed | unavailable | skipped | failed",
  "console_error_count": 0,
  "quality_bar_status": "pass | partial | fail | not_checked",
  "anti_pattern_hits": [],
  "workflow_gaps": [],
  "output_contract_drift": false,
  "user_correction": false,
  "observer_recommendation": "none | targeted-update | reflect-now",
  "reflection_trigger": "none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap"
}
```

Server runtime state and its private health token are not telemetry. Never copy
the token from the operating system temporary directory into a repository ledger.

Default reflection triggers:

- 5 meaningful executions;
- 10 generated receipts;
- 3 related workflow gaps;
- 1 severe security, containment, cleanup, or false-proof gap.
