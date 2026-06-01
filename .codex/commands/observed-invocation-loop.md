# Arcanum Spell: observed invocation loop

<!-- arcanum:capability-id observed-invocation-loop -->
<!-- arcanum:capability-kind spell -->
<!-- arcanum:capability-tier spell -->
<!-- arcanum:command observed-invocation-loop -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-observed-invocation-loop-<UTC timestamp>`.
- `capability.id`: `observed-invocation-loop`
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

Run the installed Arcanum spell `observed-invocation-loop` using the canonical spell snapshot embedded below.

## Process

1. Use the embedded canonical spell snapshot as the execution contract.
2. Execute only this installed spell unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected spell's process, quality bar, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `observed-invocation-loop`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical Spell Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/spells/observed-invocation-loop/README.md

````markdown
# Observed Invocation Loop

## Identity

- Canonical ID: `observed-invocation-loop`
- Aliases: Capability Observability Loop
- Scope: library
- Status: baseline-ready

## Purpose

Observed Invocation Loop wraps Arcanum-managed skill, sigil, and spell invocations with a guaranteed post-run observability handoff. It turns each managed invocation into a safe invocation envelope, appends exactly one telemetry signal, updates reflection counters, and routes to reflection when configured thresholds are met.

The spell does not replace `experiment-harness`. Experiment Harness remains a validation-loop producer. This spell owns the general invocation path.

The observability handoff is hook-first. Telemetry emission must be enforced by Codex hooks, wrappers, or deterministic command runners wherever possible; agent-authored closeout text is useful evidence, but it must not be the only mechanism that appends telemetry.

## Trigger Conditions

- A skill, sigil, or spell is invoked through an Arcanum Codex command, hook, wrapper, or orchestration layer.
- A maintainer needs confidence that capability telemetry was appended after a run.
- Reflection thresholds should be evaluated after real usage.
- A reusable capability needs evidence-backed maintenance without forcing every run through the experiment harness.

## Required Sigils

| Sigil | Role In Spell | Required Mode |
| ----- | ------------- | ------------- |
| `signal-observer` | Read or receive an invocation envelope, append telemetry, update reflection counters, and emit reflection recommendation. | observe |
| `workflow-reflect` | Analyze accumulated telemetry and write a reflection report when thresholds or manual routing require it. | reflect |

## Optional Sigils

| Sigil | Use When | Notes |
| ----- | -------- | ----- |
| `observability-setup` | The repository does not yet have `.arcanum/observability/`. | Install or repair the observability package before strict telemetry is required. |
| `sigil-development` | Reflection proposes a sigil update and the user approves mutation. | Reflection itself remains non-mutating. |
| `spellcraft` | Reflection proposes a spell update and the user approves mutation. | Spell lifecycle execution stays outside this spell. |
| `decision-gate` | Telemetry strictness, privacy, or reflection routing has a blocker-level ambiguity. | Use only for consequential unresolved choices. |

## Prerequisites

- Invocation is routed through an Arcanum-managed Codex command, hook, orchestrator, or wrapper.
- The managed adapter or hook is responsible for observation closeout; agent attention is only a fallback/manual repair path.
- Repository observability exists at `.arcanum/observability/`, or the run explicitly allows telemetry to be skipped.
- The invoked capability can provide enough post-run evidence to assemble an invocation envelope.
- Privacy rules permit storing summaries, paths, validation state, and signal metadata.

## Shared State

| State | Owner | Updated By | Consumed By |
| ----- | ----- | ---------- | ----------- |
| invocation envelope | Codex hook or wrapper | capability wrapper | `signal-observer` |
| central signal ledger | observability package | `signal-observer` | `workflow-reflect`, maintainers |
| hook operations ledger | observability package | observer/reflection hooks | hook-health review |
| reflection state | observability package | `signal-observer`, `workflow-reflect` | threshold evaluator |
| reflection reports | observability package | `workflow-reflect` | `sigil-development`, `spellcraft`, maintainers |

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| ----- | ----- | ----- | ------ | ---- | -------------- |
| 1 | Codex command or hook | user request and target capability | observed run metadata | target capability resolved | block if capability cannot be resolved |
| 2 | target capability | managed invocation context | primary capability result | primary run completed, blocked, or failed with evidence | return primary result honestly |
| 3 | Codex hook or wrapper | primary result and metadata | invocation envelope | envelope has required fields and no sensitive raw content | flag when telemetry is skipped; block only if strict mode requires telemetry |
| 4 | `signal-observer` | invocation envelope | telemetry row and threshold recommendation | exactly one append or deduped skip | never hide primary result unless strict telemetry mode is active |
| 5 | `workflow-reflect` | telemetry ledger and threshold result | reflection report or insufficient-signal result | only run on threshold or manual request | skip when no threshold and no manual reflection request |
| 6 | spell closeout | phase outputs | observed invocation result | primary result and observability state are reported | flag unresolved telemetry or reflection gaps |

## Gates

| Gate | Required Evidence | Result |
| ---- | ----------------- | ------ |
| managed invocation | capability ran through Arcanum command, hook, wrapper, or orchestrator | pass or block |
| envelope validity | timestamp, capability id, kind, mode, execution status, outputs, validation, observer evidence | pass or flag |
| telemetry append | ledger append, dedupe skip, or explicit skipped reason | pass, flag, or block in strict mode |
| threshold evaluation | reflection trigger and recommendation recorded | pass or flag |
| reflection route | report written, skipped with reason, or queued | pass or flag |
| hook enforcement | Codex hook or deterministic wrapper performed the observation handoff | pass or flag |

## Command And Hook Contract

Arcanum-managed agent commands must make observer envelope setup task zero. Native agent receipts, Codex hooks, and deterministic wrappers such as `tools/arcanum --exec --adapter local-skill` perform the observability handoff. The system must not rely on the agent remembering to call `signal-observer`.

Required phases:

| Phase | Responsibility | Required Evidence |
| --- | --- | --- |
| start | Resolve capability id, kind, tier, mode, request summary, and run id. | observed run metadata or equivalent local variables |
| execute | Run or dry-run the target capability while preserving the primary result. | primary status, outputs, changed files, validation |
| envelope | Assemble a privacy-safe invocation envelope. | `capability.id`, `capability.kind`, legacy `sigil`, execution status, observer fields |
| observe | Call `framework/observability/scripts/observe-invocation.sh`. | `OBSERVATION`, `LEDGER`, `LEDGER_LINE`, `REFLECTION_TRIGGER`, `RECOMMENDATION`, `DEDUPE_KEY` |
| reflect | If enabled and recommended, call `framework/observability/scripts/reflect-invocation-signals.sh`. | report path or skipped reason |
| closeout | Return primary result plus telemetry status. | observed invocation result |

Required capability kinds:

| Kind | Example Adapter | Required `capability.kind` |
| --- | --- | --- |
| skill | `.codex/commands/arcanum-orchestrate.md` | `skill` |
| sigil | `.codex/commands/arcanum-sigil-signal-observer.md` | `sigil` |
| spell | `.codex/commands/arcanum-spell-invoke.md` | `spell` |

Adapter controls:

- `OBSERVED_INVOCATION_STRICT=1`: telemetry append failure blocks closeout.
- `OBSERVED_REFLECT=off|auto|always`: controls reflection report execution.
- Manual observer calls are allowed for diagnostics only and do not satisfy hook-enforcement evidence.
- `signals/sigil-invocations.jsonl` is the telemetry and dedupe recovery source of truth. `by-sigil/` and `by-capability/` contain compact indexes that can be rebuilt from the central ledger.

## Automatic Attachment

OIL should be attached through Arcanum command generation, not by hand-editing each sigil command. The propagation owner is the command-surface installer/generator: when it creates or refreshes a Codex command, the command must include observer envelope task-zero metadata and the installed hooks must be present.

Recommended generated marker:

```markdown
<!-- arcanum:capability-id <id> -->
<!-- arcanum:capability-kind <skill|sigil|spell> -->
<!-- arcanum:capability-tier <tier> -->
<!-- arcanum:capability-alias <alias> -->
<!-- arcanum:command <command> -->
```

Codex commands are the installed runtime surface:

- command: `.codex/commands/<command>.md`
- bare-id alias for sigils and spells: `.codex/commands/<id>.md`
- hook config: `.codex/hooks.json`
- hook scripts: `.codex/hooks/`
- required closeout: `UserPromptSubmit` opens the envelope, `PostToolUse` records evidence, `Stop` closes through `observe-invocation.sh`

Prefixed commands such as `arcanum-spell-invoke` remain stable compatibility names. Bare aliases such as `invoke` and `interrogation` are the preferred user-facing command names when there is no collision.

Existing adapters should be refreshed idempotently by marker block. If a file has local changes and no safe marker insertion point, report a conflict instead of overwriting.

## Local Customization

- Spell root: `.arcanum/spells/`
- Local paths: `.arcanum/observability/`
- Gate strictness: standard by default; strict mode may block when telemetry cannot be appended.
- Interaction mode: guided-auto for managed Codex commands.

## Observability

Record spell-level telemetry when `.arcanum/observability/` exists:

- target capability id and kind,
- invocation mode,
- primary execution status,
- envelope path,
- telemetry append status,
- dedupe status,
- reflection trigger,
- reflection report path or skip reason,
- follow-up route.

## Output Contract

Return:

```markdown
## Observed Invocation Loop Result

- Spell: observed-invocation-loop
- Capability: <id>
- Capability kind: skill | sigil | spell
- Mode: <mode>
- Primary status: pass | flag | block | fail
- Envelope: <path or n/a>
- Telemetry: recorded | deduped | skipped | failed
- Ledger: <path or n/a>
- Reflection trigger: none | manual | usage-threshold | output-threshold | gap-threshold | severe-gap
- Reflection: report written | skipped | queued | failed
- Report: <path or n/a>
- Next route: none | workflow-reflect | sigil-development | spellcraft | decision-gate
```

````
