# Arcanum Spell: sigil maintenance loop

<!-- arcanum:capability-id sigil-maintenance-loop -->
<!-- arcanum:capability-kind spell -->
<!-- arcanum:capability-tier spell -->
<!-- arcanum:command arcanum-spell-sigil-maintenance-loop -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-spell-sigil-maintenance-loop-<UTC timestamp>`.
- `capability.id`: `sigil-maintenance-loop`
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

Run the installed Arcanum spell `sigil-maintenance-loop` using the canonical spell snapshot embedded below.

## Process

1. Use the embedded canonical spell snapshot as the execution contract.
2. Execute only this installed spell unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected spell's process, quality bar, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `sigil-maintenance-loop`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical Spell Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/spells/sigil-maintenance-loop/README.md

````markdown
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
````
