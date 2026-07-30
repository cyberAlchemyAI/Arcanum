# Work Pack Readiness Audit

- Canonical ID: `work-pack-readiness-audit`
- Verdict: `block`
- Snapshot: `b95d9ab6b870adcfc98f54197315147f3e52477bcba15e69c534cb5848909335`; drift `false`
- Plan contract: `block`
- Runtime admission: `pass`
- Receipt semantics: `pass`
- Ready frontier: `SWU-DFE-001`
- Selected unit: `none`
- Authority effect: `none`
- Mutation ready: `false`
- Next owner: `invoke:refresh`

## Finding Counts

- `command`: 9

## Unit Results

| Unit | Plan | Runtime | Blockers |
| --- | --- | --- | --- |
| `SWU-DFE-001` | `block` | `pass` | WPA-001 |
| `SWU-DFE-002` | `block` | `pass` | WPA-001, WPA-002 |
| `SWU-DFE-003` | `block` | `pass` | WPA-001, WPA-002, WPA-003 |
| `SWU-DFE-004` | `block` | `pass` | WPA-001, WPA-002, WPA-003, WPA-004 |
| `SWU-DFE-005` | `block` | `pass` | WPA-001, WPA-002, WPA-003, WPA-004, WPA-005 |
| `SWU-DFE-006` | `block` | `pass` | WPA-001, WPA-002, WPA-003, WPA-004, WPA-005, WPA-006 |
| `SWU-DFE-007` | `block` | `pass` | WPA-001, WPA-002, WPA-003, WPA-004, WPA-005, WPA-006, WPA-007 |
| `VERIFY-DFE-001` | `block` | `pass` | WPA-001, WPA-002, WPA-003, WPA-004, WPA-005, WPA-006, WPA-007, WPA-008 |
| `READINESS-DFE-001` | `block` | `pass` | WPA-001, WPA-002, WPA-003, WPA-004, WPA-005, WPA-006, WPA-007, WPA-008, WPA-009 |

## Findings

### WPA-001 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-DFE-001`
- Evidence: invalid relative path: .
- Targets: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-CONTRACT.md`

### WPA-002 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-DFE-002`
- Evidence: invalid relative path: .
- Targets: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-REDUCER.md`

### WPA-003 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-DFE-003`
- Evidence: invalid relative path: .
- Targets: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-CLAIM.md`

### WPA-004 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-DFE-004`
- Evidence: invalid relative path: .
- Targets: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-RECONCILE.md`

### WPA-005 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-DFE-005`
- Evidence: invalid relative path: .
- Targets: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-BOUNDARY.md`

### WPA-006 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-DFE-006`
- Evidence: invalid relative path: .
- Targets: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-BOUNDARY.md`

### WPA-007 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `SWU-DFE-007`
- Evidence: invalid relative path: .
- Targets: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-BOUNDARY.md`

### WPA-008 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `VERIFY-DFE-001`
- Evidence: invalid relative path: .
- Targets: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-VERIFY.md`

### WPA-009 — validation cwd is missing or escapes the repository

- Category: `command`
- Scope: `READINESS-DFE-001`
- Evidence: invalid relative path: .
- Targets: `spells/goal/development/invoke-runs/20260730T171428Z-decision-frontier-experiment/work-pack/tasks/TASK-DFE-READINESS.md`

## Claim Ceiling

This report is an audit-only preflight. It selects and executes no unit, authorizes no mutation, and applies no refresh.
