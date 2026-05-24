# Implementation Layering: Skill-Aware Observation Bridge

## Purpose

Define the smallest responsible implementation path for deterministic observability of explicit Codex skill invocations.

## Source Contract

- Architecture overview: [../ARCHITECTURE-OVERVIEW.md](../ARCHITECTURE-OVERVIEW.md)
- Design artifact: [SKILL-AWARE-OBSERVATION-DESIGN.md](SKILL-AWARE-OBSERVATION-DESIGN.md)
- Telemetry derivation design: [DERIVE-INVOCATION-TELEMETRY-DESIGN.md](DERIVE-INVOCATION-TELEMETRY-DESIGN.md)
- Continuation feedback design: [CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md](CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md)
- Observer authority: [../scripts/observe-invocation.sh](../scripts/observe-invocation.sh)
- Hook entrypoint: [.codex/hooks/arcanum-user-prompt-submit.sh](../../../.codex/hooks/arcanum-user-prompt-submit.sh)

## Target And Scope

- Target: skill-aware observation bridge
- Scope: framework observability and Codex hook integration
- Current state: partially implemented command-observation path

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether explicit `$skill-name` prompts can open a valid pending envelope. | Detect `$skill-name`, resolve `.agents/skills/<name>/SKILL.md`, write pending envelope. | `arcanum-user-prompt-submit.sh` skill detection and metadata extraction. | Stop-hook closeout hardening, docs refresh, CLI skill runner. | Synthetic hook input creates pending envelope with `capability.mode=skill`. | Continue to L1 when envelope validates structurally. |
| L1 | After this layer, we know whether run evidence can become meaningful telemetry before append. | `derive-invocation-telemetry.sh` enriches envelopes from final message, tool events, and optional skill profile. | Stop hook integration, derived telemetry report, skill metadata preservation. | AI-assisted derivation, continuation feedback. | Synthetic run produces enriched envelope and derived telemetry report. | Continue to append validation when derivation is deterministic. |
| L2 | After this layer, we know whether the observer can append enriched skill telemetry without special cases. | End-to-end synthetic run bundle observed through `observe-invocation.sh`. | Ledger append, indexes, reflection counters, skill metadata preservation. | Implicit skill detection, platform metadata integration. | Test envelope appends one row and creates by-capability/by-sigil indexes. | Harden or remediate based on observer result. |
| L3 | After this layer, we know whether reliability and governance hold across command and skill routes. | Regression checks for `/command`, `$skill`, markdown skill token, unknown token, and duplicate route precedence. | Validation script or documented manual fixture checks; docs updated. | Ledger migration for old unknown-kind rows. | All route fixtures pass; docs identify explicit-skill limitation. | Prepare for task-session execution or release. |
| L4 | After this layer, we know whether later user corrections can improve prior-run telemetry. | Continuation feedback attribution links next-turn corrections to prior run ids. | Active run context and continuation feedback ledger. | Full Necronomicon maintenance integration. | Follow-up correction emits linked feedback event. | Route to Necronomicon integration if useful. |
| L5 | After this layer, we know whether the bridge is package-ready. | Optional `tools/arcanum` skill-aware helpers and migration report. | `--list-skills`, `--resolve-skill`, skill route diagnostics. | Native platform post-skill event integration. | CLI helper checks and migration report. | Package when needed; otherwise defer. |

## Non Regression Guardrails

- `/command` hook behavior must remain unchanged.
- `observe-invocation.sh` remains the only telemetry append authority.
- Unknown `$TOKEN` values must not create envelopes.
- Hook operation telemetry must stay separate from capability telemetry.
- Implicit skill selection must not be guessed.
- Later user corrections must be attributed as continuation feedback, not backfilled into old invocation facts.

## Recommended Next Layer

- Next layer: L0, then L1 derivation.
- Key decision unlocked: explicit skill prompts can be recognized and represented as valid observer envelopes, then enriched before append.
- Major deferred scope: implicit skill-use detection, AI-assisted extraction, and full Necronomicon maintenance integration.
