# Implementation Readiness

## Identity

- Canonical ID: `implementation-readiness`
- Aliases: none
- Scope: library

Implementation Readiness composes `implementation-layering`, `decision-gate`, and `task-session` so a rough implementation goal becomes staged, decided, and ready for one bounded execution loop.

## Trigger Conditions

- The user has a feature, workflow, infrastructure change, or improvement idea.
- The work needs staged implementation before execution.
- Blocker decisions should be resolved before mutation.

## Required Sigils

| Sigil | Role In Spell | Required Mode |
| ----- | ------------- | ------------- |
| `implementation-layering` | Create staged implementation layers. | standard |
| `decision-gate` | Resolve blocker-level decisions revealed by the layers. | generic |
| `task-session` | Prepare or execute one selected task. | dry-run or execute |

## Shared State

| State | Owner | Updated By | Consumed By |
| ----- | ----- | ---------- | ----------- |
| layer plan | spell | `implementation-layering` | `decision-gate`, `task-session` |
| decision record | spell | `decision-gate` | `task-session` |
| task run report | spell | `task-session` | user, observability |

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| ----- | ----- | ----- | ------ | ---- | -------------- |
| 1 | `implementation-layering` | implementation goal | layer plan | minimum useful proof identified | block if scope is unclear |
| 2 | `decision-gate` | layer plan | decision record | blocker decisions resolved | block on unresolved blockers |
| 3 | `task-session` | selected layer or task | task report | done criteria and validation path known | flag if execution should wait |
| 4 | optional `inventory` | layer plan and decisions | inventory entries | inventory exists | skip if no inventory package |

## Observability

Record layer count, decision count, blockers, selected task, validation readiness, and follow-up items when `.arcanum/observability/` exists.

## Output Contract

Return a readiness report with layer plan path or summary, resolved decisions, task-session result, blockers, and recommended next action.