# Task Matrix

| ID | Complexity | Scenario | Expected Output | Status |
| --- | --- | --- | --- | --- |
| issue-loop-low | low | Dry-run a project view and select one ready issue without mutating GitHub or local files. | Contract-shaped result with candidate issue, selection reason, blocked mutation note, dependency map/test plan placeholders, and next step. | pending |
| issue-loop-medium | medium | Claim one ready issue, map dependencies, create/reuse focused tests first, refine local context, invoke only the needed artifacts, execute a small task session, and open a PR. | Contract-shaped result with claim, dependency map, regression tests, scope containment, artifacts, branch/commit/PR, validation, and telemetry path. | pending |
| issue-loop-complex | complex | Process a P1 issue that may need dependency-boundary escalation, subagent review, multiple project fields, CI polling, and explicit blocked conditions. | Contract-shaped result preserving gates, dependency/test boundary, board sync, CI truth, blockers, and reflection signal. | pending |
| sigil-new-low | low | Sigil Development lifecycle smoke case from the generated profile. | Contract-shaped result. | pending |
| sigil-update-medium | medium | Sigil Development update case from the generated profile. | Contract-shaped result with gates. | pending |
| sigil-observe-medium | medium | Sigil Development observe case from the generated profile. | Observer inference separated from edits. | pending |
| sigil-reflect-complex | complex | Sigil Development reflection case from the generated profile. | Promotion, hold, or revision recommendation. | pending |
| sigil-harness-validation-complex | complex | Sigil Development harness-validation case from the generated profile. | Evidence usability verdict. | pending |
