---
tags: [subagent-strategy, runtime-binding, append-only-ledger, cross-platform-validation]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-27T13:12:14-03:00
updated_at: 2026-08-27T13:12:14-03:00
expires: 2026-10-26
decisions_made: true
contradictions_found: true
specs_updated:
  - arcana/subagent-strategy/SKILL.md
  - formulae/dispatch-spec/dispatch.schema.yml
  - runtime/orchestrate/SKILL.md
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session closed critical gaps between confirmed strategy, durable registration, executable runtime topology, cross-process safety, and cross-platform enforcement."
---

# Subagent strategy runtime hardening

## Summary

The session compared Arcanum's subagent-strategy lifecycle with the stronger DomainSpec registration discipline and then reviewed the implementation adversarially. It established that the confirmed strategy must remain a temporary JSON while the durable record is an append-only YAML dispatch row paired with a close row, with no new material-strategy artifact. The registrar was hardened with composite readiness, admitted-model and identity checks, predicted-disagreement coverage, cross-process locking, durable append, exact-content idempotency, path confinement, and semantic close validation. Dispatch Spec registration moved to v0.2 and now binds the exact sheet digest plus a canonical executable projection digest. Orchestrate recomputes that projection, compares it with both registration and ledger, verifies group-to-wave cardinality and blocking dependencies, and refuses resolved closeout without matching totals, loop bounds, digest, and exit state. Stage handoffs gained a typed validator, the observability package gained its missing state and ledgers, and append-only enforcement was added for Claude hooks and CI. Documentation, profile ownership, workflow path filters, generated runtime surfaces, and Windows-safe commands were brought into alignment. Local Windows validation passed 102 registrar cases, an eight-process concurrency test, runtime and Dispatch Spec suites, generation checks, guards, syntax checks, and a junction-escape test. Linux execution is configured in the same GitHub Actions matrix but was not witnessed locally, so cross-platform validation remains flagged until that run passes.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Subagent Strategy](../arcana/subagent-strategy/SKILL.md) | `validates` | This session records the implementation and adversarial tests for the capability's temporary-sheet, registration, execution, and closeout contracts. |
| [Orchestrate runtime](../runtime/orchestrate/SKILL.md) | `validates` | This session records the projection and topology binding now enforced before native actions and resolved closeout. |
| [Dispatch Spec](../formulae/dispatch-spec/SKILL.md) | `implements` | The session implements the v0.2 strategy-registration proof shape in the Dispatch Spec schema and validator. |

## Next steps

1. Run the `windows-latest` and `ubuntu-latest` workflow matrix and retain the resulting CI evidence.
2. If both jobs pass, change the Craft context gate to `pass` and resolve `GAP-SUBAGENT-STRATEGY-LINUX-CI-001`; otherwise preserve the failing platform evidence and open a bounded repair task.

## Recommendation

Prioritize the first CI matrix run because it is the only remaining evidence gap and directly determines whether the new cross-platform contract can move from local `flag` to repository-witnessed `pass`.

## Files touched

- `.agents/skills/orchestrate/SKILL.md`
- `.agents/skills/orchestrate/scripts/native_dispatch_coordinator.py`
- `.arcanum/observability/config.json`
- `.arcanum/observability/reflection-state.json`
- `.arcanum/observability/signals/sigil-invocations.jsonl`
- `.arcanum/observability/hooks/hook-operations.jsonl`
- `.arcanum/observability/hooks/failures.jsonl`
- `.arcanum/observability/hooks/dedupe.jsonl`
- `.claude/hooks/enforce-append-only-dispatch.cjs`
- `.claude/settings.json`
- `.github/workflows/subagent-strategy-runtime.yml`
- `arcana/research/SKILL.md`
- `arcana/review/SKILL.md`
- `arcana/subagent-strategy/SKILL.md`
- `arcana/subagent-strategy/README.md`
- `arcana/subagent-strategy/profiles/arcanum.yaml`
- `arcana/subagent-strategy/scripts/append-dispatch.cjs`
- `arcana/subagent-strategy/scripts/validate-readiness.cjs`
- `arcana/subagent-strategy/scripts/validate-stage-handoff.cjs`
- `arcana/subagent-strategy/scripts/enforce-append-only-dispatch.cjs`
- `arcana/subagent-strategy/scripts/check-ledger-history.cjs`
- `arcana/subagent-strategy/development/test-append-dispatch.cjs`
- `arcana/subagent-strategy/development/test-append-concurrency.cjs`
- `arcana/subagent-strategy/development/test-runtime-guards.cjs`
- `formulae/dispatch-spec/SKILL.md`
- `formulae/dispatch-spec/dispatch.schema.yml`
- `formulae/dispatch-spec/scripts/validate-dispatch.py`
- `runtime/orchestrate/SKILL.md`
- `runtime/orchestrate/scripts/native_dispatch_coordinator.py`
- `runtime/orchestrate/tests/test_strategy_registration_integration.py`
- `.craft/ledger.yml`
- `CRAFT.md`
- `sessions/2026-08-27-1312-subagent-strategy-runtime-hardening.md`

## Craft registration

- Context: `CTX-SUBAGENT-STRATEGY-RUNTIME-HARDENING`
- Session artifact: `ART-SUBAGENT-STRATEGY-HARDENING-SESSION`
- Remaining evidence gap: `GAP-SUBAGENT-STRATEGY-LINUX-CI-001`
