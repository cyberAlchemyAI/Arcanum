---
name: MOGT Live Approval Repair Patch Proposal
description: Proposal-only patch content for converting the repair-needed verdict into executable MOGT repair SWUs.
created: 2026-06-08
mutation_mode: proposal-only
status: proposed
---

# Refresh Patch Proposal: MOGT Live Approval Repair Pack

## Proposed Target

Apply only after approval, either by:

- appending this as a new section to `research/mogt-agentic-conversation/development/WORK-PACK.md`; or
- creating a separate approved work-pack at `research/mogt-agentic-conversation/development/MOGT-LIVE-APPROVAL-REPAIR-PACK.md`.

## Proposed Section

```markdown
## MOGT-LIVE-APPROVAL-REPAIR-PACK

### Objective

Repair the local approval blockers that prevent MOGT E1/E2/E4 from moving into
claim-bearing live evidence collection. Keep E3 second-wave by default.

### Boundary

Do not run live experiments. Do not update `results/MOGT-EVIDENCE-STATUS.md`,
paper result sections, or publication claims. This pack prepares the approval
surface only.

### SWU Manifest

| SWU ID | Parent Task | Status | Objective | Acceptance Evidence |
| --- | --- | --- | --- | --- |
| SWU-MOGT-REPAIR-001 | TASK-MOGT-REPAIR-001 | ready | Create and record 3-5 reviewer calibration examples. | Calibration set artifact; at least two independent reviewer scores; adjudication notes for disagreement greater than `0.25`. |
| SWU-MOGT-REPAIR-002 | TASK-MOGT-REPAIR-002 | ready | Close E1 protocol hard gates G1-G3. | E1 protocol gate table updated with evidence links; source bundle and inventory readiness notes. |
| SWU-MOGT-REPAIR-003 | TASK-MOGT-REPAIR-003 | ready | Close E2 protocol hard gates G1-G3 and source-normalization notes. | E2 protocol gate table updated with evidence links; Pareto/weighted-sum source-normalization note. |
| SWU-MOGT-REPAIR-004 | TASK-MOGT-REPAIR-004 | ready | Close E4 protocol hard gates G1-G3 and overhead thresholds. | E4 protocol gate table updated with evidence links; latency/cost/reviewer-burden stop thresholds. |
| SWU-MOGT-REPAIR-005 | TASK-MOGT-REPAIR-005 | ready | Define concrete live-run parameters and evidence mutation owners. | Model/version, temperature, scenario counts, policy regimes, cost bounds, output paths, mutation owner, adjudication gate, and paper rewrite owner. |
| SWU-MOGT-REPAIR-006 | TASK-MOGT-REPAIR-006 | pending | Rerun `MOGT-LIVE-EVIDENCE-APPROVAL` after repairs. | Approval result becomes either approve-ready, repair-needed, research-gap, or block from local evidence. |

### Promotion Rule

`SWU-MOGT-REPAIR-006` cannot start until `SWU-MOGT-REPAIR-001` through
`SWU-MOGT-REPAIR-005` have recorded acceptance evidence.
```

## Non-Changes

- Do not modify claim evidence status.
- Do not promote fixture evidence into live evidence.
- Do not move E3 into first-wave execution.
- Do not mutate canonical Arcanum spell, sigil, or tool contracts.
