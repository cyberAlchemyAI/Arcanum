---
tags: [subagent-dispatch, prompt-identity, orchestration, closeout-accounting]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-28T17:49:25-03:00
updated_at: 2026-08-28T17:49:25-03:00
expires: 2026-10-27
decisions_made: true
contradictions_found: true
specs_updated: [formulae/dispatch-spec/SKILL.md, runtime/orchestrate/SKILL.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "The remediation closes the gap between confirmed subagent identity evidence and the exact prompt executed by the native host."
---

# Subagent prompt identity review remediation

## Summary

This session applied the verified findings from the adversarial review of governed subagent prompt identity. It established a breaking migration boundary at strategy sheet `0.7.0` and registration proof `v0.3` because agent identity and prompt admission changed materially. Each capability-bound role now carries one agent binding per planned instance, including the pool-backed name, exact confirmed initial prompt, and typed briefing. Registration verification compares those names and prompts with the append-only ledger before compiling any action. The native driver validates prompt identity and body against the briefing and passes the confirmed prompt unchanged to the host. Closeout accounting now separates planned, launched, and unlaunched agents so partial/error termination remains truthful while resolved closeout requires all planned launches. Shannon now admits the `synthesizer` role, resolving the pool/enum contradiction. Fixtures, examples, generated Orchestrate assets, session history, and validation documentation were migrated together. Focused validation passed with 107 registrar cases, 27 top-level Orchestrate tests, 10 adversarial briefing cases, five generation-parity tests, the eight-writer concurrency check, 21 native-driver tests, and five native-spawn tests. Historical append-only `0.6.1` ledger rows were preserved without rewriting.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Prompt identity review](../docs/analysis/subagent-prompt-identity/review.md) | `resolves` | This session implements the six verified change requests from the adversarial review. |
| [Original prompt identity session](2026-08-28-1648-subagent-prompt-identity.md) | `refines` | It corrects the original test count and strengthens identity preservation from prefix-only projection to exact prompt execution. |
| [Orchestrate](../runtime/orchestrate/SKILL.md) | `validates` | The recorded tests support the revised registration and native-spawn contract. |

## Files touched

- `.agents/skills/orchestrate/SKILL.md`
- `.agents/skills/orchestrate/schemas/action.schema.json`
- `.agents/skills/orchestrate/scripts/native_dispatch_coordinator.py`
- `.agents/skills/orchestrate/scripts/native_dispatch_driver.py`
- `arcana/subagent-strategy/README.md`
- `arcana/subagent-strategy/development/VALIDATION.md`
- `arcana/subagent-strategy/development/fixtures/strategy-form-version-drift-medium.expected.md`
- `arcana/subagent-strategy/development/fixtures/strategy-form-version-drift-medium.md`
- `arcana/subagent-strategy/development/fixtures/strategy-single-confirmation-readiness-medium.expected.md`
- `arcana/subagent-strategy/development/fixtures/strategy-single-confirmation-readiness-medium.md`
- `arcana/subagent-strategy/development/test-append-dispatch.cjs`
- `arcana/subagent-strategy/profiles/arcanum.yaml`
- `arcana/subagent-strategy/templates/runtime-profile.md`
- `formulae/dispatch-spec/SKILL.md`
- `formulae/dispatch-spec/development/run-confirmed-role-briefing-tests.py`
- `formulae/dispatch-spec/dispatch.schema.yml`
- `formulae/dispatch-spec/examples/capability-bound-artifact-repair.json`
- `runtime/orchestrate/SKILL.md`
- `runtime/orchestrate/tests/test_compile_actions.py`
- `runtime/orchestrate/tests/test_reduce_receipts.py`
- `runtime/orchestrate/tests/test_strategy_registration_integration.py`
- `sessions/2026-08-28-1648-subagent-prompt-identity.md`
- `sessions/2026-08-28-1749-subagent-prompt-identity-remediation.md`
