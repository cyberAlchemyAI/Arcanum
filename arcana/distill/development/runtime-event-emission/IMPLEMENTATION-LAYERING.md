# Implementation Layering: Distill Runtime-Event Emission

## Target And Scope

- Target: Distill runtime-event production and direct usage telemetry
- Scope: public canonical sigil, deterministic helpers/fixtures, readiness
  evidence, and generated runtime packages
- Current state: accepted consumer backend; missing live producer

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether Distill can append one accepted runtime event without changing evidence authority. | `SWU-DRE-001`: one capability-probe append through the Distill emitter | emitter, accepted schema input, optimistic ledger digest, one positive/negative fixture | complete role sequences, telemetry, docs, mirrors | event accepted by existing resolver primitives; drift blocks | continue, repair, or stop |
| L1 | After this layer, we know whether both role paths emit resolvable evidence with their required identity semantics. | `SWU-DRE-002` and `SWU-DRE-003` | true-subagent and role-simulation sequences, path-specific negatives, cross-path shape check | direct telemetry and readiness closeout | both complete sequences resolve; identity fraud blocks | harden or remediate |
| L2 | After this layer, we know whether direct telemetry and evidence-emission status remain truthful under success and failure. | `SWU-DRE-004` through `SWU-DRE-006` | direct observer, status semantics, canonical docs, gap/readiness state | generated packaging | telemetry dedupe; status fixtures; full canonical validation | package or remediate |
| L3 | After this layer, we know whether installed runtime profiles preserve the accepted canonical behavior. | `SWU-DRE-007` plus closeout verification | bootstrap regeneration, parity, integrated suite, public-boundary check | new runtimes and operational corpus | exact mirror parity and complete closeout | close gap, pilot, or hold |

## Non-Regression Guardrails

- Preserve all current Distill modes, budgets, roles, techniques, cycle guards,
  verdicts, output semantics, and next routes.
- Preserve Invoke's validator and mutation-handoff authority.
- Preserve one append owner for direct and invoked telemetry.
- Preserve append-only historical events and signals.
- Do not close `GAP-DEE-002` before L3 evidence passes.

## Recommended Next Layer

- Next layer: L0
- Selected unit: `SWU-DRE-001`
- Decision unlocked: whether a Distill-owned producer can emit one
  consumer-accepted event without widening authority
- Major deferred scope: full role sequences, direct telemetry, readiness
  closure, and generated profiles
