# Arcanum Spell: implementation readiness

<!-- arcanum:capability-id implementation-readiness -->
<!-- arcanum:capability-kind spell -->
<!-- arcanum:capability-tier spell -->
<!-- arcanum:command arcanum-spell-implementation-readiness -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-spell-implementation-readiness-<UTC timestamp>`.
- `capability.id`: `implementation-readiness`
- `capability.kind`: `spell`
- `capability.tier`: `spell`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum spell `implementation-readiness` using the canonical spell snapshot embedded below.

## Process

1. Use the embedded canonical spell snapshot as the execution contract.
2. Execute only this installed spell unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected spell's process, quality bar, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `implementation-readiness`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical Spell Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/spells/implementation-readiness/README.md

````markdown
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
````
