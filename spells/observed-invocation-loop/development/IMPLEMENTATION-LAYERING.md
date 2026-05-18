# Implementation Layering: Observed Invocation Loop

## Purpose

Define a decision-first rollout for generalized invocation telemetry and reflection routing.

## Target And Scope

- Target: `observed-invocation-loop`
- Scope: spell plus supporting observability scripts and runtime adapter integration
- Current state: partially implemented through experiment-harness-specific observation and existing observability helpers

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether a generic envelope can append one valid telemetry row. | One fixture envelope observed by a generic script. | envelope validation, ledger append, hook row, dedupe | runtime adapters, reflection reports | fixture command appends exactly one row | continue if generic observation works |
| L1 | After this layer, we know whether the generic observer is repeatable outside experiment harness. | Experiment harness delegates to generic observer without behavior loss. | root resolution, thresholds, reflection state update, machine output | adapter-wide coverage | existing experiment harness gates pass | harden if regression-free |
| L2 | After this layer, we know whether reflection routing is governed and non-mutating. | Threshold hit writes or queues one workflow-reflect report. | reflect runner, threshold handoff, report paths, failure policy | full runtime packaging | threshold fixture produces report or explicit skip | scale if reports are useful |
| L3 | After this layer, we know whether managed skills, sigils, and spells can use the pipeline. | Runtime adapters call the observed invocation wrapper. | adapter docs, command wrappers, validation fixtures for skill/sigil/spell | non-Arcanum native hooks | toy skill/sigil/spell invocation telemetry evidence | package or defer per runtime |

## Non Regression Guardrails

- Existing experiment harness telemetry must remain valid.
- Hook operation rows must never become normal capability telemetry.
- Telemetry append must be enforced by hooks, adapters, or deterministic wrappers; agent-authored closeout is evidence, not the enforcement mechanism.
- Reflection must not mutate target artifacts.
- Primary capability results must remain visible even when observation fails.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: generic observation can be reused without experiment harness ownership
- Major deferred scope: runtime-wide adapter integration
