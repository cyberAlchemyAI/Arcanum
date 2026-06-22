# Usage Telemetry: GitHub Project Issue Loop

Append one JSON object per meaningful execution.

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "sigil": "github-project-issue-loop",
  "tier": "arcana",
  "mode": "execute | observe | reflect | dry-run",
  "meaningful_execution": true,
  "project": {
    "owner": "<org-or-user>",
    "number": 0,
    "view_url": "<url-or-null>"
  },
  "repository": "<owner/name>",
  "issue": {
    "number": 0,
    "title": "<title>",
    "selection_reason": "<reason>"
  },
  "claim": {
    "assignee": "<login>",
    "result": "assigned | already-assigned | blocked",
    "project_status": "In Progress | In Review | Done | not-updated | blocked"
  },
  "lifecycle_route": ["refine", "invoke-define", "invoke-design", "invoke-plan", "task-session"],
  "generated_outputs": {
    "count": 0,
    "paths": []
  },
  "regression_boundary": {
    "upstream_dependencies": ["<caller-route-contract-test-or-source>"],
    "downstream_dependents": ["<ui-api-artifact-ci-or-consumer>"],
    "write_scope": ["<intended-path-or-module>"],
    "non_goals": ["<explicit-out-of-scope-behavior>"],
    "status": "mapped | partial | blocked"
  },
  "regression_tests": {
    "strategy": "created | updated | reused | blocked",
    "pre_fix_baseline": "pass | fail | not-run | not-applicable",
    "focused_commands": ["<command>"],
    "containment_checks": ["<command-or-invariant>"]
  },
  "scope_containment": {
    "status": "pass | flag | block | not_checked",
    "summary": "<how changed files and validation stayed within the dependency map>"
  },
  "implementation": {
    "branch": "<branch-or-null>",
    "commit": "<sha-or-null>",
    "pull_request": "<url-or-null>"
  },
  "validation": [
    {
      "command": "<command>",
      "status": "pass | fail | not-run",
      "summary": "<summary>"
    }
  ],
  "ci": {
    "status": "pass | fail | pending | unknown",
    "summary": "<summary>"
  },
  "quality_bar_status": "pass | partial | fail | not_checked",
  "anti_pattern_hits": [],
  "workflow_gaps": [
    {
      "category": "trigger | input | process | quality-bar | anti-pattern | output-contract | template | observability | reflection",
      "severity": "low | medium | high | severe",
      "summary": "<gap summary>",
      "evidence": "<file, command, issue, PR, or user correction>"
    }
  ],
  "output_contract_drift": false,
  "user_correction": false,
  "observer_recommendation": "none | targeted-update | reflect-now",
  "reflection_trigger": "none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap"
}
```

## Reflection Counters

- Meaningful executions since reflection: 0
- Generated outputs since reflection: 0
- Related workflow gaps since reflection: 0
- Severe workflow gaps since reflection: 0
