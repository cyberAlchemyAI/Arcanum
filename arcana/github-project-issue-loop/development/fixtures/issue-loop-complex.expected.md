# Expected Output: issue-loop-complex

## Result

- Status: pass or flag
- Output includes explicit selection reason, subagent gate state, project status, dependency map, regression tests, scope containment, PR URL if opened, CI pending truth if applicable, blockers, and next step.
- Unclear dependency boundaries cause invoke design/plan escalation or a blocker before implementation.
- Missing meaningful regression tests are reported as a blocker or explicit risk, not silently skipped.
- Severe gaps trigger reflection rather than silent continuation.
