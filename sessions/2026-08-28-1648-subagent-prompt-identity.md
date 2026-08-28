---
tags: [subagent-dispatch, prompt-identity, orchestration, observability]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-28T16:48:42-03:00
updated_at: 2026-08-28T16:48:42-03:00
expires: 2026-10-27
decisions_made: true
contradictions_found: true
specs_updated: [arcana/subagent-strategy/SKILL.md, runtime/orchestrate/SKILL.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "The session established and enforced a cross-runtime identity invariant for every newly governed subagent launch."
---

# Subagent prompt identity enforcement

## Summary

The session first inspected whether governed subagent dispatch JSON records were temporary and whether durable history was confined to telemetry. It established that successful strategy and close temporary records are consumed, while failed close records and other runtime JSON can remain for diagnosis, and that a recent migration left historical and active dispatch ledgers at different paths. The session then traced how `agent_name`, `initial_prompt`, confirmed briefings, and native host requests relate. It decided that every new governed agent must have a pool-backed name and that the exact initial prompt must begin with `You are {agent_name}.`, followed by a blank line and bounded instructions. The Subagent Strategy registrar and readiness gate now reject missing names, mismatched prefixes, and empty instruction bodies. Native Orchestrate requests now begin with the confirmed briefing identity and reject a declared `agent_name` that differs from `agent_identity`; the generated Codex package was regenerated from the canonical runtime. Validation passed with 105 registrar tests, the eight-writer concurrency check, and 39 targeted Orchestrate tests, while existing append-only ledgers and already-confirmed dispatches were not rewritten.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Subagent Strategy](../arcana/subagent-strategy/SKILL.md) | `is-part-of` | This session changed the capability's confirmation and launch identity invariant. |
| [Orchestrate](../runtime/orchestrate/SKILL.md) | `validates` | The recorded tests demonstrate that the native host projection begins with and preserves the confirmed identity. |

## Open questions

- Should the stricter admission semantics trigger a strategy-sheet schema bump from `0.6.1`, or remain a grandfathered validator hardening under the current version?
- Should `synthesizer` remain in the admitted role enum when no current agent-pool identity declares that role, or should the pool or enum be aligned?

## Recommendation

Resolve the schema-version question before distributing the updated registrar beyond this repository, because it controls whether external `0.6.1` producers receive a compatible hardening or an explicit migration boundary.

## Files touched

- `.agents/skills/orchestrate/SKILL.md`
- `.agents/skills/orchestrate/scripts/native_dispatch_coordinator.py`
- `.agents/skills/orchestrate/scripts/native_dispatch_driver.py`
- `arcana/subagent-strategy/README.md`
- `arcana/subagent-strategy/SKILL.md`
- `arcana/subagent-strategy/development/test-append-concurrency.cjs`
- `arcana/subagent-strategy/development/test-append-dispatch.cjs`
- `arcana/subagent-strategy/profiles/arcanum.yaml`
- `arcana/subagent-strategy/scripts/append-dispatch.cjs`
- `arcana/subagent-strategy/scripts/validate-readiness.cjs`
- `arcana/subagent-strategy/templates/dispatch-record.example.json`
- `arcana/subagent-strategy/templates/runtime-profile.md`
- `runtime/orchestrate/SKILL.md`
- `runtime/orchestrate/scripts/native_dispatch_coordinator.py`
- `runtime/orchestrate/scripts/native_dispatch_driver.py`
- `runtime/orchestrate/tests/native-driver/test_native_dispatch_driver.py`
- `runtime/orchestrate/tests/native-spawn/fixtures/expected-spawn-request.json`
- `runtime/orchestrate/tests/test_compile_actions.py`
- `runtime/orchestrate/tests/test_strategy_registration_integration.py`
- `sessions/2026-08-28-1648-subagent-prompt-identity.md`
