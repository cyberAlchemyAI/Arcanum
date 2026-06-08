# Sigil Maintenance Loop

## Identity

- Canonical ID: `sigil-maintenance-loop`
- Aliases: none
- Scope: library

Sigil Maintenance Loop composes `signal-observer`, `workflow-reflect`, and `sigil-development` so reusable sigils improve from usage evidence.

## Trigger Conditions

- A sigil has meaningful execution history.
- Telemetry shows repeated gaps, output drift, user corrections, or quality failures.
- The user asks to tune, reflect on, or improve a sigil.

## Required Sigils

| Sigil | Role In Spell | Required Mode |
| ----- | ------------- | ------------- |
| `signal-observer` | Record post-run behavior signals. | observe |
| `workflow-reflect` | Analyze accumulated signals and propose changes. | reflect |
| `sigil-development` | Apply approved targeted updates. | update or reflect |

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| ----- | ----- | ----- | ------ | ---- | -------------- |
| 1 | `signal-observer` | latest invocation envelope | telemetry row | evidence is sufficient | skip when no meaningful run exists |
| 2 | `workflow-reflect` | telemetry ledger | reflection report | threshold or manual trigger met | stop if insufficient signal |
| 3 | `sigil-development` | reflection report | updated sigil or no-change decision | user approves change scope | block on contract-breaking changes |
| 4 | spell report | phase outputs | maintenance report | validation performed | flag remaining gaps |

## Observability

Record signal counts, thresholds, proposed changes, accepted changes, rejected changes, validation status, and next reflection trigger.

## Output Contract

Return a maintenance report with observed sigil, reflection trigger, proposal summary, files changed if any, validation, and next lifecycle step.