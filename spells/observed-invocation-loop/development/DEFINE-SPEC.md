# Invoke Define Spec: Observed Invocation Loop

## Intent Record

- User goal: make every Arcanum-managed skill, sigil, or spell invocation emit telemetry and trigger reflection when thresholds are met.
- Selected artifact type: spell.
- Reason: the capability composes runtime adapters, `signal-observer`, `workflow-reflect`, and optional lifecycle update routes.
- Explicit non-goal: do not force all telemetry through `experiment-harness`.

## Problem

Telemetry currently exists for experiment reports, but the general invocation path is not guaranteed. Hook operations may show observer activity, yet capability signals can be missing, duplicated, written to the wrong root, or left without a reflection handoff.

## Capability Definition

Observed Invocation Loop is a runtime-adjacent spell that guarantees post-run observation for Arcanum-managed invocations:

1. Run the requested capability through a managed adapter.
2. Assemble a safe invocation envelope from the primary result.
3. Append one signal-observer-compatible telemetry row.
4. Update reflection counters.
5. Evaluate thresholds.
6. Route to `workflow-reflect` when the recommendation is `reflect-now`.

The guarantee must come from adapters, wrappers, and deterministic hooks rather than agent memory. Agent-authored summaries can enrich the envelope, but the closeout append must not depend on the agent remembering to call an observer.

## Boundary

Included:

- skill, sigil, and spell invocations routed through Arcanum adapters,
- generic invocation envelopes,
- central telemetry append,
- hook operation rows,
- dedupe,
- threshold evaluation,
- reflection report routing.

Excluded:

- direct native invocations outside Arcanum adapters,
- mutating sigil or spell contracts from reflection,
- replacing `experiment-harness`,
- storing raw sensitive conversation content.

## Required Outputs

- spell contract,
- invocation envelope contract,
- observer integration design,
- reflection routing design,
- implementation plan,
- implementation layering artifact,
- work-pack and execution handoff.

## Decisions

| Decision | Result | Rationale |
| --- | --- | --- |
| Spell or sigil | Spell | The behavior orchestrates multiple capabilities and lifecycle phases. |
| Core telemetry owner | `signal-observer` | It already owns append-only telemetry and reflection trigger semantics. |
| Reflection owner | `workflow-reflect` | It already owns accumulated-signal analysis and proposal reports. |
| Experiment harness role | Producer only | It should delegate to generic observation rather than own all runtime telemetry. |
| Attention-span dependency | Disallowed | Observation closeout is a hook/runtime responsibility; agent attention is fallback evidence only. |
| Strictness default | Standard | Observability failures should not hide the primary result by default. |

## Unresolved Gaps

| Gap | Severity | Route |
| --- | --- | --- |
| Runtime adapter coverage for every installed environment is not yet verified. | non-blocker | plan L3 packaging slice |
| Direct native skill invocations cannot be guaranteed without runtime hook support. | accepted limitation | document boundary |

## Template Selection

- Primary template: `invoke.spell`
- Companions: implementation-plan, implementation-layering, work-pack
- Lifecycle authority for implementation: `spellcraft`

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: spells/invoke/define.md
- Outputs: spells/observed-invocation-loop/development/DEFINE-SPEC.md, spells/observed-invocation-loop/development/GLOSSARY.md
- Template selection: invoke.spell plus planning companions
- Decisions: create a spell that composes existing observability sigils
- Unresolved gaps: runtime adapter coverage verification
- Next route: spellcraft
