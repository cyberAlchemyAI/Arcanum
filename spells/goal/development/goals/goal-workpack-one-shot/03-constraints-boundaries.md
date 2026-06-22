# Constraints And Boundaries

## Capability Lanes

| Lane | Allowed For | Receipt Gate |
| --- | --- | --- |
| `spellcraft` | W0 lifecycle validation. | Validation report or block. |
| `local-fallback` | W0 staged source-state sync proposal only. | Proposal or explicit deferral; no active ledger mutation. |
| `task-session` | W1-W3 bounded runtime SWUs after their gates pass. | One SWU receipt at a time. |
| `decision-gate` | Approval-token or blocker decisions only when required. | Durable decision record or held/rejected state. |
| `experiment-harness` | W3 reusable behavior evidence after runtime behavior exists. | Experiment report. |
| `runtime-installer` | Generated runtime package dry-run or separately approved apply. | Installer evidence; no hand-authored generated surfaces. |

Subagents are not authorized by this profile. If a future run needs them, stop
and request explicit authorization plus role receipt requirements.

## Write Boundaries

Allowed write areas, subject to each SWU gate:

- `arcanum/spells/goal/development/spellcraft-runs/`
- `arcanum/spells/goal/development/task-session-runs/`
- `arcanum/spells/goal/development/experiment-runs/`
- staged proposal artifacts under `arcanum/spells/goal/development/`
- installer evidence under `arcanum/spells/goal/development/`
- runtime/source files selected by Spellcraft or Task Session for the current
  SWU only

Protected:

- active Craft ledger rows,
- filled decision profiles,
- generated host surfaces unless produced by installer,
- registry status,
- publication, commit, push, PR, or parent gitlink movement.

## Public/Private Boundary

Public artifacts may include neutral schema/profile shape only. Do not copy
filled runtime profile data into `arcanum` or into validation reports.

## Fallback Exploration

Fallback exploration is named-gaps-only:

- `G-GOAL-SCHEMA-HOME`
- `G-GOAL-CRAFT-SYNC`
- `G-GOAL-RUNTIME-SOURCE`
- `G-GOAL-FIXTURE-SET`
- `B-GOAL-PROMOTION-EVIDENCE`

Every extra source must be reported with path, justifying gap, and effect.
